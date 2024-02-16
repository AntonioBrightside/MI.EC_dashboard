import numpy as np

from source.GoogleSpreadSheets import *
from source.BigQuery import *
from source.CSVProcessing import *
from google.cloud import bigquery
import pandas as pd

if __name__ == "__main__":
    # Download EC data from Google SpreadSheets
    # downloadDataFromGStoCSV(getAPIConnection(scopes))

    # CSV PreProcessing
    df = makeDF()
    df = preProcessingDF(df)
    df = createNewColumns(df)

    print(df.info())




