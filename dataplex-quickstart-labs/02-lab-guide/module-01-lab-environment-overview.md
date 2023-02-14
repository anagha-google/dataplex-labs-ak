# M1: About the lab environment setup

In the next module, we will provision a few Google Cloud services and upload artifacts to Cloud Storage buckets using Terraform. This module gives you an overview of what is automatically created and available when you start the actual Dataplex Lab series from Module 3.

## Prerequisites

Please read the narrative of the lab in the landing page for the quickstart lab series to understand what to expect, what we will work on in the lab modules.

<hr>

## APIs enabled

compute.googleapis.com<br>
dataproc.googleapis.com<br>
bigqueryconnection.googleapis.com<br>
bigquerydatapolicy.googleapis.com<br>
storage-component.googleapis.com<br>
bigquerystorage.googleapis.com<br>
datacatalog.googleapis.com<br>
dataplex.googleapis.com<br>
bigquery.googleapis.com<br>
cloudresourcemanager.googleapis.com<br>
cloudidentity.googleapis.com<br>
storage.googleapis.com<br>
composer.googleapis.com<br>
metastore.googleapis.com<br>
orgpolicy.googleapis.com<br>
dlp.googleapis.com<br>
logging.googleapis.com<br>
monitoring.googleapis.com<br>
dataplex.googleapis.com<br>
datacatalog.googleapis.com<br>
cloudresourcemanager.googleapis.com<br>
datapipelines.googleapis.com<br>
cloudscheduler.googleapis.com<br>
datalineage.googleapis.com

<hr>

## Services provisioned

VPC<br>
Subnet<br>
Firewall Rule<br>
Cloud Storage<br>
BigQuery<br>
Dataproc Metastore Service<br>
Cloud Composer

## Security setup

1. A user managed service account with requisite permissions
2. Permissions for you to impersonate the user managed service account
3. Requisite permissions for Google Managed Service Accounts as required by the GCP services


<hr>

## What's in Cloud Storage?

A number of buckets will be automatically created by the Terraform, and content copied into them. The following is a listing.

### Declare variables

