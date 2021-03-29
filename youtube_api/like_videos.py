#!/usr/bin/python

# This script goes through all the videos id of a specific channel.
# It then proceeds to like all videos uploaded on this channel.
# NOTE: To use the sample, you must provide one several secret_code.json obtained
#       in the Google APIs Console.
#        You also need to add the user from which the actions will be done
         #into your test pool in the Google APIs Console.



from youtube_v3_api import *
from search_videos_id import SearchVideosId
from quota_estimation import QuotaEstimation


class LikeVideos(YoutubeV3API):
	def __init__(self):
		super().__init__()
		self.client_secret_file_dict = cfg.oauth_client_id_dict
		self.scopes=["https://www.googleapis.com/auth/youtube"]
		self.inst_quotas=QuotaEstimation()
		return

	def get_videos_id(self):
		all_videos_id=[]
		inst_search_videos_id=SearchVideosId()
		for channel_id in self.channel_id_dict.values():
			all_videos_id+=inst_search_videos_id.get_all_videosId(channel_id)

		return all_videos_id


	def check_viability(self):
		#Taking into account the units consummed that day in the pickle file, 
		#This methods verify that we have enough units remaining to run the code
		#Init
		viability=None

		#Retrieve quota estimate for this class
		quota_estimate=self.inst_quotas.get_quota()

		#Retrieve daily quota already used
		self.daily_quota_already_used=self.inst_quotas.get_current_daily_quota_use()

		#Retrieve max amount of API project needed
		self.nbr_of_api_projects=self.inst_quotas.get_nbr_projects_needed()

		#Get available units to run this script, considering you've made available the same amount of projects oath_client_id, as per QuotaEstimation() output
		available_units=self.nbr_of_api_projects*self.max_quotas_per_api_project-self.daily_quota_already_used

		if quota_estimate > available_units:
			print("Not enough units avaible to run this script: Available units: %d ; Units needed to run the script: %d \n " %(available_units, quota_estimate))
			viability=False
		else:
			print("You can run this script: Available units: %d ; Units needed to run the script: %d \n " %(available_units, quota_estimate))
			viability=True

		return viability

	def give_likes(self):
		#This method will be in charge of liking videos automatically.
		viability=self.check_viability()

		if viability == True:
			#Init
			quota=0 #To keep track of units consumption
			counter=0 #To keep track of when we will need to switch between projects in order to keep having enough units to like all videos
			n_used_quota=self.daily_quota_already_used
			counter_treshold_per_project={}
			
			#Retrieve all your videos_id
			videos_id_list=self.get_videos_id()

			#Set the counter_treshold showing when the script should move from one project to another as we use up their units
			for i in range(0, self.nbr_of_api_projects):
				counter_treshold_per_project[i]= math.floor(
										(self.max_quotas_per_api_project-n_used_quota) /self.cost_dict['video_rate']
										)

				#We consider being in the context where only project 1 may have had some units used during quota estimation
				n_used_quota=0
				#This literally consider that you use your project units just for the sake of this script.
				#####

				#Build youtube object and oauth flows
				flow=InstalledAppFlow.from_client_secrets_file(self.client_secret_file_dict[i], self.scopes)
				oauth_credentials = flow.run_console()
				youtube = build(
								self.youtube_api_service_name, 
								self.youtube_api_version,
                         		credentials=oauth_credentials
                         		)

				#Like all videos
				for one_video_id in videos_id_list:
					youtube.videos().rate(rating="like", id=one_video_id).execute()
					##Quotas
					quota+=self.cost_dict['video_rate']
					#####
					counter+=1 #Following video by video the amount of time we use up the units of one project to like
					
					#When we reach the unit counter treshold of a specific project, we break this loop to change project
					#and start another oauth flow to use the units of another project.
					if counter == counter_treshold_per_project[i]:
						print("One project's units have been totally consummed. Switch to another: \n")
						del(videos_id_list[0:counter]) 
						#After breaking this nested for loop we will fall back into upper for loop and go back into liking videos listed in videos_id_list
						#So the latter should be updated and not contained the videos we already liked
						counter=0 #fresh counter for next Projects
						break

			##Update Quotas
			self.inst_quotas.update_daily_quota_use(quota)
			###
			print("\n")
			print("... \u2764\ufe0f  Love was successfully given \u2764\ufe0f  ...")

		else:
			exit(1)

		return




def main():
   inst_lk=LikeVideos()
   inst_lk.give_likes()
   return




if __name__=="__main__":
    main()






