# Amazon Clone — Complete Deployment Guide
### AWS EC2 → Docker → Kind Kubernetes → ArgoCD

One-file, copy-paste version. Follow top to bottom on a fresh Ubuntu 22.04 EC2 instance.

---

## Architecture

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

## Prerequisites

- AWS Account
- GitHub Account
- Domain (optional)

---

## Step 1 — Launch EC2 Instance

- AMI: **Ubuntu Server 22.04 LTS**
- Instance type: **t3.large** (t3.xlarge if you also want headroom for local Docker Compose testing)
- Storage: **30 GB**
- Security Group — allow inbound:
  - `22` SSH
  - `80` HTTP
  - `443` HTTPS
  - `30000-32767` NodePort
  - `6443` Kubernetes API
  - `3000` (frontend port-forward, optional)
  - `8080` (ArgoCD port-forward, optional)

Download the PEM key, then launch.

---

## Step 2 — Connect to EC2

From Linux/Mac:

```bash
chmod 400 amazon.pem
ssh -i amazon.pem ubuntu@YOUR_PUBLIC_IP
```

From Windows PowerShell:

```powershell
cd Downloads
ssh -i "amazon.pem" ubuntu@YOUR_PUBLIC_IP
```

Update the system:

```bash
sudo apt update
sudo apt upgrade -y
```

---

## Step 3 — Install Git

```bash
sudo apt install git -y
git --version
```

---

## Step 4 — Clone the Repository

```bash
cd ~
git clone https://github.com/kalyan0996/Amazon-Clone.git
cd Amazon-Clone
ls
```

Expected:

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

## Step 5 — Install Docker

Remove any old Docker packages:

```bash
sudo apt remove docker docker-engine docker.io containerd runc -y
```

Install dependencies:

```bash
sudo apt install ca-certificates curl gnupg lsb-release -y
```

Add Docker's GPG key:

```bash
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

Add the Docker repository:

```bash
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

Install Docker:

```bash
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
```

Enable and start Docker:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

Add your user to the docker group:

```bash
sudo usermod -aG docker $USER
```

Log out and reconnect for the group change to take effect:

```bash
exit
ssh -i amazon.pem ubuntu@YOUR_PUBLIC_IP
```

(Alternatively, run `newgrp docker` instead of reconnecting.)

Verify:

```bash
docker version
docker ps
```

---

## Step 6 — Configure Environment Files

Every backend service ships with a `.env.example`. Copy each one to `.env`:

```bash
cd ~/Amazon-Clone/backend

for d in */; do
  service="${d%/}"
  if [ -f "$service/.env.example" ]; then
    cp "$service/.env.example" "$service/.env"
  fi
done
```

Edit each `.env` with real values (DB credentials, secret keys, service URLs) as needed, e.g.:

```bash
nano auth-service/.env
```

Frontend:

```bash
cd ~/Amazon-Clone/frontend
cp .env.example .env
```

If `.env.example` doesn't exist for the frontend, create `.env.local` manually:

```bash
nano frontend/.env.local
```

```env
NEXT_PUBLIC_API_GATEWAY_URL=http://localhost:8000
```

> Never commit real `.env` files to Git.

---

## Step 7 (Optional) — Sanity-Check Locally with Docker Compose

Before touching Kubernetes, confirm the app works with plain Docker Compose.

```bash
cd ~/Amazon-Clone
docker compose -f docker-compose.dev.yml up --build -d
docker compose -f docker-compose.dev.yml ps
```

Check logs for any service:

```bash
docker compose -f docker-compose.dev.yml logs -f api-gateway
```

Tear it down once confirmed, so it doesn't compete with Kubernetes for resources:

```bash
docker compose -f docker-compose.dev.yml down
```

---

## Step 8 — Install kubectl

```bash
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/
kubectl version --client
```

---

## Step 9 — Install Kind

```bash
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x kind
sudo mv kind /usr/local/bin/
kind version
```

---

## Step 10 — Create the Kubernetes Cluster

```bash
cd ~/Amazon-Clone/infrastructure/kind
chmod +x create-cluster.sh
./create-cluster.sh
kubectl get nodes
```

