# ======================================================================================
# ABOUT
# This script orchestrates the execution of the Chicago crimes reports
# ======================================================================================

import os
from airflow.models import Variable
from datetime import datetime
from airflow import models
from airflow.providers.google.cloud.operators.dataproc import (DataprocCreateBatchOperator,DataprocGetBatchOperator)
from datetime import datetime
from airflow.utils.dates import days_ago
import string
import random 
from airflow.operators import dummy_operator
from airflow.utils import trigger_rule

# Read environment variables into local variables
PROJECT_ID = models.Variable.get('project_id')
PROJECT_NBR = models.Variable.get('project_nbr')
REGION = models.Variable.get("region")
UMSA = models.Variable.get("umsa")
SUBNET  = models.Variable.get("subnet")

# User Managed Service Account FQN
UMSA_FQN=UMSA+"@"+PROJECT_ID+".iam.gserviceaccount.com"

# PySpark script files in GCS, of the individual Spark applications in the pipeline
GCS_URI_CURATE_CRIMES_PYSPARK= f"gs://oda-raw-code-{PROJECT_NBR}/pyspark/chicago-crimes-analytics/curate_crimes.py"
GCS_URI_CRIME_TRENDS_REPORT_PYSPARK= f"gs://oda-raw-code-{PROJECT_NBR}/pyspark/chicago-crimes-analytics/crimes_report.py"

# Dataproc Metastore Resource URI
DPMS_RESOURCE_URI = f"projects/{PROJECT_ID}/locations/{REGION}/services/lab-dpms-{PROJECT_NBR}"

# Define DAG name
dag_name= "Chicago_Crime_Trends_Spark"

# Generate Pipeline ID
randomizerCharLength = 10 
BATCH_ID = ''.join(random.choices(string.digits, k = randomizerCharLength))

# Report bases
REPORT_BASE_NM_CRIMES_YEAR="chicago-crimes-trend-by-year"
REPORT_BASE_NM_CRIMES_MONTH="chicago-crimes-trend-by-month"
REPORT_BASE_NM_CRIMES_DAY="chicago-crimes-trend-by-day"
REPORT_BASE_NM_CRIMES_HOUR="chicago-crimes-trend-by-hour"
REPORT_BASE_DIR=f"gs://oda-consumption-data-{PROJECT_NBR}/"


# Curate Crimes Spark application args
CURATE_CRIMES_ARGS_ARRAY = [ 
        f"--projectNbr={PROJECT_NBR}", \
        f"--projectID={PROJECT_ID}"]

# Curate Crimes Spark application conf
CURATE_CRIMES_DATAPROC_SERVERLESS_BATCH_CONFIG = {
    "pyspark_batch": {
        "main_python_file_uri": GCS_URI_CURATE_CRIMES_PYSPARK,
        "args": CURATE_CRIMES_ARGS_ARRAY,
        "jar_file_uris": [
      "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.22.2.jar"
    ]
    },
    "environment_config":{
        "execution_config":{
              "service_account": UMSA_FQN,
            "subnetwork_uri": SUBNET
            },
        "peripherals_config": {
            "metastore_service": DPMS_RESOURCE_URI
                
            },
        },
}

# Crimes By Year args
CRIMES_BY_YEAR_ARGS_ARRAY = [f"--projectNbr={PROJECT_NBR}", \
        f"--projectID={PROJECT_ID}" \
        f"--reportDirGcsURI=\"{REPORT_BASE_DIR}/{REPORT_BASE_NM_CRIMES_YEAR}\"" \
        f"--reportName='Chicago Crime Trend by Year'" \
        f"--reportSQL='SELECT case_year,count(*) AS crime_count FROM oda_curated_zone.crimes_chicago_curated_spark GROUP BY case_year;'" \
        f"--reportPartitionCount=1" \
        f"--reportTableFQN='oda_consumption_zone.crimes_chicago_by_year_spark'" \
            ]

# Crimes By Year Spark application conf
CRIMES_BY_YEAR_DATAPROC_SERVERLESS_BATCH_CONFIG = {
    "pyspark_batch": {
        "main_python_file_uri": GCS_URI_CRIME_TRENDS_REPORT_PYSPARK,
        "args": CRIMES_BY_YEAR_ARGS_ARRAY,
        "jar_file_uris": [
      "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.22.2.jar"
    ]
    },
    "environment_config":{
        "execution_config":{
              "service_account": UMSA_FQN,
            "subnetwork_uri": SUBNET
            },
        "peripherals_config": {
            "metastore_service": DPMS_RESOURCE_URI
                
            },
        },
}

# Crimes By Month args
CRIMES_BY_MONTH_ARGS_ARRAY = [f"--projectNbr={PROJECT_NBR}", \
        f"--projectID={PROJECT_ID}" \
        f"--reportDirGcsURI=\"{REPORT_BASE_DIR}/{REPORT_BASE_NM_CRIMES_MONTH}\"" \
        f"--reportName='Chicago Crime Trend by Month'" \
        f"--reportSQL='SELECT case_month,count(*) AS crime_count FROM oda_curated_zone.crimes_chicago_curated_spark GROUP BY case_month;'" \
        f"--reportPartitionCount=1" \
        f"--reportTableFQN='oda_consumption_zone.crimes_chicago_by_month_spark'" \
            ]

