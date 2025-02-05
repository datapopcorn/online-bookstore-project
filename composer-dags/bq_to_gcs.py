# this file is running on the composer environment to backup the bigquery tables to gcs 
# send slack message to the channel when the backup is started and completed and show the is_manual flag

from __future__ import annotations

import os
from datetime import datetime
from airflow import DAG
from airflow.providers.google.cloud.transfers.bigquery_to_gcs import BigQueryToGCSOperator
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import json
import datetime

# ========== 設定參數 ==========
BQ_TABLE_BOOKS = "online-bookstore-449113.bookstore_raw.books"  # BigQuery 資料表
BQ_TABLE_TRANSACTIONS = "online-bookstore-449113.bookstore_raw.transactions"  # BigQuery 資料表
BQ_TABLE_USERS = "online-bookstore-449113.bookstore_raw.users"  # BigQuery 資料表

GCS_BUCKET = "gs://online-bookstore/data_from_bq"  # GCS 存儲桶
GCS_FILE_PATH_BOOKS = f"{GCS_BUCKET}/{BQ_TABLE_BOOKS.split('.')[-1]}_backup_{datetime.datetime.now().strftime('%Y%m%d')}.csv"
GCS_FILE_PATH_TRANSACTIONS = f"{GCS_BUCKET}/{BQ_TABLE_TRANSACTIONS.split('.')[-1]}_backup_{datetime.datetime.now().strftime('%Y%m%d')}.csv"
GCS_FILE_PATH_USERS = f"{GCS_BUCKET}/{BQ_TABLE_USERS.split('.')[-1]}_backup_{datetime.datetime.now().strftime('%Y%m%d')}.csv"

# 環境變數 (可在 Cloud Composer 環境變數設定)
SLACK_WEBHOOK_CONN_ID = os.environ.get("SLACK_WEBHOOK_CONN_ID", "slack_default")
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/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"

# ========== 定義發送 Slack 訊息的函數 ==========
def get_trigger_type(**kwargs):
    """取得觸發方式：手動 (manual) 或 排程 (scheduled)"""
    dag_run = kwargs.get("dag_run")
    is_manual = dag_run.run_id.startswith("manual__")
    return "手動執行 (Manually Triggered)" if is_manual else "排程執行 (Scheduled Run)"

def send_slack_start(**kwargs):
    """發送 Slack 開始通知，包含觸發方式"""
    trigger_type = get_trigger_type(**kwargs)
    execution_date = kwargs["execution_date"].strftime('%Y-%m-%d %H:%M:%S')

    slack_start = SlackWebhookOperator(
        task_id="slack_start_notification",
        slack_webhook_conn_id=SLACK_WEBHOOK_CONN_ID,
        message=(
            f":rocket: *BigQuery 備份任務開始*\n"
            f"📅 執行時間: `{execution_date}`\n"
            f"🔄 觸發方式: `{trigger_type}`\n"
            f"💾 目標 GCS: `{GCS_BUCKET}`"
        ),
    )
    slack_start.execute(kwargs)

def send_slack_end(**kwargs):
    """發送 Slack 結束通知"""
    trigger_type = get_trigger_type(**kwargs)
    execution_date = kwargs["execution_date"].strftime('%Y-%m-%d %H:%M:%S')

    slack_end = SlackWebhookOperator(
        task_id="slack_end_notification",
        slack_webhook_conn_id=SLACK_WEBHOOK_CONN_ID,
        message=(
            f":white_check_mark: *BigQuery 備份完成*\n"
            f"📅 完成時間: `{execution_date}`\n"
            f"🔄 觸發方式: `{trigger_type}`\n"
            f"✅ 備份位置: `{GCS_BUCKET}`"
        ),
    )
    slack_end.execute(kwargs)

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": days_ago(1),
    "retries": 1,
}

with DAG(
    "bq_backup_to_gcs",
    default_args=default_args,
    schedule_interval="0 2 * * *",  # 每天凌晨 2 點執行
    catchup=False,
    description="每日備份 BigQuery 資料到 GCS 並發送 Slack 通知",
) as dag:

    # ========== 送出 Slack 開始通知 ==========
    start_slack_notification = PythonOperator(
        task_id="start_slack_notification",
        python_callable=send_slack_start,
        provide_context=True,
    )

    # ========== BigQuery 備份到 GCS ==========
    export_bq_to_gcs_books = BigQueryToGCSOperator(
        task_id="export_bq_to_gcs_books",
        source_project_dataset_table=BQ_TABLE_BOOKS,
        destination_cloud_storage_uris=[GCS_FILE_PATH_BOOKS],
        export_format="CSV",
        field_delimiter=",",
        print_header=True,
    )

    export_bq_to_gcs_transactions = BigQueryToGCSOperator(
        task_id="export_bq_to_gcs_transactions",
        source_project_dataset_table=BQ_TABLE_TRANSACTIONS,
        destination_cloud_storage_uris=[GCS_FILE_PATH_TRANSACTIONS],
        export_format="CSV",
        field_delimiter=",",
        print_header=True,
    )

    export_bq_to_gcs_users = BigQueryToGCSOperator(
        task_id="export_bq_to_gcs_users",
        source_project_dataset_table=BQ_TABLE_USERS,
        destination_cloud_storage_uris=[GCS_FILE_PATH_USERS],
        export_format="CSV",
        field_delimiter=",",
        print_header=True,
    )

    # ========== 送出 Slack 結束通知 ==========
    end_slack_notification = PythonOperator(
        task_id="end_slack_notification",
        python_callable=send_slack_end,
        provide_context=True,
    )

    # ========== 設定 DAG 任務順序 ==========
    start_slack_notification >> export_bq_to_gcs_books >> export_bq_to_gcs_transactions >> export_bq_to_gcs_users >> end_slack_notification