Expected (naming may vary by cluster config):

```
amazon-clone-control-plane
amazon-clone-worker
amazon-clone-worker2
```

---

## Step 11 — Install Helm

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
helm version
```

---

## Step 12 — Deploy Base Kubernetes Resources

```bash
cd ~/Amazon-Clone/infrastructure/kubernetes/base
kubectl apply -f .
kubectl get ns
kubectl get pv
kubectl get pvc
```

Expected namespaces:

```
amazon-clone
default
kube-system
local-path-storage
```

---

## Step 13 — Build Docker Images

```bash
cd ~/Amazon-Clone/scripts
chmod +x build.sh
./build.sh
```

> If your repo layout has the script under `infrastructure/scripts` instead, `cd` there instead — see **Troubleshooting → Problem 2**.

If the build fails with an "invalid tag" error, the script is looking in the wrong backend directory — see **Troubleshooting → Problem 3** below to fix `build.sh`, then rerun.

Verify:

```bash
docker images
```

Expected images include:

```
amazon-clone/admin-service
amazon-clone/analytics-service
amazon-clone/api-gateway
amazon-clone/auth-service
amazon-clone/cart-service
amazon-clone/catalog-service
amazon-clone/inventory-service
amazon-clone/notification-service
amazon-clone/order-service
amazon-clone/payment-service
amazon-clone/pricing-service
amazon-clone/product-service
amazon-clone/rating-service
amazon-clone/recommendation-service
amazon-clone/review-service
amazon-clone/search-service
amazon-clone/seller-service
amazon-clone/shipping-service
amazon-clone/user-service
amazon-clone/wishlist-service
amazon-clone/frontend
```

---

## Step 14 — Load Images into Kind

```bash
cd ~/Amazon-Clone/infrastructure/kind
chmod +x load-images.sh
./load-images.sh
```

Verify:

```bash
docker exec -it amazon-clone-control-plane ctr -n k8s.io images ls
```

---

## Step 15 — Install NGINX Ingress

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
```

Wait for it to be ready:

```bash
kubectl wait \
  --namespace ingress-nginx \
  --for=condition=Ready \
  pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=300s
```

Verify:

```bash
kubectl get pods -n ingress-nginx
```

---

## Step 16 — Install ArgoCD

```bash
kubectl create namespace argocd

kubectl apply -n argocd \
  -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

Wait until all pods are `Running`:

```bash
kubectl get pods -n argocd
```

Expected:

```
argocd-server
argocd-repo-server
argocd-application-controller
argocd-dex-server
argocd-redis
```

---

## Step 17 — Expose ArgoCD

If port 8080 is free:

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443 --address 0.0.0.0
```

Open:

```
https://YOUR_PUBLIC_IP:8080
```

(Ignore the browser certificate warning.) Make sure port 8080 is allowed in the EC2 security group.

Run it inside `screen` or `tmux` so it survives your SSH session ending:

```bash
screen -S argocd
kubectl port-forward svc/argocd-server -n argocd 8080:443 --address 0.0.0.0
```

Press `Ctrl+A` then `D` to detach without killing it.

**If port 8080 is busy:**

```bash
sudo ss -tlnp | grep 8080
sudo kill -9 <PID>
```

Or just use a different local port:

```bash
kubectl port-forward svc/argocd-server -n argocd 9090:443 --address 0.0.0.0
```

Then open `https://YOUR_PUBLIC_IP:9090`.

---

## Step 18 — Get the ArgoCD Password

Username:

```
admin
```

Password:

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d
echo
```

Log in, then change the password:

```bash
argocd account update-password
```

---

## Step 19 — Deploy AppProject and App of Apps

```bash
cd ~/Amazon-Clone/infrastructure/argocd
kubectl apply -f app-project.yaml
kubectl apply -f app-of-apps.yaml
kubectl get applications -n argocd
```

You should see applications for all services, e.g.:

```
admin-service        analytics-service     api-gateway
auth-service          cart-service          catalog-service
inventory-service     notification-service  order-service
payment-service       pricing-service       product-service
rating-service        recommendation-service review-service
search-service        seller-service        shipping-service
user-service          wishlist-service
```

---

## Step 20 — Fix Common ArgoCD Manifest Issues

### Fix AppProject destination

If applications get stuck due to an invalid destination:

```bash
nano infrastructure/argocd/app-project.yaml
```

Replace:

```yaml
destinations:
  - namespace: amazon-clone
    server: https://kubernetes.default.svc
