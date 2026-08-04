# Amazon Clone — Complete Deployment Guide (AWS EC2 → Kubernetes → ArgoCD)

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
* t3.large (minimum) — t3.xlarge if you also want headroom for local Docker Compose testing
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

# Step 6 : Configure Environment Variables

Every backend service ships with an `.env.example`. Copy each to `.env` before building or deploying.

```
cd ~/Amazon-Clone/backend

for d in */; do
  service="${d%/}"
  if [ -f "$service/.env.example" ]; then
    cp "$service/.env.example" "$service/.env"
  fi
done
```

Edit each `.env` with real values (DB credentials, secret keys, service URLs):

```
nano auth-service/.env
```

Do the same for the frontend:

```
cd ~/Amazon-Clone/frontend

cp .env.example .env
```

Never commit real `.env` files to Git.

---

# Step 7 (Optional) : Sanity-Check Locally with Docker Compose

Before touching Kubernetes, confirm the app works with plain Docker Compose.

```
cd ~/Amazon-Clone

docker compose -f docker-compose.dev.yml up --build -d

docker compose -f docker-compose.dev.yml ps
```

Check logs for any service

```
docker compose -f docker-compose.dev.yml logs -f api-gateway
```

Tear it down once confirmed, so it doesn't compete with Kubernetes for resources

```
docker compose -f docker-compose.dev.yml down
```

---

# Step 8 : Install kubectl

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

# Step 9 : Install Kind

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

# Step 10 : Create Kubernetes Cluster

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

# Step 11 : Install Helm

```
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Verify

```
helm version
```

---

# Step 12 : Deploy Base Kubernetes Resources

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

# Step 13 : Build Docker Images

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

# Step 14 : Load Images into Kind

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

# Step 15 : Install NGINX Ingress

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

# Step 16 : Install ArgoCD

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

# Step 17 : Expose ArgoCD

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

If you're connecting from your local machine to the EC2 instance rather than a browser running on the server itself, add `--address 0.0.0.0` to the port-forward command and open `https://YOUR_PUBLIC_IP:8080` instead — just make sure port 8080 is allowed in the EC2 security group.

---

# Step 18 : Get ArgoCD Password

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

Login, then change the password:

```
argocd account update-password
```

---

# Step 19 : Deploy App of Apps

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

# Step 20 : Verify Pods

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

# Step 21 : Access the Frontend

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

# Step 22 : View Logs

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

# Step 23 : Restart Deployment

```
kubectl rollout restart deployment DEPLOYMENT_NAME
```

Example

```
kubectl rollout restart deployment auth-service
```

---

# Step 24 : Scaling

```
kubectl scale deployment auth-service --replicas=3
```

Verify

```
kubectl get pods
```

---

# Step 25 (Optional) : Enable Monitoring

The repo ships Prometheus, Alertmanager, Loki, and Tempo configs.

Quick local check via Docker Compose:

```
cd ~/Amazon-Clone

docker compose -f docker-compose.monitoring.yml up -d
```

In-cluster, apply configs under `infrastructure/monitoring/` and `infrastructure/logging/` using whichever Helm chart your team standardizes on (e.g. `kube-prometheus-stack`), pointing at:

```
infrastructure/monitoring/prometheus.yml
infrastructure/monitoring/alertmanager.yml
infrastructure/monitoring/tempo.yml
infrastructure/logging/loki-config.yml
infrastructure/logging/promtail-config.yml
```

---

# Step 26 : Delete Cluster

```
cd ~/Amazon-Clone/infrastructure/kind

./delete-cluster.sh
```

---

# Troubleshooting

Pods stuck in `Pending`

```
kubectl describe pod POD_NAME -n NAMESPACE
```

`ImagePullBackOff` — image not loaded into Kind

```
cd ~/Amazon-Clone/infrastructure/kind

./load-images.sh
```

ArgoCD app stuck `OutOfSync`

```
argocd app diff APP_NAME
```

Can't reach the ArgoCD UI — confirm port 8080 is open in the EC2 security group, and that the `port-forward` process is still running. Use `screen` or `tmux` so it survives your SSH session ending:

```
screen -S argocd

kubectl port-forward svc/argocd-server -n argocd 8080:443 --address 0.0.0.0
```

(Press `Ctrl+A` then `D` to detach without killing it.)

Django migrations failing — check `.env` values for the affected service, especially database host/credentials.

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
Configure .env files
        ↓
(Optional) Sanity-check with Docker Compose
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
3. Installed Git, configured environment variables, and optionally sanity-checked with Docker Compose.
4. Installed Docker, kubectl, Kind, and Helm.
5. Cloned the GitHub repository.
6. Created a local Kubernetes cluster with Kind.
7. Built all service Docker images.
8. Loaded the images into the Kind cluster.
9. Installed the NGINX Ingress Controller.
10. Installed and configured ArgoCD.
11. Deployed all microservices using the App of Apps pattern.
12. Verified deployments, services, pods, and ingress.
13. Accessed the application and used ArgoCD for GitOps-based management.
