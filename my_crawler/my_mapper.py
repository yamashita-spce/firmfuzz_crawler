from selenium import webdriver
from collections import defaultdict
import logging
# add import file
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

'''
This module is responsible for returning the different
url scraped from the router webpage.
'''

# logger = logging.getLogger('fuzzer.map_url')
logger = logging.getLogger(__name__)

class Scrape(object):

  def __init__(self):
    self.url_list = []

  def scrape_url(self):
    raise NotImplementedError("Needs to be implemented by subclass")

  def get_url(self):
    raise NotImplementedError("Needs to be implemented by subclass")

  
  def scrape_href(self, webPage, url_list):

    print("###  current running url: " + webPage.current_url + "###")
    blacklist = ['logout', 'javascript']
    
    attribute_elements = webPage.find_elements(By.XPATH, "//a")
    for element in attribute_elements:
      print("[*] Find " + element.get_attribute("outerHTML"))
    
    # time.sleep(1)

    #訪れた配列で格納
    href_candidates = filter(lambda x: x.get_attribute("href"), attribute_elements)
    hrefs = map(lambda x: x.get_attribute("href"), href_candidates)

    # add exception handling
    try:
      for candidate in hrefs:
          if candidate not in url_list and candidate[-1] != '#' and not any(member in candidate for member in blacklist):
              try:
                  webPage.get(candidate)
                  url_list.add(candidate)
                  print("[*] add url list " + candidate)
        
              except Exception as e:
                  print("recursion　Error: " + str(e))
                  print("[*] skippping " + candidate)
                  logger.info('Skipping %s', candidate)
                  continue

              self.scrape_href(webPage, url_list)  # 再帰呼び出し

    except Exception as e:
      print("hrefs Error: " + str(e))


  def remove_dead_links(self, url_list):
    '''
    Removes all duplicate URL and URL starting with #

    Parameters:
    url_list (list_str): List to contain the scraped URL

    Returns:
    url_list (list_str): The augmented scraped URL list
    '''
    url_list = filter(lambda x: "#" not in x, url_list)
    return set(url_list)

class ScrapeFlatHref(Scrape):
 
  def scrape_url(self, webPage):
    temp_list = set()
    self.scrape_href(webPage, temp_list)
    self.url_list = list(temp_list)

  def get_url(self, webPage):
    try:
      url = self.url_list.pop() 
      webPage.get(url)
      return url 
    except IndexError:
      return None

class ScrapeHrefWithFrames(Scrape):
 
  def scrape_url(self, webPage):
    #Checking if the URL has frames and creating appropriate obj
    frame_list = self.get_frames(webPage)
    current_url = webPage.current_url

    for frame in frame_list:
      temp_list = set()
      webPage.get(current_url)

      webPage.switch_to.frame(frame)
      self.scrape_href(webPage, temp_list) 

      self.url_list.extend(list(temp_list))
      webPage.switch_to.default_content()

  def get_frames(self, webPage):
    frame_list = []
    frame_elements = webPage.find_elements(By.XPATH, "//frame")
    for frame in frame_elements:
      frame_list.append(frame.get_attribute("name"))
    return frame_list

  def get_url(self, webPage):
    try:
      url = self.url_list.pop() 
      webPage.get(url)
      return url 
    except IndexError:
      return None
