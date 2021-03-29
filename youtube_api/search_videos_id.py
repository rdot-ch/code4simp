#!/usr/bin/python

# This sample executes a search within a specific youtube channel id.
#           It retrieves its upload playlist id.
#           Then uses the latter to go through every page of this playlist
#           and retrieve all video_ids contained in said playlist.
# NOTE: To use the sample, you must provide a developer key obtained
#       in the Google APIs Console.
# Set DEVELOPER_KEY to the API key value from the APIs & auth > Registered apps
#   https://cloud.google.com/console
# Please ensure that you have enabled the YouTube Data API for your project.


from youtube_v3_api import *
from quota_estimation import QuotaEstimation

class SearchVideosId(YoutubeV3API):
	def __init__(self):
		super().__init__()
		self.inst_quotas=QuotaEstimation()
		return

	def get_all_videosId(self, channel_id):
		#Taking into account a channel_id, this method will go through every page to get the video_id contained on the channel
		#Will be called by another Class
		#Init
		quota=0
		all_pages_data_list=[]
		next_page_token=None

		#Build youtube object
		youtube = build(
						self.youtube_api_service_name, 
						self.youtube_api_version,
                      	developerKey=self.developer_key
                      	)

		#part="contentDetails" to allow to get information such as playlistId
		channel_response = youtube.channels().list(
                                               part="contentDetails",
                                               id=channel_id
                                               ).execute()

		###Quotas
		quota+=self.cost_dict['channel_list']
		###

		#Fetch the playlistId of the upload playlist of this channel.
		#This playlist contains all the videos uploaded by the user.
		playlist_id=channel_response["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
		#Go through every page of this playlist and fetch all the videos_id found.

		while(1):
			playlist_response=youtube.playlistItems().list(
										part="contentDetails",
										playlistId=playlist_id,
										maxResults=self.max_results_per_page,
										pageToken=next_page_token
										).execute()

			###Quotas
			quota+=self.cost_dict['playlistItem_list']
			###

			all_pages_data_list.append(playlist_response["items"])

			#Needs to put a protection here to handle the moment we will reach the last page.
			try:
				next_page_token = playlist_response["nextPageToken"]
			except:
				break

		#Extract video_ids of each video found on each page of the upload playlist
		videos_id_list=[]

		for each_page in all_pages_data_list:
			for each_video in each_page:
				videos_id_list.append(each_video["contentDetails"]["videoId"])

		###UPDATE Quotas
		self.inst_quotas.update_daily_quota_use(quota)
		###

		return videos_id_list
		





