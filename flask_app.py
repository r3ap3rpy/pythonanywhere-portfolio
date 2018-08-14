from flask import Flask, render_template,send_from_directory
from github import Github
from datetime import datetime, timedelta
import requests
import os

try:
	from dotenv import load_dotenv

	project_folder = os.path.expanduser('~/mysite')
	load_dotenv(os.path.join(project_folder, '.env'))
except:
	TOKEN = os.getenv('PAT')
	CHNID = os.getenv('YTCHN')
	CHAPI = os.getenv('YTAPI')


app = Flask(__name__)
delta = 60 * 20
gth = Github(TOKEN)


@app.route("/favicon.ico")
def favicon():
	return send_from_directory(os.path.join(app.root_path,'static'), 'favicon.ico', mimetype = 'image/vnd.microsoft.icon')


hubCache = {'response':{'rendered':None,'time':datetime.now()}}
@app.route("/github")
def github():
	if hubCache['response']['rendered']:
		if datetime.strptime(hubCache['response']['time'], "%Y-%m-%d %H:%M:%S.%f") < datetime.now():			
			hubCache['response']['rendered'] = [ _ for _ in gth.get_user().get_repos() if not 'r3ap3rpy' in _.name]
			hubCache['response']['time'] = str(datetime.now() + timedelta(seconds=delta))
	else:		
		hubCache['response']['rendered'] = [ _ for _ in gth.get_user().get_repos() if not 'r3ap3rpy' in _.name]
		hubCache['response']['time'] = str(datetime.now() + timedelta(seconds=delta))

	return render_template('github.html', repos = hubCache['response']['rendered'] )
	

tubeCache = {'response':{'rendered':None,'time':datetime.now()}}
@app.route("/ytube")
def ytube():
	if tubeCache['response']['rendered']:
		if datetime.strptime(tubeCache['response']['time'], "%Y-%m-%d %H:%M:%S.%f") < datetime.now():
			Channel = requests.get(url="https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}".format(CHNID,CHAPI)).json()['items'][0]['snippet']
			Playlists = requests.get(url="https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={}&key={}&maxResults=50".format(CHNID,CHAPI)).json()['items']
			ChannelInfo = {
				'ID': CHNID,
				'Title': Channel['title'],
				'Description' : Channel['description'],
				'Videos' : []
			}

			for item in Playlists:
				ItemsToProcess = []
				url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}".format(item['id'],CHAPI)
				PlaylistResponse = requests.get(url=url).json()
				ItemsToProcess.append(PlaylistResponse['items'])

				while PlaylistResponse.get('nextPageToken'):
					url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken={}&playlistId={}&key={}".format(PlaylistResponse.get('nextPageToken'),item['id'],CHAPI)
					PlaylistResponse = requests.get(url=url).json()
					ItemsToProcess.append(PlaylistResponse['items'])

				for kitem in ItemsToProcess:
					for jitem in kitem:
						ChannelInfo['Videos'].append({'ChannelName':item['snippet']['title'],'VideoPic':jitem['snippet']['thumbnails']['medium']['url'],'VideoName':jitem['snippet']['title'],'ID':jitem['snippet']['resourceId']['videoId'],'Description':jitem['snippet']['description'].replace('\n\n','<br>').replace('\n','<br>')})
			tubeCache['response']['rendered'] = ChannelInfo
			tubeCache['response']['time'] = str(datetime.now() + timedelta(seconds=delta))
	else:
		Channel = requests.get(url="https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}".format(CHNID,CHAPI)).json()['items'][0]['snippet']
		Playlists = requests.get(url="https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={}&key={}&maxResults=50".format(CHNID,CHAPI)).json()['items']
		ChannelInfo = {
			'ID': CHNID,
			'Title': Channel['title'],
			'Description' : Channel['description'],
			'Videos' : []
		}
		for item in Playlists:
			
			ItemsToProcess = []
			url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}".format(item['id'],CHAPI)
			PlaylistResponse = requests.get(url=url).json()
			ItemsToProcess.append(PlaylistResponse['items'])
			while PlaylistResponse.get('nextPageToken'):
				url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken={}&playlistId={}&key={}".format(PlaylistResponse.get('nextPageToken'),item['id'],CHAPI)
				print(url)
				PlaylistResponse = requests.get(url=url).json()
				ItemsToProcess.append(PlaylistResponse['items'])
			for kitem in ItemsToProcess:
				for jitem in kitem:
					print(jitem['snippet']['thumbnails']['medium'])
					ChannelInfo['Videos'].append({'ChannelName':item['snippet']['title'],'VideoPic':jitem['snippet']['thumbnails']['medium']['url'],'VideoName':jitem['snippet']['title'],'ID':jitem['snippet']['resourceId']['videoId'],'Description':jitem['snippet']['description'].replace('\n\n','<br>').replace('\n','<br>')})
		tubeCache['response']['rendered'] = ChannelInfo
		tubeCache['response']['time'] = str(datetime.now() + timedelta(seconds=delta))

	return render_template('ytube.html', ytbchnl = tubeCache['response']['rendered'])


@app.route("/education")
def education():
	return render_template('education.html')

@app.route("/experience")
def experience():
	return render_template('experience.html')

@app.route("/")
def index():
	return render_template('index.html')


	return render_template("index.html", ytbchnl = ChannelInfo)

if __name__ == '__main__':
	app.run(debug = True, host = '0.0.0.0', port = 8000)