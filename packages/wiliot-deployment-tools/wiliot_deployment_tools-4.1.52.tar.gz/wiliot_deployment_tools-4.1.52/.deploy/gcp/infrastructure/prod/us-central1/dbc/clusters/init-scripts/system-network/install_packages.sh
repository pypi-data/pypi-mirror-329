#!/bin/bash
# upgrade base packages
PYSPARK_PYTHON=/databricks/python3/bin/python3
"${PYSPARK_PYTHON}" -m pip install --upgrade pip wheel setuptools

# install external python packages
EXTERNAL_PACKAGES="\
    azure-identity \
    black \
    boto3 \
    databricks-feature-store==0.10.0 \
    geopandas \
    inflection \
    kafka-python \
    loguru \
    msgraph-core==0.2.2 \
    openpyxl \
    pandas<2 \
    prometheus_client \
    pydantic>=2 \
    pytest \
    python-json-logger \
    pyyaml \
    rich \
    ruff \
    setuptools-scm \
    sgqlc \
    shapely \
    singlestoredb \
    sortedcontainers \
    sqlalchemy \
    threadpoolctl \
    tokenize-rt \
    tqdm \
    xgboost \
    "

# install wiliot internal packages - to use GCP set the env var GCP to 1
INTERNAL_PACKAGES="\
    wiliot-api==4.4.0 \
    offline-analytics-common==1.1.1119 \
    offline-sensing-common==1.1.307 \
    wiliot-signals-analysis
    "

if ! command -v gcloud &> /dev/null
then
    echo "Google Cloud SDK not installed. Installing..."
    apt-get update && apt-get install apt-transport-https ca-certificates gnupg curl -y
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
    apt-get update && apt-get install google-cloud-cli -y
else
    echo "Google Cloud SDK is already installed."
fi


## get the access token from the databricks service account
ACCESS_TOKEN=$(gcloud auth print-access-token)

# install external libs from GCP repo
"${PYSPARK_PYTHON}" -m pip install --upgrade --index-url https://oauth2accesstoken:$ACCESS_TOKEN@us-central1-python.pkg.dev/wiliot-infra/python-global/simple/ ${EXTERNAL_PACKAGES}
# install internal libs from GCP repo
"${PYSPARK_PYTHON}" -m pip install --upgrade --index-url https://oauth2accesstoken:$ACCESS_TOKEN@us-central1-python.pkg.dev/wiliot-infra/python-global/simple/ ${INTERNAL_PACKAGES}
