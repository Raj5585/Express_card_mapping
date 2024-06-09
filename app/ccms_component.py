
from glob import glob
import os
import time
from robot.libraries.BuiltIn import BuiltIn
from RPA.Browser.Selenium import Selenium, ChromeOptions
from selenium.common.exceptions import TimeoutException
from selenium import webdriver

from qrlib.QRComponent import QRComponent
from qrlib.QREnv import QREnv
from Utils import rename_and_move,delete_files_in_folder
import Constants
import pandas as pd

display = BuiltIn().log_to_console


class CCMSComponent(QRComponent):
    def __init__(self):
        super().__init__()
        self.selenium = Selenium()
        self.username = ''
        self.password = ''
        self.url = ''
        self.download_path = "C:/Users/RPA/Documents/bots/prime-card-activation/prime-card-activation/download_folder"

    def load_ccms_vault(self):
        self.ccms_vault = QREnv.VAULTS['ccms']
        self.username = self.ccms_vault['username']
        self.password = self.ccms_vault['password']
        self.url = self.ccms_vault['url']
        # display(f"usernmae: {self.username}, password: {self.password}, url: {self.url}")

    def open_ccms(self):
        logger = self.run_item.logger
        ie_options=webdriver.IeOptions()
        ie_options.attach_to_edge_chrome=True
        ie_options.ignore_zoom_level=True
        # ie_options.edge_executable_path=BROWSER_PATH
        ie_options.native_events = True
        ie_options.ignore_protected_mode_settings=True
        ie_options.require_window_focus=False
        ie_options.add_additional_option("ie.edgechromium", True)
        edge_options = webdriver.EdgeOptions()
        edge_options.use_chromium = True
        edge_options.add_argument("ie-mode-test")
        self.selenium.set_download_directory(Constants.download_path)

        self.selenium.open_available_browser(url=self.url, browser_selection='edge') #, download=True, options=ie_options)
        display("opened Browser")
        self.selenium.maximize_browser_window()
        display("maximized Browser")
        logger.info("Browser opened")
        logger.info('CCMS browser opened successfully')

    def login_ccms(self):
        for i in range(1, 4):
            try:
                self.selenium.wait_until_element_is_visible('//div[@class="login-box"]', timeout=Constants.TIMEOUT)
                self.selenium.wait_until_element_is_visible('//input[@name="_username"]', timeout=Constants.TIMEOUT)
                self.selenium.input_text('//input[@name="_username"]', text=self.username, clear=True)
                self.selenium.wait_until_element_is_visible('//input[@name="_password"]', timeout=Constants.TIMEOUT)
                self.selenium.input_password('//input[@name="_password"]', password=self.password, clear=True)
                self.selenium.wait_until_element_is_visible('//button[@type="submit"]', timeout=Constants.TIMEOUT)
                self.selenium.click_button('//button[@type="submit"]')
                self.selenium.wait_until_element_is_visible('//span[contains(text(),"Card Request")]', timeout=15)
                break
            except Exception as e:
                if self.selenium.is_element_visible("//div[contains(@class, 'login-error-msg')]"):
                    continue
                else:
                    raise Exception(e)

    def logout_ccms(self):
        logger = self.run_item.logger
        logger.info("logging out from CCMS")
        display("logging out from CCMS")
        self.wait_and_click('//a[@class="dropdown-toggle"]/span[@class="hidden-xs"]')
        self.wait_and_click('//div[@class="pull-right"]/a[@class="btn btn-default btn-flat"]')
        logger.info("logged out from CCMS")
        display("logged out from CCMS")

        
    def close_browser(self):
        self.selenium.close_browser()
                    
    def download(self):
        logger = self.run_item.logger
        delete_files_in_folder(logger,Constants.download_path)
        xpath ={
            'debit':"//a[contains(text(),'Debit Card')]",
            'sid_card_express':"//span[contains(text(),'Siddhartha Express Card')]",
            'link_acc_to_switch':"//span[contains(text(),'Linked Account to Switch')]",
            
            'filter':"//div[@class='col-md-12 filter-btn-group clearfix']/button[contains(text(),'Filter')]",
            'card_remarks':"//select[@id ='card_list_to_switch_filter_remarks']",
            'no_record_found':"//p[contains(text(),'No record(s) found')]",
            'select_all':'//input[@name="selectAll"]',
            'download':'//a[@title="Export Excel"]'

        }
        logger.info(f"Debit card processing ..")
        display(f"Debit card processing ..")
        self.wait_and_click(xpath['debit'])
        self.wait_and_click(xpath['sid_card_express'])
        self.wait_and_click(xpath['link_acc_to_switch'])
        self.selenium.wait_until_element_is_visible(xpath['filter'])
        # display(f"--{card_remarks}---")
        # self.selenium.select_from_list_by_value(xpath['card_remarks'],f"{card_remarks}")
        self.wait_and_click(xpath['filter'])
        try:
            elem = self.selenium.find_element(xpath['no_record_found'])
            display(f"No record to download  {elem}")
        except:
            self.wait_and_click(xpath['select_all'])
            self.selenium.select_from_list_by_value(xpath['send_to_switch'],"export")
            self.wait_and_click(xpath['go'])
            text = self.selenium.handle_alert(action="ACCEPT",timeout=Constants.TIMEOUT)
            display(text)
            time.sleep(2)
            self.check_file_downloaded_or_not('.txt')
            # rename_and_move(logger,f'debit_{card_remarks}')
        display(f"downloading text file Completed ")
        logger.info(f"downloading text file Completed ")
                    
    def upload_file(self):
        logger = self.run_item.logger
        delete_files_in_folder(logger,Constants.download_path)
        xpath ={
            'debit':"//a[contains(text(),'Debit Card')]",
            'sid_card_express':"//span[contains(text(),'Siddhartha Express Card')]",
            'link_card_mapping':"//span[contains(text(),'Linked Card Mapping')]",
            'choose_file':'//input[@id="instant_card_mapping_form_mappingFile"]',
            'upload':'//button[@value="Upload"]',
        }
        logger.info(f"Uploading formatted file  ..")
        display(f"Uploading formatted file ..")
        self.wait_and_click(xpath['debit'])
        self.wait_and_click(xpath['sid_card_express'])
        self.wait_and_click(xpath['link_card_mapping'])
        self.selenium.choose_file(xpath['choose_file'], Constants.formatted_file)
        self.selenium.wait_until_element_is_visible(xpath['upload'])
        self.wait_and_click(xpath['upload'])
        display(f"formatted file upload to ccms ")
        logger.info("formatted file upload to ccms ")

    def wait_and_click(self, xpath):
        logger = self.run_item.logger if hasattr(self, 'run_item') else self.logger
        try:
            self.selenium.wait_until_element_is_visible(xpath, timeout=Constants.TIMEOUT)
            self.selenium.click_element(xpath)
        except Exception as e:
            logger.error(f'error processing xpath: {xpath}')
            logger.error(e)
            raise e
        
    def check_file_downloaded_or_not(self,file_extension):
        logger = self.run_item.logger

        file_path = Constants.download_path
        start_time = time.time()
        timeout_second = 700
        while (time.time() - start_time) < timeout_second: 
            # Use glob to check for files with the .xlsx extension
            files = glob(os.path.join(file_path, f"*{file_extension}"))
            # If files list is not empty, it means at least one .xlsx file exists
            if files:
                logger.info(f'downloaded files == {files}')
                break
            time.sleep(1)
        else:
            raise Exception(f"Time out while downloading file")