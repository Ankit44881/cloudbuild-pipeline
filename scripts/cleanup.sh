#!/bin/bash

# Do not use set -e here so cleanup continues even if one resource fails/doesn't exist

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
echo "Deleting GKE Cluster"
echo "====================================="
if gcloud container clusters describe $CLUSTER_NAME --zone=$ZONE >/dev/null 2>&1; then
    echo "Deleting cluster '$CLUSTER_NAME' (this may take a few minutes)..."
    gcloud container clusters delete $CLUSTER_NAME --zone=$ZONE --quiet
    echo "✅ GKE Cluster deleted."
else
    echo "ℹ️ Cluster '$CLUSTER_NAME' not found or already deleted."
fi

echo "====================================="
echo "Deleting Artifact Registry"
echo "====================================="
if gcloud artifacts repositories describe $REPOSITORY_NAME --location=$REGION >/dev/null 2>&1; then
    echo "Deleting repository '$REPOSITORY_NAME'..."
    gcloud artifacts repositories delete $REPOSITORY_NAME --location=$REGION --quiet
    echo "✅ Artifact Registry deleted."
else
    echo "ℹ️ Artifact Registry '$REPOSITORY_NAME' not found or already deleted."
fi

echo ""
echo "✅ Cleanup Completed Successfully!"