```

with:

```yaml
destinations:
  - namespace: "*"
    server: https://kubernetes.default.svc
```

Apply:

```bash
kubectl apply -f infrastructure/argocd/app-project.yaml
```

### Fix repoURL

Search for a placeholder repo URL:

```bash
grep -R "https://example.com/amazon-clone.git" infrastructure/argocd
```

Replace it everywhere:

```bash
find infrastructure/argocd \
  -type f -name "*.yaml" \
  -exec sed -i 's|https://example.com/amazon-clone.git|https://github.com/kalyan0996/Amazon-Clone.git|g' {} \;
```

Verify (no output means success):

```bash
grep -R "example.com" infrastructure/argocd
```

### Push the fix to GitHub

```bash
git add infrastructure/argocd
git commit -m "Fix ArgoCD manifests"
git push origin main
```

### Recreate and refresh applications

```bash
kubectl delete applications --all -n argocd

kubectl apply -f infrastructure/argocd/app-project.yaml
kubectl apply -f infrastructure/argocd/app-of-apps.yaml

kubectl annotate application amazon-clone-app-of-apps \
  -n argocd \
  argocd.argoproj.io/refresh=hard \
  --overwrite

kubectl rollout restart statefulset argocd-application-controller -n argocd
```

Verify all applications show `Synced` / `Healthy`:

```bash
kubectl get applications -n argocd
```

---

## Step 21 — Verify the Deployment

```bash
kubectl get pods -A
kubectl get svc -A
kubectl get deployments -A
```

Check a specific service's image and pull policy:

```bash
kubectl get deployment auth-service -n amazon-clone -o yaml | grep imagePullPolicy
```

Expected: `IfNotPresent`

Restart a deployment if needed:

```bash
kubectl rollout restart deployment auth-service -n amazon-clone
```

Watch pods come up:

```bash
kubectl get pods -n amazon-clone -w
```

---

## Step 22 — Access the Frontend

Port-forward:

```bash
kubectl port-forward svc/frontend 3000:3000
```

Open:

```
http://localhost:3000
```

(Or `http://YOUR_PUBLIC_IP:3000` if forwarding with `--address 0.0.0.0` from a remote machine.)

If exposed via Ingress instead, browse to your configured host or the EC2 public IP.

---

## Step 23 — Logs, Scaling, and Cleanup

View logs:

```bash
kubectl logs POD_NAME -n amazon-clone
kubectl logs POD_NAME -n amazon-clone --previous   # crash logs
kubectl logs -f POD_NAME -n amazon-clone           # follow
```

Describe a pod:

```bash
kubectl describe pod POD_NAME -n amazon-clone
```

Rollout status / ReplicaSets:

```bash
kubectl rollout status deployment auth-service -n amazon-clone
kubectl get rs -n amazon-clone
```

Scale:

```bash
kubectl scale deployment auth-service --replicas=3 -n amazon-clone
# or scale everything down to 1 replica if resources are tight
kubectl scale deployment --all --replicas=1 -n amazon-clone
```

Check node resources:

```bash
kubectl get nodes
kubectl describe nodes
kubectl top nodes
nproc
free -h
```

Delete the cluster entirely:

```bash
cd ~/Amazon-Clone/infrastructure/kind
./delete-cluster.sh
```

---

## Step 24 (Optional) — Monitoring & Logging

The repo ships Prometheus, Alertmanager, Loki, and Tempo configs.

Quick local check via Docker Compose:

```bash
cd ~/Amazon-Clone
docker compose -f docker-compose.monitoring.yml up -d
```

