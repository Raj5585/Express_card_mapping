import subprocess
import re
import os
import shutil

import pandas as pd
import Constants
from qrlib.QRUtils import display
downloaded_files_names = []

def delete_files_in_folder(logger,path):
    # path = Constants.download_path
    files = os.listdir(path=path)
    for file in files:
        display(file)
        file_path = os.path.join(path, file)
        os.remove(file_path)
        logger.info(f'{file} deleted')

def rename_and_move(logger,card_type):
    path = Constants.download_path
    files = os.listdir(path=path)
    for file in files:
        display(file)
        file_path = os.path.join(path, file)
        if os.path.isfile(file_path):
            name, ext = os.path.splitext(file)  # Split filename and extension
            new_name = f'{name}_{card_type}{ext}'  # Append '_new' to the filename
            renamed = os.path.join(path, new_name)
            try:
                os.rename(file_path, renamed)
                downloaded_files_names.append(new_name)
                logger.info(f'new pdf name: {new_name} and path is: {renamed}')
            except Exception as e:
                logger.error(f'Error renaming file: {file}. {e}')
                continue

            # Create the directory if it doesn't exist
            final_folder_path = os.path.join(Constants.final_path, 'all_files')
            if not os.path.exists(final_folder_path):
                os.makedirs(final_folder_path)

            moved_name = os.path.join(final_folder_path, new_name)
            shutil.move(renamed, moved_name)

def close_edge():
    call = 'TASKLIST', '/FI', 'imagename eq msedge.exe'
    tasks = subprocess.check_output(call).decode().split("\r\n")
    arr1 = []
    for task in tasks:
        m = re.match("(.+?) +(\d+) (.+?) +(\d+) +(\d+.* K).*",task)
        if m is not None:
            arr1.append({"image":m.group(1),
                        "pid":m.group(2),
                        "session_name":m.group(3),
                        "session_num":m.group(4),
                        "mem_usage":m.group(5)
                        })
    for item in arr1:
        call1 = 'wmic path Win32_PerfFormattedData_PerfProc_Process where "IDProcess=%s" get PercentProcessorTime' % item["pid"]
        output1 = subprocess.check_output(call1).decode()
        last_line = output1.strip().split('\r\n')[-1]
        print(last_line)
        print(type(last_line))

        if len(last_line) > 0:
            percent = int(last_line)
            if percent >=65:
                print("taskkill")
                subprocess.run(['taskkill', '/pid', f'{item["pid"]}', '/f'])


# def file_decryption():
# from Crypto.Cipher import AES
# import os

# def double_click_and_decrypt(file_path, password):
#     if os.name == 'nt':  # For Windows
#         subprocess.Popen(['start', '', file_path], shell=True)
#     elif os.name == 'posix':  # For Unix/Linux/Mac
#         subprocess.Popen(['xdg-open', file_path])
#     else:
#         raise NotImplementedError("Unsupported operating system")

#     # Wait for the user to interact with the file

#     # Assuming the file is now decrypted and saved as decrypted_file_path
#     decrypted_file_path = file_path + ".decrypted"

#     # Decrypt the file
#     cipher = AES.new(password, AES.MODE_ECB)
#     with open(file_path, 'rb') as encrypted_file:
#         with open(decrypted_file_path, 'wb') as decrypted_file:
#             decrypted_file.write(cipher.decrypt(encrypted_file.read()))

#     return decrypted_file_path

# # Usage:
# file_path = '/path/to/encrypted/file.txt'
# password = b'your_password_here'  # Convert password to bytes if not already
# decrypted_file_path = double_click_and_decrypt(file_path, password)
# print(f"File decrypted and saved at: {decrypted_file_path}")
def formatting_excel_file():
    df_sample = pd.read_excel(Constants.sample_file,dtype=str)
    display("sample----------------")
    display(df_sample)
    df_raw = pd.read_excel(Constants.raw_file,dtype=str,skiprows=[0])
    display("raw----------------")
    display(df_raw)
    # df1 = pd.concat([df1, df2], ignore_index=True)
    df_raw.columns = df_sample.columns
    display("merg----------------")
    display(df_raw)
    df_raw.to_excel(Constants.formatted_file,index=False,engine='xlsxwriter')
    
        

        