import gspread
import pandas
from oauth2client.service_account import ServiceAccountCredentials

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/cloud-platform"
]

# ECenter data. Jetstat statistics
spreadSheet = "1hkFVZAI8xjH17fKyMhzpTzLX6jn26JGdH-maHz36o0U"


def getAPIConnection(scopes):
    """
    Get connection to API Google SpreadSheets
    :return: worksheet
    """

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        r"D:\1. Other\1. Work\1. Programming\# keys\Google API\continual-block-407808-f16acc48f950.json",
        scopes=scopes)

    file = gspread.authorize(credentials)
    wb = file.open("Jetstat_отчет")
    worksheet = wb.get_worksheet_by_id(962690706)  # by gid

    return worksheet


def downloadDataFromGStoCSV(worksheet):
    """
    Download *csv data from 'Jetstat' tab to 'data' directory
    """
    dataFrame = pandas.DataFrame(worksheet.get_all_records())

    dataFrame.to_csv(r"D:\1. Other\1. Work\1. Programming\1. Projects\EdgeCenter Google Docs stat\data\jetstat.csv",
                     index=False,
                     header=True,
                     encoding="utf-8")


def downloadDataFromGStoXLSX(worksheet):
    """
    Download *xlsx data from 'Jetstat' tab to 'data' directory. Works much slower than *csv variant (~3-6 times)
    """
    dataFrame = pandas.DataFrame(worksheet.get_all_records())

    dataFrame.to_excel(r"D:\1. Other\1. Work\1. Programming\1. Projects\EdgeCenter Google Docs stat\data\jetstat.xlsx",
                       index=False,
                       header=True,
                       sheet_name="Jetstat")
