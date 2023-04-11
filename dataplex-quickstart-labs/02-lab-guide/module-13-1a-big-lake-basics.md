# M13-1: BigLake basics

In this lab module, we will create data for the Biglake lab series.


<hr>

## LAB

<hr>


## 1. Create a bucket for the data

From Cloud Shell create a bucket-
```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
DATAPLEX_LOCATION="us-central1"
BQ_LOCATION_MULTI="us"
BQ_DATASET_ID="oda_raw_zone"
LAKE_NM="oda-lake"
UMSA_FQN="lab-sa@$PROJECT_ID.iam.gserviceaccount.com"
BUCKET_NM="gs://nyc-taxi-data-$PROJECT_NBR"
BIGLAKE_PERSISTENCE_ZONE_NM="oda-curated-zone"

gsutil mb -l $BQ_LOCATION_MULTI $BUCKET_NM
```

<hr>


## 2. Create a BigQuery managed table with the data we need

The SQL below will create a managed table in BigQuery called nyc_taxi_trips_yellow in the dataset oda_raw_zone. Run this in the BigQuery UI-

```
DROP TABLE IF EXISTS oda_raw_zone.nyc_yellow_taxi_trips_raw;
CREATE TABLE oda_raw_zone.nyc_yellow_taxi_trips_raw (trip_year INT64,
    trip_month INT64,
    trip_day INT64,
    taxi_type STRING,
    vendor_id STRING,
    pickup_datetime TIMESTAMP,
    dropoff_datetime TIMESTAMP,
    passenger_count INT64,
    trip_distance NUMERIC,
    rate_code STRING,
    store_and_fwd_flag STRING,
    payment_type STRING,
    fare_amount NUMERIC,
    extra NUMERIC,
    mta_tax NUMERIC,
    tip_amount NUMERIC,
    tolls_amount NUMERIC,
    imp_surcharge NUMERIC,
    airport_fee NUMERIC,
    total_amount NUMERIC,
    pickup_location_id STRING,
    dropoff_location_id STRING)
  PARTITION BY RANGE_BUCKET(trip_year,  GENERATE_ARRAY(2020,2022,1))
   AS (
  SELECT
    CAST(EXTRACT(YEAR
      FROM
        pickup_datetime) AS INT) AS trip_year,
    EXTRACT(MONTH
    FROM
      pickup_datetime) AS trip_month,
    EXTRACT(DAY
    FROM
      pickup_datetime) AS trip_day,
    "YELLOW" AS taxi_type,
    vendor_id,
    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    rate_code,
    store_and_fwd_flag,
    payment_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    imp_surcharge,
    airport_fee,
    total_amount,
    pickup_location_id,
    dropoff_location_id
  FROM
    `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2020`
  UNION ALL
  SELECT
    CAST(EXTRACT(YEAR
      FROM
        pickup_datetime) AS INT) AS trip_year,
    EXTRACT(MONTH
    FROM
      pickup_datetime) AS trip_month,
    EXTRACT(DAY
    FROM
      pickup_datetime) AS trip_day,
    "YELLOW" AS taxi_type,
    vendor_id,
    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    rate_code,
    store_and_fwd_flag,
    payment_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    imp_surcharge,
    airport_fee,
    total_amount,
    pickup_location_id,
    dropoff_location_id
  FROM
    `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2021`
  UNION ALL
  SELECT
    CAST(EXTRACT(YEAR
      FROM
        pickup_datetime) AS INT) AS trip_year,
    EXTRACT(MONTH
    FROM
      pickup_datetime) AS trip_month,
    EXTRACT(DAY
    FROM
      pickup_datetime) AS trip_day,
    "YELLOW" AS taxi_type,
    vendor_id,
    pickup_datetime,
    dropoff_datetime,
    passenger_count,
    trip_distance,
    rate_code,
    store_and_fwd_flag,
    payment_type,
    fare_amount,
    extra,
    mta_tax,
    tip_amount,
    tolls_amount,
    imp_surcharge,
    airport_fee,
    total_amount,
    pickup_location_id,
    dropoff_location_id
  FROM
    `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2022` );

DELETE FROM oda_raw_zone.nyc_yellow_taxi_trips_raw where trip_year NOT IN (2020,2021,2022);
```

<hr>

