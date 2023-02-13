# M1: About the lab environment setup

In the next module, we will provision a few Google Cloud services and upload artifacts to Cloud Storage buckets using Terraform. This module gives you an overview of what is automatically created and available when you start the actual Dataplex Lab series from Module 3.

## Prerequisites

Please read the narrative of the lab in the landing page for the quickstart lab series to understand what to expect, what we will work on in the lab modules.

<hr>

## Services provisioned

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

### Listing of Cloud Storage Buckets

Run the command below for bucket listing in Cloud Shell-
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
gs://raw-model-705495340985/
gs://raw-model-metrics-705495340985/
gs://raw-model-mleap-bundle-705495340985/
gs://raw-notebook-705495340985/
gs://us-central1-oda-70549534098-275215ea-bucket/
```

### Raw Datasets
```
gsutil ls gs://raw-data-$PROJECT_NBR/
```

This is what it should look like-
```
THIS IS INFORMATIONAL

-BANKING DATA SAMPLE-
---------------------
├── banking
│   ├── credit_card_reference_data_raw
│   │   ├── card_read_type
│   │   │   └── card_read_type.csv
│   │   ├── card_type_facts
│   │   │   └── card_type_facts.csv
│   │   ├── currency
│   │   │   └── currency.csv
│   │   ├── events_type
│   │   │   └── events_type.csv
│   │   ├── origination_code
│   │   │   └── origination_code.csv
│   │   ├── payment_methods
│   │   │   └── payment_methods.csv
│   │   ├── signature
│   │   │   └── signature.csv
│   │   ├── swiped_code
│   │   │   └── swiped_code.csv
│   │   └── trans_type
│   │       └── trans_type.csv
│   ├── credit_card_transactions_raw
│   │   └── credit_card_authorizations
│   │       └── date=2022-05-01
│   │           └── credit_card_auth_transactions.csv
│   ├── customers_raw
│   │   ├── credit_card_customers
│   │   │   └── date=2022-05-01
│   │   │       └── credit_card_customers.csv
│   │   └── customers
│   │       └── date=2022-05-01
│   │           └── customers.csv
│   └── merchants_raw
│       ├── mcc_codes
│       │   └── date=2022-05-01
│       │       └── mcc_codes.csv
│       └── merchants
│           └── date=2022-05-01
│               └── merchants.csv


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

### Curated Datasets
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
```

```

### Scripts
```

```





<hr>


## What's in BigQuery?

<hr>


## What's in Cloud Composer?


<hr>

## What's in the Dataproc Metastore?



<hr>
This concludes the module. Please proceed to the next module.

<hr>
