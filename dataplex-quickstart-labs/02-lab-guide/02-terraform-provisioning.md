# Provisioning the lab environment

The previous lab module covered what gets provisioned automatically. In this module, we will provision the **foundational** lab environment with Terraform. For the rest, we will use CLI and UI for the intended learning experience. 

<hr>

## 1. Declare variables
 
Paste this in Cloud Shell
```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
GCP_ACCOUNT_NAME=`gcloud auth list --filter=status:ACTIVE --format="value(account)"`
ORG_ID=`gcloud organizations list --format="value(name)"`
CLOUD_COMPOSER_IMG_VERSION="composer-2.1.3-airflow-2.3.4"
YOUR_GCP_REGION="us-central1"
YOUR_GCP_ZONE="us-central1-a"
YOUR_GCP_MULTI_REGION="US"
BQ_CONNECTOR_JAR_GCS_URI="gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.22.2.jar"
```

<hr>

## 2. Run the Terraform plan
```
cd ~/dataplex-oda/00-resources/terraform

terraform init

terraform plan \
  -var="project_id=${PROJECT_ID}" \
  -var="project_number=${PROJECT_NBR}" \
  -var="gcp_account_name=${GCP_ACCOUNT_NAME}" \
  -var="org_id=${ORG_ID}"  \
  -var="cloud_composer_image_version=${CLOUD_COMPOSER_IMG_VERSION}" \
  -var="gcp_region=${YOUR_GCP_REGION}" \
  -var="gcp_zone=${YOUR_GCP_ZONE}" \
  -var="gcp_multi_region=${YOUR_GCP_MULTI_REGION}" \
  -var="bq_connector_jar_gcs_uri=${BQ_CONNECTOR_JAR_GCS_URI}" 
```

<hr>

## 3. Provision the environment
```
cd ~/dataplex-oda/00-resources/terraform

terraform apply \
  -var="project_id=${PROJECT_ID}" \
  -var="project_number=${PROJECT_NBR}" \
  -var="gcp_account_name=${GCP_ACCOUNT_NAME}" \
  -var="org_id=${ORG_ID}"  \
  -var="cloud_composer_image_version=${CLOUD_COMPOSER_IMG_VERSION}" \
  -var="gcp_region=${YOUR_GCP_REGION}" \
  -var="gcp_zone=${YOUR_GCP_ZONE}" \
  -var="gcp_multi_region=${YOUR_GCP_MULTI_REGION}" \
  -var="bq_connector_jar_gcs_uri=${BQ_CONNECTOR_JAR_GCS_URI}" \
  --auto-approve
```

<hr>

## 4. Validate the environment setup

The Cloud Composer and Dataproc Metastore creation run simultaneously and take about 30 minutes. You can validate the rest of the setup, in the interim.

### 4.1. Network

### 4.2. Storage

### 4.3. Datasets

### 4.4. Notebooks

### 4.5. Scripts

### 4.6. Dataproc Metastore

### 4.7. Cloud Composer

<hr>

Proceed to the next lab module.

<hr>

