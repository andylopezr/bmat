<img src="https://i.imgur.com/nvF2LV7.png" alt="process">

# Large CSV Processor

## Introduction

> This is a Django project that provides a Celery-based solution for processing large CSV files containing song play data. The project takes an input CSV file containing song play data, processes the data to calculate the total number of plays for each song and date combination, and generates an output CSV file containing the processed data.

## Installation
Before installing this project, you must have Python 3.6 or later, pip, and Redis installed on your system. Follow these steps to install the project:

1. Clone the repository:
```shell
$ git clone https://github.com/andylopezr/large-csv-processor.git
$ cd large-csv-processor
```

2. Create a virtual environment:
```shell
$ python3 -m venv venv
$ source venv/bin/activate
```

3. Install the required packages:
```shell
$ pip install -r requirements.txt
```

4. Start Redis server in a separate terminal window:

```shell
$ redis-server
```

5. Create a `.env` file with the following contents:
```shell
SECRET_KEY=<your_secret_key>
```

## Running the Project

> To run the project, follow these steps:

1. Start the Celery worker in a separate terminal window:
```shell
$ celery -A large_csv_processor worker -l info
```

2. Start the Django development server:
```shell
$ python manage.py runserver
```

Open your web browser and go to http://127.0.0.1:8000/api/docs.

Upload a CSV file containing song play data.

Wait for the file to be processed. You can monitor the progress of the processing task in the terminal window where the Celery worker is running.
When you try to use the download_csv file and the processing is not done, your output will be:
```shell
{
  "status": "processing"
}
```

Download the output CSV file containing the processed data.

## Files

`large_csv_processor/celery.py`
This file contains the Celery configuration for the project. It sets up a Celery instance and loads the Django settings from settings.py.

`large_csv_processor/settings.py`
This file contains the Django settings for the project. It defines various settings, such as the database configuration, static file paths, and installed apps.

`large_csv_processor/tasks.py`
This file contains the Celery task that processes the CSV file containing song play data. It reads the input file in chunks, groups the data by song and date, and calculates the total number of plays for each combination. The processed data is written to an output CSV file.

## Usage

1. Uploading a CSV File

> To upload a CSV file containing song play data, follow these steps:
Open your web browser and go to http://127.0.0.1:8000/api/docs.
<img src="https://i.imgur.com/xgJELS6.png" alt="process">
Click the "Choose File" button and select the CSV file you want to upload.
Click the "Upload" button to upload the file.

2. Downloading the Output File
To download the output CSV file containing the processed data, follow these steps:

Enter the task_id generated in the previous step:
```shell
{
  "task_id": "785266c6-581d-43d1-a717-d8000ac1a39a"
}
```

Wait for the file to be processed.

<img src="https://i.imgur.com/70hYpet.png" alt="process">
Once the file has been processed, click the `Download file` button to download the file.

## Conclusion
This project provides a scalable solution for processing large CSV files containing song play data. The Celery-based approach allows the processing to be distributed across multiple workers, which can significantly reduce the processing time for large files.
