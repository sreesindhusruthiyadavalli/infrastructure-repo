# Infrastructure Engineer Roadmap and Capstone Plan

This document is meant to be a practical route for becoming an infrastructure engineer and building a portfolio that resembles real enterprise infrastructure work.

## 1. What infrastructure engineering actually is

Infrastructure engineering is not only about installing servers or creating a cluster. It is about making systems reliable, secure, repeatable, observable, and operable at scale.

A strong infrastructure engineer can:
- provision systems with code
- secure access and secrets properly
- deploy applications safely across environments
- monitor systems and diagnose failures
- recover from incidents and outages
- reduce operational friction for application teams
- balance speed, reliability, and cost

The main mindset is:
- Is this environment reproducible?
- Is it secure?
- Is it observable?
- Is it recoverable?
- Is it easy to operate?

---

## 2. Core skills to build

The following skills matter most:

### 2.1 Operating systems and networking
- Linux fundamentals
- Process management and service management
- Filesystems and permissions
- SSH and remote access
- DNS, routing, NAT, load balancing
- HTTP/HTTPS, TLS, certificates
- Firewall basics and network segmentation
- Basic troubleshooting with `curl`, `ping`, `nslookup`, `dig`, `tcpdump`

### 2.2 Cloud fundamentals
Pick one major platform and learn it deeply:
- AWS, Azure, or GCP

Learn:
- IAM and RBAC
- Compute
- Storage
- Networking
- Managed databases
- Load balancing
- Auto scaling
- Cost controls
- Monitoring and logging services

### 2.3 Infrastructure as Code
Learn Terraform well.

Understand:
- modules
- variables and outputs
- workspaces or environment separation
- remote state
- state security
- drift management
- dependency ordering
- reusable patterns

### 2.4 Containers and orchestration
Learn:
- Docker and container basics
- Docker networking
- health checks
- image builds
- deployment patterns
- Kubernetes concepts such as pods, deployments, services, ingress, secrets, configmaps, and HPA

### 2.5 CI/CD
Learn to build safe deployment pipelines.

Understand:
- build/test/lint workflows
- artifact promotion
- approval gates
- environment-specific configuration
- rollback plans
- release safety

### 2.6 Observability
Learn to make systems visible.

Common tools:
- Prometheus
- Grafana
- Loki
- OpenTelemetry
- Alertmanager
- Elastic stack

Learn:
- metrics
- logs
- traces
- dashboards
- SLOs and alert quality

### 2.7 Security
This is especially important in infrastructure engineering.

Learn:
- least-privilege IAM
- secrets management
- vulnerability scanning
- patching workflows
- TLS and cert rotation
- network policy and segmentation
- audit logging
- supply chain security

### 2.8 Scripting and automation
You need strong automation skills.

Learn:
- Bash
- Python
- Go is a big plus for platform tooling

Use automation for:
- health checks
- migrations
- backups
- deployment automation
- self-service scripts
- incident response tasks

### 2.9 Reliability and operations
Production systems need operational maturity.

Learn:
- high availability patterns
- backups and restore testing
- disaster recovery
- runbooks
- incident handling
- capacity planning
- postmortems
- change management

### 2.10 Systems thinking
This is the difference between “tool user” and “infrastructure engineer.”

You need to understand:
- dependency mapping
- failure domains
- blast radius
- service ownership
- rollout safety
- recovery paths
- cost vs reliability tradeoffs

---

## 3. 3-month roadmap

This roadmap is designed to help you build confidence and portfolio value without spreading yourself too thin.

## Month 1: foundations + cloud + IaC

### Week 1-2: Linux, networking, scripting
Focus:
- Linux fundamentals
- SSH and access
- service management
- permissions and ownership
- logs and troubleshooting
- DNS, routing, NAT, HTTP, TLS
- Bash and Python basics

Hands-on projects:
- Build a Linux VM
- Configure Nginx with TLS
- Write a health check script that verifies a service is up
- Build a simple log-analysis script

Deliverable:
- a repository called `infra-basics-lab`
- contains setup instructions, scripts, and troubleshooting notes

### Week 3-4: Cloud + Terraform
Choose one cloud: AWS, Azure, or GCP.

