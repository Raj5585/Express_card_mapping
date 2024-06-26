import datetime
from ftplib import FTP
import time
from qrlib.QREnv import QREnv
from qrlib.QRComponent import QRComponent
from qrlib.QRUtils import  display
import zipfile
import os


class FTPComponent(QRComponent):
    def __init__(self):
        """
        ftp_working_dir must start with '/'
        ftp_working_dir should be provided just after default working dir
        """
        super().__init__()
        self.__ftp_default_directory = "/Payment/RPA_CARD_BTRT/Neps"  # default directory for this bot in ftp /RPA/ManIntAdjustment
        # self.__ftp_default_directory = "E:\\RPA_TEST" # default directory for this bot in ftp /RPA/ManIntAdjustment
        self.ftp_working_dir = self.__ftp_default_directory   # "/RPA/ManIntAdjustment + / + 1"

    def load_ftp_vault(self):
        logger = self.run_item.logger
        logger.info("Accessing FTP vault")
        self.__ftp_vault = QREnv.VAULTS['ftp']
        logger.info(f'Vault {self.__ftp_vault}')
        self.__username = self.__ftp_vault['username']
        self.__password = self.__ftp_vault['password']
        self.__server = self.__ftp_vault['server']
        self.__port = int(self.__ftp_vault['port'])
        logger.info("Accessing FTP vault successful")

    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, *args):
        logger = self.run_item.logger
        self.__ftp.close()

    def __goto_working_directory(self):
        """Working directory of bot will be RPA/ManIntAdjustment/<folder>"""
        
        logger = self.run_item.logger

        logger.info('Checking present working directory is')
        if self.__ftp.pwd() == '/':
            logger.info('In root folder')
        else:
            logger.info('Not in default directory moving to root folder and changing to default directory')
            self.__ftp.cwd("/")
        logger.info(f'Changing to default bot directory in ftp {self.ftp_working_dir}')
        self.__ftp.cwd(self.ftp_working_dir)
        return self.__ftp.pwd()
    
    def connect(self):
        logger = self.run_item.logger
        self.__ftp = FTP()
        logger.info('Login to specific location')
        self.load_ftp_vault()
        self.__ftp.connect(self.__server, self.__port)
        self.__ftp.login(self.__username, self.__password)
        logger.info(f'Welcome message {self.__ftp.welcome}')
        logger.info('Login to FTP successful')
        logger.info('Changing to working directory based on config file')
        display('Changing to working directory based on config file---------------------connecteed')
        self.__goto_working_directory()

    def close_connection(self):
        logger = self.run_item.logger
        logger.info('Closing FTP connection')
        self.__ftp.close()

    def check_pwd(self):
        """Present working directory"""
        logger = self.run_item.logger
        pwd = self.__ftp.pwd()
        logger.info(f'Present directory is {pwd}')
        display(f'Present directory is {pwd}')
        return pwd

    def set_cwd(self, dir_name):
        """Change working directory within given ftp working directory"""
        working_dir = self.ftp_working_dir + '/' + dir_name
        display(f'from set_cwd------{working_dir}')
        self.__ftp.cwd(working_dir)
        display(f'current directory == {self.__ftp.cwd(working_dir)}')

    def reset_wd(self):
        """Reset working directory to default directory"""
        logger = self.run_item.logger
        logger.info('Resetting to working directory')
        self.__goto_working_directory()
        logger.info(f'Working directory after reset is {self.__ftp.pwd()}')

    # Check if directory exists (in current location)
    def directory_exists(self,dir):
        filelist = []
        self.__ftp.retrlines('LIST', filelist.append)
        for f in filelist:
            if f.split()[-1] == dir and f.upper().startswith('D'):
                return True
        return False
    
    def upload_file(self, local_path, filename):
        """Set the uploading directory and then upload file"""
        logger = self.run_item.logger
        file_path = local_path + '/' + filename
        logger.info(f'File to upload is {file_path}')
        with open(file_path, 'rb') as file:
            self.__ftp.storbinary(f'STOR {filename}', file)
        logger.info(f'File uploaded successfully to {file_path}')

    
    
    def upload_file_and_delete(self, local_path, filename):
        """Set the uploading directory and then upload file"""
        logger = self.run_item.logger
        file_path = local_path + '/' + filename
        logger.info(f'File to upload is {file_path}')
        with open(file_path, 'rb') as file:
            self.__ftp.storbinary(f'STOR {filename}', file)
        logger.info(f'File uploaded successfully to {file_path}')
        os.remove(file_path)
        logger.info(f'File deleted locally to {file_path}')



    # def list_and_download_txt_files(self, download_dir):
    #     """
    #     List all files in the FTP server and download files with '.txt' extension to the specified directory.
    #     """
    #     logger = self.run_item.logger
    #     listed_data = self.__ftp.nlst()
    #     logger.info(f"Listed data is {listed_data}")
        
    #     txt_files = [file for file in listed_data if file.endswith('.gpg')]
        
    #     for txt_file in txt_files:
    #         local_file_path = os.path.join(download_dir, txt_file)
    #         with open(local_file_path, 'wb') as local_file:
    #             self.__ftp.retrbinary(f'RETR {txt_file}', local_file.write)
    #         logger.info(f"Downloaded {txt_file} to {local_file_path}")


def list_and_download_txt_files(self, download_dir):
    """
    List all files in the FTP server and download files with '.gpg' extension to the specified directory.
    """
    logger = self.run_item.logger
    retries = 0
    while retries < 36:  # Retry for up to 3 hours (36 retries with a 5-minute interval)
        listed_data = self.__ftp.nlst()
        logger.info(f"Listed data is {listed_data}")
        txt_files = [file for file in listed_data if file.endswith('.gpg')]
        if txt_files:
            for txt_file in txt_files:
                local_file_path = os.path.join(download_dir, txt_file)
                with open(local_file_path, 'wb') as local_file:
                    self.__ftp.retrbinary(f'RETR {txt_file}', local_file.write)
                logger.info(f"Downloaded {txt_file} to {local_file_path}")
            break  # Break out of the loop if txt files are found and downloaded
        else:
            logger.info("No .gpg files found. Retrying in 5 minutes...")
            time.sleep(300)  # Wait for 5 minutes before retrying
            retries += 1
    else:
        logger.info("No .gpg files found even after waiting for 3 hours.")