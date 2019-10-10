import requests;
import os;
import json;
import argparse;
import random
import string

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

client_secrets_file = "client_secret_929159790117-e2jfbd1es2tgdncpkhk8a4l3nil55711.apps.googleusercontent.com.json"

class youtubeAPI:
	def __init__(self):
		self.authenthicate();
	
	def authenthicate(self):
		# Disable OAuthlib's HTTPS verification when running locally.
		# *DO NOT* leave this option enabled in production.
		os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

		scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
		api_service_name = "youtube"
		api_version = "v3"

		
		# Get credentials and create an API client
		flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
			client_secrets_file, scopes)
			
		credentials = flow.run_console()
		
		self.youtube = googleapiclient.discovery.build(
			api_service_name, api_version, credentials=credentials)
	
	
	def getVideoByChannelId(self,channelId):
		playlistId=self.__getUploadPlaylistId(channelId)
		return self.getAllVideosOfPlayList(playlistId)
	
	def __getUploadPlaylistId(self,channelid,pageToken=None):
		query=self.youtube.channels().list(part="contentDetails",id=channelid,maxResults=50,pageToken=pageToken)
		res=query.execute()
		print("Total amount of channels: %d" % res["pageInfo"]["totalResults"])
		print("Len of items array: %d" % len(res["items"]))
		
		return res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

	def getAllVideosOfPlayList(self,playlistId):
		videos=[]
		info,new=self.__requestPlaylistItemPage(playlistId)
		videos=videos+new
		print("Request yielded: TotalResults: %s, ResultsPerPage: %s, Counter: %d" % 
			(info["totalResults"], info["resultsPerPage"], len(new)) )
		
		while("nextPageToken" in info):
			info,new=self.__requestPlaylistItemPage(playlistId, info["nextPageToken"])
			videos=videos+new
			print("Request yielded: TotalResults: %s, ResultsPerPage: %s, Counter: %d" % 
				(info["totalResults"], info["resultsPerPage"], len(new)) )
		
		print("Done. Count: %d vs totalResults: %s" % (len(videos), info["totalResults"]))
		return videos
	
	def __requestPlaylistItemPage(self, playlistId, pageToken=None):
		query=self.youtube.playlistItems().list(
			part="snippet",
			playlistId=playlistId,
			maxResults=50,
			pageToken=pageToken)
		
		res=query.execute()
		ret=[]
		
		for item in res["items"]:
			obj={}
			obj["title"]=item["snippet"]["title"]
			obj["description"]=item["snippet"]["description"]
			if (obj["title"] == "Private video" and obj["description"] == "This video is private.") or \
				(obj["title"] == "Deleted video" and obj["description"] == "This video is unavailable."):
				continue
				
			if "standard" in item["snippet"]["thumbnails"]:
				obj["img"]=item["snippet"]["thumbnails"]["standard"]["url"]
			else:
				obj["img"]=item["snippet"]["thumbnails"]["high"]["url"]

			obj["id"]=item["snippet"]["resourceId"]["videoId"]
			obj["link"]="https://www.youtube.com/watch?v="+obj["id"]
			
			ret.append(obj)
			
		
		info={}
		info["kind"]=res["kind"]
		info["totalResults"]=res["pageInfo"]["totalResults"]
		info["resultsPerPage"]=res["pageInfo"]["resultsPerPage"]
		if("nextPageToken" in res):
			info["nextPageToken"]=res["nextPageToken"]
			
		return info, ret

	
if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--channelid', help="gets all the videos of a channelid")
	parser.add_argument('--playlistbychannel', help="gets all the playlists of a channel")
	parser.add_argument('--playlists', nargs='+', help="Specify multiple playlists")
	args = parser.parse_args()

	videochannel=args.channelid
	playlistbychannel=args.playlistbychannel
	playlists=args.playlists

	if videochannel is None and playlistbychannel is None and playlists is None:
		print(parser.print_help())
		exit()
	
	if videochannel is not None:
		print("Retrieving videos by channel...")
		print(videochannel)
		utube=youtubeAPI()
		videos=utube.getVideoByChannelId(videochannel);
		fileName=videochannel
	elif playlistbychannel is not None:
		print("Retrieving playlists by channel...")
		print("Not implemented")
		exit()
	elif playlists is not None:
		print("Retrieving playlists...")
		print(playlists)
		if len(playlists)==1:
			fileName=playlists[0]
		else:
			ascii=string.ascii_lowercase;
			fileName=playlists[0]+"".join([random.choice(ascii) for i in range(10)])
			
		utube=youtubeAPI()
		videos=[]
		for playlist in playlists:
			new=utube.getAllVideosOfPlayList(playlist);
			videos=videos+new
	
	print("Writing file...")
	str=json.dumps(videos)
	with open(fileName+".json", "w") as f:
		f.write(str)
		
	print("Finished!")
