

## **1: Introduction to Kubernetes**

### **1. What is Kubernetes?**

- **Definition:**
  - Kubernetes, often abbreviated as **K8s**, is an open-source platform designed for automating deployment, scaling, and management of containerized applications.
- **Origin:**
  - Developed by Google and donated to the **Cloud Native Computing Foundation (CNCF)** in 2015.
- **Purpose:**
  - Orchestrate containers across multiple hosts.
  - Simplify the management of complex applications.

### **2. The Need for Container Orchestration**

- **Challenges with Containers:**
  - Managing numerous containers across multiple environments.
  - Handling load balancing, scaling, and networking.
  - Ensuring high availability and fault tolerance.
- **Solution:**
  - **Container Orchestration Tools** automate the deployment, scaling, networking, and management of containers.
- **Evolution:**
  - Early tools: **Docker Swarm**, **Apache Mesos**.
  - Kubernetes emerged as a leading orchestration platform due to its robust feature set and community support.

### **3. Key Benefits of Kubernetes**

- **Automated Rollouts and Rollbacks:**
  - Manage updates and rollbacks efficiently.
- **Service Discovery and Load Balancing:**
  - Automatically exposes containers using DNS names or IP addresses.
- **Self-Healing:**
  - Restarts failed containers, replaces containers, kills containers that don't respond.
- **Secret and Configuration Management:**
  - Deploy and update secrets and application configuration without rebuilding your image.
- **Storage Orchestration:**
  - Mount storage systems like local storage, public cloud providers, and network storage systems.

### **4. Use Cases**

- **Microservices Architecture:**
  - Efficiently manage microservices deployments.
- **Continuous Deployment and Integration:**
  - Integrate with CI/CD pipelines for automated testing and deployment.
- **Hybrid and Multi-Cloud Deployments:**
  - Deploy applications across on-premises and multiple cloud providers.
- **Big Data and Machine Learning:**
  - Run scalable data processing and ML workloads.

---

## **2: Kubernetes Architecture and Key Concepts**

### **1. Kubernetes Architecture Overview**

- **Master (Control Plane):**
  - **API Server:** Exposes the Kubernetes API.
  - **Etcd:** Key-value store for cluster data.
  - **Scheduler:** Assigns workloads to nodes.
  - **Controller Manager:** Manages controllers that regulate the state of the cluster.
- **Nodes (Worker Machines):**
  - **Kubelet:** Agent that runs on each node, communicates with the API server.
  - **Container Runtime:** Software like Docker or containerd that runs containers.
  - **Kube-Proxy:** Network proxy that runs on each node, maintains network rules.

#### **Diagram:**

*Include a diagram showing the interaction between the Master and Nodes, highlighting components like API Server, etcd, Kubelet, and Pods.*

### **2. Key Concepts and Objects**

#### **a. Pods**

- **Definition:**
  - The smallest and simplest unit in the Kubernetes object model.
- **Characteristics:**
  - Represents a single instance of a running process.
  - Can contain one or more containers that share storage and network resources.

#### **b. Services**

- **Definition:**
  - An abstraction that defines a logical set of Pods and a policy by which to access them.
- **Purpose:**
  - Enables loose coupling between dependent Pods.
  - Types of Services:
  - **ClusterIP:** Exposes the service on a cluster-internal IP.
  - **NodePort:** Exposes the service on each Node's IP at a static port.
  - **LoadBalancer:** Exposes the service externally using a cloud provider's load balancer.

#### **c. Deployments**

- **Definition:**
  - Manages stateless applications.
- **Purpose:**
  - Declaratively updates Pods and ReplicaSets.
  - Provides rollout and rollback capabilities.

#### **d. ReplicaSets**

- **Definition:**
  - Ensures a specified number of Pod replicas are running at any given time.
- **Purpose:**
  - Provides high availability by maintaining desired Pod counts.

#### **e. ConfigMaps and Secrets**

- **ConfigMaps:**
  - Stores configuration data in key-value pairs.
- **Secrets:**
  - Similar to ConfigMaps but intended to hold sensitive information.

#### **f. Volumes**

- **Definition:**
  - A directory accessible to containers in a Pod.
