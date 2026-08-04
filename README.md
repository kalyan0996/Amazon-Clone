# Amazon Clone Deployment Guide (EC2 + Kind + Kubernetes + ArgoCD)

Deploy the **Amazon Clone Microservices Application** on an **AWS EC2** instance using **Docker**, **Kind**, **Kubernetes**, and **ArgoCD**.

---

# Architecture

* Frontend: React
* Backend: Django Microservices (20 Services)
* API Gateway
* Docker
* Kind Kubernetes Cluster
* ArgoCD (GitOps)
* NGINX Ingress

---

# Prerequisites

Before starting, ensure you have:

* AWS Account
* AWS CLI configured
* Git installed on your local machine
* SSH client

Verify AWS CLI:

```bash
aws --version
```

---

# Part A - Launch EC2 Instance (Run on Your Local Machine)

## Step 1 - Create a Key Pair

```bash
aws ec2 create-key-pair \
--key-name amazon-clone-key \
--query 'KeyMaterial' \
--output text > amazon-clone-key.pem

chmod 400 amazon-clone-key.pem
```

---

## Step 2 - Create Security Group

```bash
SG_ID=$(aws ec2 create-security-group \
--group-name amazon-clone-sg \
--description "Amazon Clone Deployment" \
--query GroupId \
--output text)

echo $SG_ID
```

---

## Step 3 - Open Required Ports

```bash
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 80 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 443 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 3000 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 8080 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 6443 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id $SG_ID --protocol tcp --port 30000-32767 --cidr 0.0.0.0/0
```

---

## Step 4 - Launch EC2 Instance

Replace the Ubuntu AMI with the latest Ubuntu 22.04 AMI available in your AWS region.

```bash
AMI_ID="ami-xxxxxxxxxxxxxxxx"

INSTANCE_ID=$(aws ec2 run-instances \
--image-id $AMI_ID \
--instance-type t3.large \
--key-name amazon-clone-key \
--security-group-ids $SG_ID \
--block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":30}}]' \
--query 'Instances[0].InstanceId' \
--output text)

echo $INSTANCE_ID
```

Wait until the instance is running.

```bash
aws ec2 wait instance-running --instance-ids $INSTANCE_ID
```

Get the public IP.

```bash
PUBLIC_IP=$(aws ec2 describe-instances \
--instance-ids $INSTANCE_ID \
--query 'Reservations[0].Instances[0].PublicIpAddress' \
--output text)

echo $PUBLIC_IP
```

SSH into the instance.

```bash
ssh -i amazon-clone-key.pem ubuntu@$PUBLIC_IP
```

---

# Part B - Deploy Application (Run on EC2)

---

## Step 1 - Update System

```bash
sudo apt update
sudo apt upgrade -y
```

---

## Step 2 - Install Git

```bash
sudo apt install git -y
```

Verify:

```bash
git --version
```

---

## Step 3 - Clone Repository

```bash
cd ~

git clone https://github.com/kalyan0996/Amazon-Clone.git

cd Amazon-Clone
```

---

## Step 4 - Install Docker

```bash
sudo apt remove docker docker-engine docker.io containerd runc -y || true

sudo apt install \
ca-certificates \
curl \
gnupg \
lsb-release \
-y

sudo mkdir -p /etc/apt/keyrings

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | \
sudo tee /etc/apt/sources.list.d/docker.list

sudo apt update

sudo apt install \
docker-ce \
docker-ce-cli \
containerd.io \
docker-buildx-plugin \
docker-compose-plugin \
-y

sudo systemctl enable docker

sudo systemctl start docker

sudo usermod -aG docker $USER

newgrp docker
```

Verify:

```bash
docker --version
```

---

## Step 5 - Configure Environment Files

```bash
cd ~/Amazon-Clone/backend

for d in */; do
service="${d%/}"

if [ -f "$service/.env.example" ]; then
cp "$service/.env.example" "$service/.env"
fi

done

cd ~/Amazon-Clone/frontend

cp .env.example .env || true
```

---

## Step 6 - Install kubectl

```bash
curl -LO \
"https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

chmod +x kubectl

sudo mv kubectl /usr/local/bin/
```

Verify:

```bash
kubectl version --client
```

---

## Step 7 - Install Kind

```bash
curl -Lo kind \
https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64

chmod +x kind

sudo mv kind /usr/local/bin/
```

Verify:

```bash
kind version
```

---

## Step 8 - Create Kind Cluster

