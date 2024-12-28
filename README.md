# 🌟 Pulumi Python + FastAPI POC Project 🌟

This is a **Proof of Concept (POC)** project showcasing the integration of **Pulumi Python** with **FastAPI** via the *
*Pulumi Automation SDK**. 🎉

## 🏗️ Project Scope

The core idea of this project is to create an **Infrastructure as Code (IaC) SaaS** platform, allowing users to
dynamically manage cloud resources using REST endpoints. 🌐

### 🌟 Features:

✅ **AWS Cloud Resources**: Initial implementation supports AWS services such as:

- **EC2** 🖥️
- **IAM Roles** 🛡️
- **ECS Fargate Clusters** 🚢
- **Security Groups** 🔒

✅ **RESTful Endpoints**: Testable locally via **OpenAPI Swagger
**: [http://localhost:8001/docs#/](http://localhost:8001/docs#/)

![Pulumi Architecture](img.png)

---

### 🎯 Action Controllers:

- **Action Types**: `CREATE`, `PREVIEW`, `UP`, and `DESTROY`. These determine the operations to perform:
    - `PREVIEW` 🔎: Executes like the Pulumi `preview` command, showing changes without applying them.
    - `UP` 🚀: Deploys the desired resources.
    - `DESTROY` 🗑️: Deletes resources.

> Both actions support **state validation** and resource lifecycle management for an accurate and secure IaC process.

## 📋 Prerequisites:

Before running the application, ensure the following are in place:

1. ✅ **Pulumi Access Token**: Generate one at [Pulumi Tokens](https://app.pulumi.com/user/settings/tokens), then set it
   as an environment variable:

```plaintext
PULUMI_ACCESS_TOKEN=<your_pulumi_access_token>
```

2. ✅ **AWS CLI Default Profile**: Proper AWS credentials in the default profile for access.
3. ✅ Tooling:
    - **Python** 🐍
    - **Pip** 📦
    - **Pulumi CLI** 🔧
    - (**Optional**) **AWS CLI** 🪄

All Python dependencies will be automatically installed from the `requirements.txt` file.

---

## 🚀 How to Start the Application

1. Run the main Python application file:
   ```bash
   python __main__.py
   ```
2. Application will be hosted locally at: **[http://localhost:8001](http://localhost:8001)**

---

## ✨ Why Pulumi? What’s the Value?

### Key Benefits:

1. 🚀 **Stateful IaC Implementation**: Pulumi provides a robust state management system, ensuring deployments track
   resources across the deployment lifecycle.
2. 🔄 **Cross-Cloud Adaptability**: Resource management logic is shared across cloud providers, reducing complexity and
   maintenance compared to CDKs.
3. 🔧 **Automation-Friendly**: Pulumi’s **Automation SDK** is a wrapper around the CLI, making it easy to build **SaaS**
   platforms with stable IaC workflows.

> Pulumi also provides commands like `REFRESH` to ensure resources are consistent with the declared state. This is a *
*huge advantage** over CDKs, which lack comparable state management capabilities. 💪

---

## 📦 Example Usage (Testing Bodies)

Below are some examples of request bodies you can use. 🌟  
More details can be found in **Swagger**:

### 🚢 **Create an ECS Cluster**

```json
{
  "stack_name": "ecs-poc-cluster",
  "project_name": "automation-dev",
  "ecs_fargate": {
    "cluster_name": "automation-cluster"
  }
}
```

---

### 🔒 **Create an ECS Service with IAM & Security Group**

```json
{
  "stack_name": "ecs-poc-service",
  "project_name": "automation-dev",
  "ecs_fargate": {
    "name": "pulumi-at",
    "subnet_ids": [
      "subnet-0ac23ab19ef387fbc"
    ],
    "vpc_id": "vpc-01c3be072799793f4",
    "container_definitions": {
      "container_name": "pulumi-at",
      "image": "pulumi-at:latest"
    },
    "desired_count": 1,
    "enable_load_balancer": false,
    "enabled": true,
    "cluster_name": "automation-cluster"
  }
}
```

---

### 🖥️ **Create an EC2 Instance with Bound IAM & Security Group**

```json
{
  "stack_name": "ec2-instance",
  "project_name": "automation-dev",
  "security_group": {
    "name": "automation-poc",
    "vpc_id": "vpc-01c3be072799793f4",
    "ingress": [
      {
        "rule_type": "ingress",
        "protocol": "tcp",
        "from_port": 80,
        "to_port": 80,
        "cidr_blocks": [
          "0.0.0.0/0"
        ]
      }
    ]
  },
  "iam_role": {
    "name": "automation-poc",
    "description": "IAM role for EC2 instances",
    "managed_policy_arns": [
      "arn:aws:iam::aws:policy/AmazonEC2FullAccess",
      "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
    ],
    "inline_policies": {
      "S3AccessPolicy": "{\"Version\": \"2012-10-17\", \"Statement\": [{\"Effect\": \"Allow\", \"Action\": \"s3:*\", \"Resource\": \"*\"}]}"
    }
  },
  "ec2_instance": {
    "name": "pul-atm",
    "instance_type": "t2.micro",
    "ami_id": "ami-0b5673b5f6e8f7fa7",
    "subnet_id": "subnet-0ac23ab19ef387fbc"
  }
}
```

---

## 🔍 Conclusion

This POC leverages Pulumi's extensive IaC capabilities to provide a scalable, cross-cloud solution with a **stateful
architecture**. 💡 It demonstrates how Pulumi's **Automation SDK + FastAPI** can create dynamic, API-driven cloud
resource management tools. 🌎

> **Note**: Being a POC, it should be treated as such and not used in production without necessary adjustments. ⚠️