# Nova Platform — Technical Architecture Document
**Version:** 2.4  
**Last Updated:** March 2026  
**Owner:** Platform Engineering Team  
**Classification:** Internal Only

---

## 1. Overview

Nova is a real-time data analytics platform serving enterprise customers across financial services, healthcare, and logistics verticals. The platform ingests, processes, and visualizes event streams from customer systems, enabling sub-second alerting and historical trend analysis at scale.

As of Q1 2026, Nova processes approximately 4.2 billion events per day across 340 enterprise tenants. Peak throughput sits at 180,000 events per second during market-hours surges from our financial services customers.

---

## 2. System Components

### 2.1 Ingestion Layer

The ingestion layer is built on Apache Kafka (v3.6) deployed across three availability zones in AWS us-east-1. Each zone runs 12 broker nodes with r6i.4xlarge instances. Topics are partitioned at 128 partitions per topic, with a replication factor of 3.

Customer data arrives via three pathways:
- **REST Ingest API** — HTTPS endpoint accepting JSON or Avro payloads, rate-limited per tenant at 50,000 events/second. Backed by a Go-based gateway service (nova-gateway) running on EKS.
- **Kafka Mirror** — For customers running their own Kafka clusters, we use MirrorMaker 2 to replicate topics directly into our ingestion cluster.
- **SDK Agents** — Lightweight agents (available in Python, Java, Go, Node.js) that batch and compress events locally before transmission.

Ingestion API uptime SLA is 99.95%. Breaches in the last 12 months: 2 (both caused by upstream AWS network events, not Nova infrastructure).

### 2.2 Stream Processing Layer

Stream processing is handled by Apache Flink (v1.18) running on a dedicated EKS node pool. We maintain three Flink clusters:

- **nova-realtime** — Processes the hot path for alerting. 200ms end-to-end latency target (p99).
- **nova-enrichment** — Joins event streams with customer reference data (from PostgreSQL read replicas) to add context like user profiles, product metadata, and geo data.
- **nova-aggregation** — Computes rolling window metrics (1m, 5m, 1h, 24h) and writes results to TimescaleDB.

Flink jobs are deployed via a custom CI/CD pipeline using ArgoCD. Job definitions live in the nova-jobs GitHub repository. Deployment to production requires two engineer approvals and passes an automated performance regression test suite.

### 2.3 Storage Layer

Nova uses three storage systems depending on query pattern:

| Store | Technology | Use Case | Retention |
|---|---|---|---|
| Hot store | Apache Cassandra (v5.0) | Raw event lookup by ID, last 7 days | 7 days |
| Warm store | TimescaleDB (PostgreSQL extension) | Aggregated metrics, time-range queries | 13 months |
| Cold store | AWS S3 + Parquet | Full historical archive, bulk export | Indefinite |

Data tiering is managed automatically. Events older than 7 days are compacted and moved from Cassandra to TimescaleDB aggregations. Raw events are always archived to S3 in Parquet format for compliance and bulk analytics.

### 2.4 Query API

The Query API is a Python FastAPI service (nova-query) that translates customer queries into the appropriate backend call:

- Point lookups → Cassandra
- Time-series aggregations → TimescaleDB
- Historical bulk exports → Athena over S3

The Query API implements per-tenant row-level security. Every query is scoped to the requesting tenant's data namespace at the database level, not the application level. This is enforced via PostgreSQL row security policies and Cassandra keyspace isolation.

### 2.5 Frontend

The Nova dashboard is a React (v19) single-page application served via CloudFront. It uses Recharts for time-series visualizations and React Query for data fetching with automatic cache invalidation. The frontend communicates exclusively with the Query API and a separate Auth API — it never talks directly to storage.

### 2.6 Authentication & Authorization

Auth is handled by a dedicated service (nova-auth) built on top of Auth0. Enterprise customers can bring their own IdP via SAML 2.0 or OIDC federation.

Within Nova, authorization is role-based:
- **Viewer** — Read-only dashboard access
- **Analyst** — Can create and save custom queries
- **Admin** — Can manage users, configure alert rules, manage API keys
- **SuperAdmin** — Anthropic internal; full access for support and debugging

API keys are hashed (SHA-256 + salt) before storage. Keys are never stored in plaintext. Rotation is enforced every 365 days with 30-day grace periods.

---

## 3. Infrastructure & Deployment

### 3.1 Cloud Provider

Primary: AWS us-east-1 (N. Virginia)  
DR Region: AWS us-west-2 (Oregon) — warm standby, 15-minute RTO

All production infrastructure is defined as Terraform (v1.7). The IaC repository is nova-infra, with state managed in S3 + DynamoDB locking. Infrastructure changes require a Terraform plan review in a pull request before apply.

### 3.2 Kubernetes

Nova runs on EKS (Kubernetes 1.29). There are four node groups:

- **system** — Cluster-level services (CoreDNS, cluster-autoscaler, ALB controller)
- **api** — Stateless API services, auto-scales 3–40 nodes based on CPU and request rate
- **flink** — Flink task managers, reserved capacity (not auto-scaled to avoid reprocessing on scale-down)
- **gpu** — G5 instances for ML inference workloads (anomaly detection models)

### 3.3 CI/CD

- Source: GitHub (github.com/nova-internal)
- CI: GitHub Actions — runs lint, unit tests, integration tests, security scans (Snyk, Trivy)
- CD: ArgoCD — GitOps deployment, all changes tracked in git
- Environments: dev → staging → canary → production
- Production deployments require all CI checks to pass + manual approval from the on-call engineer

### 3.4 Observability

- Metrics: Prometheus + Grafana (hosted on Grafana Cloud)
- Logs: Loki (self-hosted on EKS)
- Traces: OpenTelemetry → Jaeger
- Alerting: PagerDuty, 24/7 on-call rotation, 5-minute response SLA for P1 incidents
- Uptime monitoring: Checkly (synthetic monitoring from 8 global regions)

---

## 4. Security Architecture

### 4.1 Network

All inter-service communication happens inside the VPC. Services communicate via internal load balancers. No service exposes ports to the public internet except the ingestion gateway and frontend CDN.

Network policies (Kubernetes NetworkPolicy + AWS Security Groups) enforce that only explicitly allowed service-to-service communication is permitted. By default, all pods are denied ingress and egress until explicitly allowed.

### 4.2 Encryption

- Data in transit: TLS 1.3 minimum, enforced at ingress and between all internal services (mTLS via Istio service mesh)
- Data at rest: AES-256 via AWS KMS for EBS volumes, S3, and RDS. Customer-managed keys (CMK) available for enterprise tier customers.
- Key rotation: Automatic annual rotation for AWS-managed keys. CMK rotation is customer-controlled.

### 4.3 Compliance

Nova is SOC 2 Type II certified (last audit: January 2026, clean report).  
HIPAA BAA available for healthcare customers.  
GDPR: EU customer data is processed in eu-west-1 (Ireland) only, with no cross-region replication.

---

## 5. Known Limitations & Planned Work

- **Cassandra hot store** — Write amplification under heavy cardinality is a known issue. We are evaluating migration to ScyllaDB in H2 2026.
- **Flink job deploys** — Currently require a full job restart (checkpoint restore), causing ~30s processing delay. We are implementing savepoint-based rolling upgrades.
- **Multi-region active-active** — Currently DR is warm standby only. Active-active across us-east-1 and eu-west-1 is on the H2 2026 roadmap.
- **Self-serve onboarding** — New tenant provisioning currently requires manual steps from the platform team. Automated tenant provisioning API is scheduled for Q2 2026.
