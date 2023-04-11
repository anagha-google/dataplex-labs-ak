# M13-1: Data Creation for BigLake lab module

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
TARGET_BUCKET_GCS_URI=f"gs://nyc-taxi-data-{PROJECT_NBR}/"
S8S_BATCH_ID=$RANDOM
BIGLAKE_PERSISTENCE_ZONE_NM="oda_curated_zone"
TABLE_FQN="oda_raw_zone.nyc_yellow_taxi_trips_raw"

# Delete any existing content in the bucket
gsutil rm -r $BUCKET_NM/nyc_yellow_taxi_trips

# Persist NYC Yellow Taxi trips to Cloud Storage
gcloud dataproc batches submit pyspark gs://raw-code-${PROJECT_NBR}/pyspark/nyc-taxi-trip-analytics/taxi_trips_data_generator.py \
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

## 6. 



