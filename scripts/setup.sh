#!/bin/bash

set -e

# -----------------------------
# Configuration
# -----------------------------
PROJECT_ID="project-e88d1c23-e44c-4d58-8dd"
REGION="us-central1"
ZONE="us-central1-a"

CLUSTER_NAME="gke-cluster"
REPOSITORY_NAME="om-app-repo"

echo "====================================="
echo "Setting GCP Project"
echo "====================================="

gcloud config set project $PROJECT_ID

echo "====================================="
echo "Enabling Required APIs"
echo "====================================="

gcloud services enable \
container.googleapis.com \
artifactregistry.googleapis.com \
cloudbuild.googleapis.com

echo "====================================="
echo "Creating Artifact Registry"
echo "====================================="

gcloud artifacts repositories create $REPOSITORY_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Docker Repository"

echo "====================================="
echo "Configuring Docker"
echo "====================================="

gcloud auth configure-docker ${REGION}-docker.pkg.dev --quiet

echo "====================================="
echo "Creating GKE Cluster"
echo "====================================="

gcloud container clusters create $CLUSTER_NAME \
    --zone=$ZONE \
    --num-nodes=1

echo "====================================="
echo "Getting Cluster Credentials"
echo "====================================="

gcloud container clusters get-credentials \
$CLUSTER_NAME \
--zone=$ZONE

echo "====================================="
echo "Cluster Ready!"
echo "====================================="

kubectl get nodes

echo ""
echo "✅ Setup Completed Successfully!"