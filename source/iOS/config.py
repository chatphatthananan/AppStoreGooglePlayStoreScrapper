import datetime
import os
from datetime import date

email = {
        'sender' : 'xxx',
        'to' : 'xxx',
        'cc' : '',
        'subject' : '',
        'body' : '',
        'is_html' : True
    }

SGTAM_log_config = {
                    'logTaskID' : 109,
                    'statusFlag' : 2,
                    'logMsg' : 'iOS Version Scraper Started',
                    'logID' : None
                }

# url for each app
mewatch_ios = 'https://apps.apple.com/sg/app/mewatch-video-movies-tv/id566561555'
cna_ios = 'https://apps.apple.com/sg/app/cna-channel-newsasia/id520773971'
eight_world_ios = 'https://apps.apple.com/sg/app/8world/id920447931'
berita_ios = 'https://apps.apple.com/sg/app/berita-mediacorp/id982151128'
berita_harian_ios = 'https://apps.apple.com/sg/app/berita-harian-sg-for-iphone/id743558902'
seithi_ios = 'https://apps.apple.com/sg/app/seithi-mediacorp/id982161322'
zaobao_ios = 'https://apps.apple.com/sg/app/%E6%97%A9%E6%8A%A5/id654946831'

# store all urls into an array
ios_app_url_list = [mewatch_ios, cna_ios, eight_world_ios, berita_ios, berita_harian_ios, seithi_ios, zaobao_ios]

# output directories
output_D_drive = 'D:/SGTAM_DP/Working Project/AppStoreGooglePlayStoreScraper/source/iOS/output/'

# set first deployment date
deployed_date = datetime.datetime(2022,10,2).strftime("%Y-%m-%d")

# today's date
date_today = datetime.datetime.now().strftime("%Y-%m-%d")

# yesterday's date
date_yesterday = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d")

# csv name
file_name = "iOS_apps_infos_" + date_today + ".csv"
file_name_previous = "iOS_apps_infos_" + date_yesterday + ".csv"
file_name_unmatched = "unmatched_iOS_" + date_today + ".csv"