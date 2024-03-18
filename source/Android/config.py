import datetime
import os
from datetime import date

##******Android******##
# No version
mewatch_android = 'sg.mediacorp.android'
cna_android = 'com.channelnewsasia'
# Have versions
eight_world_android = 'com.mediacorp.sg.channel8news'
berita_android = 'com.mediacorp.sg.beritamediacorp'
berita_harian_android = 'com.sph.bhandroid'
seithi_android = 'com.mediacorp.sg.seithimediacorp'
zaobao_android = 'com.zb.sph.zaobaosingapore'

android_app_list = [mewatch_android, cna_android, eight_world_android, 
            berita_android, berita_harian_android, seithi_android, zaobao_android]


# set first deployment date
deployed_date = datetime.datetime(2022,10,8).strftime("%Y-%m-%d")

# today's date
date_today = datetime.datetime.now().strftime("%Y-%m-%d")

# yesterday's date
date_yesterday = (datetime.datetime.now() - datetime.timedelta(1)).strftime("%Y-%m-%d")

# csv name
file_name = "android_apps_infos_" + date_today + ".csv"
file_name_previous = "android_apps_infos_" + date_yesterday + ".csv"
file_name_unmatched = "unmatched_android_" + date_today + ".csv"

# output directories
#output_M_drive = "M:/05. Data Production/Project/AppStoreGooglePlayStoreScraper/files/Android/"
output_D_drive = "D:/SGTAM_DP/Working Project/AppStoreGooglePlayStoreScraper/source/Android/output/"
#output_personal = 'D:/AppStoreGooglePlayStoreScraper/source/'

#SGTAMDPTeam@gfk.com
email = {
        'sender' : 'xxx',
        'to' : 'xxx',
        'cc' : '',
        'subject' : '',
        'body' : '',
        'is_html' : True
    }


SGTAM_log_config = {
                    'logTaskID' : 110,
                    'statusFlag' : 2,
                    'logMsg' : 'Android App Version Scraper Started',
                    'logID' : None
                }

