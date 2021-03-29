#!/usr/bin/python


# MOTHER CLASS


from os import path
from datetime import datetime
import math

from apiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

import api_config as cfg


class YoutubeV3API():
	def __init__(self):
		self.channel_id_dict=cfg.channel_id_dict
		self.developer_key=cfg.dev_key
		self.max_results_per_page=cfg.max_results_per_page #max results retrieved per page
		self.youtube_api_service_name=cfg.api_service_name
		self.youtube_api_version=cfg.api_version
		self.cost_dict=cfg.units
		self.max_quotas_per_api_project=cfg.max_quotas_per_api_project
		return

		



