# Amazon Clone — Deployment (EC2 → Kubernetes → ArgoCD)

Copy-paste commands to go from **no EC2 instance** to a **running app**.

- **Part A** — run locally (needs AWS CLI configured). Creates the EC2 instance and SSHes in.
- **Part B** — run on the EC2 instance. Installs everything and deploys the app.

If you already have a running EC2 instance, skip straight to Part B.

---

## Part A — Launch EC2 (run locally)

```bash
# 1. Create a key pair (skip if you already have one)
aws ec2 create-key-pair --key-name amazon-clone-key \
  --query 'KeyMaterial' --output text > amazon-clone-key.pem
chmod 400 amazon-clone-key.pem

# 2. Create a security group
SG_ID=$(aws ec2 create-security-group \
  --group-name amazon-clone-sg \
  --description "Amazon Clone deployment" \
  --query 'GroupId' --output text)

# 3. Open required ports
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 22   --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 80   --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 443  --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 3000 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 8080 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 6443 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id "$SG_ID" --protocol tcp --port 30000-32767 --cidr 0.0.0.0/0

# 4. Launch the instance (Ubuntu 22.04 LTS, t3.large, 30GB)
# Replace AMI_ID with the current Ubuntu 22.04 AMI for your region:
# https://cloud-images.ubuntu.com/locator/ec2/
AMI_ID="ami-0XXXXXXXXXXXXXXXX"

INSTANCE_ID=$(aws ec2 run-instances \
  --image-id "$AMI_ID" \
  --instance-type t3.large \
  --key-name amazon-clone-key \
  --security-group-ids "$SG_ID" \
  --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":30}}]' \
  --query 'Instances[0].InstanceId' --output text)

echo "Waiting for instance to be running..."
aws ec2 wait instance-running --instance-ids "$INSTANCE_ID"

PUBLIC_IP=$(aws ec2 describe-instances --instance-ids "$INSTANCE_ID" \
  --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)

echo "Instance ready: $INSTANCE_ID @ $PUBLIC_IP"

# 5. SSH in
ssh -i amazon-clone-key.pem ubuntu@"$PUBLIC_IP"
```

---

## Part B — Deploy the app (run on the EC2 instance)

```bash
set -euo pipefail

# --- System update ---
sudo apt update && sudo apt upgrade -y

# --- Git ---
sudo apt install git -y

# --- Clone repo ---
cd ~
git clone https://github.com/kalyan0996/Amazon-Clone.git
cd Amazon-Clone

# --- Docker ---
sudo apt remove docker docker-engine docker.io containerd runc -y || true
sudo apt install ca-certificates curl gnupg lsb-release -y
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
  sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
"deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker "$USER"
newgrp docker

# --- Configure .env files ---
cd ~/Amazon-Clone/backend
for d in */; do
  service="${d%/}"
  if [ -f "$service/.env.example" ]; then
    cp "$service/.env.example" "$service/.env"
  fi
done
cd ~/Amazon-Clone/frontend
[ -f .env.example ] && cp .env.example .env || true

# --- kubectl ---
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

# --- Kind ---
curl -Lo ./kind https://kind.sigs.k8s.io/dl/latest/kind-linux-amd64
chmod +x kind
sudo mv kind /usr/local/bin/

# --- Create Kind cluster ---
cd ~/Amazon-Clone/infrastructure/kind
chmod +x create-cluster.sh
./create-cluster.sh
kubectl get nodes

# --- Helm ---
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash

# --- Base Kubernetes resources ---
cd ~/Amazon-Clone/infrastructure/kubernetes/base
kubectl apply -f .

# --- Build all Docker images ---
cd ~/Amazon-Clone/scripts
chmod +x build.sh
./build.sh
docker images

# --- Load images into Kind ---
cd ~/Amazon-Clone/infrastructure/kind
chmod +x load-images.sh
./load-images.sh

# --- NGINX Ingress ---
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/kind/deploy.yaml
kubectl wait --namespace ingress-nginx \
  --for=condition=Ready pod \
  --selector=app.kubernetes.io/component=controller \
  --timeout=300s

# --- ArgoCD ---
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
kubectl -n argocd rollout status deploy/argocd-server --timeout=300s

# --- Deploy AppProject + App of Apps ---
cd ~/Amazon-Clone/infrastructure/argocd
kubectl apply -f app-project.yaml
kubectl apply -f app-of-apps.yaml
kubectl get applications -n argocd
```

---

## Final Steps (manual)

**1. Get the ArgoCD admin password:**

```bash
kubectl -n argocd get secret argocd-initial-admin-secret \
  -o jsonpath="{.data.password}" | base64 -d; echo
```

**2. Expose the ArgoCD UI** (run in `screen`/`tmux` so it survives logout):

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443 --address 0.0.0.0
```

Open `https://<EC2_PUBLIC_IP>:8080` — username `admin`.

**3. Once ArgoCD shows all apps `Synced` / `Healthy`, access the frontend:**

```bash
kubectl port-forward svc/frontend 3000:3000 --address 0.0.0.0
```

Open `http://<EC2_PUBLIC_IP>:3000`.

---

## Troubleshooting Quick Reference

| Problem | Fix |
|---|---|
| Build script not found | `find ~/Amazon-Clone -name build.sh` and `cd` there |
| Invalid Docker tag | Ensure `build.sh` uses `../backend/*/` not `backend/*/` |
| ImagePullBackOff | `cd ~/Amazon-Clone/infrastructure/kind && ./load-images.sh` |
| ArgoCD app stuck `Unknown` | `kubectl describe application amazon-clone-app-of-apps -n argocd` |
| repoURL / destination errors | Fix `infrastructure/argocd/app-project.yaml`, push, `kubectl apply`, hard-refresh app |
| Port 8080 busy | `sudo ss -tlnp \| grep 8080` then `sudo kill -9 <PID>`, or forward to `9090` instead |
| Pods stuck Pending | `kubectl describe pod POD -n amazon-clone`; check `nproc` / `free -h`; scale replicas down |

---

## Author

**Kalyan** — [github.com/kalyan0996](https://github.com/kalyan0996)
