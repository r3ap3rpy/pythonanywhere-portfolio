from flask import Flask, render_template
from github import Github
import requests
import sys
import os
from pprint import pprint
from dotenv import load_dotenv

project_folder = os.path.expanduser('~/mysite')
load_dotenv(os.path.join(project_folder, '.env'))

app = Flask(__name__)

TOKEN = os.getenv('PAT')
CHNID = os.getenv('YTCHN')
CHAPI = os.getenv('YTAPI')
	
gth = Github(TOKEN)

@app.route("/")
def index():
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
				ChannelInfo['Videos'].append({'ChannelName':item['snippet']['title'],'VideoName':jitem['snippet']['title'],'ID':jitem['snippet']['resourceId']['videoId'],'Description':jitem['snippet']['description'].replace('\n\n','<br>').replace('\n','<br>')})

	return render_template("index.html", repos =[ _ for _ in gth.get_user().get_repos() if not 'r3ap3rpy' in _.name], ytbchnl = ChannelInfo)