In-cluster, apply the configs under `infrastructure/monitoring/` and `infrastructure/logging/` using whichever Helm chart your team standardizes on (e.g. `kube-prometheus-stack`), pointing at:

```
infrastructure/monitoring/prometheus.yml
infrastructure/monitoring/alertmanager.yml
infrastructure/monitoring/tempo.yml
infrastructure/logging/loki-config.yml
infrastructure/logging/promtail-config.yml
```

---

## Troubleshooting

### Problem 1 — SSH connection closed immediately

**Fix:** Check the EC2 Security Group inbound rule for port 22 (source = your IP), and confirm the SSH service is running:

```bash
sudo systemctl status ssh
```

### Problem 2 — Wrong build script path

**Error:**

```
cd ~/Amazon-Clone/infrastructure/scripts
No such file or directory
```

**Fix:** Locate the script and `cd` to wherever it actually is:

```bash
find ~/Amazon-Clone -name build.sh
cd ~/Amazon-Clone/scripts   # or wherever it was found
```

### Problem 3 — Invalid Docker tag / build.sh points at the wrong directory

**Error:**

```
invalid tag amazon-clone/*:latest
```

**Cause:** `build.sh` is looking at `backend/*/` instead of `../backend/*/` (relative path is wrong depending on where the script lives).

**Fix:**

```bash
nano scripts/build.sh
```

Correct version:

```bash
#!/usr/bin/env bash
set -euo pipefail

for svc_dir in ../backend/*/
do
    svc=$(basename "$svc_dir")
    echo "Building image amazon-clone/$svc..."
    docker build -t amazon-clone/$svc:latest "$svc_dir"
done

docker build -t amazon-clone/frontend:latest ../frontend
```

Save (`CTRL+O`, `Enter`, `CTRL+X`), then:

```bash
chmod +x build.sh
./build.sh
```

### Problem 4 — npm not found

```bash
sudo apt update
sudo apt install nodejs npm -y
node -v
npm -v
```

### Problem 5 — Next.js build failed

```bash
cat frontend/next.config.js
```

Should contain at least:

```javascript
const nextConfig = {
  reactStrictMode: true,
  output: "standalone",
};
```

Make sure the env var is set:

```bash
nano frontend/.env.local
```

```env
NEXT_PUBLIC_API_GATEWAY_URL=http://localhost:8000
```

### Problem 6 — Dockerfile fails on `COPY public` (not found)

```bash
cd ~/Amazon-Clone/frontend
mkdir -p public
```

Rebuild:

```bash
cd ~/Amazon-Clone
docker build \
  --build-arg NEXT_PUBLIC_API_GATEWAY_URL=http://localhost:8000 \
  -t amazon-clone/frontend:latest \
  frontend
```

### Problem 7 — Port already in use (e.g. ArgoCD 8080)

```bash
sudo ss -tlnp | grep 8080
sudo kill -9 <PID>
```

Or use a different port:

```bash
kubectl port-forward svc/argocd-server -n argocd 9090:443 --address 0.0.0.0
```

### Problem 8 — ArgoCD application shows "Unknown / Unknown"

```bash
kubectl describe application amazon-clone-app-of-apps -n argocd
```

### Problem 9 — Invalid destination / repoURL wrong

See **Step 20 — Fix Common ArgoCD Manifest Issues** above (AppProject destination + repoURL fix + push + recreate + refresh).

### Problem 10 — ImagePullBackOff / ErrImagePull

```bash
kubectl describe pod POD_NAME -n amazon-clone
```

Look for `ErrImagePull` / `ImagePullBackOff` in the events, then confirm the image is loaded into Kind:

```bash
docker exec -it amazon-clone-control-plane ctr -n k8s.io images ls | grep auth-service
```

If missing, reload:

```bash
cd ~/Amazon-Clone/infrastructure/kind
./load-images.sh
kubectl rollout restart deployment auth-service -n amazon-clone
```

### Problem 11 — imagePullPolicy is "Always" instead of "IfNotPresent"

```bash
kubectl get deployment auth-service -n amazon-clone -o yaml | grep imagePullPolicy
```

