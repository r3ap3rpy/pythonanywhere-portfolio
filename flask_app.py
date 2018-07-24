from flask import Flask, render_template,g
from github import Github 
import json
import requests
import os
from pprint import pprint

app = Flask(__name__)

@app.route("/")
def index():
	TOKEN = os.getenv('PAT')
	CHNID = os.getenv('YTCHN')
	CHAPI = os.getenv('YTAPI')

	gth = Github(TOKEN)
	Channel = json.loads(requests.get(url="https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}".format(CHNID,CHAPI)).text)['items'][0]['snippet']
	Playlists = json.loads(requests.get(url="https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={}&key={}&maxResults=50".format(CHNID,CHAPI)).text)['items']
	ChannelInfo = {
		'ID': CHNID,
		'Title': Channel['title'],
		'Description' : Channel['description'],
		'Videos' : []
	}


	for item in Playlists:		
		print('#################################################')
		print('#################################################')
		ItemsToProcess = []

		url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}".format(item['id'],CHAPI)

		PlaylistResponse = json.loads(requests.get(url=url).text)
		print(len(PlaylistResponse['items']))
		ItemsToProcess.append(PlaylistResponse['items'])

		print(item['id'],item['snippet']['title'])
		while PlaylistResponse.get('nextPageToken'):
			url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&pageToken={}&playlistId={}&key={}".format(PlaylistResponse.get('nextPageToken'),item['id'],CHAPI)
			PlaylistResponse = json.loads(requests.get(url=url).text)
			print(len(PlaylistResponse['items']))
			ItemsToProcess.append(PlaylistResponse['items'])

		
		for kitem in ItemsToProcess:
			print(len(kitem))
			for jitem in kitem:	
				ChannelInfo['Videos'].append({'ChannelName':item['snippet']['title'],'VideoName':jitem['snippet']['title'],'ID':jitem['snippet']['resourceId']['videoId'],'Description':jitem['snippet']['description'].replace('\n\n','<br>').replace('\n','<br>')})
		print('#################################################')
	#return render_template("index.html")
	return render_template("index.html", repos = [ _ for _ in gth.get_user().get_repos() if not 'r3ap3rpy' in _.name], ytbchnl = ChannelInfo)

