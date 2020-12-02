from airflow import DAG
from airflow.contrib.hooks.fs_hook import FSHook
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.hooks.mysql_hook import MySqlHook
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import pandas as pd
import os
from datetime import datetime

FILE_CONNECTION_ID = 'fs_default'
FILE_NAME = "time_series_covid19_confirmed_global.csv"
OUTPUT_TRANSFORM_FILE = '_time_series_covid19_confirmed_global_tmp.csv'
COLUMNS_BASE = {
    "country_region":"Country/Region",
    "province_state":"Province/State",
    "lat":"Lat",
    "long":"Long"
}
COLUMNS_FINAL = {
    "country_region":"Country/Region",
    "province_state":"Province/State",
    "lat":"Lat",
    "long":"Long",
    "event_date": "event_date",
    "cases": "cases"
}
dag = DAG('confirmed_load', description='Load of confirmed cases of covid',
          default_args={
              'owner': 'friendly.system',
              'depends_on_past': False,
              'max_active_runs': 1,
              'start_date': days_ago(5)
          },
          schedule_interval='0 0 * * *',
          catchup=False)

file_sensor_task = FileSensor(dag=dag,
                              task_id="file_sensor",
                              fs_conn_id=FILE_CONNECTION_ID,
                              filepath=FILE_NAME,
                              poke_interval=10,
                              timeout=300
                              )

def transform_func(**kwargs):
    folder_path = FSHook(conn_id=FILE_CONNECTION_ID).get_path()
    file_path = f"{folder_path}/{FILE_NAME}"
    destination_file = f"{folder_path}/{OUTPUT_TRANSFORM_FILE}"
    df = pd.read_csv(file_path, header=0,encoding="ISO-8859-1")
    col_sec = list(set(df.columns)-set(COLUMNS_BASE.values()))
    df_base = df[COLUMNS_BASE.values()]
    df_sec = df[col_sec]
    df_final = pd.DataFrame(columns = COLUMNS_FINAL.keys())
    for date_i in df_sec.columns:
        for row_i in range(len(df_sec[date_i])):
            piv_reg = {
                "country_region":df_base.iloc[row_i,0],
                "province_state":df_base.iloc[row_i,1],
                "lat":df_base.iloc[row_i,2],
                "long":df_base.iloc[row_i,3],
                "event_date": datetime.strptime(date_i, '%m/%d/%y'),
                "cases": df_sec[date_i][row_i]
            }
            df_final = df_final.append(piv_reg,ignore_index=True)
    df_final.to_csv(destination_file, index=False)
    os.remove(file_path)
    return destination_file

transform_process = PythonOperator(dag=dag,
                                   task_id="transform_process",
                                   python_callable=transform_func,
                                   provide_context=True
                                   )

def insert_process(**kwargs):
    ti = kwargs['ti']
    source_file = ti.xcom_pull(task_ids='transform_process')
    db_connection = MySqlHook('airflow_db').get_sqlalchemy_engine()
    df = pd.read_csv(source_file)
    with db_connection.begin() as transaction:
        transaction.execute("DELETE FROM covid.confirmed WHERE 1=1")
        df.to_sql("confirmed", con=transaction, schema="covid", if_exists="append",
                  index=False)
    os.remove(source_file)

insert_process = PythonOperator(dag=dag,
                                task_id="insert_process",
                                provide_context=True,
                                python_callable=insert_process)

file_sensor_task >> transform_process >> insert_process