Should read `IfNotPresent` (needed since Kind has no registry). Fix in the manifest/Helm values, push, then force an ArgoCD refresh:

```bash
kubectl annotate application amazon-clone-app-of-apps \
  -n argocd \
  argocd.argoproj.io/refresh=hard \
  --overwrite
```

### Problem 12 — CrashLoopBackOff

```bash
kubectl logs POD_NAME -n amazon-clone --previous
kubectl logs POD_NAME -n amazon-clone
```

### Problem 13 — Pods stuck Pending (e.g. insufficient CPU)

```bash
kubectl describe pod POD_NAME -n amazon-clone
kubectl describe nodes
nproc
free -h
```

Scale down if the node is under-resourced:

```bash
kubectl scale deployment --all --replicas=1 -n amazon-clone
```

### Problem 14 — Django/service migrations failing

Check the affected service's `.env` values, especially database host/credentials.

### Problem 15 — Can't reach the ArgoCD UI

Confirm port 8080 (or your chosen port) is open in the EC2 security group and that the `port-forward` process is still running — run it inside `screen`/`tmux` (see Step 17).

---

## Useful Commands Cheat Sheet

**Docker**

```bash
docker ps
docker ps -a
docker images
docker rm CONTAINER_ID
docker rmi IMAGE_ID
docker system prune -a
```

**Kubernetes**

```bash
kubectl get nodes
kubectl get ns
kubectl get pods -A
kubectl get svc -A
kubectl get deployments -A
kubectl get rs -A
kubectl get ingress -A
kubectl get pv
kubectl get pvc
kubectl logs POD_NAME
kubectl delete pod POD_NAME
kubectl rollout restart deployment DEPLOYMENT_NAME
kubectl scale deployment DEPLOYMENT_NAME --replicas=1
```

**ArgoCD**

```bash
kubectl get applications -n argocd
kubectl describe application APP_NAME -n argocd
argocd app diff APP_NAME
```

**Git**

```bash
git clone https://github.com/kalyan0996/Amazon-Clone.git
git status
git pull
git add .
git commit -m "message"
git push origin main
git branch
git log
```

---

## Deployment Flow Summary

```
Launch EC2
    │
    ▼
SSH into EC2
    │
    ▼
Install Git
    │
    ▼
Clone GitHub Repository
    │
    ▼
Install Docker
    │
    ▼
Configure .env files
    │
    ▼
(Optional) Sanity-check with Docker Compose
    │
    ▼
Install kubectl
    │
    ▼
Install Kind
    │
    ▼
Create Kubernetes Cluster
    │
    ▼
Install Helm
    │
    ▼
Deploy Base Kubernetes Resources
    │
    ▼
Build Docker Images
    │
    ▼
Load Images into Kind
    │
    ▼
Install NGINX Ingress
    │
    ▼
Install ArgoCD
    │
    ▼
Deploy AppProject + App of Apps
    │
    ▼
Push Changes to GitHub
    │
    ▼
ArgoCD Auto Sync
    │
    ▼
All Microservices Running
    │
    ▼
Verify Pods / Services / Deployments
    │
    ▼
Access Frontend
```

---

## Project Structure

```
Amazon-Clone/
├── backend/
│   ├── admin-service
│   ├── analytics-service
│   ├── api-gateway
│   ├── auth-service
│   ├── cart-service
│   ├── catalog-service
│   ├── inventory-service
│   ├── notification-service
│   ├── order-service
│   ├── payment-service
│   ├── pricing-service
│   ├── product-service
│   ├── rating-service
│   ├── recommendation-service
│   ├── review-service
│   ├── search-service
│   ├── seller-service
│   ├── shipping-service
│   ├── user-service
│   └── wishlist-service
│
├── frontend/
│
├── infrastructure/
│   ├── argocd
│   ├── docker
│   ├── helm
│   ├── kind
│   ├── kubernetes
│   ├── logging
│   └── monitoring
│
└── scripts/
```

---

## Author

**Kalyan** — [github.com/kalyan0996](https://github.com/kalyan0996)

## License

This project is intended for educational and learning purposes.
