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
BQ_LOCATION_MULTI="us"
BQ_DATASET_ID="oda_raw_zone"
LAKE_NM="oda-lake"
UMSA_FQN="lab-sa@$PROJECT_ID.iam.gserviceaccount.com"
BUCKET_NM="gs://nyc-taxi-data-$PROJECT_NBR"

gsutil mb -l $BQ_LOCATION_MULTI $BUCKET_NM

```

<hr>


## 2. Create a BigQuery managed table with the data we need

The SQL below will create a managed table in BigQuery called nyc_taxi_trips_yellow in the dataset oda_raw_zone. Run this in the BigQuery UI-

```
DROP TABLE IF EXISTS oda_raw_zone.nyc_taxi_trips_yellow;
CREATE TABLE oda_raw_zone.nyc_taxi_trips_yellow (trip_year INT64,
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

DELETE FROM oda_raw_zone.nyc_taxi_trips_yellow where trip_year NOT IN (2020,2021,2022);
```

<hr>

## 3. Run a Spark job that reads the data in BigQuery and persists to Cloud Storage


```

```

<hr>

## 4. Lets create a BigLake table on the data in Cloud Storage





