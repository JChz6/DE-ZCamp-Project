variable "credentials" {
  description = "GCP credentials"
  default     = "YOUR CREDENTIALS FILE"
}

variable "project" {
  description = "Project id"
  default     = "YOUR PROJECT ID"
}

variable "region" {
  description = "Region"
  default     = "us-east1"
}

variable "location" {
  description = "Project location"
  default     = "US"
}

variable "bq_dataset_name" {
  description = "Nombre del dataset de BigQuery"
  default     = "peru_real_state"
}

variable "gcs_bucket_name" {
  description = "Bucket Name"
  default     = "peru-real-state-datalake"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default     = "STANDART"
}

variable "dataproc_cluster_name" {
  description = "Dataproc Cluster Pipeline"
  default     = "project-pipeline2"
}

variable "composer_environment" {
  description = "Cloud Composer Environment"
  default     = "project-workflow1"
}