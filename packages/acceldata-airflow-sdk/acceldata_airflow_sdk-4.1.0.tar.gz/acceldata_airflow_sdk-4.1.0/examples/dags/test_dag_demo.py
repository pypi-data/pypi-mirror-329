import botocore
import boto3
import psycopg2
import snowflake.connector
from airflow.operators.python_operator import PythonOperator
from faker import Faker
import os
from torch_airflow_sdk.dag import DAG
from torch_airflow_sdk.operators.torch_initialiser_operator import TorchInitializer
from torch_airflow_sdk.decorators.job import job
from torch_airflow_sdk.decorators.span import span
from torch_sdk.events.generic_event import GenericEvent
from torch_sdk.models.job import JobMetadata, Node
import time
from datetime import datetime
import json
import random
from torch_sdk.models.pipeline import PipelineMetadata

# Set the following values as per the environment.
pipeline_name = "verisk_torch_pipeline"
pipeline_uid = "verisk.demo.pipeline"
snowflake_ds = "Snwoflake-DS"
# postgres_ds = constants.postgres_ds
s3_ds = "S3-DS"
s3_asset = "csv-file-bucket"


# s3_lambda_customers = constants.s3_lambda_customers
# s3_lambda_customers_op = constants.s3_lambda_customers_op
# s3_lambda_customers_joined = constants.s3_lambda_customers_joined

# sf_table_name = constants.sf_table_name
# pg_table = constants.pg_table
# pgjoin_lambda_function = constants.postgres_s3_join_lambda
# s3_upload_lambda_function = constants.s3_upload_snowflake_lambda

def now_ms():
    return int(round(time.time() * 1000))


def create_conn_rds(context):
    rds_host = context['dag_run'].conf['rds_host']
    rds_port = context['dag_run'].conf['rds_port']
    rds_database = context['dag_run'].conf['rds_database']
    rds_user = context['dag_run'].conf['rds_user']
    rds_password = context['dag_run'].conf['rds_password']

    return psycopg2.connect(
        host=rds_host,
        port=rds_port,
        database=rds_database,
        user=rds_user,
        password=rds_password)


def snowflake_create_conn(context):
    snowflake_username = context['dag_run'].conf['snowflake_username']
    snowflake_password = context['dag_run'].conf['snowflake_password']
    snowflake_account = context['dag_run'].conf['snowflake_account']
    snowflake_warehouse = context['dag_run'].conf['snowflake_warehouse']
    snowflake_database = context['dag_run'].conf['snowflake_database']
    snowflake_schema = context['dag_run'].conf['snowflake_schema']
    conn = snowflake.connector.connect(
        user=snowflake_username,
        password=snowflake_password,
        account=snowflake_account,
        warehouse=snowflake_warehouse,
        database=snowflake_database,
        schema=snowflake_schema
    )
    return conn


def get_aws_session(context):
    aws_region = context['dag_run'].conf['aws_region']
    return boto3.Session(
        region_name=aws_region
    )


def generate_customer_data(size):
    print("entering generate_customer_data")
    faker = Faker()
    customers = []
    for i in range(0, size):
        customer = {
            'name': faker.name(),
            'address': Faker('it_IT').name(),
            'dept_id': str(random.randint(1, 9))
        }
        customers.append(customer)

    return customers


path = '/tmp'

if os.path.isdir(path):
    os.chdir(path)
else:
    os.mkdir(path)
    os.chdir(path)


@span(span_uid='torch.verisk.data.generation')
def write_file_func(**context):
    print("entering write_file_func")
    file = f'/tmp/s3.csv'
    size = context['dag_run'].conf['csv_size']
    try:
        number_of_lines = len(open(file, 'x').readlines())
    except Exception as e:
        print(e)
        number_of_lines = len(open(file, 'r').readlines())

    span_context_parent = context['span_context_parent']
    span_context_parent.send_event(GenericEvent(
        context_data={'client_time': str(datetime.now()), 'Size': size - 1, 'total_file': 1,
                      'schema': 'name,email,phone,address'},
        event_uid="torch.verisk.data.generation.metadata"))
    span_context_parent.send_event(GenericEvent(
        context_data={'client_time': str(datetime.now()), 'source': 'S3', 'sync': 'RDS', 'middleware': 'Snowflake'},
        event_uid="torch.verisk.data.generation.information"))
    print(number_of_lines)
    with open(file, 'w') as f:
        customers = generate_customer_data(size)
        if number_of_lines == 0:
            f.write(f'name,email,dept_id\n')
        for i in customers:
            name = i['name']
            add = i['address']
            dept_id = str(i['dept_id'])
            f.write(f'{name},{add},{dept_id}\n')


