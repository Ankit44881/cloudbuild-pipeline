# Chai Politics - Order Management Application

This project is a simple Order Management Application developed for **Chai Politics**. I created it to get hands-on experience with building and deploying a complete containerized application on **Google Cloud Platform (GCP)**.

The application consists of a frontend, a Python Flask backend and a MySQL database. Each component runs inside its own Docker container and is deployed on a **Google Kubernetes Engine (GKE)** cluster. Along with application deployment, the project also focuses on automating the CI/CD process using **Google Cloud Build**.

---

## Technologies Used

* Python (Flask)
* HTML, CSS and JavaScript
* MySQL
* Docker
* Kubernetes (GKE)
* Google Cloud Build
* Google Artifact Registry
* SonarQube
* pytest
* pytest-cov

---

## Project Structure

```text
cloudbuild-pipeline/
│
├── backend/                  # Flask application and unit tests
├── frontend/                 # Frontend application
├── database/                 # MySQL schema
├── kubernetes/               # Kubernetes manifests
├── scripts/                  # GKE and Artifact Registry setup scripts
├── cloudbuild.yaml           # Main Cloud Build pipeline
├── rollback.yaml             # Rollback pipeline
├── sonar-project.properties  # SonarQube configuration
└── README.md
```

---

## Application Features

* Displays the Chai Politics menu.
* Allows customers to place orders.
* Stores application data in a MySQL database.
* Frontend and backend run as separate Docker containers.
* Kubernetes manages application deployment and scaling.
* Cloud Build automates the build and deployment process.
* Supports rollback to a previous application version when required.

---

## Infrastructure Setup

To avoid creating cloud resources manually every time, I created simple shell scripts that automate the setup and cleanup process.

Create the required infrastructure:

```bash
chmod +x scripts/setup.sh scripts/cleanup.sh
./scripts/setup.sh
```

This script creates:

* Google Kubernetes Engine (GKE) Cluster
* Google Artifact Registry Repository
* Docker authentication
* Kubernetes cluster credentials

To remove the resources after testing:

```bash
./scripts/cleanup.sh
```

---

## CI/CD Pipeline

Whenever changes are pushed to the repository, Cloud Build performs the following steps automatically:

1. Runs unit tests using **pytest**.
2. Generates code coverage using **pytest-cov**.
3. Performs code quality analysis with **SonarQube**.
4. Builds Docker images.
5. Pushes the images to **Google Artifact Registry**.
6. Updates the Kubernetes deployment with the latest image.
7. Deploys the application to **Google Kubernetes Engine (GKE)**.

If required, the rollback pipeline can redeploy a previously working image.

---

## Why I Built This Project

I wanted to learn how a real-world application is deployed on Google Cloud instead of deploying a simple sample application. Since I am also working on my own food business idea, **Chai Politics**, I decided to use it as the project theme.

This project helped me understand Docker, Kubernetes, Cloud Build, container registries, automated deployments, unit testing and code quality checks in a practical way.

---

## Future Improvements

The next improvements I plan to make are:

* Trivy for container image vulnerability scanning.
* OWASP ZAP for automated DAST testing.
* Prometheus and Grafana for monitoring.
* Helm charts for Kubernetes deployments.
* Argo CD for GitOps-based continuous deployment.

---

## Author

**Ankit Raj**

Cloud | DevOps | DevSecOps Enthusiast
