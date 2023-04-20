"""
    Process CSV Task.
"""
import pandas as pd
from redis import Redis
from celery import shared_task
# from time import sleep

@shared_task()
def process_csv_task(input_file: str) -> str:
    """
        Process a CSV file with song play data,
        aggregating the total number of plays for
        each song and date combination.

        Args:
        input_file (str): Path to the input CSV file.

        Returns:
        str: Path to the output CSV file, which contains the processed data.

        The input file is read in chunks using pandas read_csv method,
        Each chunk is grouped by the 'Song' and 'Date' columns,
        and the total number of plays for each combination is calculated by
        aggregating the 'Number of Plays' column. The output CSV file contains
        three columns: 'Song', 'Date', and 'Total Number of Plays for Date'.

        Any existing output file with the same name as the input file will be overwritten.

        The method also deletes the input file from Redis after processing is complete.
    """
    redis = Redis()
    chunksize = 100000
    output_cols = ['Song', 'Date', 'Total Number of Plays for Date']
    output_file = f'processed_{input_file}'

    output_df = pd.DataFrame(columns=output_cols)

    for chunk in pd.read_csv(input_file, chunksize=chunksize):
        # sleep(10)
        grouped = chunk.groupby(['Song', 'Date'])['Number of Plays'].agg(['sum', 'count']).reset_index()
        grouped.columns = ['Song', 'Date', 'Total Number of Plays for Date', 'Number of Plays']
        output_df = pd.concat([output_df, grouped], ignore_index=True)
        output_df = output_df.drop('Number of Plays', axis=1)

    output_df.to_csv(output_file, index=False)

    redis.delete(input_file)

    return output_file
