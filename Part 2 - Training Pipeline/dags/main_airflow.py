from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
#import processing


default_args = {
  'owner': 'team3',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'catchup': False,
    'email': ['jayshil97@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


dag = DAG('EdgarMainPipeline',default_args=default_args,schedule_interval=None,max_active_runs=1)


t1 = BashOperator(
    task_id='Install_All_Libraries',
    bash_command='pip install boto3',
    dag=dag)
t21 = BashOperator(
    task_id='Upload_Raw_Data_to_AWS_S3',
    bash_command='python /root/Training_pipeline/dags/Upload_Raw_Data_to_AWS_S3.py',
    dag=dag)
t22 = BashOperator(
    task_id='Preprocess_The_Data',
    bash_command='python /root/Training_pipeline/dags/Preprocess_The_Data.py',
    dag=dag)

t23 = BashOperator(
    task_id='Establish_Connection_With_Google_API',
    bash_command='python /root/Training_pipeline/dags/Establish_Connection_With_Google_API.py',
    dag=dag)

t4 = BashOperator(
    task_id='MainPreprocessing',
    bash_command='python /root/Training_pipeline/dags/processing.py',
    dag=dag)

t5 = BashOperator(
    task_id='Generating_Analytics_Files',
    bash_command='python /root/Training_pipeline/dags/Generating_Analytics_Files.py',
    dag=dag)

t6 = BashOperator(
    task_id='Upload_to_AWS_S3',
    bash_command='python /root/Training_pipeline/dags/Upload_to_AWS_S3.py',
    dag=dag)

#python /home/jayshil/PycharmProjects/EdgarPipeline/dags/processing.py

# Traing Pipeline


t7 = BashOperator(
    task_id='Extracting_Label_Data_From_AWS_S3',
    bash_command='pip list',
    dag=dag)
t8 = BashOperator(
    task_id='Training_the_Model',
    bash_command='pip install --user boto3',
    dag=dag)
t9 = BashOperator(
    task_id='Testing_the_Model',
    bash_command='pip list',
    dag=dag)

t10 = BashOperator(
    task_id='Validating_the_Model',
    bash_command='pip list',
    dag=dag)

t11 = BashOperator(
    task_id='Implementing_Keras_to_Preprocess_Data',
    bash_command='pip list',
    dag=dag)


t12 = BashOperator(
    task_id='Uploadig_into_AWS_S3_and_Staging_Data',
    bash_command='python /root/Training_pipeline/keras_final.py',
    dag=dag)

t1 >> [t21 , t22, t23]  >> t4 >> t5 >> t6 >> t7 >> [t8, t9, t10] >> t11 >> t12