Paste the below in Cloud Shell scoped to the project you will use for the Dataplex Quickstart Lab. Modify these variables as needed-
```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
GCP_ACCOUNT_NAME=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`
ORG_ID=`gcloud organizations list --format="value(name)"`
CLOUD_COMPOSER_IMG_VERSION="composer-2.1.3-airflow-2.3.4"
YOUR_GCP_REGION="us-central1"
YOUR_GCP_ZONE="us-central1-a"
YOUR_GCP_MULTI_REGION="US"
```

### Cloud Storage Buckets created

After running the next module, you should see the listing below, when you paste the command below in Cloud Shell-
```
gsutil ls
```

The author's output-
```
THIS IS INFORMATIONAL 
(the author's project number is 705495340985, and therefore appears as suffix, your listing will reflect your project number)

gs://curated-data-705495340985/
gs://lab-spark-bucket-705495340985/
gs://product-data-705495340985/
gs://raw-code-705495340985/
gs://raw-data-705495340985/
gs://raw-data-sensitive-705495340985/
gs://raw-model-705495340985/
gs://raw-model-metrics-705495340985/
gs://raw-model-mleap-bundle-705495340985/
gs://raw-notebook-705495340985/
gs://us-central1-oda-70549534098-275215ea-bucket/
```

### Raw Datasets

After running the next module, you should see the listing below, when you paste the command below in Cloud Shell-

```
gsutil ls -r gs://raw-data-$PROJECT_NBR/
```

This is what it should look like-
```
THIS IS INFORMATIONAL

-CELL TOWER DATA SAMPLE-
------------------------
├── cell-tower-anomaly-detection
│   ├── reference_data
│   │   └── ctad_service_threshold_ref.csv
│   └── transactions_data
│       └── ctad_transactions.csv


-CRIMES DATA SAMPLE-
--------------------
├── chicago-crimes
│   └── reference_data
│       └── crimes_chicago_iucr_ref.csv

-ICECREAM SALES DATA SAMPLE-
----------------------------
├── icecream-sales-forecasting
│   └── isf_icecream_sales_transactions.csv

-TELCO CUSTOMER CHURN DATA SAMPLE-
----------------------------------
└── telco-customer-churn-prediction
    ├── machine_learning_scoring
    │   └── tccp_customer_churn_score_candidates.csv
    └── machine_learning_training
        └── tccp_customer_churn_train_candidates.csv

```

### Raw Sensitive Datasets

After running the next module, you should see the listing below-

```
gsutil ls -r gs://raw-data-sensitive-$PROJECT_NBR/
```

This is what it should look like-
```
THIS IS INFORMATIONAL

-BANKING DATA SAMPLE-
---------------------
├── banking
│   ├── customers_raw
│   │   ├── credit_card_customers
│   │   │   └── date=2022-05-01
│   │   │       └── credit_card_customers.csv
│   │   └── customers
│   │       └── date=2022-05-01
│   │           └── customers.csv


```

### Curated Datasets

After running the next module, you should see the listing below, when you paste the command below in Cloud Shell-

```
gsutil ls gs://curated-data-$PROJECT_NBR/
```

This is what it should look like-
```
THIS IS INFORMATIONAL


-CELL TOWER DATA SAMPLE-
------------------------
├── cell-tower-anomaly-detection
│   ├── master_data
│   │   ├── ctad_part-00000-fc7d6e20-dbda-4143-91b5-d9414310dfd1-c000.snappy.parquet
│   │   ├── ctad_part-00001-fc7d6e20-dbda-4143-91b5-d9414310dfd1-c000.snappy.parquet
│   │   ├── ctad_part-00002-fc7d6e20-dbda-4143-91b5-d9414310dfd1-c000.snappy.parquet
│   │   └── ctad_part-00003-fc7d6e20-dbda-4143-91b5-d9414310dfd1-c000.snappy.parquet

-RETAIL TRANSACTIONS DATA SAMPLE-
---------------------------------
├── retail-transactions-anomaly-detection
│   └── rtad_sales.parquet


```

### Notebooks

After running the next module, you should see the listing below, when you paste the command below in Cloud Shell-

```
gsutil ls gs://raw-notebook-$PROJECT_NBR/
```

This is what it should look like-
```
THIS IS INFORMATIONAL


-CHICAGO CRIMES ANALYSIS STARTER NOTEBOOK-
------------------------------------------

├── chicago-crimes-analysis
│   └── chicago-crimes-analytics.ipynb
├── icecream-sales-forecasting
│   └── icecream-sales-forecasting.ipynb

-RETAIL TRANSACTIONS STARTER NOTEBOOK-
--------------------------------------

├── retail-transactions-anomaly-detection
│   └── retail-transactions-anomaly-detection.ipynb

-TELCO CUSTOMER CHURN PREDICTION STARTER NOTEBOOK-
--------------------------------------------------

└── telco-customer-churn-prediction
    ├── batch_scoring.ipynb
    ├── hyperparameter_tuning.ipynb
    ├── model_training.ipynb
    └── preprocessing.ipynb


```

### Scripts


After running the next module, you should see the listing below, when you paste the command below in Cloud Shell-

```
gsutil ls gs://raw-notebook-$PROJECT_NBR/
```

This is what it should look like-
```
THIS IS INFORMATIONAL


-AIRFLOW DAG STARTER SCRIPTS-
------------------------------------------

├── airflow
│   └── chicago-crimes-analytics
│       ├── bq_lineage_pipeline.py
│       └── spark_custom_lineage_pipeline.py

-PYSPARK STARTER SCRIPTS-
--------------------------------------

├── pyspark
│   └── chicago-crimes-analytics
│       ├── crimes_report.py
│       └── curate_crimes.py

-SPARK SQL STARTER SCRIPTS-
--------------------------------------------------

└── spark-sql
    └── retail-transactions-anomaly-detection
        └── retail-transactions-anomaly-detection.sql


```

### The rest of the buckets
```
- THIS IS INFORMATIONAL -


gs://lab-spark-bucket-705495340985/ --> For use by Dataproc Serverless Spark

gs://raw-model-705495340985/ --> For use in the Teco Customer Churn Prediction exercise with Dataplex Explore notebooks
gs://raw-model-metrics-705495340985/ --> For use in the Telco Customer Churn Prediction exercise with Dataplex Explore notebooks
gs://raw-model-mleap-bundle-705495340985/ --> For use in the Telco Customer Churn Prediction exercise with Dataplex Explore notebooks

gs://us-central1-oda-70549534098-275215ea-bucket/ --> Automatically created bucket by Cloud Composer service
```

<hr>


## What's in BigQuery?

Nothing is provisioned at the onset of the lab.

<hr>


## What's in Cloud Composer?

1. A Cloud Composer environment is created
2. Two DAGs are placed in the cloud composer DAG directory

Here is the author's listing-
```
- THIS IS INFORMATIONAL -

└── chicago-crimes-analytics
    ├── bq_lineage_pipeline.py
    └── spark_custom_lineage_pipeline.py
```

And here are the DAGs in the Airflow UI-

![AF](../01-images/01-01.png)   
<br><br>

<hr>

## What's in the Dataproc Metastore?

Its empty at the onset and does not have any precreated databases.


<hr>
This concludes the module. Please proceed to the next module.

<hr>
