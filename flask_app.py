from flask import Flask, render_template
from github import Github 
import pprint 
import json
import requests
import os
import re

TOKEN = os.getenv('PAT')
CHNID = os.getenv('YTCHN')
CHAPI = os.getenv('YTAPI')

g = Github(TOKEN)

app = Flask(__name__)

Channel = json.loads(requests.get(url="https://www.googleapis.com/youtube/v3/channels?part=snippet&id={}&key={}".format(CHNID,CHAPI)).text)['items'][0]['snippet']
Playlists = json.loads(requests.get(url="https://www.googleapis.com/youtube/v3/playlists?part=snippet&channelId={}&key={}".format(CHNID,CHAPI)).text)['items']
pprint.pprint(Channel)
ChannelInfo = {
	'ID': CHNID,
	'Title': Channel['title'],
	'Description' : Channel['description'],
	'Videos' : []
}


for item in Playlists:
	url = "https://www.googleapis.com/youtube/v3/playlistItems?part=snippet&playlistId={}&key={}".format(item['id'],CHAPI)
	for jitem in json.loads(requests.get(url=url).text)['items']:
		ChannelInfo['Videos'].append({'ChannelName':item['snippet']['title'],'VideoName':jitem['snippet']['title'],'ID':jitem['snippet']['resourceId']['videoId'],'Description':jitem['snippet']['description'].replace('\n\n','<br>').replace('\n','<br>')})

for video in ChannelInfo['Videos']:
	for line in video['Description'].split('<br>'):
		if 'ttp' in line:
			print(line)




@app.route("/")
def index():
	return render_template("index.html", repos = [ _ for _ in g.get_user().get_repos() if not 'r3ap3rpy' in _.name], ytbchnl = ChannelInfo)

