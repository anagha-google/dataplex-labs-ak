# Dataplex Quickstart for Cloud Architects and Engineers

## 1. About

Dataplex is a Google Cloud service for Data Governance and Management. Using Dataplex and complementary Data Analytics services, enterprises can stand up Data Mesh architecture in their Google Cloud data estate. To get started with Data Mesh on Google Cloud, one of the prerequisites is knowledge of Dataplex.<br>

This repository is designed to demystify Dataplex features, through a series of self-contained instructional lab modules, with minimal automation, detailed instructions with screenshots for the full developer experience. Once you are well versed with dataplex, you can proceeed to the advanced labs that feature Data Mesh. The labs are product sponsored and you can expect to see new modules released as and when there are new features/updates to features announced.

<hr>

## 2. Format & Duration
The lab is fully scripted (no research needed), with (fully automated) environment setup, data, code, commands, notebooks, orchestration, and configuration. Clone the repo and follow the step by step instructions for an end to end developer experience. <br><br>

Expect to spend ~8 hours to fully understand and execute if new to GCP and the services and at least ~6 hours otherwise.

<hr>

## 3. Level
L200 - L300 (includes Apache Spark code, Apache Airflow orchestration, Data Science notebooks and more)

<hr>

## 4. Audience
The intended audience is anyone with interest in architecting governance and Data Mesh on Google Cloud.

<hr>

## 5. Prerequisites
Foundational knowledge of governance, and GCP products would be beneficial but is not entirely required, given the format of the lab. Access to Google Cloud is a must unless you want to just read the content.

<hr>

## 6. Goal
Simplify your learning and adoption journey of our product stack for governance with - <br> 
1. Just enough product knowledge of Dataplex for governance<br>
2. Quick start code that can be repurposed for your use cases<br>
3. Terraform for provisioning a variety of Google Cloud data services, that can be repurposed for your use case<br>

<hr>

## 7. Use cases covered
There are various usecases covered including Chicago Crimes Analytics, TelCo Customer Churn Prediction, Cell Tower Anomaly Detection, Icecream Sales Forecasting and more. This is an ever-evovlving lab series, we recommend reviewing the release history for updates on use cases.

<hr>

## 8. Flow of the lab

![LP-00](01-images/landing-page-00.png)   
<br><br>

For your convenience, all the code is pre-authored, so you can focus on understanding product features and integration.

<hr>

## 9. The lab modules
Complete the lab modules in a sequential manner. For a better lab experience, read *all* the modules and then start working on them.

| # | Feature | Module | Duration<br>minutes | 
| -- |:--- | :--- | :--- |
| 01 | N/A | [Lab environment overview](02-lab-guide/module-01-lab-environment-overview.md) | 10  |
| 02 | N/A | [Lab environment provisioning with Terraform](02-lab-guide/module-02-terraform-provisioning.md) | 45  |
| 03 | Dataplex Lakes and Zones | [Organize your Data Lake with Dataplex](02-lab-guide/module-03-organize-your-data-lake.md) | 15  |
| 04 | Dataplex Lakes and Zones | [Register assets into your Dataplex lake zones](02-lab-guide/module-05-register-assets-into-zones.md) | 15  |
| 05 | Dataplex Discovery |[Create an Exploration Environment Dataplex Exploration Workbench](02-lab-guide/module-04-create-exploration-environment.md) | 15  |
| 06 | Dataplex Discovery |[Discovery of structured Cloud Storage objects - study of entities, schemas, automated external table defintions in Dataproc Metastore Service and BigQuery](02-lab-guide/module-06-discovery.md) | 15  |
| 07 | Dataplex Catalog | [Walkthrough of Cloud Catalog](02-lab-guide/module-07-0-walkthrough-of-catalog.md) | 10  |
| 08 | Dataplex Catalog | [Creating a custom metadata entry](02-lab-guide/module-07-1-custom-entry-in-catalog.md) | 10  |
| 09 | Dataplex Catalog | [Creating a tag template and populating tags](02-lab-guide/module-07-2-create-tag-template-for-catalog-entry.md) | 15  |
| 10 | Dataplex Catalog | [Searching the catalog](02-lab-guide/module-07-4-search-catalog.md) | 10  |
| 11 | Dataplex Explore | [Exploring data & metadata with Spark SQL workbench](02-lab-guide/module-08-1-explore-with-spark-sql.md) | 15  |
| 12 | Dataplex Explore | [Exploring data with Jupyter notebooks](02-lab-guide/module-08-2-explore-with-jupyter-notebooks.md) | 15  |
| 13 | Dataplex Lineage | [Out of the box lineage capture for BigQuery objects](02-lab-guide/module-09-1-data-lineage-with-bigquery.md) | 15  |
| 14 | Dataplex Lineage | [BigQuery lineage with Apache Airflow on Cloud Composer for orchestration ](02-lab-guide/module-09-2-data-lineage-with-cloud-composer-bq.md) | 15  |
| 15 | Dataplex Lineage | [Custom lineage for Apache Spark applications on Cloud Dataproc with Apache Airflow on Cloud Composer pipelines ](02-lab-guide/module-09-3-data-lineage-with-cloud-composer-spark.md) | 30  |
| 16 | Dataplex Lineage | [Custom lineage for custom entries in Catalog & managing lineage with Dataplex Lineage API](02-lab-guide/module-09-4-custom-lineage.md) | 15  |
| 17 | Dataplex Profiling | [Data profiling by example](02-lab-guide/module-10-1-data-profiling.md) | 15  |
| 18 | Dataplex Quality | [Auto Data Quality for completeness checks](02-lab-guide/module-11-1a-auto-dq-completeness.md) | 15  |
| 19 | Dataplex Quality | [Auto Data Quality for validity - pattern checks](02-lab-guide/module-11-1b-auto-dq-validity.md) | 15  |
| 20 | Dataplex Quality | [Auto Data Quality for validity - allowed values checks](02-lab-guide/module-11-1c-auto-dq-value-set.md) | 15  |



## 10. Dont forget to 
Shut down/delete resources when done to avoid unnecessary billing.

<hr>

## 11. Credits
| # | Google Cloud Collaborators | Contribution  | 
| -- | :--- | :--- |
| 1. | Anagha Khanolkar | Creator |



<hr>

## 12. Contributions welcome
Community contribution to improve the lab is very much appreciated. <br>

<hr>

## 13. Getting help
If you have any questions or if you found any problems with this repository, please report through GitHub issues.

<hr>

## 14. Release History
| Date | Details | 
| -- | :--- | 
| 20230227 |  Initial release |




