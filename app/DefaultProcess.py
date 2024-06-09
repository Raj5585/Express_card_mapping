import os
from qrlib.QRProcess import QRProcess
from qrlib.QRDecorators import run_item
from qrlib.QRRunItem import QRRunItem
from ccms_component import CCMSComponent
from Email_component import EmailComponent
from FTP_Component import FTPComponent
from qrlib.QRUtils import get_secret, display
import Constants
from datetime import datetime
from Utils import close_edge,formatting_excel_file

class DefaultProcess(QRProcess):

    def __init__(self):
        super().__init__()
        self.data = []

        self.ccms_component = CCMSComponent()
        self.email_component = EmailComponent()
        self.ftp_component = FTPComponent()
        self.register(self.ccms_component)
        self.register(self.email_component)
        self.register(self.ftp_component)

    @run_item(is_ticket=False)
    def before_run(self, *args, **kwargs):
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)
        close_edge()
        self.ccms_component.load_ccms_vault()
        self.ccms_component.open_ccms()
        self.ccms_component.login_ccms()
        # self.ccms_component.download_excelfile()

    @run_item(is_ticket=False, post_success=False)
    def before_run_item(self, *args, **kwargs):
        run_item = QRRunItem(is_ticket=True)
        self.notify(run_item)
        logger = run_item.logger
        
        self.ccms_component.download()
        files = os.listdir(Constants.download_path)
        txt_files = [file for file in files if file.endswith('.txt')]
        
        with self.ftp_component as ftp:
            ftp.reset_wd()
            display(f'{Constants.zip_file}.zip')
            ftp.upload_file_and_delete(Constants.download_path,txt_files[0])
        display(f"sucessfully uploaded {Constants.zip_file} to ftp")
        logger.info(f"sucessfully uploaded {Constants.zip_file} to ftp")
        
        logger.info(f"Sending mail to neps")
        self.email_component.mail_to_neps()
        logger.info(f"Mail sent to Neps")
        
        run_item.report_data["Process Status"] = f" mail sent to neps"
        report_data = {'Mail to neps': 'sent'}
        run_item.report_data = report_data
        run_item.set_success()
        run_item.post()

    @run_item(is_ticket=True)
    def execute_run_item(self, *args, **kwargs):
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)
        
    
        

    @run_item(is_ticket=True)
    def execute_run_item_credit_other(self, *args, **kwargs):
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)
        

    @run_item(is_ticket=False, post_success=False)
    def after_run_item(self, *args, **kwargs):
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)


    @run_item(is_ticket=False, post_success=False)
    def after_run(self, *args, **kwargs):
        run_item: QRRunItem = kwargs["run_item"]
        self.notify(run_item)
        try:
            self.ccms_component.logout_ccms()
        except:
            display("CCMS not logged in  ......")
        close_edge()

    def execute_run(self):
        run_item = QRRunItem(is_ticket=True)
        self.notify(run_item)
        logger = run_item.logger
        
        # display("downloadig the file from ftp")
        # with self.ftp_component as ftp:
        #     ftp.list_and_download_txt_files(Constants.download_path)
        # display("download sucessfull ")
        formatting_excel_file()
        display("excel file formatted and saved sucessfull ")
        
        
        
        
        run_item.report_data["Process Status"] = f" Task completed"
        report_data = {'card': 'debit and credit'}
        run_item.report_data = report_data
        run_item.set_success()
        run_item.post()

