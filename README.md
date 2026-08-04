
# Amazon Clone - Complete Deployment Guide (AWS EC2 → Kubernetes → ArgoCD)

# Amazon Clone Deployment Guide

This guide explains how to deploy the complete Amazon Clone project from scratch on a fresh AWS EC2 Ubuntu server.

No prior setup is assumed. Follow every step in order.

---

# Architecture

```
Developer
      │
      ▼
GitHub Repository
      │
      ▼
AWS EC2 (Ubuntu)
      │
      ▼
Docker
      │
      ▼
Kind Kubernetes Cluster
      │
      ▼
NGINX Ingress
      │
      ▼
ArgoCD
      │
      ▼
Deploy All Microservices
```

---

# Prerequisites

* AWS Account
* GitHub Account
* Domain (Optional)
* Ubuntu 22.04 EC2 Instance

Recommended EC2

* Ubuntu 22.04
* t3.large (minimum)
* 30GB Storage

---

# Step 1 : Launch EC2

Go to AWS Console

```
EC2
```

Click

```
Launch Instance
```

Choose

```
Ubuntu Server 22.04 LTS
```

Instance Type

```
t3.large
```

Storage

```
30 GB
```

Security Group

Allow

```
22 SSH
80 HTTP
443 HTTPS
30000-32767 NodePort
6443 Kubernetes API
```

Launch the instance.

---

# Step 2 : Connect to EC2

```
chmod 400 amazon.pem

ssh -i amazon.pem ubuntu@YOUR_PUBLIC_IP
```

Update system

```
sudo apt update

sudo apt upgrade -y
```

---

# Step 3 : Install Git

```
sudo apt install git -y

git --version
```

---

# Step 4 : Clone Repository

```
cd ~

git clone https://github.com/kalyan0996/Amazon-Clone.git

cd Amazon-Clone
```

Verify

```
ls
```

You should see

```
backend/
frontend/
infrastructure/
scripts/
docker-compose.dev.yml
.gitlab-ci.yml
README.md
```

---

# Step 5 : Install Docker

Remove old Docker

```
sudo apt remove docker docker-engine docker.io containerd runc -y
```

Install dependencies

```
sudo apt install \
ca-certificates \
curl \
gnupg \
lsb-release -y
```

Add Docker Key

```
sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

Add Docker Repository

```
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Install Docker

```
sudo apt update

sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

Enable Docker

```
sudo systemctl enable docker

sudo systemctl start docker
```

Add current user

```
sudo usermod -aG docker $USER
```

Logout

Reconnect

```
ssh -i amazon.pem ubuntu@YOUR_PUBLIC_IP
```

Verify

```
docker version
```

---

# Step 6 : Install kubectl

```
curl -LO https://dl.k8s.io/release/$(curl -L -s \
https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl

chmod +x kubectl

sudo mv kubectl /usr/local/bin/
```

Verify

```
kubectl version --client
```

---

# Step 7 : Install Kind

```
curl -Lo ./kind \
https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64

chmod +x kind

sudo mv kind /usr/local/bin/
```

Verify

```
kind version
```

---

# Step 8 : Create Kubernetes Cluster

Go to

```
cd ~/Amazon-Clone/infrastructure/kind
```

Create cluster

```
chmod +x create-cluster.sh

./create-cluster.sh
```

Verify

```
kubectl get nodes
```

Expected

```
NAME
kind-control-plane
```

---

# Step 9 : Install Helm

```
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Verify

```
helm version
```

---

# Step 10 : Deploy Base Kubernetes Resources

```
cd ~/Amazon-Clone/infrastructure/kubernetes/base

kubectl apply -f .
```

Verify

```
kubectl get ns

kubectl get pv

kubectl get pvc
```

---

# Step 11 : Build Docker Images

Go to

```
cd ~/Amazon-Clone/infrastructure/scripts
```

Run

```
chmod +x build.sh

./build.sh
```

This builds every service.

---

# Step 12 : Load Images into Kind

```
cd ~/Amazon-Clone/infrastructure/kind

chmod +x load-images.sh

./load-images.sh
```

Verify

```
docker images
```

---

# Step 13 : Install NGINX Ingress

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Wait

```
kubectl wait \
--namespace ingress-nginx \
--for=condition=Ready \
pod \
--selector=app.kubernetes.io/component=controller \
--timeout=300s
```

---

# Step 14 : Install ArgoCD

Create namespace

```
kubectl create namespace argocd
```

Install

