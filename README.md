# yt-usage
Various python utilities for collecting usage data from youtube channels

Overview
This repo contains a set of python utilities that retrieves usage data for video titles on YouTube channels using the YouTube APIs.

Prerequisites

Python 2.7 or greater
The pip package management tool
The Google APIs Client Library for Python:
pip install --upgrade google-api-python-client
The google-auth, google-auth-oauthlib, and google-auth-httplib2 for user authorization
pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
Others: pandas
pip install --upgrade pandas
    
Setting up a project and running code samples

1.  Create a project in the Google API Console, enable YouTube APIs, and set up credentials (OAuth client ID) for 'other'.
2.  Save the client_secrets.json file associated with your credentials to a local file.
3.  Copy the code sample to a local file in the same directory as the client_secrets.json file 
4.  Run the sample from the command line and set command-line arguments as necessary:

    ```python sample.py --arg1=value1 --arg2=value2 ...```

5.  Most samples print data to STDOUT and output to .json/.csv.

Code Samples:

Retrieve videos id (my_uploads.py)
    Methods: youtube.channels.list, youtube.playlistItems.list
python my_uploads.py
return: videos titles and ids, output file: video_ids.txt

Retrieve detailed video information (videos.py)
    Methods: youtube.videos.list
python videos.py --videoIDs ‘paste ids in video_ids.txt returned by my_uploads.py’
return: metadata for videos, output file: videos.json

Create a reporting job (create_reporting_job.py)
Method: youtubeReporting.reportTypes.list, youtubeReporting.jobs.create
python create_reporting_job.py --name=’prefered name’ --report-type=’xxx’
prompt user for selections if not provided

Retrieve reports (retrieve_reports.py), requiring up to 48 hrs after reporting_job created 
Method: youtubeReporting.jobs.list,youtubeReporting.reports.list,
   youtubeReporting.media.download
python retrieve_reports.py --job_id=’xxx’ --local_file ‘reports.csv’
prompt job_ids for selections if not provided 
Return province viewer stats, stored in reports.csv 

Here is an example for a report job of ‘channel_province_a2’ type (desired)
 
head -1 reports.csv

date,channel_id,video_id,live_or_on_demand,subscribed_status,country_code,province_code,views,watch_time_minutes,average_view_duration_seconds,average_view_duration_percentage,annotation_click_through_rate,annotation_close_rate,annotation_impressions,annotation_clickable_impressions,annotation_closable_impressions,annotation_clicks,annotation_closes,card_click_rate,card_teaser_click_rate,card_impressions,card_teaser_impressions,card_clicks,card_teaser_clicks,red_views,red_watch_time_minutes

cat  reports.csv | grep "^20"

20180511,UCJgDI_pBbQ4ATUlU5dTekNg,mgDmuzA9-iM,on_demand,unknown,US,US-CA,18,85.756416666666667,285.85472222222222,91.914701679171131,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
20180608,UCJgDI_pBbQ4ATUlU5dTekNg,mgDmuzA9-iM,on_demand,unknown,US,US-CA,1,0.07481666666666667,4.489,1.4434083601286174,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
20180509,UCJgDI_pBbQ4ATUlU5dTekNg,mgDmuzA9-iM,on_demand,unknown,US,US-CA,1,0.80166666666666664,48.1,15.466237942122186,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
20180510,UCJgDI_pBbQ4ATUlU5dTekNg,mgDmuzA9-iM,on_demand,unknown,US,US-KS,4,2.7753,41.6295,13.385691318327975,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
20180510,UCJgDI_pBbQ4ATUlU5dTekNg,mgDmuzA9-iM,on_demand,unknown,US,US-CA,30,121.38006666666666,242.76013333333333,78.057920685959274,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
20180508,UCJgDI_pBbQ4ATUlU5dTekNg,mgDmuzA9-iM,on_demand,unknown,US,US-KS,1,4.0238666666666667,241.432,77.630868167202578,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
20180508,UCJgDI_pBbQ4ATUlU5dTekNg,yY9_MY7YKk8,on_demand,unknown,US,US-CA,4,1.15365,17.30475,5.45891167192429,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
20180508,UCJgDI_pBbQ4ATUlU5dTekNg,mgDmuzA9-iM,on_demand,unknown,US,US-CA,5,2.30205,27.624599999999997,8.88250803858521,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
20180508,UCJgDI_pBbQ4ATUlU5dTekNg,sBkl5Lz965o,on_demand,unknown,US,US-CA,8,4.5977333333333332,34.483,11.343092105263159,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
20180508,UCJgDI_pBbQ4ATUlU5dTekNg,yY9_MY7YKk8,on_demand,unknown,US,US-KS,1,5.2826166666666667,316.957,99.986435331230282,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
20180609,UCJgDI_pBbQ4ATUlU5dTekNg,mgDmuzA9-iM,on_demand,unknown,US,US-CA,2,0.098683333333333331,2.9605,0.9519292604501608,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0


Retrieve view stats for provinces (yt_analytics_v2.py) 
Takes a series of startDate/endDate/video IDs/country IDs/channel ID/local_file as inputs 
Methods: youtubeAnalytics.reports().query
python yt_analytics_v2.py  --startDate '5/10/2018' --endDate '5/11/2018'  --videoIDs ‘mgDmuzA9-iM’ ‘sBkl5Lz965o’ --countryID ‘US’ ‘CA’ --channelID ‘xx’ --local_file ‘viewerStat.json’
Return viewerStat.json

Datasets desired

Video dataset: call YouTube data API (my_uploads.py, videos.py) to retrieve detail info for each video, individually. Output saved as a JSON file.

Viewer dataset (two options):  

Calling YT Report API: create a report job (create_reporting_job.py) followed by report retrieval (retrieve_reports.py). Reports stored in a CSV file. 

Calling YT Analytics API (yt_analytics_v2.py), taking dates/video IDs/country ID/channel ID as parameters, output regional (province) viewer stats.
    

