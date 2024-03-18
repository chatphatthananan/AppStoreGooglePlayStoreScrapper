from ast import Index
from operator import index
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#from packaging.version import Version, parse #To compare version numbers
import pandas as pd
import datetime
import os
import logging
from datetime import date
import config
from SGTAMProdTask import SGTAMProd
from config import SGTAM_log_config
from pretty_html_table import build_table

if __name__ == '__main__':
  # setup logging
  logging.basicConfig(
      filename= f"log\{datetime.datetime.now().strftime('%Y%m%d%H%M')}_iOSVersionScraper.log",
      format='%(asctime)s %(levelname)s %(message)s',
      level=logging.INFO
  )

  s = SGTAMProd()
  config.SGTAM_log_config['statusFlag'], config.SGTAM_log_config['logID']  = s.insert_tlog(**config.SGTAM_log_config)

  logging.info("iOS Version Scraper Started")

  # your script here
  try:
    # set pandas to show all columns on terminal
    pd.set_option('display.max_columns', None)

    # Creating an empty Dataframe with column names only
    df_appInfos = pd.DataFrame(columns=['App_Name', 'Latest_Version', 'Last_Updated_Date'])

    # set up chrome driver
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    
    # driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    # temporary fix for Chrome driver being outdated
    driver = webdriver.Chrome(executable_path=r"D:\SGTAM_DP\Working Project\AppStoreGooglePlayStoreScraper\source\iOS\chromeDrivers\chromedriver.exe", options=chrome_options)
    
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 20)

    # loop through each url to scrape the respective app information
    for app in config.ios_app_url_list:  
      driver.get(app)
      # wait for the page to load
      wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[3]/main/div[2]/section[1]/div/div[2]/header/h1")))

      # scrape app name
      title = driver.find_element(by=By.XPATH, value='/html/body/div[3]/main/div[2]/section[1]/div/div[2]/header/h1')
      app_title = title.text

      # scrape app latest version and update date
      driver.find_element(by=By.CLASS_NAME, value='version-history').click()
      ul = driver.find_element(by=By.CLASS_NAME, value='version-history__items')
      lis = ul.find_elements(by=By.CLASS_NAME, value='version-history__item')
      version = lis[0].find_element(by=By.CLASS_NAME, value='version-history__item__version-number')
      last_updated_date = lis[0].find_element(by=By.CLASS_NAME, value='version-history__item__release-date')
      app_version = version.text
      last_updated = last_updated_date.text
      
      # Put all info into a row before append to the data frame
      new_row = {'App_Name':app_title, 'Latest_Version':app_version, 'Last_Updated_Date':last_updated}
      df_appInfos = df_appInfos.append(new_row, ignore_index=True)

    # close driver
    #driver.close()
    driver.quit()

    # export daily app info to csv file with date, to D and M drive. (M is for Lars)
    df_appInfos.to_csv(config.output_D_drive + config.file_name, index=False , header=True, sep=';')
    logging.info('Today records exported to '+ config.output_D_drive + config.file_name)
    #df_appInfos.to_csv(config.output_M_drive + config.file_name, index=False , header=True, sep=';')
    #logging.info('Today records exported to '+ config.output_M_drive + config.file_name)
    #df_appInfos.to_csv(config.output_personal + config.file_name, index=False, header=True, sep=';' )

    # comparison stage
    if config.date_today == config.deployed_date: #if today is first deployment date then not doing any comparison
      config.SGTAM_log_config['statusFlag'] = 1
      config.SGTAM_log_config['logMsg'] = 'App is deployed today, no previous csv file to compare.'
      logging.info(config.SGTAM_log_config['logMsg'])
      print(config.SGTAM_log_config['logMsg'])
    else: # will do comparison and export out results and send email if there is any difference
      # read in today and ytd csv file
      logging.info("Comparision started.")  
      df_appInfos_today = pd.read_csv(config.output_D_drive + config.file_name)
      df_appInfos_yesterday = pd.read_csv(config.output_D_drive + config.file_name_previous)
     
      # compare and get the difference for both today and ytd file, and then insert date column into both dataframes
      results_todayfile = df_appInfos_today[~df_appInfos_today.apply(tuple,1).isin(df_appInfos_yesterday.apply(tuple,1))]
      results_yesterdayfile = df_appInfos_yesterday[~df_appInfos_yesterday.apply(tuple,1).isin(df_appInfos_today.apply(tuple,1))]
      logging.info("Comparision completed.") 
      # insert date column into result df
      results_todayfile.insert(loc=0, column='Date', value=config.date_today)
      results_yesterdayfile.insert(loc=0, column='Date', value=config.date_yesterday)
      
      
      # if no unmatched, no action will be taken, update tlog
      if results_todayfile.empty and results_yesterdayfile.empty:
        config.SGTAM_log_config['statusFlag'] = 1
        config.SGTAM_log_config['logMsg'] = 'No unmatched records.'
        logging.info(config.SGTAM_log_config['logMsg'])  
      # if unmatched, send out warning email and export out unmatched records in csv file
      else:
        config.SGTAM_log_config['statusFlag'] = 3
        config.SGTAM_log_config['logMsg'] = 'Unmatched records found.'
        logging.info(config.SGTAM_log_config['logMsg'])
        print(config.SGTAM_log_config['logMsg'])
        unmatched_today_yesterday = pd.concat([results_todayfile, results_yesterdayfile])
        unmatched_today_yesterday.to_csv(config.output_D_drive + config.file_name_unmatched, index=False , header=True, sep=';')
        logging.info("Unmatched records exported to " + config.output_D_drive)
        html_unmatched = build_table(unmatched_today_yesterday, 'blue_light') 
        config.email['subject'] = '[WARNING] iOS Version Scraper'
        config.email['body'] = "*This is auto generated email, please do not reply to it." + "<p>Unmatched records for iOS Version Scraper found.</p>" + "<p>More details and comparison can be found at: </p>" + config.output_D_drive + "<p></p>" + html_unmatched 
  except Exception as exception:
    config.SGTAM_log_config['statusFlag'] = 2
    config.SGTAM_log_config['logMsg'] = exception
    logging.info(exception)
    print('There is an exception, please check the log\n')
    print(exception)
    config.email['subject'] = '[ERROR] iOS Version Scraper'
    config.email['body'] = config.SGTAM_log_config['logMsg']
  finally:
    if config.SGTAM_log_config['statusFlag'] in [2,3]:
      #send email and update tlog
      print("There is/are unmatched record(s) or possibly an error, email is sent.")
      s.send_email(**config.email)
      s.update_tlog(**config.SGTAM_log_config)
      logging.info("There is/are unmatched record(s) or possibly an error, email is sent.")
    else:
      print("No unmatched records, email will not be sent.")
      s.update_tlog(**config.SGTAM_log_config)
      logging.info("No unmatched records, email will not be sent.")

      


  


