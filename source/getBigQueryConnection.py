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
