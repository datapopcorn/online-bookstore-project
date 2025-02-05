import dlt
from dlt.sources.sql_database import sql_database

# def load_select_tables_from_database() -> None:
#     # Define the pipeline
#     pipeline = dlt.pipeline(
#         pipeline_name="dlt_postgres_to_duckdb_test",
#         destination="duckdb",
#         dataset_name="bookstore"
#     )

#     # Fetch tables inventory.books, sales.transactions, and auth.users
#     #source = sql_database(table_names=['books', 'transactions', 'users'])
#     # or
#     source = sql_database().with_resources("inventory.books", "sales.transactions", "auth.users")

#     # Run the pipeline
#     info = pipeline.run(source)

#     # Print load info
#     print(info)

def load_entire_database() -> None:
    # Define the pipeline
    pipeline = dlt.pipeline(
        pipeline_name="dlt_postgres_to_bigquery",
        destination="bigquery",
        dataset_name="bookstore_raw"
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
    load_entire_database()