# Crimes By Month Spark application conf
CRIMES_BY_MONTH_DATAPROC_SERVERLESS_BATCH_CONFIG = {
    "pyspark_batch": {
        "main_python_file_uri": GCS_URI_CRIME_TRENDS_REPORT_PYSPARK,
        "args": CRIMES_BY_MONTH_ARGS_ARRAY,
        "jar_file_uris": [
      "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.22.2.jar"
    ]
    },
    "environment_config":{
        "execution_config":{
              "service_account": UMSA_FQN,
            "subnetwork_uri": SUBNET
            },
        "peripherals_config": {
            "metastore_service": DPMS_RESOURCE_URI
                
            },
        },
}

# Crimes By Day args
CRIMES_BY_DAY_ARGS_ARRAY = [f"--projectNbr={PROJECT_NBR}", \
        f"--projectID={PROJECT_ID}" \
        f"--reportDirGcsURI=\"{REPORT_BASE_DIR}/{REPORT_BASE_NM_CRIMES_DAY}\"" \
        f"--reportName='Chicago Crime Trend by Day'" \
        f"--reportSQL='SELECT case_day_of_week,count(*) AS crime_count FROM oda_curated_zone.crimes_chicago_curated_spark GROUP BY case_day_of_week;'" \
        f"--reportPartitionCount=1" \
        f"--reportTableFQN='oda_consumption_zone.crimes_chicago_by_day_spark'" \
            ]

# Crimes By Day Spark application conf
CRIMES_BY_DAY_DATAPROC_SERVERLESS_BATCH_CONFIG = {
    "pyspark_batch": {
        "main_python_file_uri": GCS_URI_CRIME_TRENDS_REPORT_PYSPARK,
        "args": CRIMES_BY_DAY_ARGS_ARRAY,
        "jar_file_uris": [
      "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.22.2.jar"
    ]
    },
    "environment_config":{
        "execution_config":{
              "service_account": UMSA_FQN,
            "subnetwork_uri": SUBNET
            },
        "peripherals_config": {
            "metastore_service": DPMS_RESOURCE_URI
                
            },
        },
}

# Crimes By Hour args
CRIMES_BY_HOUR_ARGS_ARRAY = [f"--projectNbr={PROJECT_NBR}", \
        f"--projectID={PROJECT_ID}" \
        f"--reportDirGcsURI=\"{REPORT_BASE_DIR}/{REPORT_BASE_NM_CRIMES_HOUR}\"" \
        f"--reportName='Chicago Crime Trend by Hour'" \
        f"--reportSQL='SELECT case_hour_of_day,count(*) AS crime_count FROM oda_curated_zone.crimes_chicago_curated_spark GROUP BY case_hour_of_day;'" \
        f"--reportPartitionCount=1" \
        f"--reportTableFQN='oda_consumption_zone.crimes_chicago_by_hour_spark'" \
            ]

# Crimes By Hour Spark application conf
CRIMES_BY_HOUR_DATAPROC_SERVERLESS_BATCH_CONFIG = {
    "pyspark_batch": {
        "main_python_file_uri": GCS_URI_CRIME_TRENDS_REPORT_PYSPARK,
        "args": [
          CRIMES_BY_HOUR_ARGS_ARRAY
        ],
        "jar_file_uris": [
      "gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.22.2.jar"
    ]
    },
    "environment_config":{
        "execution_config":{
              "service_account": UMSA_FQN,
            "subnetwork_uri": SUBNET
            },
        "peripherals_config": {
            "metastore_service": DPMS_RESOURCE_URI
                
            },
        },
}


# Build the pipeline
with models.DAG(
    dag_name,
    schedule_interval=None,
    start_date = days_ago(2),
    catchup=False,
) as dag_serverless_batch:

    start = dummy_operator.DummyOperator(
        task_id='start',
        trigger_rule='all_success'
    )

    curate_chicago_crimes = DataprocCreateBatchOperator(
        task_id="CURATE_CRIMES",
        project_id=PROJECT_ID,
        region=REGION,
        batch=CURATE_CRIMES_DATAPROC_SERVERLESS_BATCH_CONFIG,
        batch_id=f"curate-crimes-af-{BATCH_ID}"
    )

    trend_by_year = DataprocCreateBatchOperator(
        task_id="CRIME_TREND_BY_YEAR",
        project_id=PROJECT_ID,
        region=REGION,
        batch=CRIMES_BY_YEAR_DATAPROC_SERVERLESS_BATCH_CONFIG,
        batch_id=f"chicago-crimes-trend-by-year-af-{BATCH_ID}"
    )

    trend_by_month = DataprocCreateBatchOperator(
        task_id="CRIME_TREND_BY_MONTH",
        project_id=PROJECT_ID,
        region=REGION,
        batch=CRIMES_BY_MONTH_DATAPROC_SERVERLESS_BATCH_CONFIG,
        batch_id=f"chicago-crimes-trend-by-month-af-{BATCH_ID}"
    )

    trend_by_day = DataprocCreateBatchOperator(
        task_id="CRIME_TREND_BY_DAY",
        project_id=PROJECT_ID,
        region=REGION,
        batch=CRIMES_BY_DAY_DATAPROC_SERVERLESS_BATCH_CONFIG,
        batch_id=f"chicago-crimes-trend-by-day-af-{BATCH_ID}"
    )

    trend_by_hour = DataprocCreateBatchOperator(
        task_id="CRIME_TREND_BY_HOUR",
        project_id=PROJECT_ID,
        region=REGION,
        batch=CRIMES_BY_HOUR_DATAPROC_SERVERLESS_BATCH_CONFIG,
        batch_id=f"chicago-crimes-trend-by-hour-af-{BATCH_ID}"
    )

    end = dummy_operator.DummyOperator(
        task_id='end',
        trigger_rule='all_done'
    )


start >> curate_chicago_crimes >> [trend_by_year, trend_by_month, trend_by_day, trend_by_hour] >> end