@job(job_uid='torch.verisk.s3-migration',
     inputs=[],
     outputs=[Node(asset_uid=f'{s3_ds}.{s3_asset}')],
     metadata=JobMetadata('Jason', 'COKE', 'https://github.com/coke/reports/customers.kt'),
     span_uid='torch.verisk.s3.migration')
def upload_file_to_s3(**context):
    print("entering upload_file_to_s3")
    span_context_parent = context['span_context_parent']
    span_context_parent.send_event(GenericEvent(
        context_data={'client_time': str(datetime.now()), 'Bucket': context['dag_run'].conf['s3_bucket_name'],
                      'total_file': 1,
                      'location': context['dag_run'].conf['initialize_csv'], 'local_file_location': '/tmp/s3.csv',
                      'boto-session': 'ACTIVE'},
        event_uid="torch.verisk.s3.migration.metadata"))
    s3 = get_aws_session(context).resource('s3')
    # write_file_func()
    s3.meta.client.upload_file(Filename='/tmp/s3.csv', Bucket='airflow-sdk-demo',
                               Key='demo/basu/s3_data.csv')


@job(job_uid='torch.verisk.snowflake-migration',
     inputs=[Node(asset_uid=f'{s3_ds}.{s3_asset}')],
     outputs=[Node(asset_uid=f'{snowflake_ds}.FINANCE.FINANCE.TEST_PIPELINE_DEMO')],
     metadata=JobMetadata('SMITH', 'COKE', 'https://github.com/coke/reports/customers.kt'),
     span_uid='torch.verisk.snowflake.migration')
def s3_to_snowflake(**context):
    aws_session = get_aws_session(context)
    s3 = get_aws_session(context).resource('s3')
    file = s3.meta.client.read_csv(path="s3://airflow-sdk-demo/demo/basu/s3_data.csv", sep=',',
                                   boto3_session=aws_session)
    span_context_parent = context['span_context_parent']
    span_context_parent.send_event(GenericEvent(
        context_data={'client_time': str(datetime.now()), 'total_file_to_be_read': 1, 'POSTGRES_TABLES': '1',
                      'PG_ACCOUNT': 'kf71436.us-east-1',
                      'PG_USER': 'winash',
                      's3-location': 's3://airflow-sdk-demo/demo/basu/s3_data.csv',
                      'boto-session': 'TERMINATING'},
        event_uid="torch.verisk.snowflake.migration.metadata"))
    rds_conn = create_conn_rds(context)

    last_customer_index_sql = """SELECT * FROM finance.test_pipeline_demo  ORDER BY id DESC LIMIT 1;"""
    cur = rds_conn.cursor()
    cur.execute(last_customer_index_sql)
    row = cur.fetchall()
    rds_conn.commit()
    last_customer_index = 0
    try:
        last_customer_index = row[0][0]
    except:
        pass
    last_customer_index = last_customer_index + 1
    cur.close()
    cur = rds_conn.cursor()
    print('LAST CUST INDEX : ', last_customer_index)

    task_instance = context['ti']
    task_instance.xcom_push(key="last_index", value=last_customer_index)

    insert_swiggy_data_sql = """INSERT INTO finance.test_pipeline_demo(id, name, address, dept_id) VALUES ( %s, %s, %s, %s); """
    count = 0
    print('file:: ', file.values)
    for row in file.values:
        if count <= 100:
            cur.execute(insert_swiggy_data_sql,
                        (last_customer_index, row[0], row[1], row[2]))
            count = count + 1
            last_customer_index = last_customer_index + 1
    rds_conn.commit()
    cur.close()
    rds_conn.close()
    print(count)


default_args = {'start_date': datetime(2022, 5, 31)}

dag = DAG(
    dag_id='verisk_torch_pipeline',
    schedule_interval=None,
    default_args=default_args,
    start_date=datetime(2022, 6, 6),
    override_success_callback=True
)

torch_initializer_task = TorchInitializer(
    task_id='torch_pipeline_initializer',
    pipeline_uid=pipeline_uid,
    pipeline_name=pipeline_name,
    meta=PipelineMetadata(owner='Demo', team='demo_team', codeLocation='...'),
    dag=dag
)

write_file_func_task = PythonOperator(
    task_id='generate_data',
    python_callable=write_file_func,
    provide_context=True,
    dag=dag
)

upload_file_to_s3_task = PythonOperator(
    task_id='migration_to_s3',
    python_callable=upload_file_to_s3,
    provide_context=True,
    dag=dag
)

s3_to_snowflake_task = PythonOperator(
    task_id='s3_to_snowflake_migration',
    python_callable=s3_to_snowflake,
    provide_context=True,
    dag=dag
)
torch_initializer_task >> write_file_func_task >> upload_file_to_s3_task >> s3_to_snowflake_task