```
kubectl apply -n argocd \
-f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Wait

```
kubectl get pods -n argocd
```

All should become Running.

---

# Step 15 : Expose ArgoCD

```
kubectl port-forward svc/argocd-server \
-n argocd \
8080:443
```

Open

```
https://localhost:8080
```

Ignore browser certificate warning.

---

# Step 16 : Get ArgoCD Password

Username

```
admin
```

Password

```
kubectl -n argocd get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" | base64 -d

echo
```

Login.

---

# Step 17 : Deploy App of Apps

Go to

```
cd ~/Amazon-Clone/infrastructure/argocd
```

Deploy

```
kubectl apply -f app-project.yaml

kubectl apply -f app-of-apps.yaml
```

Verify

```
kubectl get applications -n argocd
```

You should see all applications such as:

```
admin-service
analytics-service
api-gateway
auth-service
cart-service
catalog-service
inventory-service
notification-service
order-service
payment-service
pricing-service
product-service
rating-service
recommendation-service
review-service
search-service
seller-service
shipping-service
user-service
wishlist-service
```

---

# Step 18 : Verify Pods

```
kubectl get pods -A
```

Verify services

```
kubectl get svc -A
```

Verify deployments

```
kubectl get deploy -A
```

---

# Step 19 : Access the Frontend

If using port-forward:

```
kubectl port-forward svc/frontend 3000:3000
```

Open

```
http://localhost:3000
```

If exposed using Ingress, browse to your configured host or EC2 public IP.

---

# Step 20 : View Logs

Single pod

```
kubectl logs POD_NAME
```

Follow logs

```
kubectl logs -f POD_NAME
```

Specific namespace

```
kubectl logs POD_NAME -n default
```

---

# Step 21 : Restart Deployment

```
kubectl rollout restart deployment DEPLOYMENT_NAME
```

Example

```
kubectl rollout restart deployment auth-service
```

---

# Step 22 : Scaling

```
kubectl scale deployment auth-service --replicas=3
```

Verify

```
kubectl get pods
```

---

# Step 23 : Delete Cluster

```
cd ~/Amazon-Clone/infrastructure/kind

./delete-cluster.sh
```

---

# Useful Commands

Docker

```
docker ps

docker images

docker system prune -a
```

Kubernetes

```
kubectl get pods

kubectl get svc

kubectl get ingress

kubectl get deployments

kubectl describe pod POD_NAME

kubectl delete pod POD_NAME
```

ArgoCD

```
kubectl get applications -n argocd

kubectl describe application APP_NAME -n argocd
```

Git

```
git pull

git status

git log
```

---

# Project Structure

```
Amazon-Clone/

backend/
frontend/
infrastructure/

backend/
├── admin-service
├── analytics-service
├── api-gateway
├── auth-service
├── cart-service
├── catalog-service
├── inventory-service
├── notification-service
├── order-service
├── payment-service
├── pricing-service
├── product-service
├── rating-service
├── recommendation-service
├── review-service
├── search-service
├── seller-service
├── shipping-service
├── user-service
└── wishlist-service

frontend/

infrastructure/
├── argocd
├── docker
├── helm
├── kind
├── kubernetes
├── logging
├── monitoring
└── scripts
```

---

# Deployment Flow Summary

```
Launch EC2
        ↓
SSH into EC2
        ↓
Install Git
        ↓
Clone GitHub Repository
        ↓
Install Docker
        ↓
Install kubectl
        ↓
Install Kind
        ↓
Create Kubernetes Cluster
        ↓
Install Helm
        ↓
Deploy Base Kubernetes Resources
        ↓
Build Docker Images
        ↓
Load Images into Kind
        ↓
Install NGINX Ingress
        ↓
Install ArgoCD
        ↓
Deploy App of Apps
        ↓
ArgoCD Sync
        ↓
All Microservices Running
        ↓
Access Frontend
```

---

# Congratulations

You have successfully deployed the Amazon Clone project by following this workflow:

1. Created an AWS EC2 Ubuntu instance.
2. Connected via SSH.
3. Installed Git, Docker, kubectl, Kind, and Helm.
4. Cloned the GitHub repository.
5. Created a local Kubernetes cluster with Kind.
6. Built all service Docker images.
7. Loaded the images into the Kind cluster.
8. Installed the NGINX Ingress Controller.
9. Installed and configured ArgoCD.
10. Deployed all microservices using the App of Apps pattern.
11. Verified deployments, services, pods, and ingress.
12. Accessed the application and used ArgoCD for GitOps-based management.