Focus:
- IAM
- VPC/VNet design
- public/private subnets
- NAT and egress controls
- security groups or firewall rules
- object storage
- basic managed database understanding
- Terraform modules and remote state

Hands-on project:
- Provision a `dev` and `stage` environment with Terraform
- Add remote state backend
- Create reusable modules for networking, compute, and IAM
- Add tagging and simple budget alerts

Deliverable:
- project: `cloud-foundation-with-terraform`

---

## Month 2: containers + CI/CD + observability

### Week 5-6: Docker and app deployment
Focus:
- Dockerfiles
- image optimization
- health checks
- environment variables
- secrets handling
- Docker Compose
- service dependency patterns

Hands-on project:
- Containerize a multi-service app with:
  - frontend
  - backend API
  - Postgres
  - Redis
- Use Docker Compose for local orchestration

Deliverable:
- project: `containerized-multi-service-app`

### Week 7-8: CI/CD and release safety
Focus:
- Git workflows
- tests and linting
- package and image build
- vulnerability scans
- deployment approval gates
- rollback flows
- environment promotion

Hands-on project:
- Set up GitHub Actions or GitLab CI
- Pipeline includes:
  - lint
  - test
  - Docker build
  - security scan
  - deploy to dev
  - approval gate for prod
  - rollback job

Deliverable:
- project: `enterprise-cicd-pipeline`

---

## Month 3: Kubernetes + security + reliability

### Week 9-10: Kubernetes and platform patterns
Focus:
- deployments
- services
- ingress
- configmaps
- secrets
- readiness/liveness probes
- HPA
- Helm or Kustomize

Hands-on project:
- Deploy the service stack to Kubernetes
- Use namespaces for `dev`, `stage`, and `prod`
- Add ingress and autoscaling
- Standardize deployment template

Deliverable:
- project: `multi-environment-kubernetes-platform`

### Week 11-12: Observability, security, recovery
Focus:
- Prometheus
- Grafana
- logs aggregation
- tracing
- alert rules
- secrets management
- least privilege
- backup and restore
- incident runbooks

Hands-on project:
- Add monitoring for app and infrastructure
- Add alerting
- Hook in secrets management
- Test one restoration or failover scenario
- Write an incident runbook

Deliverable:
- project: `reliable-observable-platform`

---

## 4. Portfolio project ideas

These are the projects that will help you build your infra portfolio.

### Project 1: Cloud foundation with Terraform
Build:
- dev, stage, prod environments
- VPC/VNet
- subnets and routing
- NAT or egress controls
- IAM policies
- remote state backend
- tagging policies

What it proves:
- you understand environment separation and reproducible infrastructure

### Project 2: Containerized multi-service app
Build:
- frontend + API + PostgreSQL + Redis
- Docker Compose setup
- health checks
- service discovery
- environment config

What it proves:
- you can package and ship real application stacks

### Project 3: Enterprise CI/CD pipeline
Build:
- lint
- test
- image build
- dependency and image scanning
- deployment policies
- approval gates
- rollback process

What it proves:
- your deployments are controlled and safe

### Project 4: Kubernetes platform
Build:
- Kubernetes stack with namespaces and ingress
- Helm charts or Kustomize manifests
- autoscaling
- secrets and config
- environment overlays

What it proves:
- you can manage modern app platform patterns

### Project 5: Observability and incident lab
Build:
- Prometheus and Grafana
- centralized logs
- tracing
- alerting rules
- SLO dashboard
- runbook and outage drill

What it proves:
- you can operate systems in production-like conditions

---

## 5. Best single capstone: enterprise-style internal platform

If you only build one large project, build this.

### Capstone goal
Create a small internal platform that allows engineering teams to deploy services safely across `dev`, `stage`, and `prod` with:
- automation
- security controls
- standard deployment templates
- monitoring
- backups
- clear operational process

This mimics the way enterprise infrastructure teams operate.

