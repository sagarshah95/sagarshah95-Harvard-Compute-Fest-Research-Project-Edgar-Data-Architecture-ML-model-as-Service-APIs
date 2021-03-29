from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from airflow.utils.dates import days_ago
#import processing


default_args = {
	'owner': 'team2',
    'depends_on_past': False,
    'start_date': days_ago(2),
    'catchup': False,
    'email': ['akashmdubey15@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}


dag = DAG('training',default_args=default_args,schedule_interval=None,max_active_runs=1)



t0 = BashOperator(
    task_id='Extracting_Label_Data_From_AWS_S3',
    bash_command='pip list',
    dag=dag)
t1 = BashOperator(
    task_id='Training_the_Model',
    bash_command='pip install --user boto3',
    dag=dag)
t2 = BashOperator(
    task_id='Testing_the_Model',
    bash_command='pip list',
    dag=dag)

t3 = BashOperator(
    task_id='Validating_the_Model',
    bash_command='pip list',
    dag=dag)

t4 = BashOperator(
    task_id='Implementing_Keras_to_Preprocess_Data',
    bash_command='pip list',
    dag=dag)


t5 = BashOperator(
    task_id='Uploadig_into_AWS_S3_and_Staging_Data',
    bash_command='python /root/Training_pipeline/keras_final.py',
    dag=dag)

t0 >> [t1, t2, t3] >> t4 >> t5