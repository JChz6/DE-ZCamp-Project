terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  # GCP creds
  credentials = file(var.credentials)
  project     = var.project
  region      = var.region
}

#Cloud Storage Bucket for the raw data
resource "google_storage_bucket" "data-lake-bucket" {
  name     = var.gcs_bucket_name
  location = var.location

  storage_class               = "STANDARD"
  uniform_bucket_level_access = true
  versioning {
    enabled = true
  }
  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }
  force_destroy = true
}


#Dataproc Cluster for Spark processing
resource "google_dataproc_cluster" "simplecluster" {
  name   = var.dataproc_cluster_name
  region = var.region
  
  cluster_config {
    # Reduce el número de nodos a 2
    master_config {
      num_instances = 1
      machine_type = "n1-standard-2"
    }

    worker_config {
      num_instances = 2
      machine_type = "n1-standard-2"
    }

    initialization_action {
      script = "gs://dataproc-initialization-actions/jupyter/jupyter.sh"
    }
  }
}





#BigQuery Dataset for warehousing
resource "google_bigquery_dataset" "dataset" {
  dataset_id = var.bq_dataset_name
  project    = var.project
  location   = var.region
}


#Service account permissions required for Cloud Composer
resource "google_service_account_iam_member" "custom_service_account" {
  provider           = google-beta
  service_account_id = "projects/{your-project-id}/serviceAccounts/{your-service-account-id}@{your-project-id}.iam.gserviceaccount.com"
  role               = "roles/composer.ServiceAgentV2Ext"
  member             = "serviceAccount:service-{your-compute-SA-number}@cloudcomposer-accounts.iam.gserviceaccount.com"
}



#Cloud Composer (airflow) for orchestration
resource "google_composer_environment" "project_workflow" {
  provider = google-beta
  name     = var.composer_environment
  project  = var.project
  region   = var.region
  config {
    software_config {
      image_version = "composer-2-airflow-2"
    }
    node_config {
      service_account = "{your-service-account}@{your-project-id}.iam.gserviceaccount.com" 
    }
  }
}