### Technologies to use
Recommended stack:
- Cloud: AWS (or Azure/GCP equivalent)
- IaC: Terraform
- Compute: Kubernetes (EKS preferred if using AWS)
- Containers: Docker
- Deployment packaging: Helm or Kustomize
- CI/CD: GitHub Actions or GitLab CI
- Monitoring: Prometheus + Grafana
- Logs: Loki or ELK
- Tracing: OpenTelemetry
- Secrets: AWS Secrets Manager or Vault
- Scanning: Trivy, tfsec, Checkov
- Database: Postgres
- Cache: Redis
- Storage: S3 or equivalent

---

## 6. Capstone architecture

### High-level architecture

```text
Developer / Git Push
        |
        v
CI Pipeline
  - lint
  - unit tests
  - security scans
  - container build
  - artifact push
  - deploy to dev
  - approval gate
        |
        v
Terraform-managed Cloud Infrastructure
  - VPC / network
  - IAM / RBAC
  - EKS cluster
  - managed DB
  - Redis
  - monitoring stack
  - secrets manager
        |
        v
Kubernetes workloads
  - web-frontend
  - api-service
  - worker-service
        |
        v
Ingress / Load Balancer
        |
        v
Observability stack
  - Prometheus
  - Grafana
  - Loki
  - Alertmanager
  - traces
        |
        v
Operations and runbooks
  - backup / restore
  - incident response
  - rollback / recovery
```

### System components

#### 1. Network and security layer
- VPC/VNet
- public and private subnets
- NAT and egress controls
- load balancer
- firewall rules and security groups
- IAM roles and RBAC

#### 2. Kubernetes layer
- cluster per environment
- namespaces for app teams or workloads
- ingress controller
- autoscaling
- configmaps and secrets
- service templates

#### 3. Application layer
Three sample services:
- `web-frontend`: UI or static front-end app
- `api-service`: backend service with business logic
- `worker-service`: async processing worker or job runner

#### 4. Data layer
- Postgres for relational data
- Redis for cache/session patterns
- optional S3-like storage for asset or backup use

#### 5. Observability layer
- Prometheus for metrics
- Grafana for dashboards
- Alertmanager for alerts
- Loki or ELK for logs
- OpenTelemetry for traces

#### 6. Security layer
- IAM least privilege
- secret rotation
- image scanning
- IaC security scanning
- policy enforcement

#### 7. Operations layer
- backup scripts
- restore drill
- health checks
- runbooks
- incident response docs
- rollback automation

---

## 7. Recommended repo layout

Use a monorepo for easier learning and faster iteration.

```text
enterprise-infra-platform/
  README.md
  docs/
    architecture.md
    network-diagram.md
    runbooks/
      incident-response.md
      backup-restore.md
      prod-deploy.md
    decisions/
      001-cloud-choice.md
      002-k8s-vs-ecs.md

  terraform/
    environments/
      dev/
      stage/
      prod/
    modules/
      network/
      iam/
      eks/
      rds/
      redis/
      observability/
      secrets/

  platform/
    base/
      namespaces/
      ingress/
      cert-manager/
      external-dns/
    observability/
      prometheus/
      grafana/
      loki/
      alertmanager/
    security/
      policies/
      network-policies/
      rbac/

  services/
    api-service/
      src/
      Dockerfile
      helm/
      tests/
    worker-service/
      src/
      Dockerfile
      helm/
      tests/
    web-frontend/
      src/
      Dockerfile/
      helm/
      tests/

  ci/
    workflows/
      build.yml
      deploy-dev.yml
      stage-promotion.yml
      prod-promotion.yml
      rollback.yml

  scripts/
    bootstrap.sh
    smoke-test.sh
    backup.sh
    restore.sh
    chaos-test.sh

  .github/
    workflows/
```

This structure helps you practice real-world separation of concerns:
- infrastructure code
- platform configuration
- application deployment manifests
- CI/CD logic
- operational scripts

---

## 8. Implementation phases

### Phase 1: foundation
Build:
- cloud account / subscription structure
- Terraform remote state
- VPC/VNet and routing
- IAM and security boundaries
- dev and stage environments

Exit criteria:
- infrastructure can be created with a single command
- access policies are documented
- state is stored remotely and protected

### Phase 2: platform core
Build:
- Kubernetes cluster
- ingress controller
- certificates
- namespace design
- base RBAC and policies

