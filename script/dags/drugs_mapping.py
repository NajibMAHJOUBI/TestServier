from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

from extract_tasks.extract_csv_to_df import extract_csv_to_df
from extract_tasks.extract_json_to_csv import extract_json_to_df
from load_drugs_json.load_drugs_json import load_drugs_json
from transform_drugs_publication.transform_drugs_publication import transform_drugs_publication
from utils.get_list_files import get_list_files

path_data = '/home/data-ops/Documents/Github/TestServier/data/publication'

path_drugs = '/home/data-ops/Documents/Github/TestServier/data/drugs.csv'

path_work = '/home/data-ops/Documents/Github/TestServier/work'

path_save = '/home/data-ops/Documents/Github/TestServier/drugs_mapping/drugs_mapping.json'

with DAG('drugs_mapping',
         start_date=datetime(2022, 1, 1),
         schedule_interval='@daily',
         catchup=False) as dag:

    get_list_files = PythonOperator(task_id='get_list_files',
                                    python_callable=get_list_files,
                                    op_kwargs={'path_data': path_data},
                                    dag=dag)

    extract_json_to_df = PythonOperator(task_id='extract_json_to_df',
                                        python_callable=extract_json_to_df,
                                        op_kwargs={'dir_extract': path_work},
                                        dag=dag)

    extract_csv_to_df = PythonOperator(task_id='extract_csv_to_df',
                                       python_callable=extract_csv_to_df,
                                       op_kwargs={'dir_extract': path_work},
                                       dag=dag)

    transform_drugs_publication = PythonOperator(task_id='transform_drugs_publication',
                                                 python_callable=transform_drugs_publication,
                                                 op_kwargs={'path_drugs': path_drugs,
                                                            'path_work': path_work},
                                                 dag=dag)

    load_to_json = PythonOperator(task_id='load_to_json',
                                  python_callable=load_drugs_json,
                                  op_kwargs={'path_save': path_save},
                                  dag=dag)


get_list_files >> [extract_json_to_df, extract_csv_to_df] >> transform_drugs_publication >> load_to_json
