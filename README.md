PostgreSQL + FastAPI + BigQuery Data Pipeline with Composer, dbt, and LookML

This project demonstrates the creation of an end-to-end data engineering pipeline using local PostgreSQL, FastAPI for API development, and BigQuery as the data warehouse. It also showcases user authentication, book purchase functionality, and data synchronization to BigQuery for analytics. Additionally, it leverages dbt for transforming raw BigQuery data into analytics-ready models and LookML for defining business logic and creating interactive dashboards in Looker Core.

Project Overview

Features:

User Authentication:

JWT-based authentication for secure user login.

Book Purchase API:

Allows users to browse books and simulate purchases.

Data Pipeline:

Synchronizes book and transaction data from PostgreSQL to BigQuery.

Swagger UI:

Interactively test APIs with FastAPI's built-in Swagger interface.

Dockerized PostgreSQL:

Local PostgreSQL instance running in a Docker container.

Data Orchestration:

Google Cloud Composer for automating data workflows.

Data Analytics in BigQuery:

Leverage synchronized data for insights.

LookML for BI:

Use Looker Core and LookML for custom dashboards and data modeling.

Data Modeling with dbt:

Transform raw BigQuery data into analytics-ready models.

Technologies Used

Backend: FastAPI, Python

Database: PostgreSQL (via Docker)

Data Warehouse: BigQuery

Authentication: JSON Web Tokens (JWT)

Data Pipeline: dlt (Data Load Tool)

Orchestration: Google Cloud Composer

Business Intelligence: Looker Core with LookML

Data Modeling: dbt (Data Build Tool)

Containerization: Docker