<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>TUTORIAL</title>
</head>
<body>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Folder Navigation</title>
</head>
<body>
  <h1>Folder Navigation</h1>

  <h2>airflow</h2>
  <strong>- project_workflow.py</strong>
  <p>Python Script with the Airflow DAG and tasks to orchestrate and automate all the steps of the project.</p>

  <h2>batch_processing</h2>
  <strong>- pipeline.ipynb</strong>
  <p>Jupyter Notebook for data cleaning and transformation. This file's purpose is to test the transformations and execute it partially. If you want to run the script, make sure you have Apache Spark installed (I used a GCP Virtual Machine).</p>
  <strong>- pipeline.py</strong>
  <p>Clean Python script with all the transformations and BigQuery connector. This script will be submitted as a Dataproc Job.</p>

  <h2>datasets</h2>
  <strong>- clean.parquet</strong>
  <p>Processed data, ready to be ingested into BigQuery.</p>
  <strong>- raw.csv</strong>
  <p>Raw data, right out of the scraping process.</p>

  <h2>terraform</h2>
  <strong>- main.tf</strong>
  <p>Main configuration file for Terraform, defining the infrastructure as code to provision (or destroy) all the necessary resources in the cloud.</p>
  <strong>- variables.tf</strong>
  <p>File containing variable definitions used in the main Terraform file (main.tf), facilitating code customization and reuse.</p>


  <h2>web_scraping</h2>
  <p>This folder contains all the Scrapy spiders and configuration for data extraction.</p>
  <p>It also contains the Dockerfile used to build the image and submit it to Google Cloud Run.</p>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Tutorial</title>
</head>
<body>
  <h1>Tutorial</h1>

  <h2>Getting Started</h2>
  <p>For this tutorial, I will focus on the data engineering part of the project, not on the web scraping. So, we'll start with the raw dataset that's already been scraped (find it in <code>./datasets/raw.csv</code>).</p>


  <h2>1. Provisioning Cloud Resources</h2>
  <p>We'll use Terraform to provision the resources required for this project:</p>
  <ul>
    <li>A Cloud Storage bucket (Data lake)</li>
    <li>A Dataproc cluster (for processing and transforming)</li>
    <li>A BigQuery dataset (for warehousing)</li>
    <li>A Cloud Composer environment (for orchestration and automation)</li>
  </ul>
  <p>The code for implementing all these resources is in <code>./terraform/main.tf</code>. You can customize the names, zones, and values in the <code>./terraform/variables.tf</code> file.</p>


  <h3>1. Authenticate</h3>
  <ul>
    <li>Obtain a .json key for your Google Cloud Service Account with permissions for Storage, BigQuery, Dataproc, and Composer.</li>
    <li>Update the values for the service account permissions and the Composer configurations in <code>main.tf</code> under:
      <ul>
        <li><code>resource "google_service_account_iam_member"</code></li>
        <li><code>resource "google_composer_environment"</code></li>
      </ul>
    </li>
  </ul>

  <h3>2. Deploy</h3>
  <ul>
    <li>Open a terminal and run the following commands:</li>
    <li><code>terraform init</code></li>
    <li><code>terraform plan</code></li>
    <li><code>terraform apply</code></li>
    <li>Check the provisioned resources in Google Cloud Platform.</li>
  </ul>

  <h2>2. Load the Raw Data into the GCS Folder</h2>
  <ul>
    <li>Upload the <code>raw.csv</code> file into the <code>peru-real-state-datalake</code> GCS bucket created with Terraform.</li>
    <li>Create two new folders inside the same bucket: <code>code</code> and a folder with the current date, e.g., <code>2024-03-26</code>.</li>
    <li>Upload the <code>./batch_processing/pipeline.py</code> file into the <code>code</code> folder.</li>
    <li>Upload the <code>./datasets/raw.csv</code> file into the date folder.</li>
  </ul>

  <h2>3. Run the Pipeline</h2>
  <ul>
    <li>In the Google Cloud Console, navigate to Dataproc to find the cluster created with Terraform. Select the cluster and create a new job.</li>
    <li>For the job to run correctly, Dataproc requires three things: the Python script with transformations, an argument specifying the date, and the path to a .jar file to connect and load the data into BigQuery.</li>
    <li>If you followed the previous steps, the Python script will be located at <code>gs://peru-real-state-datalake/code/pipeline.py</code>.</li>
    <li>The .jar file path, according to the documentation, is <code>gs://spark-lib/bigquery/spark-bigquery-with-dependencies_2.12-0.36.1.jar</code>.</li>
    <li>The argument for the variable "date" should be something like: <code>date=2024-03-26</code>, adjusted to match the date used for your GCS folder to inform PySpark where to find the data.</li>
  </ul>

  <p>The Dataproc job will:</p>
  <ul>
    <li>Retrieve the raw data from the GCS folder.</li>
    <li>Perform transformations, clean the data, create new aggregated columns, and assign the correct data types.</li>
    <li>Export the data as .parquet and save it into a new GCS bucket.</li>
    <li>Connect to BigQuery and load the data into a table in the dataset created with Terraform.</li>
  </ul>

  <h2>4. Automate (optional)</h2>
  <ul>
    <li>In  <code>./airflow/project_workflow</code> is the Airflow DAG that'll run the scraping script, load the raw data in the data lake and run all the steps resulting in the new data being loaded into BigQuery</li>
    <li>You can decide which steps you want to automate by removing or adding tasks to the DAG</li>
    <li>Navigate to Cloud Composer and open the DAG Folder (it's a GCS bucket)</code>.</li>
    <li>Load the <code>./airflow/project_workflow</code> into the DAGs folder and wait a couple minutes for Composer to show the DAG.</li>
    <li>Run it.</li>
  </ul>
</body>
</html>