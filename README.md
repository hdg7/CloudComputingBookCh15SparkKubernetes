# Chapter 15 Spark on Kubernetes

This repository contains the Spark on Kubernetes tutorial mentioned in **Chapter 15** of the book:

[**Cloud Computing for Artificial Intelligence: Concepts, Methods, and Practical Tools**](https://amzn.eu/d/02lMPIKf)

# Spark on Kubernetes with Kind

This guide explains how to build a Spark image, create a Kubernetes cluster using **Kind**, and run a Spark job in **native Kubernetes mode**.

---

## **Prerequisites**
- **Docker** installed and running.
- **Kind** installed ([Kind documentation](https://kind.sigs.k8s.io/)).
- **kubectl** installed and configured.
- Spark job files (e.g., `linear_regression.py`) and Kubernetes manifests (`rbac.yaml`, `spark.job.yaml`).

---

## **Steps to Run Spark on Kubernetes**

### **1. Build the Spark Docker Image**
Create a Docker image that includes Spark and your application code:

```bash
sudo docker build -t spark-env .
```

This command:
- Uses the `Dockerfile` in your current directory.
- Tags the image as `spark-env`.

---

### **2. Create a Kind Cluster**
Use your custom Kind configuration file to create a cluster:

```bash
sudo kind create cluster --name mycluster --config kind.config.yaml
```

- `--name mycluster`: Names the cluster `mycluster`.
- `--config kind.config.yaml`: Uses your configuration file (e.g., specifying control-plane and worker nodes).

---

### **3. Load the Spark Image into the Kind Cluster**
Since Kind runs Kubernetes inside Docker, you need to load your local image into the cluster:

```bash
sudo kind load docker-image spark-env --name mycluster
```

This makes the `spark-env` image available to all nodes in the Kind cluster.

---

### **4. Apply RBAC Configuration**
Spark needs permissions to create executor pods. Apply the RBAC manifest:

```bash
sudo kubectl apply -f rbac.yaml
```

This creates:
- A `ServiceAccount` for Spark.
- A `RoleBinding` granting permissions to manage pods in the namespace.

---

### **5. Submit the Spark Job**
Apply the Kubernetes Job manifest that runs `spark-submit` inside the cluster:

```bash
sudo kubectl apply -f spark.job.yaml
```

This starts a Kubernetes Job that:
- Uses `spark-submit` with `--master k8s://...`.
- Deploys the Spark driver and executor pods.

---

### **6. Check Job Status**
Describe the Job to see its details and events:

```bash
sudo kubectl describe job spark-submit-job
```

---

### **7. View Driver Logs**
The output of your Spark application (e.g., `print()` statements) appears in the **driver pod logs**, not in the Job logs. Find the driver pod name and view its logs:

```bash
sudo kubectl logs linear-regression-c15a419af9612181-driver
```

> Replace `linear-regression-c15a419af9612181-driver` with the actual driver pod name.  
You can list pods with:
```bash
kubectl get pods -l spark-role=driver
```

---

### **8. Delete the Cluster**
When finished, delete the Kind cluster:

```bash
sudo kind delete cluster --name mycluster
```

---

## **Tips**
- To resubmit a job, delete the old Job and apply it again:
  ```bash
  kubectl delete job spark-submit-job
  kubectl apply -f spark.job.yaml
  ```
