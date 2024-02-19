import numpy as np

from source.GoogleSpreadSheets import *
from source.BigQuery import *
from source.CSVProcessing import *
from google.cloud import bigquery
import pandas as pd

if __name__ == "__main__":
    # Download EC data from Google SpreadSheets
    # downloadDataFromGStoCSV(getAPIConnection(scopes))

    # JetStat *CSV PreProcessing
    pd.options.mode.chained_assignment = None
    # jetstatDF = pd.read_csv("data/jetstat.csv", delimiter=",", low_memory=False)
    pd.set_option('display.max_columns', None)
    # jetstatDF = preProcessingJetStatDF(jetstatDF)
    # jetstatDF = createNewColumnsJetStatDF(jetstatDF)
    # print(jetstatDF.info())

    # Leads *XLSX PreProcessing
    leadsDF = pd.read_excel("data/leads_before.xlsx")

    leadsDF['UTM Term'].fillna(value="n/a", inplace=True)
    columnsToAdd = ['UID', 'CID', 'GID', 'GEO', 'DEVICE']

    for num, column in enumerate(columnsToAdd, start=0):
        leadsDF.insert(num, column, 'str')

    for num, cell in enumerate(leadsDF['UTM Campaign'], start=0):
        campaignName = cell.split(sep='_')
        leadsDF['UID'].loc[num] = campaignName[-1].replace(' ', '')

    for num, cell in enumerate(leadsDF['UTM Content'], start=0):
        contentName = cell.split(sep='|')
        leadsDF['CID'].loc[num] = contentName[contentName.index('cid') + 1]
        leadsDF['GID'].loc[num] = contentName[contentName.index('gid') + 1]
        leadsDF['DEVICE'].loc[num] = contentName[contentName.index('dvc') + 1]

        try:
            leadsDF['GEO'].loc[num] = contentName[contentName.index('region_name') + 1]
        except ValueError:
            leadsDF['GEO'].loc[num] = np.nan

    for column in columnsToAdd:
        if column in ['CID', 'GID']:
            leadsDF[column] = leadsDF[column].astype('int64')
        else:
            leadsDF[column] = leadsDF[column].astype('string')

    leadsDF['UTM Term'] = leadsDF['UTM Term'].astype('string')

    leadsDF = leadsDF.drop(axis='columns', columns=['UTM Source', 'UTM Medium', 'UTM Campaign', 'UTM Content',
                                                    'Причина провала', 'Источник удалить', '№'])

    print(leadsDF.head())
    print(leadsDF.info())

    # leadsDF.to_excel(r"C:\Users\Antonio\Desktop\leads_test.xlsx", index=False)
