from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.providers.google.cloud.operators.cloud_run import CloudRunExecuteJobOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocSubmitJobOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocStartClusterOperator
from airflow.providers.google.cloud.operators.dataproc import DataprocStopClusterOperator


#Common variables
project_id = "big-query-406221"
region = "us-east1"

#Define the date
now = datetime.now()
utc_offset = timedelta(hours=-5)
now_utc_minus_5 = now + utc_offset
today = now_utc_minus_5.strftime('%Y-%m-%d')

# Default arguments
default_args = {
    #'owner' : "airflow",    
    'start_date': datetime(2024, 3, 14),
    'email_on_failure': False,
    'email_on_retry': False,
}

#Spark job schema
pyspark_job = {
    "reference": {"project_id": project_id},
    "placement": {"cluster_name": 'project-pipeline2'},
    "pyspark_job": {
        "main_python_file_uri": 'gs://peru-real-state-datalake/code/pipeline.py',
        "args": ['--date', str(today)],
        'jar_file_uris': ["gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.36.1.jar"]    
    },  
}


# DAG definitions
with DAG(dag_id='Project Workflow',
         catchup=False,
         schedule_interval='30 1 1,15 * *',
         default_args=default_args
         ) as dag:

# Dummy start   
    start = DummyOperator(
        task_id='start',
        dag=dag,
    )


#Executes the web scraping job
    cloud_run_scraper = CloudRunExecuteJobOperator(
        task_id='scrape',
        project_id=project_id,
        region=region,
        job_name='peru-rs-scraping',
        dag=dag,
        deferrable=False,
    )




    ''' ********************************************************************************'''
    ''' ********                 START OF DATAPROC STUFF                        ********'''
    ''' ********************************************************************************'''

#Starting my Dataproc Cluster
    start_cluster = DataprocStartClusterOperator(
        task_id="start_dp_cluster",
        cluster_name='project-pipeline2',
        project_id=project_id,
        region=region,
        gcp_conn_id='google_cloud_default'
    )
  
#Submitting a job to my Dataproc Cluster
    pyspark_task = DataprocSubmitJobOperator(
                task_id="pyspark_task",
                job= pyspark_job,
                region=region,
                project_id=project_id,
                )
    
#Turns off the DP cluster
    stop_cluster = DataprocStopClusterOperator(
            task_id = 'stop_dp_cluster',
            cluster_name='project-pipeline2',
            region=region,
            project_id=project_id,
            gcp_conn_id='google_cloud_default',
            )



    ''' ********************************************************************************'''
    ''' ********                   END OF DATAPROC STUFF                        ********'''
    ''' ********************************************************************************'''


# Dummy end task
    end = DummyOperator(
        task_id='end',
        dag=dag,
    )

start >> cloud_run_scraper >> start_cluster >> pyspark_task >> stop_cluster >>  end