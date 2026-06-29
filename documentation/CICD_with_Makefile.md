
# **Understanding CI/CD with Makefile and Azure Deployment**

## **1. Role of Makefile in CI/CD**

### **1.1 What is a Makefile?**

- A **Makefile** is a script used by the `make` build automation tool to automate tasks.
- **Makefiles** define **targets**, **dependencies**, and **recipes** (commands) to execute.

### **1.2 Advantages of Using Makefile in CI/CD**

- **Consistency:**
  - Standardizes build, test, and deployment processes.
- **Simplicity:**
  - Provides a straightforward syntax for defining tasks.
- **Reusability:**
  - Can be used across different environments and integrated into CI/CD pipelines.
- **Integration:**
  - Works well with various CI/CD tools and can be invoked in pipeline scripts.

---

## **2. Sample Application on Azure**

For this example, we'll use a simple Python Flask application.

### **2.1 Application Structure**

```
├── app.py
├── requirements.txt
├── Dockerfile
├── Makefile
```

### **2.2 app.py**

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, Azure!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
```

### **2.3 requirements.txt**

```
flask
```

### **2.4 Dockerfile**

```dockerfile
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80
EXPOSE 80

# Run the application
CMD ["python", "app.py"]
```

---

## **3. Creating the Makefile**

The Makefile will automate the following tasks:

- **Building the Docker image**
- **Running tests**
- **Pushing the Docker image to Azure Container Registry (ACR)**
- **Deploying the application to Azure App Service**

### **3.1 Define Variables**

```makefile
# Azure settings
RESOURCE_GROUP = myResourceGroup
ACR_NAME = myContainerRegistry
APP_SERVICE_PLAN = myAppServicePlan
WEB_APP_NAME = myWebApp
LOCATION = eastus

# Docker settings
IMAGE_NAME = myflaskapp
DOCKER_IMAGE = $(ACR_NAME).azurecr.io/$(IMAGE_NAME):latest
```

### **3.2 Define Targets**

#### **3.2.1 Login to Azure**

```makefile
.PHONY: az-login

az-login:
    az login
```

#### **3.2.2 Create Resource Group**

```makefile
.PHONY: create-resource-group

create-resource-group:
    az group create --name $(RESOURCE_GROUP) --location $(LOCATION)
```

#### **3.2.3 Create Azure Container Registry**

```makefile
.PHONY: create-acr

create-acr:
    az acr create --resource-group $(RESOURCE_GROUP) --name $(ACR_NAME) --sku Basic
```

#### **3.2.4 Build Docker Image**

```makefile
.PHONY: docker-build

docker-build:
    docker build -t $(DOCKER_IMAGE) .
```

#### **3.2.5 Push Docker Image to ACR**

```makefile
.PHONY: docker-push

docker-push:
    az acr login --name $(ACR_NAME)
    docker push $(DOCKER_IMAGE)
```

#### **3.2.6 Create App Service Plan**

```makefile
.PHONY: create-app-service-plan

create-app-service-plan:
    az appservice plan create --name $(APP_SERVICE_PLAN) --resource-group $(RESOURCE_GROUP) --is-linux --sku B1
```

#### **3.2.7 Create Web App**

```makefile
.PHONY: create-web-app

create-web-app:
    az webapp create --resource-group $(RESOURCE_GROUP) --plan $(APP_SERVICE_PLAN) --name $(WEB_APP_NAME) --deployment-container-image-name $(DOCKER_IMAGE)
```

#### **3.2.8 Configure Web App to Use ACR**

```makefile
.PHONY: configure-web-app

configure-web-app:
    az webapp config container set --name $(WEB_APP_NAME) --resource-group $(RESOURCE_GROUP) --docker-custom-image-name $(DOCKER_IMAGE)
```

#### **3.2.9 Deploy Application**

```makefile
.PHONY: deploy

deploy: docker-build docker-push create-app-service-plan create-web-app configure-web-app
    @echo "Deployment complete. Visit http://$(WEB_APP_NAME).azurewebsites.net"
```

#### **3.2.10 Clean Up Resources**

```makefile
.PHONY: clean

clean:
    az group delete --name $(RESOURCE_GROUP) --yes --no-wait
```

### **3.3 Full Makefile**

```makefile
# Variables
RESOURCE_GROUP = myResourceGroup
ACR_NAME = myContainerRegistry
APP_SERVICE_PLAN = myAppServicePlan
WEB_APP_NAME = myWebApp123456 # Ensure this name is unique in Azure
LOCATION = eastus

