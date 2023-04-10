# M13-1: Data Creation for BigLake lab module

In this lab module, we will create data for the Biglake lab series.


## LAB


## 1. Create a bucket for the data

From Cloud Shell create a bucket-
```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
BQ_LOCATION_MULTI="us"
BQ_DATASET_ID="oda_raw_zone"
LAKE_NM="oda-lake"
UMSA_FQN="lab-sa@$PROJECT_ID.iam.gserviceaccount.com"
BUCKET_NM="gs://nyc-taxi-data-$PROJECT_NBR"

gsutil mb -l $BQ_LOCATION_MULTI $BUCKET_NM

## 2. Launch notebook that generates data

Launch to the notebook as shown below-

## 3. Run the notebook

1. Read the contents of the notebook and then run it. 
2. The notebook first creates a single managed BQ partitioned table with the data in 3 BigQuery public dataset tables hosting New York taxi data.
3. Then it persists the data to Cloud Storage in an unoptimized manner (too many, very small files) to a directory called taxi_trips_unoptimized
4. It also persists a slightly more optimized version of the above (fewer small files) to a directory called taxi_trips_optimized
5. Review the notebook output in Cloud Storage

```
gsutil ls -r $BUCKET_NM
```

## 3. Lets create a BigLake table on two datasets





