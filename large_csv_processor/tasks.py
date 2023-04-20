import os
import pandas as pd
from celery import shared_task
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from redis import Redis
# from time import sleep

@shared_task()
def process_csv_task(input_file):
    redis = Redis()
    chunksize = 100000
    output_cols = ['Song', 'Date', 'Total Number of Plays for Date']
    output_file = f'processed_{input_file}'

    output_df = pd.DataFrame(columns=output_cols)

    for chunk in pd.read_csv(input_file, chunksize=chunksize):
        # sleep(10)
        grouped_chunk = chunk.groupby(['Song', 'Date'])['Number of Plays'].agg(['sum', 'count']).reset_index()
        grouped_chunk.columns = ['Song', 'Date', 'Total Number of Plays for Date', 'Number of Plays']
        output_df = pd.concat([output_df, grouped_chunk], ignore_index=True)
        output_df = output_df.drop('Number of Plays', axis=1)

    output_df.to_csv(output_file, index=False)

    redis.delete(input_file)

    return output_file
