# ⚡ **SMARD Energy Data Pipeline**

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white) ![Terraform](https://img.shields.io/badge/Terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## **Project Overview**
This data pipeline visualizes the data of the German energy market in a dashboard. It gives an overview of the generated and consumed power, the usage of the different energy sources and the market price for Germany.

![Dashboard Scrrenshot](screenshots/dashboard.png)

The energy market data come from [Bundesnetzagentur | SMARD.de](https://www.smard.de/home), the website of the German Federal Network Agency. The data are published under the CC BY 4.0 licence.

## 📁 Repository Structure

```text
smard-energy-pipeline/
├── aws/
│   ├── lambda/
│   │   ├── ingest/
|   |   |   └── handler.py
│   │   └── query/
|   |       └── handler.py
│   ├── layer.zip
│   └── upload_to_s3.py
|
├── dashboard/
│   ├── backend/
|   |   └── server.py
│   ├── frontend/
|   |   ├── favicon.ico
|   |   ├── index.html
|   |   ├── script.js
|   |   └── style.css
│   └── requirements.txt
|
├── local/
│   ├── downloader.py
│   ├── main.py
│   └── requirements.txt
|
├── screenshots/
│   └── dashboard.png
|
├── smard_pipeline/
│   ├── __init__.py
│   ├── config.py
|   ├── current_week.py
|   ├── ingest.py
|   ├── logging_config.py
|   ├── smard_api.py
|   ├── storage_s3.py
│   └── transformations.py
|
├── terraform/
│   ├── modules/
|   |   ├── api_gateway/
|   |   |   ├── main.tf
|   |   |   ├── outputs.tf
|   |   |   └── variables.tf
|   |   ├── eventbridge/
|   |   |   ├── main.tf
|   |   |   ├── outputs.tf
|   |   |   └── variables.tf
|   |   ├── iam/
|   |   |   ├── main.tf
|   |   |   ├── outputs.tf
|   |   |   └── variables.tf
|   |   ├── lambda/
|   |   |   ├── main.tf
|   |   |   ├── outputs.tf
|   |   |   └── variables.tf
|   |   ├── lambda_layer/
|   |   |   ├── main.tf
|   |   |   ├── outputs.tf
|   |   |   └── variables.tf
|   |   └── s3/
|   |       ├── main.tf
|   |       ├── outputs.tf
|   |       └── variables.tf
|   ├── locals.tf
|   ├── main.tf
|   ├── outputs.tf
|   ├── providers.tf
|   └── variables.tf
|
├── .gitignore
├── pyproject.toml
└── README.md
```


## 🏗️ Architecture & Technologies

## 🚀 Getting started

## 💻 Local Deployment

## ☁️ AWS Deployment