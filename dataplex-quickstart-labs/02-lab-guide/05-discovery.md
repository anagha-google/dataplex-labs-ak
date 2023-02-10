# Automated discovery, schema inference and external table creation

When a Dataplex Zone's discovery option is enabled, and assets are added to the Dataplex Zone of a Dataplex Lake that has a Dataproc Metastore Service (DPMS) attached with Data Catalog Sync enabled, the following happen automatically-
1. Assets will be discovered
2. Schema will be inferred for objects in Cloud Storage
3. External table definition will be created, based on schema inference in Dataproc Metastore Service (Hive Metastore Service) 
4. External table definition will ALSO be created, based on schema inference in BigQuery
5. The tables will be available as Dataplex Zone level entities
6. The tables will be cataloged in Data Catalog and will be searchable

This lab module covers the above for assets registered in the prior module.

## Lab - Discovery and Entities

### 1. Discovery of data assets in the Raw Zone: oda-raw-zone

1.1. Navigate to the Dataplex Zones UI for ODA-RAW-ZONE, and you will see "Miscellaneous Datasets" asset. Notice that it has an "Action required" flag.

![DISC-1](../01-images/05-01.png)   
<br><br>

1.2. Click on "Entities". You should see "icecream_sales_forecasting" and "telco_customer_churn_prediction" as two GCS based tables. The names are based off of the directory names in GCS.

![DISC-2](../01-images/05-02.png)   
<br><br>

1.3. Click on "icecream_sales_forecasting"; And then "Details". Review the details.

![DISC-3](../01-images/05-03.png)   
<br><br>

1.4. Click on "SCHEMA AND COLUMN TAGS". Review the schema inferred.

![DISC-4](../01-images/05-04.png)   
<br><br>

1.5. Switch to the BigQuery UI and to the dataset called oda_raw_zone. This dataset was automatically created by Dataplex when we created a zone. Notice the two tables listed there. Run a query on the Icecream Sales Forecasting table and review the results.

```
SELECT * FROM `oda_raw_zone.icecream_sales_forecasting` LIMIT 1000
```

![DISC-5](../01-images/05-05.png)   
<br><br>

1.6. Switch to the Dataplex UI ODA-RAW-ZONE->Miscellaneous Datasets->Actions

Observe the "Action" from the schema inference job.

![DISC-6](../01-images/05-06.png)   
<br><br>


![DISC-7](../01-images/05-07.png)   
<br><br>

The data in question is for the Telco Customer Churn Prediction usecase. Both the files in the underlying GCS buckets have different set of columns. Paste the below in Cloud Shell.

```
PROJECT_ID=`gcloud config list --format "value(core.project)" 2>/dev/null`
PROJECT_NBR=`gcloud projects describe $PROJECT_ID | grep projectNumber | cut -d':' -f2 |  tr -d "'" | xargs`

gsutil ls gs://oda-raw-data-$PROJECT_NBR/telco-customer-churn-prediction
```

Author's output - <br>
gs://oda-raw-data-36819656457/telco-customer-churn-prediction/customer_churn_score_data.csv<br>
gs://oda-raw-data-36819656457/telco-customer-churn-prediction/customer_churn_train_data.csv<br>


Lets look at the schema of customer_churn_train_data.csv:
```
gsutil cat gs://oda-raw-data-$PROJECT_NBR/telco-customer-churn-prediction/customer_churn_train_data.csv | head -1
```

Author's output:<br>
customerID,gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges,Churn<br>


Lets look at the schema of customer_churn_score_data.csv:
```
gsutil cat gs://oda-raw-data-$PROJECT_NBR/telco-customer-churn-prediction/customer_churn_score_data.csv | head -1
```

Author's output:<br>
customerID,gender,SeniorCitizen,Partner,Dependents,tenure,PhoneService,MultipleLines,InternetService,OnlineSecurity,OnlineBackup,DeviceProtection,TechSupport,StreamingTV,StreamingMovies,Contract,PaperlessBilling,PaymentMethod,MonthlyCharges,TotalCharges<br>

Notice that the train data has the column "Churn".<br>

<hr>


### 2. Discovery of data assets in the Curated Zone: oda-curated-zone

Review the asset, entities, schema, external table in BigQuery for assets in the Dataplex oda-curated-zone.


### 3. Discovery of non-data assets in the RAW Zone: oda-misc-zone

Review the asset, entities, in the Dataplex oda-misc-zone. Notice that Dataplex does not do schema inference, create external tables etc and categorizes the assets as of "fileset" type.
<br>

![DISC-8](../01-images/05-08.png)   
<br><br>

<hr>
This concludes the lab module. Proceed to the next module, where we will create a Dataplex "Environment" lanuch up a Jupyter notebook and explore metadata.
<hr>
