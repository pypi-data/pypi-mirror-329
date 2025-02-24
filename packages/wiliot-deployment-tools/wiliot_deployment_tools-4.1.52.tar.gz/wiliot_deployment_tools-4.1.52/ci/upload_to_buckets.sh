#!/bin/bash
#Logic to sync the init scripts to the s3 and gcs buckets. Dealing if path does not exists
init_script_clusters=".deploy/${CLOUD}/infrastructure/${ENV}/us-east-2/dbc/clusters/init-scripts/."
init_script_job_clusters=".deploy/${CLOUD}/infrastructure/${ENV}/us-east-2/dbc/job-clusters/init-scripts/."

if [ -d "$init_script_clusters" ]; then
    if [ "$CLOUD" = "aws" ]; then
        #Export AWS credentials and assume role accordingly to the deploy environment 
        export AWS_ACCESS_KEY_ID=$CLOUD_AWS_ACCESS_KEY_ID
        export AWS_SECRET_ACCESS_KEY=$CLOUD_AWS_SECRET_ACCESS_KEY
        export AWS_REGION=us-east-2
        export ENV_UP=$(echo "$ENV" | tr '[:lower:]' '[:upper:]')
        eval "role_arn=\$${ENV_UP}_TERRAGRUNT_IAM_ROLE"
        role_credentials=$(aws sts assume-role --role-arn $role_arn --role-session-name ${ENV})
        access_key=$(echo "$role_credentials" | jq -r '.Credentials.AccessKeyId')
        secret_key=$(echo "$role_credentials" | jq -r '.Credentials.SecretAccessKey')
        session_token=$(echo "$role_credentials" | jq -r '.Credentials.SessionToken')
        export AWS_ACCESS_KEY_ID="$access_key"
        export AWS_SECRET_ACCESS_KEY="$secret_key"
        export AWS_SESSION_TOKEN="$session_token"
        aws s3 sync "$init_script_clusters" s3://wiliot-dbc-us-east-2-${ENV}-monitoring-and-logs/clusters/init-scripts
    else
        #Export GCP key file
        echo -n $CLOUD_GCP_KEY | base64 -d > cloud_gcp_key.json
        gcloud auth activate-service-account --key-file=${PWD}/cloud_gcp_key.json
        export GOOGLE_APPLICATION_CREDENTIALS=${PWD}/cloud_gcp_key.json
        gsutil rsync -r "$init_script_clusters" gs://wiliot-${ENV}-us-central1-monitoring-and-logging/job-clusters/init-scripts
    fi
else
    # Directory does not exist
    echo "No cluster init scripts found to upload in the path: $init_script_clusters"
fi

if [ -d "$init_script_job_clusters" ]; then
    if [ "$CLOUD" = "aws" ]; then
        aws s3 sync "$init_script_job_clusters" s3://wiliot-dbc-us-east-2-${ENV}-monitoring-and-logs/job-clusters/init-scripts
    else
        gsutil rsync -r "$init_script_job_clusters" gs://wiliot-${ENV}-us-central1-monitoring-and-logging/job-clusters/init-scripts
    fi
else
    # Directory does not exist
    echo "No job clusters init scripts found to upload in the path: $init_script_job_clusters"
fi

