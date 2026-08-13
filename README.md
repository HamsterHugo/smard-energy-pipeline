# ⚡ **SMARD Energy Data Pipeline**

![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white) ![Terraform](https://img.shields.io/badge/Terraform-%235835CC.svg?style=for-the-badge&logo=terraform&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

## **Project Overview**
This data pipeline visualizes the data of the German energy market in a dashboard. It gives an overview of the generated and consumed power, the usage of the different energy sources and the market price for Germany.

![Dashboard Scrrenshot](images/dashboard.png)

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
├── images/
│   ├── architecture.excalidraw
│   ├── architecture.png
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

![Architecture Diagram](images/architecture.png)

### 🛠️ Used AWS Services
 * S3 Bucket
 * Lambda function and layer
 * API Gateway
 * EventBridge
 * CloudWatch

## 🚀 Getting started

1. Clone the repo to your local machine:
```bash
git clone https://github.com/HamsterHugo/smard-energy-pipeline.git
```

2. Create a virtual environment for Python
If you are using Visual Studio Code you can do it by executing the following command:
```bash
python -m venv .venv
```

3. Download and preprocess the historical data from SMARD.de
You have execute the Python scripts for downloading the timeseries. For that go to the folder `local/`:
```bash
cd local
```

If not already done, you have to install all the Python packages. For that enter the following command:
```bash
pip install -r requirements.txt
```

Now, you can download and preprocess the timeseries data from SMARD.de by using the script `main.py`. Here is a list of all valid commands:

* ``python main.py historical <category> <subcategory>``
* ``python main.py historical <category> all``
* ``python main.py historical combine``
* ``pyhton main.py merge <category> <subcategory>``
* ``python main.py merge <category> all``
* ``python main.py current <category> <subcategory>``
* ``python main.py current <category> all``
* ``python main.py current combine``

Replace `<category>` and `<subcategory>` with the names of the desired category and subcategory. 


## 💻 Local Deployment

## ☁️ AWS Deployment