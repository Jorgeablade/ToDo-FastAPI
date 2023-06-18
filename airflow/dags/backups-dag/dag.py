from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.ssh.operators.ssh import SSHOperator
from airflow.providers.ssh.hooks.ssh import SSHHook

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'transfer_db_sqlite',
    default_args=default_args,
    description='Transfer db.sqlite3 using SCP',
    schedule_interval=None,
    start_date=datetime(2023, 6, 17),
    catchup=False,
)

ssh_hook = SSHHook(ssh_conn_id='ssh-todo')

scp_transfer = SSHOperator(
    task_id='scp_transfer',
    command='scp hola@172.22.0.9:/todo-list/db.sqlite3 /opt/airflow/backups/',
    ssh_hook=ssh_hook,
    dag=dag,
)