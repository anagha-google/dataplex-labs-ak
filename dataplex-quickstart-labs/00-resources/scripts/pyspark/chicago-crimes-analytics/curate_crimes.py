# ............................................................
# Curate Chicago Crimes
# ............................................................
# This script -
# 1. subsets raw Chicago crimes data
# 2. augments with temporal attributes 
# 3. persists to GCS in the curated zone as parquet
# 4. creates an external table in HMS over #2
# ............................................................

import sys,logging,argparse
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from datetime import datetime


def fnParseArguments():
# {{ Start 
    """
    Purpose:
        Parse arguments received by script
    Returns:
        args
    """
    argsParser = argparse.ArgumentParser()
    argsParser.add_argument(
        '--tableFQN',
        help='Table fully qualified name',
        type=str,
        required=True)
    argsParser.add_argument(
        '--peristencePath',
        help='GCS location',
        type=str,
        required=True)
    return argsParser.parse_args()
# }} End fnParseArguments()

def fnMain(logger, args):
# {{ Start main

    # 1. Capture Spark application input
    tableFQN = args.tableFQN
    peristencePath = args.peristencePath

    # 2. Create Spark session
    logger.info('....Initializing spark & spark configs')
    spark = SparkSession.builder.appName("Curate Chicago Crimes").getOrCreate()
    logger.info('....===================================')

    

    # 4. Create curated crimes SQL
    curatedCrimesSQL="SELECT case_number,primary_type as case_type,date as case_date,year AS case_year,date_format(date, 'MMM') AS case_month,date_format(date,'E') AS case_day_of_week, hour(date) AS case_hour_of_day FROM oda_raw_zone.crimes_raw;"
    print(f"Curated Crimes SQL: {curatedCrimesSQL}")
    logger.info('....===================================')
    
    try:
        # 5. Drop table if exists
        logger.info('....Dropping table if it exists')
        spark.sql(f"DROP TABLE IF EXISTS {tableFQN}").show(truncate=False)
        logger.info('....===================================')
        
        # 6. Curate crimes
        logger.info('....Creating dataframe')
        curatedCrimesDF = spark.sql(curatedCrimesSQL)
        curatedCrimesDF.dropDuplicates()
        logger.info('....===================================')
    
        # 7. Persist to the data lake bucket in the curated zone
        logger.info('....Persisting dataframe in overwrite mode')
        curatedCrimesDF.coalesce(1).write.parquet(peristencePath, mode='overwrite')
        logger.info('....===================================')
    
        # 8. Create table definition
        logger.info('....Create table')
        CREATE_TABLE_DDL=f"CREATE TABLE IF NOT EXISTS {tableFQN}(case_number string, case_type string,case_date timestamp, case_year long, case_month string, case_day_of_week string, case_hour_of_day integer) STORED AS PARQUET LOCATION \"{peristencePath}\";"
        print(f"Create Curated Crimes DDL: {CREATE_TABLE_DDL}")
        spark.sql(CREATE_TABLE_DDL).show(truncate=False)
        logger.info('....===================================')

        # 9. Refresh table 
        logger.info('....Refresh table')
        spark.sql(f"REFRESH TABLE {tableFQN};").show(truncate=False)
        logger.info('....===================================')


    except RuntimeError as coreError:
            logger.error(coreError)
    else:
        logger.info('Successfully completed curating Chicago crimes!')
# }} End fnMain()

def fnConfigureLogger():
# {{ Start 
    """
    Purpose:
        Configure a logger for the script
    Returns:
        Logger object
    """
    logFormatter = logging.Formatter('%(asctime)s - %(filename)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("data_engineering")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    logStreamHandler = logging.StreamHandler(sys.stdout)
    logStreamHandler.setFormatter(logFormatter)
    logger.addHandler(logStreamHandler)
    return logger
# }} End fnConfigureLogger()

if __name__ == "__main__":
    arguments = fnParseArguments()
    logger = fnConfigureLogger()
    fnMain(logger, arguments)