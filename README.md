# Chai Politics - Order Management Application

This is a simple Order Management application created for **Chai Politics**. I built this project to practice deploying a real application on Google Cloud using Docker, Kubernetes and Cloud Build.

The application has a frontend, a Python Flask backend and a MySQL database. The complete application is deployed on **Google Kubernetes Engine (GKE)**.

---

## Technologies Used

* Python (Flask)
* HTML, CSS and JavaScript
* MySQL
* Docker
* Kubernetes
* Google Kubernetes Engine (GKE)
* Google Artifact Registry
* Google Cloud Build
* SonarQube

---

## Project Structure

```
cloudbuild-pipeline/
│
├── backend/
├── frontend/
├── database/
├── kubernetes/
├── scripts/
├── cloudbuild.yaml
├── rollback.yaml
├── sonar-project.properties
└── README.md
```

---

## What this project does

* Shows the Chai Politics menu
* Accepts customer orders
* Stores data in MySQL
* Runs frontend and backend in separate Docker containers
* Deploys the application to GKE
* Uses Cloud Build to automate deployment
* Supports rollback to a previous deployment when required

---

## Infrastructure

The setup script creates the required cloud resources automatically.

Resources created:

* GKE Cluster
* Artifact Registry
* Docker authentication
* Kubernetes cluster credentials

Run:

```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

To remove everything after testing:

```bash
./scripts/cleanup.sh
```

---

## Deployment Flow

Whenever I push changes to the repository, Cloud Build performs the deployment steps automatically.

* Build Docker image
* Push image to Artifact Registry
* Update Kubernetes deployment
* Deploy the latest image to GKE

If required, the rollback pipeline can deploy an older image.

---

## Why I built this project

The main goal of this project was to get hands-on experience with Docker, Kubernetes and Google Cloud. Instead of deploying a simple demo application, I wanted to use a project based on my own business idea, **Chai Politics**, so that the learning felt more practical.

---

## Future Improvements

In the future I plan to add:

* Trivy image scanning
* OWASP ZAP security testing
* Monitoring with Prometheus and Grafana
* Helm charts
* GitOps using Argo CD

---

## Author

**Ankit Raj**
