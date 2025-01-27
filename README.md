# PostgreSQL + FastAPI + BigQuery Data Pipeline with Composer, dbt, and LookML

This project demonstrates the creation of an end-to-end data engineering pipeline using local PostgreSQL, FastAPI for API development, and BigQuery as the data warehouse. It also showcases user authentication, book purchase functionality, and data synchronization to BigQuery for analytics. Additionally, it leverages dbt for transforming raw BigQuery data into analytics-ready models and LookML for defining business logic and creating interactive dashboards in Looker Core.

## Project Overview

### Features:

1. User Authentication:
   - JWT-based authentication for secure user login.

2. Book Purchase API:
   - Allows users to browse books and simulate purchases.

3. Data Pipeline:
   - Synchronizes book and transaction data from PostgreSQL to BigQuery.

4. Swagger UI:
   - Interactively test APIs with FastAPI's built-in Swagger interface.

5. Dockerized PostgreSQL:
   - Local PostgreSQL instance running in a Docker container.

6. Data Orchestration:
   - Google Cloud Composer for automating data workflows.

7. Data Analytics in BigQuery:
   - Leverage synchronized data for insights.

8. LookML for BI:
   - Use Looker Core and LookML for custom dashboards and data modeling.

9. Data Modeling with dbt:
    - Transform raw BigQuery data into analytics-ready models.

### Technologies Used

1. Backend: FastAPI, Python

2. Database: PostgreSQL (via Docker)

3. Data Warehouse: BigQuery

4. Authentication: JSON Web Tokens (JWT)

5. Data Pipeline: dlt (Data Load Tool)

6. Orchestration: Google Cloud Composer

7. Business Intelligence: Looker Core with LookML

8. Data Modeling: dbt (Data Build Tool)

9. Containerization: Docker
