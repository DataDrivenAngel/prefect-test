from prefect import flow, task
from prefect.tasks import task_input_hash
from datetime import timedelta
import requests
import pandas as pd
import httpx

from prefect.blocks.system import Secret
secret_block = Secret.load("vantage-api-key")
# Access the stored secret
api_key = secret_block.get()





@task(cache_key_fn=task_input_hash
      , cache_expiration=timedelta(minutes = 60)
      , retries = 2
      , retry_delay_seconds = 1)
def get_data():
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey={api_key}'
    result = httpx.get(url)
    data = result.json()
    df = pd.DataFrame.from_dict(data['Time Series (5min)'])
    return df

@task
def agg_data(data):

    print(data.max())


@flow
def pipe_2():
    data = get_data()
    agg_data(data)
    

if __name__ == "__main__":
    pipe_2()
