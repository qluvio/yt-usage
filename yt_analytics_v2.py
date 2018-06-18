# -*- coding: utf-8 -*-

import os
import site
site.addsitedir('/usr/local/lib/python2.7/site-packages') 
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
import pandas as pd
import json
import argparse

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly',
          'https://www.googleapis.com/auth/youtube.readonly',
          #'https://www.googleapis.com/auth/yt-analytics-monetary.readonly'
          ]

API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'
CLIENT_SECRETS_FILE = 'client_secret.json'
def get_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = flow.run_console()
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def execute_api_request(client_library_function, **kwargs):
  response = client_library_function(
    **kwargs
  ).execute()
  print(response)
  with open(args.local_file, 'a') as outfile:
      json.dump(response, outfile)

if __name__ == '__main__':
  # Disable OAuthlib's HTTPs verification when running locally.
  # *DO NOT* leave this option enabled when running in production.
  # os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

  youtubeAnalytics = get_service()

  parser = argparse.ArgumentParser()
  parser.add_argument('--startDate', default='1/1/2018',
      help='start date for the reports that you are retrieving')
  parser.add_argument('--endDate', default='6/1/2018',
      help='end date for the reports that you are retrieving')
  parser.add_argument('--videoIDs', nargs='+',
      help='videos IDs for the reports that you are retrieving')
  parser.add_argument('--countryIDs', nargs='+',
      help='country ID for the reports that you are retrieving')
  parser.add_argument('--channelID', default='MINE',
      help='channel ID for the reports that you are retrieving')
  parser.add_argument('--local_file', default='viewerStat.json',
      help='The name of the local file where the downloaded report will be written.')
  args = parser.parse_args()

  dates = pd.date_range(start=args.startDate, end=args.endDate)
  vids = args.videoIDs #['mgDmuzA9-iM','sBkl5Lz965o']
  for date in dates: #['2018-05-10', '2018-05-11']:
      dt = str(date)[:10]
      for vid in vids:
          for cid in args.countryIDs:
              response = {"date": dt,
                          "video_id": vid,
                          "country": cid,
                          "channel_id": args.channelID}
              with open('viewerStat.json', 'a') as outfile:
                  json.dump(response, outfile)

              print 'date:{}, video_id:{}, country:{}'.format(dt, vid, cid)
              execute_api_request(
                  youtubeAnalytics.reports().query,
                  ids='channel=={}'.format(args.channelID),
                  startDate=dt,
                  endDate=dt,
                  metrics='views,estimatedMinutesWatched,averageViewDuration',
                  filters='video=={};country=={}'.format(vid, cid),
                  dimensions='province',
                  sort='province'
              )



