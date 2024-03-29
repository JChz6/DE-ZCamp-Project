<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <h1>Real Estate Market in Peru</h1>

  <p>Check the dashboard <a href="https://lookerstudio.google.com/reporting/12479d0d-f7b8-4cdb-b7f3-f987547e56bb">***HERE***</a>.</p>

  <h2>Context:</h2>
  <p>One of my primary medium-term goals is to purchase my own home. Being data-driven, I actively sought out data to analyze the real estate market, exploring opportunities within my city and country to ensure I make the most informed decision tailored to my needs and budget.</p>

  <h2>Problem:</h2>
  <p>Unfortunately, there are no freely accessible data sources for my country comparable to those available for the United States. So, I decided to create my own dataset by scraping a property sales website.</p>
  
  <h2>Strategy:</h2>
  <p>Because new properties hit the market every day, I'll run my scraping script every two weeks (I'll automate this). The fresh data will then go through an automated data processing pipeline before getting stored in a data warehouse, ready to fuel an analytics dashboard.</p>

<h2>Tools:</h2>
<ol>
  <li>
    <strong>Web Scraping:</strong>
    <ul>
      <li>Python</li>
      <li>Scrapy</li>
    </ul>
  </li>
  <li>
    <strong>Cloud:</strong>
    <ul>
      <li>Google Cloud Platform (GCP)</li>
      <li>Terraform (IaC)</li>
    </ul>
  </li>
  <li>
    <strong>Data Ingestion (batch):</strong>
    <ul>
      <li>Python</li>
      <li>Google Cloud Storage</li>
      </ul>
  </li>
  <li>
    <strong>Data Warehousing:</strong>
    <ul>
      <li>Google BigQuery</li>
    </ul>
  </li>
  <li>
    <strong>Data Transformations and Processing:</strong>
    <ul>
      <li>Pyspark (Dataproc)</li>
    </ul>
  </li>
    <li>
    <strong>Orchestration and Automation:</strong>
    <ul>
      <li>Airflow (Cloud Composer)</li>
    </ul>
  </li>
  <li>
    <strong>Dashboarding:</strong>
    <ul>
      <li>Google Looker Studio</li>
    </ul>
    <p>Check the dashboard <a href="https://lookerstudio.google.com/reporting/12479d0d-f7b8-4cdb-b7f3-f987547e56bb">***here***</a>.</p>
  </li>
</ol>


  <h2>Architecture</h2>
  <p>If you consider yourserlf a visual learner, I put together this brief animation of the architecture and workflow.</p>
  
  
  
  ![Architecture](https://github.com/JChz6/DE-ZCamp-Project/assets/116318822/52293665-d9aa-4330-9bf0-5c3d556780a6)

  
  
  <h1>Folder navigation</h1>
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



  
  
  <h2>Tutorial</h2>
  <p>For the instructions and walkthrough, please refer to <a href="https://github.com/JChz6/DE-ZCamp-Project/blob/main/TUTORIAL.md">TUTORIAL.md</a> .</p>


</body>
</html>
