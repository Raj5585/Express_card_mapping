from datetime import datetime
TIMEOUT = 60

current_date = datetime.now()
present_date = current_date.strftime("%d_%m_%Y")

download_path = r'C:\Users\niraj.sharma\QuickFox\Card_mapping\download_path'
final_path= r'C:\Users\niraj.sharma\QuickFox\Card-Brt\final_file'
zip_folder= r'C:\Users\niraj.sharma\QuickFox\Card-Brt\final_file\all_files'
zipfilename = f'C:\\Users\\niraj.sharma\\QuickFox\\Card-Brt\\final_file\\BTRT_{present_date}'
zip_file = f'BTRT_{present_date}'

sample_file = r'C:\Users\niraj.sharma\QuickFox\Card_mapping\sample_file\samplefile.xlsx'
raw_file =r'C:\Users\niraj.sharma\QuickFox\Card_mapping\download_path\raw.xls'
formatted_file = r'C:\Users\niraj.sharma\QuickFox\Card_mapping\formatted_file\formatted_file.xls'
