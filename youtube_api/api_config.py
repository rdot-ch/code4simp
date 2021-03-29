#!/usr/bin/python

dev_key="<ADD-YOUR-DEVELOPER-KEY-HERE>"

oauth_client_id_dict={
		      0: "<PATH-TO-JSONFILE-0>.json",
                      1: "<PATH-TO-JSONFILE-1>.json",
                      2: "..."
                      }

api_service_name='youtube'

api_version='v3'

channel_id_dict={
		  'YOUTUBE-CHANNEL1':'CHANNEL-ID-OF-THIS-YOUTUBE-CHANNEL1',
                  'YOUTUBE-CHANNEL2':'CHANNEL-ID-OF-THIS-YOUTUBE-CHANNEL2',
                  "..."

	       }

max_quotas_per_api_project=10000

units={
         'channel_list': 1,
         'playlistItem_list':1,
         'video_rate':50

   		}

max_results_per_page=50
