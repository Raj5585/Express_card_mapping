import imaplib

from robot.libraries.BuiltIn import BuiltIn

from qrlib.QREnv import QREnv
from qrlib.QRComponent import QRComponent
from RPA.Email.ImapSmtp import ImapSmtp


display = BuiltIn().log_to_console
import Constants
from Utils import downloaded_files_names

class EmailComponent(QRComponent):
    def __init__(self):
        super().__init__()
        # send mail values
        self.body = ''
        self.recipients = '' #sender = rpa.operation@pcbl.com.np  
        
        # smtp connection
        self.account = ''
        self.password = ''
        self.server = ''
        self.port = ''
        self.cc = ''
        self.__vault_data = {}
        # self.__vault_data_imap = {}

    def _get_vault(self):
        # self.logger = self.run_item.logger
        self.__vault_data: dict = QREnv.VAULTS['smtp']
        # self.logger.info("Got vault data")
        display('Got vault data ')
    def _imap_from_vault(self):
        # self.logger = self.run_item.logger
        self.__vault_data: dict = QREnv.VAULTS['imap']
        display('Get imap vault successfully')
        # self.logger.info('Get imap vault successfully')
        

    def _get_imap_creds(self):
        # self.logger = self.run_item.logger
        self.imap_account = self.__vault_data['mail_account']
        self.imap_server = self.__vault_data['mail_host']
        self.imap_port = self.__vault_data['imap_port']
        self.imap_password = self.__vault_data['mail_password']
        display('get imap creadential successulfy')
        self.logger.info('get imap creadential successulfy')

    def imap_login(self):
        self.logger = self.run_item.logger
        self._imap_from_vault()
        imap = imaplib.IMAP4(self.__vault_data['mail_host'],int(self.__vault_data['imap_port']))
        imap.login(self.__vault_data['mail_account'],self.__vault_data['mail_password'])
        display('Logging imap cread successfully')
        self.imap = imap

    def _set_smtp_creds(self):
        # logger = self.run_item.logger
        self.account = self.__vault_data['account']
        self.server = self.__vault_data['server']
        self.port = self.__vault_data['port']
        # self.configpath = self.__vault_data['config_path']
        try:
            self.password = self.__vault_data['password']
        except:
            self.password = None

    def mail_to_neps(self):
        logger = self.run_item.logger
        recipients = ''
        self._get_vault()
        self._set_smtp_creds()
        # list_of_files =downloaded_files_names
        self.mail = ImapSmtp(smtp_server=self.server, smtp_port=int(self.port))
        self.mail.authorize_smtp(account=self.account, password=str(self.password), smtp_server=self.server, smtp_port=int(self.port),)
        self.subject = f'''{str(Constants.zip_file).replace('_','.')}'''
        #done        
        self.body = f''' 
        Dear Team,<br>
        We have attached BTRT file in FTP which contains:<br>
        '''
        # Add filenames to the body

        self.body += '''
            Request to run the BTRT in an urgent basis.
            '''
        self.mail.send_message(
            sender=self.account,
            recipients='rajdhakal.404@gmail.com',#'suraj.kaphle@pcbl.com.np',
            # cc='',
            subject=self.subject,
            body=self.body,
            # attachments=self.sending_file_list,
            html=True
        )
        display("mail sent")
        logger.info(f"Mail sent to {recipients}")
        