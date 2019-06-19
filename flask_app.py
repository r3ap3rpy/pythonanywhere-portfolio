import requests
import os
import json
import logging

from flask import Flask, render_template,send_from_directory, request
from github import Github
from datetime import datetime, timedelta
from requests.auth import HTTPBasicAuth
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

logging.basicConfig(format='%(asctime)s %(levelname)s :: %(message)s', level=logging.INFO)
logger = logging.getLogger('PyPortfolio')
handler = RotatingFileHandler("logs\\portfolio.logs", mode='a', maxBytes=1000000, backupCount=100, encoding='utf-8', delay=0)
handler.setLevel(logging.INFO)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

logger.info("#"*50)
logger.info("# Spinning up the beast!")

try:
	from dotenv import load_dotenv
	project_folder = os.path.expanduser('~/mysite')
	load_dotenv(os.path.join(project_folder, '.env'))
	logger.info(f"# Successfully loaded the environment variables from .env file!")
except:
	logger.info(f"# Trying to gather information from ENV variables!")
	pass

EnvCache = {}

for env_variable in ['PAT','YTCHN','YTAPI','CLID','CLSEC']:
	if os.getenv(env_variable):
		EnvCache[env_variable] = os.getenv(env_variable)
		logger.info(f"# Successfully loaded environment variable: {env_variable} with value: :)")
	else:
		logger.critical(f"# Cannot find environment variable: {env_variable}, cannot continue!")
		raise SystemExit

logger.info(f"# Creating basic authentication for Udemy")
auth = HTTPBasicAuth(EnvCache['CLID'],EnvCache['CLID'])

logger.info(f"# Initializing the pyGitHub client!")
pygthb = Github(EnvCache['PAT'])

delta = 60 * 20

@app.route("/favicon.ico")
def favicon():
	logger.info(f"# Serving /favicon to client on address: {request.remote_addr} with user agent: {request.user_agent}")
	return send_from_directory(os.path.join(app.root_path,'static','img'), 'favicon.ico', mimetype = 'image/vnd.microsoft.icon')

hubCache = {'response':{'rendered':None,'time':datetime.now()}}
@app.route("/github")
def github():
	logger.info(f"# Serving /github to client on address: {request.remote_addr} with user agent: {request.user_agent}")
	if hubCache['response']['rendered']:
		if datetime.strptime(hubCache['response']['time'], "%Y-%m-%d %H:%M:%S.%f") < datetime.now():			
			hubCache['response']['rendered'] = [ _ for _ in pygthb.get_user().get_repos() if not 'r3ap3rpy' in _.name]
			hubCache['response']['time'] = str(datetime.now() + timedelta(seconds=delta))
	else:		
		hubCache['response']['rendered'] = [ _ for _ in pygthb.get_user().get_repos() if not 'r3ap3rpy' in _.name]
		hubCache['response']['time'] = str(datetime.now() + timedelta(seconds=delta))

	return render_template('github.html', repos = hubCache['response']['rendered'] )

