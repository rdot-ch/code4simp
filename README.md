## General info
You can find here all sources and scripts to massively rate all the videos of any youtube channel with Youtube API.

## Technologies
Project was tested with:
* Python3

## Prerequisites
* Go to https://console.cloud.google.com/
* Create a project 
* Create an API key
* Create an OAuth Client ID
* -- Select your scope : "https://www.googleapis.com/auth/youtube"
* -- Select your test users
* Enable your app (Youtube Data API v3)

 
## Setup
To run this project:

# Modify api_config.py by providing
* A developer key obtained from the Google console
* The path(s) toward the json file(s) obtained from the Google console
* The channel_id of the youtube channel(s) you want to interact with.

# Run quota_estimation.py

```
$ python3 quota_estimation.py
```

Create enough projects and OAuth Client ID based on the output of this script.

* For exemple, if it states that you need at least 3 API projects to rate all the videos of the channels listed in the configuration file, then create at least 3 projects and OAuth Client ID in the Google console. 
* Then update api_config.py with your new .json files.


# Run like_videos.py
```
$ python3 like_videos.py
```
Follow the successive interaction requests to go through the different authentification flows.


# Down the rabbit hole,
Do we still have any excuse to not blindly love all they upload?
