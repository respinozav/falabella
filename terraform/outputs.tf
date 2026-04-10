output "pubsub_topic" {
  value = google_pubsub_topic.ventas_topic.name
}

output "bigquery_table" {
  value = google_bigquery_table.ventas_table.table_id
}