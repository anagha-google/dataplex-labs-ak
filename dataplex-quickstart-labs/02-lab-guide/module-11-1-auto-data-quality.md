
# M11-1: Auto Data Quality 

Dataplex provides the following two options to validate data quality:

**Auto data quality** (Public Preview) provides an automated experience for getting quality insights about your data. Auto data quality automates and simplifies quality definition with recommendations and UI-driven workflows. It standardizes on insights with built-in reports and drives actions through alerting and troubleshooting.

**Dataplex data quality task** (Generally Available) offers a highly customizable experience to manage your own rule repository and customize execution and results, using Dataplex for managed / serverless execution. Dataplex data quality task uses an open source component, CloudDQ, that can also open up choices for customers who want to enhance the code to their needs.

The focus of this lab module is Auto data quality.

### Prerequisites

Successful completion of prior modules

### Duration

30 minutes

### Documentation 

[Data Quality Overview](https://cloud.google.com/dataplex/docs/data-quality-overview)<br>
[About Auto Data Quality](https://cloud.google.com/dataplex/docs/auto-data-quality-overview)<br>
[Use Auto Data Quality](https://cloud.google.com/dataplex/docs/use-auto-data-quality)<br>


### Learning goals


<hr>

# LAB

<hr>

## 1. Data to use to showcase quality

### 1.1. External table with Customer Master Data

We will choose this as it has email addresses, phone nubers etc that are great for checking for quality.

![ADQ-1](../01-images/module-11-1-01.png)   
<br><br>

![ADQ-2](../01-images/module-11-1-02.png)   
<br><br>

![ADQ-3](../01-images/module-11-1-03.png)   
<br><br>




Familiarize yourself with the data in the BQ UI via this SQL-
```
SELECT * FROM oda_raw_sensitive_zone.banking_customers_raw_customers WHERE date='2022-05-01' LIMIT 5
```

![ADQ-4](../01-images/module-11-1-04.png)   
<br><br>


### 1.2. Create BigQuery managed table with Customer Master Data

In the BQ UI, run the SQL below-
```
CREATE OR REPLACE TABLE oda_product_zone.customer_master AS
SELECT * FROM oda_raw_sensitive_zone.banking_customers_raw_customers WHERE date='2022-05-01'
```

Run a quick query to test if the table is created and also review the columns-
```
SELECT * FROM oda_product_zone.customer_master LIMIT 20
```

![ADQ-5](../01-images/module-11-1-05.png)   
<br><br>

### 1.3. Add the table as managed entity

In the BQ UI, run the SQL below-
```
CREATE OR REPLACE TABLE oda_product_zone.customer_master AS
SELECT * FROM oda_raw_sensitive_zone.banking_customers_raw_customers WHERE date='2022-05-01'
```

Run a quick query to test if the table is created and also review the columns-
```
SELECT * FROM oda_product_zone.customer_master LIMIT 20
```

![ADQ-5](../01-images/module-11-1-05.png)   
<br><br>

<hr>

## 2. IAM permissions to run Data Quality checks

### 2.1. Predefined IAM roles

The following are the pre-defined roles available-

![ADQ-5](../01-images/module-11-1-06.png)   
<br><br>

Lets grant our User Managed Service Account the role ```role/dataplex.dataScanAdmin```

### 2.2. Grant the User Managed Service Account the role/dataplex.dataScanAdmin role

```
# Variables
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
UMSA_FQN="lab-sa@$PROJECT_ID.iam.gserviceaccount.com"

# Permissions

gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member=serviceAccount:${UMSA_FQN} \
    --role=roles/dataplex.dataScanAdmin
```

![ADQ-7](../01-images/module-11-1-07.png)   
<br><br>

<hr>

## 3. Create a Data Quality Scan

### 3.1. Navigate to the Data Quality menu item

![ADQ-7](../01-images/module-11-1-08.png)   
<br><br>

### 3.2. Click on create data quality scan

![ADQ-7](../01-images/module-11-1-09.png)   
<br><br>