```bash
cd ~/Amazon-Clone/infrastructure/kind

chmod +x create-cluster.sh

./create-cluster.sh
```

Verify:

```bash
kubectl get nodes
```

Expected:

```text
amazon-clone-control-plane
amazon-clone-worker
amazon-clone-worker2
```

---

## Step 9 - Install Helm

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

Verify:

```bash
helm version
```

---

## Step 10 - Deploy Base Kubernetes Resources

```bash
cd ~/Amazon-Clone/infrastructure/kubernetes/base

kubectl apply -f .
```

---

## Step 11 - Build Docker Images

```bash
cd ~/Amazon-Clone/scripts

chmod +x build.sh

./build.sh
```

Verify:

```bash
docker images | grep amazon
```

---

## Step 12 - Load Images into Kind

```bash
cd ~/Amazon-Clone/infrastructure/kind

chmod +x load-images.sh

./load-images.sh
```

Verify:

```bash
docker exec amazon-clone-control-plane crictl images | grep amazon-clone
```

---

## Step 13 - Install NGINX Ingress

```bash
kubectl apply \
-f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Wait until ready.

```bash
kubectl wait \
--namespace ingress-nginx \
--for=condition=Ready pod \
--selector=app.kubernetes.io/component=controller \
--timeout=300s
```

---

## Step 14 - Install ArgoCD

```bash
kubectl create namespace argocd

kubectl apply \
-n argocd \
-f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Wait for deployment.

```bash
kubectl rollout status \
deploy/argocd-server \
-n argocd \
--timeout=300s
```

---

## Step 15 - Deploy AppProject and App of Apps

```bash
cd ~/Amazon-Clone/infrastructure/argocd

kubectl apply -f app-project.yaml

kubectl apply -f app-of-apps.yaml
```

Verify:

```bash
kubectl get applications -n argocd
```

---

# Access ArgoCD

Get the initial admin password.

```bash
kubectl \
-n argocd \
get secret argocd-initial-admin-secret \
-o jsonpath="{.data.password}" | base64 -d

echo
```

Expose the ArgoCD UI.

```bash
kubectl port-forward \
svc/argocd-server \
-n argocd \
8080:443 \
--address 0.0.0.0
```

Open:

```text
https://<EC2_PUBLIC_IP>:8080
```

Username:

```text
admin
```

Password:

```text
<Output from previous command>
```

---

# Access Frontend

Run:

```bash
kubectl port-forward \
svc/frontend \
3000:3000 \
--address 0.0.0.0
```

Open:

```text
http://<EC2_PUBLIC_IP>:3000
```

---

# Verify Deployment

Check nodes.

```bash
kubectl get nodes
```

Check namespaces.

```bash
kubectl get ns
```

Check pods.

```bash
kubectl get pods -A
```

Check deployments.

```bash
kubectl get deploy -A
```

Check ReplicaSets.

```bash
kubectl get rs -A
```

Check services.

```bash
kubectl get svc -A
```

---

# Useful Commands

View all pods.

```bash
kubectl get pods -A
```

Describe pod.

```bash
kubectl describe pod <POD_NAME> -n amazon-clone
```

View logs.

```bash
kubectl logs <POD_NAME> -n amazon-clone
```

View previous logs.

```bash
kubectl logs <POD_NAME> -n amazon-clone --previous
```

Restart deployment.

```bash
kubectl rollout restart deployment <DEPLOYMENT_NAME> -n amazon-clone
```

Delete ReplicaSets.

```bash
kubectl delete rs --all -n amazon-clone
```

Reload ArgoCD.

```bash
kubectl annotate applications \
--all \
-n argocd \
argocd.argoproj.io/refresh=hard \
--overwrite
```

---

# Troubleshooting

## Build Script Not Found

```bash
find ~/Amazon-Clone -name build.sh
```

---

## ImagePullBackOff

Reload images.

```bash
cd ~/Amazon-Clone/infrastructure/kind

./load-images.sh
```

---

## Pods Pending

```bash
kubectl describe pod <POD_NAME> -n amazon-clone
```

Check available resources.

```bash
nproc

free -h
```

---

## ArgoCD Applications Unknown

```bash
kubectl describe application \
amazon-clone-app-of-apps \
-n argocd
```

---

## Port Already in Use

```bash
sudo ss -tlnp | grep 8080
```

Kill the process.

```bash
sudo kill -9 <PID>
```

---

# Project Repository

```text
https://github.com/kalyan0996/Amazon-Clone
```

---

# Author

**Kalyan**

GitHub: https://github.com/kalyan0996
