# -*- coding: utf-8 -*-
import time

from selenium import  webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
options = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(options=options)
driver.start_client()
driver.get('https://detail.tmall.com/item.htm?spm=a230r.1.14.8.68625295XTvdN4&id=573227813116&cm_id=140105335569ed55e27b&abbucket=9')
wait = WebDriverWait(driver,5)
driver.find_element_by_id('sufei-dialog-close')
close_button = wait.until(lambda d:d.find_element_by_id('sufei-dialog-close'))
close_button.click()


time.sleep(5)
