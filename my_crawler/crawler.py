import argparse, os, time
import my_mapper as mapper
from my_attribute_obj import attribute_obj
from selenium import webdriver
from selenium.webdriver.common.by import By

LOGIN_NAME = "admin"
LOGIN_PASSWORD = "password"


def main():

    # reference to the fuzzer.py line: 17
    parser = argparse.ArgumentParser(description='Firmfuzz v1.0 crawler ')
    parser.add_argument('-u', '--url', default='http://127.0.0.1:8080')

    args = parser.parse_args()
    url = args.url
   

    # reference to the fuzzer.py line: 82
    # webPage = webdriver.Remote(desired_capabilities=webdriver.DesiredCapabilities.HTMLUNITWITHJS)
    # webPage = webdriver.Chrome(executable_path='/Users/arx/Documents/Lab/firmfuzz_crawler/fuzzer/my_crawler/chromedriver')
    webPage = webdriver.Chrome()

    try:
        webPage.get(url)
    except:
        print("Error in loading the page")
        exit()
    
    # reference to the fuzzer.py line: 109
    perform_auth(webPage)
    frame_list = webPage.find_elements(By.XPATH, '//frame')

    if frame_list:
        url_obj = mapper.ScrapeHrefWithFrames()
    
    else:
        url_obj = mapper.ScrapeFlatHref()
    
    webpage_obj = {}

    # scrape the url
    url_obj.scrape_url(webPage)

    #Creating attribute objects for each url
    for url in url_obj.url_list:
        webpage_obj[url] = attribute_obj(url)
    
    print(webpage_obj)

#referrnce to the perform_auth function of attack.py 
def perform_auth(webPage):

    try:
        print("[*] auth page: \n" + webPage.page_source)

        text_elements = webPage.find_elements(By.XPATH, "//input[@type='text']")
        password = webPage.find_element(By.XPATH, "//input[@type='password']")

        # output text elements and password element 
        for text_element in text_elements:
            print("[*] get text element: " + text_element.get_attribute("outerHTML"))
        print("[*] get password element: " + password.get_attribute("outerHTML"))

        try: 
            submit = webPage.find_element(By.XPATH, "//input[@type='submit']")
        except:
            # add code
            try:
                submit = webPage.find_element(By.XPATH, "//input[@type='button']")
            except:
                submit = webPage.find_element(By.XPATH, "//button[@type='submit']")
        
        if(len(text_elements) != 0):
            for element in text_elements:
                if (element.is_displayed()):
                    login = element

        login.clear()
        password.clear()

        if(LOGIN_NAME != '#'):
            login.send_keys(LOGIN_NAME)
        if(LOGIN_PASSWORD != '#'):
            password.send_keys(LOGIN_PASSWORD)

        submit.click()
        time.sleep(1)

        print("[*] home page html:\n" + webPage.page_source)
    
    except:
        print("Error in authentication 0")


if __name__ == '__main__':
    main()