## 3. Run a Spark job that reads the data in BigQuery and persists to Cloud Storage

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`
LOCATION="us-central1"
SUBNET_URI="projects/$PROJECT_ID/regions/$LOCATION/subnetworks/lab-snet"
UMSA_FQN="lab-sa@$PROJECT_ID.iam.gserviceaccount.com"
TARGET_BUCKET_GCS_URI="gs://nyc-taxi-data-${PROJECT_NBR}/"
S8S_BATCH_ID=$RANDOM
BIGLAKE_PERSISTENCE_ZONE_NM="oda_curated_zone"
TABLE_FQN="oda_raw_zone.nyc_yellow_taxi_trips_raw"
PYSPARK_CODE_BUCKET="gs://raw-code-${PROJECT_NBR}/pyspark"

# Delete any existing content in the bucket
gsutil rm -r $BUCKET_NM/nyc_yellow_taxi_trips

# Persist NYC Yellow Taxi trips to Cloud Storage
gcloud dataproc batches submit pyspark $PYSPARK_CODE_BUCKET/nyc-taxi-trip-analytics/taxi_trips_data_generator.py \
--project $PROJECT_ID \
--region $LOCATION  \
--batch generate-nyc-yellow-taxi-trips-$S8S_BATCH_ID \
--subnet $SUBNET_URI \
--service-account $UMSA_FQN \
--version=1.1 \
-- --projectID=$PROJECT_ID --tableFQN=$TABLE_FQN --peristencePath="$TARGET_BUCKET_GCS_URI/nyc_yellow_taxi_trips" 

```

It takes ~16 minutes to complete.

Lets review the file listing-
```
gsutil ls -r $BUCKET_NM
```

You should see a number of parquet files listed.

<hr>


## 5. Add the bucket to the raw zone in the Dataplex lake oda-lake

Paste the below in Cloud Shell-

```
gcloud dataplex assets create nyc-taxi-trips \
--location=$DATAPLEX_LOCATION \
--lake=$LAKE_NM \
--zone=$BIGLAKE_PERSISTENCE_ZONE_NM \
--resource-type=STORAGE_BUCKET \
--resource-name=projects/$PROJECT_ID/buckets/nyc-taxi-data-$PROJECT_NBR \
--discovery-enabled \
--discovery-schedule="0 * * * *" \
--display-name 'NYC Taxi Dataset'
```

Discovery will start immediately after adding the bucket as an asset to the raw zone. Allow 5 minutes for discovery to complete and till the entity "nyc-taxi-trips" gets displayed in the Dataplex UI

## 6. Validate external table creation in BigQuery

Run the below in the BigQuery UI, to ensure you see non-zero trip counts.
```
SELECT
  trip_month,
  COUNT(*) AS trip_count
FROM
  `oda_curated_zone.nyc_yellow_taxi_trips`
WHERE
  trip_year='2020'
GROUP BY
  trip_month
ORDER BY
  CAST(trip_month AS int64)
```

## 7. Upgrade the external table in Dataplex to BigLake

### 7.1. Enable the BigQuery connections API

```
gcloud services enable bigqueryconnection.googleapis.com
```

### 7.2. Upgrade the external table to managed BigLake table

1. In the Dataplex UI, bavigate to -> Manage -> ODA-LAKE -> ODA-CURATED-ZONE -> Assets

2. Click on the NYC Taxi Dataset

3. Click on "Upgrade to Managed"


## 8. Visualize lineage



## 9. Query acceleration with BigLake

### 9.1. Create a BigQuery dataset that is not a Dataplex asset

Paste in Cloud Shell-
```
NYC_TAXI_STAGE_DS="oda_nyc_taxi_trips_staging_ds"

bq --location=$BQ_LOCATION_MULTI mk \
    --dataset \
    $PROJECT_ID:$NYC_TAXI_STAGE_DS

```

### 9.2. Create a regular external BigQuery table on the curated NYC taxi trips

```
BQ_CONNECTION=`bq ls --connection --project_id=$PROJECT_ID --location=$BQ_LOCATION_MULTI | tail -1 | cut -d ' ' -f3`
echo $BQ_CONNECTION
```

Paste the below in the BigQuery UI-
```
echo "
CREATE EXTERNAL TABLE IF NOT EXISTS oda_nyc_taxi_trips_staging_ds.nyc_yellow_taxi_trips_regular
WITH PARTITION COLUMNS (
  trip_year  INTEGER,
  trip_month INTEGER,
  trip_day INTEGER
)
OPTIONS(
hive_partition_uri_prefix =\"$TARGET_BUCKET_GCS_URI\",
uris=[\"${TARGET_BUCKET_GCS_URI}nyc_yellow_taxi_trips/*.parquet\"],
format=\"PARQUET\");"

```

### 9.3. Run a query on the Biglake table



### 9.4. Run a query on the regular external table



## 10. Attribute based access control
