from google.cloud import bigquery

client = bigquery.Client.from_service_account_json(
    json_credentials_path=
    r"D:\1. Other\1. Work\1. Programming\# keys\Google API\continual-block-407808-da38f6a782cc.json")


def testConnection(client):

    sqlQuery = """
         -- This query shows a list of the daily top Google Search terms.
     SELECT
        refresh_date AS Day,
        term AS Top_Term,
            -- These search terms are in the top 25 in the US each day.
        rank,
     FROM `bigquery-public-data.google_trends.top_terms`
     WHERE
        rank = 1
            -- Choose only the top term each day.
        AND refresh_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 WEEK)
            -- Filter to the last 2 weeks.
     GROUP BY Day, Top_Term, rank
     ORDER BY Day DESC
        -- Show the days in reverse chronological order.
    """

    query = client.query(sqlQuery)

    for row in query:
        print(row)


def loadDataset():
    job_config = bigquery.LoadJobConfig(source_format=bigquery.SourceFormat.CSV,
                                        skip_leading_rows=1,
                                        autodetect=True)
    with open(r"D:\1. Other\1. Work\1. Programming\1. Projects\EdgeCenter Google Docs stat\data\jetstat.csv", "rb") as f:
        job = client.load_table_from_file(f, "continual-block-407808.EdgeCenter.Jetstat_data", job_config=job_config)

    job.result()

    table = client.get_table("continual-block-407808.EdgeCenter.Jetstat_data")

    print(
        "Loaded {} rows and {} columns to {}".format(
            table.num_rows, len(table.schema), "continual-block-407808.EdgeCenter.Jetstat_data"
        )
    )