- **Types:**
  - **emptyDir, hostPath, nfs, persistentVolumeClaim**, etc.
- **Purpose:**
  - Persist data beyond the life of a Pod.

### **3. Kubernetes Objects and Manifests**

- **YAML Manifests:**
  - Declarative configuration files defining the desired state.
- **kubectl Command-Line Tool:**
  - Interacts with the Kubernetes API server.
  - **Common Commands:**
    - `kubectl apply -f <file.yaml>`
    - `kubectl get pods`
    - `kubectl describe service <service-name>`
    - `kubectl logs <pod-name>`

---

## **3: Working with Kubernetes – Basic Commands and Workflow**

### **1. Setting Up Kubernetes**

#### **a. Local Development**

- **Minikube:**
  - Runs a single-node Kubernetes cluster on your local machine.
  - **Installation:**
    - Download from [minikube.sigs.k8s.io](https://minikube.sigs.k8s.io/docs/start/)
  - **Start Cluster:**
    ```bash
    minikube start
    ```

#### **b. Managed Kubernetes Services**

- **Cloud Providers:**
  - **Google Kubernetes Engine (GKE)**
  - **Amazon Elastic Kubernetes Service (EKS)**
  - **Azure Kubernetes Service (AKS)**
- **Benefits:**
  - Simplify cluster setup and management.
  - Integrated with other cloud services.

### **2. Deploying Applications**

#### **a. Creating a Deployment**

- **Example Deployment YAML:**
  ```yaml
  apiVersion: apps/v1
  kind: Deployment
  metadata:
    name: nginx-deployment
  spec:
    replicas: 3
    selector:
      matchLabels:
        app: nginx
    template:
      metadata:
        labels:
          app: nginx
      spec:
        containers:
        - name: nginx
          image: nginx:1.14.2
          ports:
          - containerPort: 80
  ```
- **Apply Deployment:**
  ```bash
  kubectl apply -f deployment.yaml
  ```

#### **b. Exposing the Deployment as a Service**

- **Create a Service:**
  ```bash
  kubectl expose deployment nginx-deployment --type=LoadBalancer --name=nginx-service
  ```
- **Verify Service:**
  ```bash
  kubectl get services
  ```

### **3. Scaling and Updating Applications**

#### **a. Scaling Deployments**

- **Scale Command:**
  ```bash
  kubectl scale deployment nginx-deployment --replicas=5
  ```
- **Verify Pods:**
  ```bash
  kubectl get pods
  ```

#### **b. Rolling Updates**

- **Update Image Version:**
  ```bash
  kubectl set image deployment/nginx-deployment nginx=nginx:1.16.0
  ```
- **Monitor Update:**
  ```bash
  kubectl rollout status deployment/nginx-deployment
  ```
- **Rollback if Needed:**
  ```bash
  kubectl rollout undo deployment/nginx-deployment
  ```

### **4. Advanced Features (Brief Overview)**

#### **a. ConfigMaps and Secrets**

- **Create a ConfigMap:**
  ```bash
  kubectl create configmap app-config --from-literal=APP_COLOR=blue
  ```
- **Use in Pod Spec:**
  ```yaml
  env:
    - name: APP_COLOR
      valueFrom:
        configMapKeyRef:
          name: app-config
          key: APP_COLOR
  ```

#### **b. StatefulSets**

- **Purpose:**
  - Manage stateful applications.
- **Features:**
  - Stable, unique network identifiers.
  - Persistent storage.

#### **c. Persistent Volumes and Persistent Volume Claims**

- **PersistentVolume (PV):**
  - Represents a piece of storage in the cluster.
- **PersistentVolumeClaim (PVC):**
  - Request for storage by a user.
- **Usage:**
  - Decouple storage provisioning from Pod lifecycle.

#### **d. Ingress Controllers**

- **Purpose:**
  - Manage external access to services in a cluster, typically HTTP.
- **Features:**
  - Load balancing, SSL termination, name-based virtual hosting.

### **5. Monitoring and Logging**

#### **a. Built-in Commands**

- **View Logs:**
  ```bash
  kubectl logs <pod-name>
  ```
- **Execute Commands in Pods:**
  ```bash
  kubectl exec -it <pod-name> -- /bin/bash
  ```

#### **b. Integration with Tools**

- **Prometheus and Grafana:**
  - For metrics collection and visualization.
- **ELK Stack (Elasticsearch, Logstash, Kibana):**
  - For centralized logging.

### **6. Kubernetes Ecosystem and Tools**

- **Helm:**
  - Package manager for Kubernetes (similar to `apt` for Debian).
- **Operators:**
  - Method of packaging, deploying, and managing a Kubernetes application.
- **Kubectl Plugins:**
  - Extend kubectl with custom commands.



## **4: Kubernetes `kubectl` Command Cheat Sheet**

### **1. Cluster Information and Configuration**

- **Check Client and Server Version:**

  ```bash
  kubectl version --short
  ```

- **View Cluster Information:**

  ```bash
  kubectl cluster-info
  ```

- **Display Configuration Settings:**

  ```bash
  kubectl config view
  ```

- **List Contexts (Clusters):**

  ```bash
  kubectl config get-contexts
  ```

- **Switch Context:**

  ```bash
  kubectl config use-context <context-name>
  ```

- **Set the Default Namespace:**

  ```bash
  kubectl config set-context --current --namespace=<namespace>
  ```

### **2. Working with Namespaces**

- **List All Namespaces:**

  ```bash
  kubectl get namespaces
  ```

- **Create a Namespace:**

  ```bash
  kubectl create namespace <namespace-name>
  ```

- **Delete a Namespace:**

  ```bash
  kubectl delete namespace <namespace-name>
  ```

### **3. Managing Pods**

- **List All Pods in the Current Namespace:**

  ```bash
  kubectl get pods
  ```

- **List Pods in All Namespaces:**

  ```bash
  kubectl get pods --all-namespaces
  ```

- **Describe a Pod:**

  ```bash
  kubectl describe pod <pod-name>
  ```

- **Create a Pod from a YAML File:**

  ```bash
  kubectl apply -f pod.yaml
  ```

- **Delete a Pod:**

  ```bash
  kubectl delete pod <pod-name>
  ```

### **4. Managing Deployments**

- **List Deployments:**

  ```bash
  kubectl get deployments
  ```

- **Create a Deployment:**

  ```bash
  kubectl create deployment <deployment-name> --image=<image-name>
  ```

- **Update a Deployment Image:**

  ```bash
  kubectl set image deployment/<deployment-name> <container-name>=<new-image>
  ```

- **Scale a Deployment:**

  ```bash
  kubectl scale deployment/<deployment-name> --replicas=<number>
  ```

- **Rollout Status of a Deployment:**

  ```bash
  kubectl rollout status deployment/<deployment-name>
  ```

- **Rollback a Deployment:**

  ```bash
  kubectl rollout undo deployment/<deployment-name>
  ```

- **Delete a Deployment:**

  ```bash
  kubectl delete deployment <deployment-name>
  ```

### **5. Working with Services**

- **List Services:**

  ```bash
  kubectl get services
  ```

- **Create a Service Exposing a Deployment:**

  ```bash
  kubectl expose deployment/<deployment-name> --type=<service-type> --port=<port> --target-port=<target-port>
  ```

  - **Service Types:** `ClusterIP`, `NodePort`, `LoadBalancer`

- **Describe a Service:**

  ```bash
  kubectl describe service <service-name>
  ```

- **Delete a Service:**

  ```bash
  kubectl delete service <service-name>
  ```

### **6. ConfigMaps and Secrets**

- **Create a ConfigMap from Literal Values:**

  ```bash
  kubectl create configmap <configmap-name> --from-literal=<key>=<value>
  ```

- **Create a ConfigMap from a File:**

  ```bash
  kubectl create configmap <configmap-name> --from-file=<file-path>
  ```

- **List ConfigMaps:**

  ```bash
  kubectl get configmaps
  ```

- **Describe a ConfigMap:**

  ```bash
  kubectl describe configmap <configmap-name>
  ```

- **Create a Secret from Literal Values:**

  ```bash
  kubectl create secret generic <secret-name> --from-literal=<key>=<value>
  ```

- **Create a Secret from a File:**

  ```bash
  kubectl create secret generic <secret-name> --from-file=<file-path>
  ```

- **List Secrets:**

  ```bash
  kubectl get secrets
  ```

- **Describe a Secret:**

  ```bash
  kubectl describe secret <secret-name>
  ```

### **7. Viewing Logs and Executing Commands**

- **View Logs of a Pod:**

  ```bash
  kubectl logs <pod-name>
  ```

- **Stream Logs (Follow):**

  ```bash
  kubectl logs -f <pod-name>
  ```

- **Execute a Command Inside a Pod:**

  ```bash
  kubectl exec -it <pod-name> -- <command>
  ```

  - **Example:** Open a shell inside the pod:

    ```bash
    kubectl exec -it <pod-name> -- /bin/bash
    ```

### **8. Working with Nodes**

- **List Nodes:**

  ```bash
  kubectl get nodes
  ```

- **Describe a Node:**

  ```bash
  kubectl describe node <node-name>
  ```

- **Cordon a Node (Mark as Unschedulable):**

  ```bash
  kubectl cordon <node-name>
  ```

- **Uncordon a Node:**

  ```bash
  kubectl uncordon <node-name>
  ```

- **Drain a Node (Safely Evict All Pods):**

  ```bash
  kubectl drain <node-name> --ignore-daemonsets
  ```

### **9. Resource Usage and Monitoring**

- **Get CPU and Memory Usage of Nodes:**

  ```bash
  kubectl top nodes
  ```

- **Get CPU and Memory Usage of Pods:**

  ```bash
  kubectl top pods
  ```

### **10. Managing Resources with YAML Files**

- **Apply Configuration from a YAML File:**

  ```bash
  kubectl apply -f <file.yaml>
  ```

- **Delete Resources from a YAML File:**

  ```bash
  kubectl delete -f <file.yaml>
  ```

- **Dry Run to Test Configuration:**

  ```bash
  kubectl apply -f <file.yaml> --dry-run=client
  ```

### **11. Labeling and Annotating Resources**

- **Add a Label to a Resource:**

  ```bash
  kubectl label <resource-type>/<resource-name> <label-key>=<label-value>
  ```

- **Remove a Label:**

  ```bash
  kubectl label <resource-type>/<resource-name> <label-key>-
  ```

- **Add an Annotation:**

  ```bash
  kubectl annotate <resource-type>/<resource-name> <annotation-key>=<annotation-value>
  ```

### **12. Port Forwarding**

- **Forward a Local Port to a Port on a Pod:**

  ```bash
  kubectl port-forward <pod-name> <local-port>:<pod-port>
  ```

  - **Example:**

    ```bash
    kubectl port-forward my-pod 8080:80
    ```

### **13. Getting Help and Documentation**

- **General Help:**

  ```bash
  kubectl help
  ```

- **Command-Specific Help:**

  ```bash
  kubectl <command> --help
  ```

- **Explain a Resource or Field:**

  ```bash
  kubectl explain <resource>
  kubectl explain <resource>.<field>
  ```

  - **Example:**

    ```bash
    kubectl explain pods
    kubectl explain pods.spec.containers
    ```

### **14. Debugging and Troubleshooting**

- **Get Events:**

  ```bash
  kubectl get events
  ```

- **Describe a Resource for Detailed Information:**

  ```bash
  kubectl describe <resource-type> <resource-name>
  ```

- **Check Cluster Components:**

  ```bash
  kubectl get componentstatuses
  ```

### **15. Deleting Resources**

- **Delete a Resource by Name:**

  ```bash
  kubectl delete <resource-type> <resource-name>
  ```

- **Delete Multiple Resources with a Label Selector:**

  ```bash
  kubectl delete <resource-type> -l <label-key>=<label-value>
  ```

- **Delete All Resources in a Namespace:**

  ```bash
  kubectl delete all --all -n <namespace>
  ```

---

**Note:** Replace placeholders like `<pod-name>`, `<deployment-name>`, `<service-name>`, `<namespace>`, `<resource-type>`, etc., with your actual resource names.

**Common Resource Types:**

- `pods`
- `deployments`
- `services`
- `replicasets`
- `configmaps`
- `secrets`
- `nodes`
- `namespaces`
- `events`
- `ingress`
- `statefulsets`

