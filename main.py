import gspread
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    r"D:\1. Other\1. Work\1. Programming\# keys\Google API\continual-block-407808-f16acc48f950.json", scopes=scopes)

file = gspread.authorize(credentials)
wb = file.open("Jetstat_отчет")
sheet = wb.get_worksheet(2)

# print(sheet)
for cell in sheet.range("A1:C5"):
    print(cell.value)
    