Exit criteria:
- app workloads can be deployed in a cluster
- TLS and ingress flow works
- environment separation is clear

### Phase 3: application services
Build:
- frontend
- API service
- worker service
- Postgres and Redis
- health checks
- autoscaling

Exit criteria:
- all services run in dev successfully
- app health checks pass
- services recover after restarts

### Phase 4: CI/CD
Build:
- pipeline for tests, scans, and image build
- environment-specific deployment workflow
- approval gate for prod
- rollback path

Exit criteria:
- code pushes deploy safely to dev
- higher environment promotion is controlled
- rollback is possible and tested

### Phase 5: observability
Build:
- metrics and dashboards
- logs collection
- tracing
- alerts
- team dashboards

Exit criteria:
- system health is visible without direct access to servers
- alerting identifies real failures quickly

### Phase 6: security
Build:
- secret manager integration
- least-privilege policies
- scan tools in CI
- policy guardrails
- audit logging

Exit criteria:
- secrets are not checked into the repo
- scanning blocks risky changes
- access is purpose-based and documented

### Phase 7: resilience and operations
Build:
- backup scripts
- restore testing
- availability simulation
- runbooks
- incident process

Exit criteria:
- you can restore the app from backup
- failure scenarios are intentionally tested
- runbooks are useful under pressure

### Phase 8: polish and documentation
Build:
- architecture docs
- deployment notes
- cost notes
- onboarding guide
- project summary for portfolio/resume

Exit criteria:
- someone else can understand and use the platform
- your project reads like an enterprise system, not a toy demo

---

## 9. What makes it feel enterprise-level

Something feels enterprise-like when it includes operational rigor, not just cool tools.

Use these patterns:
- separate dev, stage, prod
- approval before production changes
- RBAC and least privilege
- secure secret handling
- versioned infrastructure
- vulnerability checks
- structured monitoring
- backup and recovery drills
- clear runbooks
- defined ownership and environment responsibilities

This matters more than using the most complex tools.

---

## 10. How to present this on your resume

Good wording:

> Built a multi-environment internal platform using Terraform, Kubernetes, GitHub Actions, Prometheus, Grafana, and Secrets Manager to provision secure infrastructure and support CI/CD pipelines across dev, stage, and prod.

That sounds much stronger than:

> Learned Kubernetes and Terraform.

Also document your work with:
- architecture diagrams
- environment summary
- deployment workflow
- monitoring notes
- backup/restore steps
- incident runbook
- screenshots from dashboards and pipelines

---

## 11. Suggested 12-week execution plan

### Week 1
- Linux basics
- networking basics
- Bash/Python scripting

### Week 2
- build Linux VM
- set up Nginx TLS reverse proxy
- create health-check script

### Week 3
- cloud account setup
- IAM design
- Terraform bootstrapping

### Week 4
- network and infra modules
- Terraform for dev and stage

### Week 5
- Dockerize app stack
- Compose local environment

### Week 6
- CI/CD pipeline
- deploy to dev via automation

### Week 7
- cluster build
- ingress and TLS

### Week 8
- deploy app stack to Kubernetes
- autoscaling and config

### Week 9
- Prometheus + Grafana
- log aggregation
- tracing

### Week 10
- secret handling
- security scanning
- policy guardrails

### Week 11
- backup/restore validation
- incident runbook
- chaos drill

### Week 12
- finalize docs
- architecture diagrams
- clean README
- portfolio summary

---

## 12. Practical advice

If you are just starting, do not spread yourself across too many technologies at once.

The best order is:
1. Linux + networking
2. one cloud platform
3. Terraform
4. Docker
5. CI/CD
6. Kubernetes
7. monitoring
8. security
9. resilience operations

Depth is more valuable than jumping to every tool in the ecosystem.

---

## 13. Final recommendation

Focus on building a single strong portfolio project that mirrors a real enterprise platform:
- cloud foundation
- multi-environment infrastructure
- application deployment
- CI/CD
- monitoring
- security
- backups and recovery

This is the project that makes you look like an infrastructure engineer, not just someone who can run a few commands.

Use this document as your working plan and build in order. Your goal is not to finish every tool, but to prove you can engineer a reliable system and operate it with discipline.