tubeCache = {'response':{'rendered':None,'time':datetime.now()}}
@app.route("/ytube")
def ytube():
	logger.info(f"# Serving /youtube to client on address: {request.remote_addr} with user agent: {request.user_agent}")
	if tubeCache['response']['rendered']:
		if datetime.strptime(tubeCache['response']['time'], "%Y-%m-%d %H:%M:%S.%f") < datetime.now():
			Channel = requests.get(url=f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={EnvCache['YTCHN']}&key={EnvCache['YTAPI']}").json()['items'][0]['snippet']
			Playlists = requests.get(url=f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={EnvCache['YTCHN']}&key={EnvCache['YTAPI']}&maxResults=50").json()['items']
			ChannelInfo = {
				'ID': EnvCache['YTCHN'],
				'Title': Channel['title'],
				'Description' : Channel['description'],
				'Videos' : []
			}

			for item in Playlists:
				ItemsToProcess = []
				url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}".format(item['id'],EnvCache['YTAPI'])
				PlaylistResponse = requests.get(url=url).json()
				ItemsToProcess.append(PlaylistResponse['items'])

				while PlaylistResponse.get('nextPageToken'):
					url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken={}&playlistId={}&key={}".format(PlaylistResponse.get('nextPageToken'),item['id'],EnvCache['YTAPI'])
					PlaylistResponse = requests.get(url=url).json()
					ItemsToProcess.append(PlaylistResponse['items'])

				for kitem in ItemsToProcess:
					for jitem in kitem:
						ChannelInfo['Videos'].append({'ChannelName':item['snippet']['title'],'VideoPic':jitem['snippet']['thumbnails']['medium']['url'],'VideoName':jitem['snippet']['title'],'ID':jitem['snippet']['resourceId']['videoId'],'Description':jitem['snippet']['description'].replace('\n\n','<br>').replace('\n','<br>')})
			tubeCache['response']['rendered'] = ChannelInfo
			tubeCache['response']['time'] = str(datetime.now() + timedelta(seconds=delta))
	else:
		Channel = requests.get(url=f"https://www.googleapis.com/youtube/v3/channels?part=snippet&id={EnvCache['YTCHN']}&key={EnvCache['YTAPI']}").json()['items'][0]['snippet']
		Playlists = requests.get(url=f"https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={EnvCache['YTCHN']}&key={EnvCache['YTAPI']}&maxResults=50").json()['items']
		ChannelInfo = {
			'ID': EnvCache['YTCHN'],
			'Title': Channel['title'],
			'Description' : Channel['description'],
			'Videos' : []
		}
		for item in Playlists:
			
			ItemsToProcess = []
			url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}".format(item['id'],EnvCache['YTAPI'])
			PlaylistResponse = requests.get(url=url).json()
			ItemsToProcess.append(PlaylistResponse['items'])
			while PlaylistResponse.get('nextPageToken'):
				url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken={}&playlistId={}&key={}".format(PlaylistResponse.get('nextPageToken'),item['id'],EnvCache['YTAPI'])
				PlaylistResponse = requests.get(url=url).json()
				ItemsToProcess.append(PlaylistResponse['items'])
			for kitem in ItemsToProcess:
				for jitem in kitem:
					ChannelInfo['Videos'].append({'ChannelName':item['snippet']['title'],'VideoPic':jitem['snippet']['thumbnails']['medium']['url'],'VideoName':jitem['snippet']['title'],'ID':jitem['snippet']['resourceId']['videoId'],'Description':jitem['snippet']['description'].replace('\n\n','<br>').replace('\n','<br>')})
		tubeCache['response']['rendered'] = ChannelInfo
		tubeCache['response']['time'] = str(datetime.now() + timedelta(seconds=delta))

	return render_template('ytube.html', ytbchnl = tubeCache['response']['rendered'])

@app.route('/udemy')
def udemy():
	logger.info(f"# Serving /udemy to client on address: {request.remote_addr} with user agent: {request.user_agent}")
	PAID = []
	FREE = []
	for course in dict(json.loads(requests.get(url = 'https://www.udemy.com/api-2.0/courses/?search=Szab%C3%B3%20D%C3%A1niel%20Ern%C5%91', auth = auth).text))['results']:
		if course['visible_instructors'][0]['initials'] == 'SE':
			if course['is_paid'] == True:
				PAID.append(course)
			else:
				FREE.append(course)

	return render_template('udemy.html', Paid = PAID, Free = FREE)


@app.route("/education")
def education():
	logger.info(f"# Serving /education to client on address: {request.remote_addr} with user agent: {request.user_agent}")
	return render_template('education.html')

@app.route("/experience")
def experience():
	logger.info(f"# Serving /experience to client on address: {request.remote_addr} with user agent: {request.user_agent}")
	return render_template('experience.html')


@app.route("/certificates")
def certificates():
	logger.info(f"# Serving /certificates to client on address: {request.remote_addr} with user agent: {request.user_agent}")
	return render_template('certificates.html',certs = os.listdir(os.path.join(app.root_path,'static','img','certs')))

@app.route("/")
def index():
	logger.info(f"# Serving /index to client on address: {request.remote_addr} with user agent: {request.user_agent}")
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug = True, host = '0.0.0.0', port = 8000)