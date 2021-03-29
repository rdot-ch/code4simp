#!/usr/bin/python

# Quota cost estimation

from youtube_v3_api import *
import pickle

class QuotaEstimation(YoutubeV3API):
	def __init__(self):
		super().__init__()
		#Init
		self.today_date=datetime.today().strftime('%Y-%m-%d') #fetch current date. Will be used in logs
		self.log_file="units_cost.log"
		self.init_quota_estimation(self.log_file)
		return

	def init_quota_estimation(self, quotas_log_filename ):
		#Initialize a pickle file that will log the quota/units used by the code during the day
		if path.exists(quotas_log_filename) == False :
			init_quota_dict={
							self.today_date : 0
							}
			#Save/Dump dict in pickle file
			pickle_log_file = open(quotas_log_filename, 'wb')
			pickle.dump(init_quota_dict, pickle_log_file)
			pickle_log_file.close()

		return

	def get_quota(self):
		#This method will calculate how many units it would cost to like all the videos of the given channels.
		#The estimate is done by using as less API queries as possible.

		#Init
		quota_used=0 #used quotas to run the estimation
		quota_estimate=0 # estimation of what it would cost to run the full code
		total_nbr_videos=0 #total number of videos found on the channel

		#Build youtube object
		youtube = build(
						self.youtube_api_service_name, 
						self.youtube_api_version,
                      	developerKey=self.developer_key
                      	)

		for channel_id in self.channel_id_dict.values():
			#part='statistics' allows us to find out how many videos there are on a channel
			channel_response = youtube.channels().list(
										part="statistics",
										id=channel_id
										).execute()

			#Fetch the total amont of videos uploaded on the channel
			#using eval to turn that returned string into an integer
			total_nbr_videos+=eval(channel_response["items"][0]["statistics"]["videoCount"])

		#Cost to fetch channel info
		quota_used=len(self.channel_id_dict)*self.cost_dict["channel_list"] #Really used to run this estimate
		quota_estimate+=quota_used #Cost that would be incurred if we would use the api all the way 

		#Cost to go through each page of a playlist
		total_nbr_pages_to_visit=math.ceil(total_nbr_videos/self.max_results_per_page)
		quota_estimate+=total_nbr_pages_to_visit*self.cost_dict["playlistItem_list"]

		#Cost to rate each video
		quota_estimate+=total_nbr_videos*self.cost_dict["video_rate"]

		#Nbr of queries sent
		total_nbr_queries=len(self.channel_id_dict)+total_nbr_pages_to_visit+total_nbr_videos

		##PRINT SOME CONSOLE LOGS
		print("###INFO#####  Number of unit(s) used to run this estimate: %d unit(s) ###INFO#### \n " %(quota_used))
		print("To automatically like %d videos will generate %d queries and cost %d units. \n" %(total_nbr_videos, total_nbr_queries, quota_estimate) )


		#Update Quotas
		self.update_daily_quota_use(quota_used)

		#Set nbr of projects needed
		self.set_nbr_projects_needed(quota_estimate)

		return quota_estimate





	def set_nbr_projects_needed(self, quota_estimate):
		self.nbr_api_projects=math.ceil(quota_estimate/self.max_quotas_per_api_project)
		print("Hence, to run the class LikeVideos(), you will need: %d API PROJECT(S) \n" %(self.nbr_api_projects))
		return self.nbr_api_projects

	def get_nbr_projects_needed(self):
		#To be called by another class
		return self.nbr_api_projects


	def update_daily_quota_use(self, quota_used):
		#Load the object saved in the pickle file
		pickle_log_file = open(self.log_file,'rb')
		quota_dict = pickle.load(pickle_log_file)
		pickle_log_file.close()

		#Update the object
		if self.today_date in quota_dict:
			quota_dict[self.today_date]+=quota_used
		else:
			quota_dict[self.today_date]=quota_used

		#Save back into pickle
		pickle_log_file = open(self.log_file, 'wb')
		pickle.dump(quota_dict, pickle_log_file)
		pickle_log_file.close()
		return

	def get_current_daily_quota_use(self):
		#Method to quickly have access to the object saved in the pickle file.
		#Returns the units consummed the current day
		#Load
		pickle_log_file = open(self.log_file,'rb')
		quota_dict = pickle.load(pickle_log_file)
		pickle_log_file.close()
		return quota_dict[self.today_date]


def main():
   inst_quota=QuotaEstimation()      
   inst_quota.get_quota()
   
   return

if __name__=="__main__":
   main()


