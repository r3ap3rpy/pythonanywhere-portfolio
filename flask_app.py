from flask import Flask, render_template,g
from github import Github 
import json
import requests
import os

app = Flask(__name__)

@app.route("/")
def index():
#	TOKEN = os.getenv('PAT')
#	CHNID = os.getenv('YTCHN')
#	CHAPI = os.getenv('YTAPI')
#
#	gth = Github(TOKEN)
#	Channel = json.loads(requests.get(url="https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}".format(CHNID,CHAPI)).text)['items'][0]['snippet']
#	Playlists = json.loads(requests.get(url="https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={}&key={}".format(CHNID,CHAPI)).text)['items']
#	ChannelInfo = {
#		'ID': CHNID,
#		'Title': Channel['title'],
#		'Description' : Channel['description'],
#		'Videos' : []
#	}
#
#
#	for item in Playlists:
#		url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}".format(item['id'],CHAPI)
#		for jitem in json.loads(requests.get(url=url).text)['items']:
#			ChannelInfo['Videos'].append({'ChannelName':item['snippet']['title'],'VideoName':jitem['snippet']['title'],'ID':jitem['snippet']['resourceId']['videoId'],'Description':jitem['snippet']['description'].replace('\n\n','<br>').replace('\n','<br>')})
	return render_template("index.html")
	#return render_template("index.html", repos = [ _ for _ in gth.get_user().get_repos() if not 'r3ap3rpy' in _.name], ytbchnl = ChannelInfo)

