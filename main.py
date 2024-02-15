from source.DownloadDataFromGS import *

if __name__ == "__main__":

    # Download EC data from Google SpreadSheets
    downloadDataFromGStoCSV(getAPIConnection(scopes, spreadSheet))


