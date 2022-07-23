from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from extract_tasks.extract_csv_to_df import extract_csv_to_df
from extract_tasks.extract_json_to_csv import extract_json_to_df
from load_drugs_json.load_drugs_json import load_drugs_json
from transform_drugs_publication.transform_drugs_publication import transform_drugs_publication


list_csv_files = ['/home/data-ops/Documents/Github/TestServier/data/clinical_trials.csv',
                  '/home/data-ops/Documents/Github/TestServier/data/pubmed.csv']
list_json_files = ['/home/data-ops/Documents/Github/TestServier/data/pubmed.json']

path_extract_csv = '/home/data-ops/Documents/Github/TestServier/data_extract/extract_csv.csv'
path_extract_json = '/home/data-ops/Documents/Github/TestServier/data_extract/extract_json.csv'

path_transform = '/home/data-ops/Documents/Github/TestServier/data_transform/drugs_mapping.csv'

path_load = '/home/data-ops/Documents/Github/TestServier/data_load/drugs_mapping.json'

with DAG('drugs_mapping',
         start_date=datetime(2022, 1, 1),
         schedule_interval='@daily',
         catchup=False) as dag:

    extract_json_to_df = PythonOperator(task_id='extract_json_to_df',
                                        python_callable=extract_json_to_df,
                                        op_kwargs={'paths_json': list_json_files, 'path_extract': path_extract_json},
                                        dag=dag)

    extract_csv_to_df = PythonOperator(task_id='extract_csv_to_df',
                                       python_callable=extract_csv_to_df,
                                       op_kwargs={'paths_csv': list_csv_files, 'path_extract': path_extract_csv},
                                       dag=dag)

    transform_data = PythonOperator(task_id='transform_data',
                                    python_callable=transform_drugs_publication,
                                    op_kwargs={'path_list': [path_extract_json, path_extract_csv],
                                               'path_transform': path_transform},
                                    dag=dag)

    load_to_json = PythonOperator(task_id='load_to_json',
                                  python_callable=load_drugs_json,
                                  op_kwargs={'path_transform': path_transform, 'path_load': path_load},
                                  dag=dag)


[extract_json_to_df, extract_csv_to_df] >> transform_data >> load_to_json
