#!/bin/bash

set -e

PROJECT_ID="project-e88d1c23-e44c-4d58-8dd"
REGION="us-central1"
ZONE="us-central1-a"

CLUSTER_NAME="gke-cluster"
REPOSITORY_NAME="om-app-repo"

gcloud config set project $PROJECT_ID

echo "Deleting GKE Cluster..."

gcloud container clusters delete \
$CLUSTER_NAME \
--zone=$ZONE \
--quiet

echo "Deleting Artifact Registry..."

gcloud artifacts repositories delete \
$REPOSITORY_NAME \
--location=$REGION \
--quiet

echo ""
echo "✅ Cleanup Completed Successfully!"