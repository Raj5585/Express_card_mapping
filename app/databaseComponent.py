
import pandas as pd
import sqlite3
from datetime import datetime
import Constants
from qrlib.QRUtils import  display
from qrlib.QRComponent import QRComponent 
import oracledb
current_date = datetime.now().strftime('%Y-%m-%d')

class DBComponent(QRComponent):
    def __init__(self):
        self.conn = None
        self.cur = None
        self.table_name = Constants.db_table_name
        
        
    def connect(self):
        self.conn = sqlite3.connect(Constants.DB_PATH)
        self.cur = self.conn.cursor()
        display("databased connected !!!! ")
    
    def close_connection(self):
        self.cur.close()
        self.conn.close()
        
    def create_table(self):
        logger = self.run_item.logger
        self.con = sqlite3.connect(Constants.DB_PATH)
        self.cur = self.con.cursor()

        query = f'''
            CREATE TABLE IF NOT EXISTS {self.table_name} (
                inserted_date VARCHAR(55),
                ftp_download VARCHAR(55),
                updated_date VARCHAR(55)
            )
        '''
        self.cur.execute(query)
        self.con.commit()
        self.con.close()
        display(f'Successfully created table {self.table_name} with columns filename and last_inserted_date')
        logger.info(f'Successfully created table {self.table_name} with columns filename and last_inserted_date')

    # def create_trigger(self):
    #     self.con = sqlite3.connect(Constants.DB_PATH)
    #     self.cur = self.con.cursor()
    #     query = f"""
    #     CREATE TRIGGER IF NOT EXISTS update_timestamp AFTER UPDATE ON  {self.table_name} FOR EACH ROW
    #     BEGIN UPDATE {self.table_name} SET updated_date = (datetime('now', 'localtime')); END;"""
    #     self.con.row_factory = sqlite3.Row
    #     self.con.execute(query)
    #     self.con.commit()
    #     self.con.close()
        
    # def create_trigger(self):
    #     self.con = sqlite3.connect(Constants.DB_PATH)
    #     self.cur = self.con.cursor()
    #     query = f"""
    #     CREATE TRIGGER IF NOT EXISTS update_timestamp AFTER UPDATE ON {self.table_name} FOR EACH ROW
    #     BEGIN 
    #         UPDATE {self.table_name} SET updated_date = datetime('now', 'localtime');
    #     END;"""
    #     self.con.execute(query)
    #     self.con.commit()
    #     self.con.close()

    def insert_data(self, inserted_date):
        display(F'INSERTED DATE PRINTING FROM DB {inserted_date}')
        logger = self.run_item.logger
        self.con = sqlite3.connect(Constants.DB_PATH)
        self.cur = self.con.cursor()
        existing_data_query = f'''
            SELECT COUNT(*) FROM {self.table_name} WHERE inserted_date = '{inserted_date}'
        '''
        self.cur.execute(existing_data_query)
        existing_data_count = self.cur.fetchone()[0]
        
        if existing_data_count > 0:
            display('Data already exists in the database for the provided inserted_date')
            logger.info('Data already exists in the database for the provided inserted_date')
        else:
            insert_query = f'''
                INSERT INTO {self.table_name} (inserted_date, batch_uploaded, ftp_uploaded, updated_date)
                VALUES ('{inserted_date}', 'pending', 'pending', '{datetime.now().strftime('%Y-%m-%d')}')
            '''
            self.cur.execute(insert_query)
            self.con.commit()
            display('Successfully inserted data into the database')
            logger.info('Successfully inserted data into the database')
        self.con.close()
        
        
    def update_ftp_status(self,ftp_status):
        logger = self.run_item.logger
        display(f'batch Status is {ftp_status} ')
        self.con = sqlite3.connect(Constants.DB_PATH)
        self.cur = self.con.cursor()
        update_query = f'''
                UPDATE {self.table_name}
                SET ftp_uploaded = '{ftp_status}'
                WHERE updated_date = '{datetime.now().strftime('%Y-%m-%d')}';
            '''
            # Execute the update query with parameters
        self.cur.execute(update_query)
        display(f'updated query is {update_query}')
        logger.info(f'updated query is {update_query}')
        self.con.execute(update_query)
        self.con.commit()
        self.con.close()
        
    def get_present_data(self):
        self.con = sqlite3.connect(Constants.DB_PATH)
        self.cur = self.con.cursor()
        query = f'''
             SELECT * FROM {self.table_name}
            WHERE updated_date ='{datetime.now().strftime('%Y-%m-%d')}';
        '''
        self.cur.execute(query)
        self.con.row_factory = sqlite3.Row
        data = self.con.execute(query).fetchall()
        if data:
            temp_value = [{str(key): item[key] for key in item.keys()} for item in data]
            result_dict = {idx: row for idx, row in enumerate(temp_value)}
            return result_dict
            # df = pd.DataFrame(temp_value)
            # return df.to_dict()
        else:
            return []
        

