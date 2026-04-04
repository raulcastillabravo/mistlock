from airflow.decorators import dag, task
from extract import Extract
from transform import Transform
from load import Load

@dag(dag_id='etl_pipeline')
def etl_pipeline():

    @task
    def extract_task():
        return Extract().run()

    @task
    def transform_task(input_path: str):
        return Transform().run(input_path)

    @task
    def load_task(input_path: str):
        return Load().run(input_path)

    extract_result = extract_task()
    transform_result = transform_task(extract_result)
    load_result = load_task(transform_result)

    extract_result >> transform_result >> load_result

dag = etl_pipeline()
