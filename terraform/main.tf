provider "google" {
  project = var.project_id
  region  = var.region
}

# 📦 Pub/Sub Topic
resource "google_pubsub_topic" "ventas_topic" {
  name = "ventas-topic"
}

# 📥 Subscription
resource "google_pubsub_subscription" "ventas_sub" {
  name  = "ventas-sub"
  topic = google_pubsub_topic.ventas_topic.name
}

# 🗄 BigQuery Dataset
resource "google_bigquery_dataset" "ventas_dataset" {
  dataset_id = "ventas_ds"
  location   = "US"
}

# 📊 BigQuery Table
resource "google_bigquery_table" "ventas_table" {
  dataset_id = google_bigquery_dataset.ventas_dataset.dataset_id
  table_id   = "ventas"

  schema = jsonencode([
    { name = "venta_id", type = "STRING" },
    { name = "producto", type = "STRING" },
    { name = "departamento", type = "STRING" },
    { name = "region", type = "STRING" },
    { name = "fecha", type = "TIMESTAMP" },
    { name = "cantidad", type = "INTEGER" },
    { name = "precio", type = "FLOAT" }
  ])
}

# 👤 Service Account para Cloud Run
resource "google_service_account" "cloud_run_sa" {
  account_id   = "cloud-run-sa"
  display_name = "Cloud Run Service Account"
}