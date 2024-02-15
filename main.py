from source.downloadDataFromGS import *
from source.getBigQueryConnection import *
from google.cloud import bigquery

if __name__ == "__main__":
    # Download EC data from Google SpreadSheets
    downloadDataFromGStoCSV(getAPIConnection(scopes))

