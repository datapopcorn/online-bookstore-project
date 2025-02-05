import pendulum

import dlt
from dlt.destinations import filesystem
from dlt.sources.sql_database import sql_database


def get_current_datetime() -> pendulum.DateTime:
    return pendulum.now()

def load_table_to_gcs():
    pipeline = dlt.pipeline(
        pipeline_name="postgres_to_gcs",
            destination=filesystem(
            layout="{table_name}/{timestamp}/{load_id}.{file_id}.{ext}",
            current_datetime=get_current_datetime,
        )
    )  

    # Fetch books from the database
    source1 = sql_database(schema='inventory', table_names=['books'])
    # Run the pipeline
    info1 = pipeline.run(source1, write_disposition="replace")    
    # Fetch transactions from the database
    source2 = sql_database(schema='sales', table_names=['transactions'])
    info2 = pipeline.run(source2, write_disposition="replace")
    # Fetch users from the database
    source3 = sql_database(schema='auth', table_names=['users'])
    info3 = pipeline.run(source3, write_disposition="replace")

    # Print load info
    print(info1)
    print(info2)
    print(info3)

if __name__ == "__main__":
    load_table_to_gcs()