IMAGE_NAME = myflaskapp
DOCKER_IMAGE = $(ACR_NAME).azurecr.io/$(IMAGE_NAME):latest

# Phony Targets
.PHONY: az-login create-resource-group create-acr docker-build docker-push create-app-service-plan create-web-app configure-web-app deploy clean

# Login to Azure
az-login:
    az login

# Create Resource Group
create-resource-group:
    az group create --name $(RESOURCE_GROUP) --location $(LOCATION)

# Create Azure Container Registry
create-acr:
    az acr create --resource-group $(RESOURCE_GROUP) --name $(ACR_NAME) --sku Basic

# Build Docker Image
docker-build:
    docker build -t $(DOCKER_IMAGE) .

# Push Docker Image to ACR
docker-push:
    az acr login --name $(ACR_NAME)
    docker push $(DOCKER_IMAGE)

# Create App Service Plan
create-app-service-plan:
    az appservice plan create --name $(APP_SERVICE_PLAN) --resource-group $(RESOURCE_GROUP) --is-linux --sku B1

# Create Web App
create-web-app:
    az webapp create --resource-group $(RESOURCE_GROUP) --plan $(APP_SERVICE_PLAN) --name $(WEB_APP_NAME) --deployment-container-image-name $(DOCKER_IMAGE)

# Configure Web App to Use ACR
configure-web-app:
    az webapp config container set --name $(WEB_APP_NAME) --resource-group $(RESOURCE_GROUP) --docker-custom-image-name $(DOCKER_IMAGE)

# Deploy Application
deploy: create-resource-group create-acr docker-build docker-push create-app-service-plan create-web-app configure-web-app
    @echo "Deployment complete. Visit http://$(WEB_APP_NAME).azurewebsites.net"

# Clean Up Resources
clean:
    az group delete --name $(RESOURCE_GROUP) --yes --no-wait
```

---

## **4. Running the Makefile**

### **4.1 Deploying the Application**

- **Step 1:** Ensure you are logged into Azure CLI.

  ```bash
  make az-login
  ```

- **Step 2:** Deploy the application.

  ```bash
  make deploy
  ```

- **Step 3:** Access the application.

  - Visit `http://<WEB_APP_NAME>.azurewebsites.net` in your browser.

### **4.2 Cleaning Up Resources**

- **Delete all resources to avoid incurring charges:**

  ```bash
  make clean
  ```

---

## **5. Integrating with CI/CD Pipeline**

While the Makefile automates local tasks, integrating it into a CI/CD pipeline ensures consistent execution in response to code changes.

### **5.1 Using GitHub Actions**

Create a GitHub Actions workflow that triggers on code pushes and uses the Makefile.

#### **5.1.1 Workflow File: `.github/workflows/ci-cd.yml`**

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2

      - name: Set up Azure CLI
        uses: azure/CLI@v1

      - name: Log in to Azure CLI
        uses: azure/login@v1
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Log in to Azure Container Registry
        run: az acr login --name ${{ env.ACR_NAME }}

      - name: Execute Makefile Deploy
        env:
          ACR_NAME: ${{ env.ACR_NAME }}
          RESOURCE_GROUP: ${{ env.RESOURCE_GROUP }}
          APP_SERVICE_PLAN: ${{ env.APP_SERVICE_PLAN }}
          WEB_APP_NAME: ${{ env.WEB_APP_NAME }}
        run: |
          make deploy
```

#### **5.1.2 Setting Up Environment Variables**

In the workflow, set environment variables using `env` or pass them directly in the Makefile invocation.

#### **5.1.3 Configuring Azure Credentials**

- **Generate Azure Credentials:**

  ```bash
  az ad sp create-for-rbac --name "github-actions" --sdk-auth --role contributor --scopes /subscriptions/{Subscription-ID}/resourceGroups/{Resource-Group}
  ```

- **Add the output JSON to GitHub Secrets as `AZURE_CREDENTIALS`.**

#### **5.1.4 Update the Makefile for CI Environment**

Modify the Makefile to accept environment variables or use default values.

```makefile
# Use environment variables if set
RESOURCE_GROUP ?= myResourceGroup
ACR_NAME ?= myContainerRegistry
APP_SERVICE_PLAN ?= myAppServicePlan
WEB_APP_NAME ?= myWebApp123456
LOCATION ?= eastus
```

### **5.2 Running the CI/CD Pipeline**

- **Push code to the `main` branch.**
- **GitHub Actions will trigger the workflow, executing the Makefile targets.**

L.,