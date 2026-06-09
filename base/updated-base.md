<!-- links
me@sharanch.dev | mailto:me@sharanch.dev
LinkedIn | https://www.linkedin.com/in/sharanchenna/
GitHub | https://github.com/sharanch/
log-explainer | https://github.com/sharanch/log-explainer
go-sre-observatory | https://github.com/sharanch/go-sre-observatory
chatops | https://github.com/sharanch/chatops
istio-mesh-demo | https://github.com/sharanch/istio-mesh-demo
postgresql-ha-lab | https://github.com/sharanch/postgres-ha-resiliency-lab
inkwell | https://github.com/sharanch/inkwell
-->

# Sharan Chenna
Site Reliability Engineer
[me@sharanch.dev](mailto:me@sharanch.dev) · [LinkedIn](https://www.linkedin.com/in/sharanchenna/) · [GitHub](https://github.com/sharanch/) · +91 82976 22321 · Hyderabad, India

## Summary

SRE with 4+ years building and operating large-scale Linux and cloud infrastructure. First hire on Oracle OCI's CloudOps SRE team — automated 15+ manual runbooks via a Python CLI, cutting resolution time from 45+ minutes to under 10, and scaled the team from 1 to 6. Owned 24×7 P0/P1 response across thousands of OCI Compute nodes. Currently shipping production-grade open source tooling in AIOps, Kubernetes observability, and cloud-native reliability engineering.

## Skills

**Infrastructure:** OCI, AWS, Kubernetes, Terraform, Linux, Docker, Helm, ArgoCD, KVM
**Observability:** Prometheus, Grafana, Alertmanager, Loki, Zabbix
**Automation/CI-CD:** Python, Bash, Go, GitHub Actions, Jenkins, Ansible, Boto3
**Reliability:** Incident command (P0/P1), post-mortems, SLO design, chaos engineering, on-call operations

## Experience

### Cloud Operations Engineer · Oracle · OCI Compute
*Feb 2024 – Sep 2025 · Hyderabad*

- First hire on the CloudOps SRE team for OCI Compute; inherited a fully manual runbook library and transformed it into automated workflows, scaling the team from 1 to 6 through structured onboarding and a buddy system.
- Owned 24×7 on-call for OCI Compute Control and Data Plane across thousands of bare-metal and VM nodes — led triage and resolution of P0/P1 outages, authored post-mortems, and drove systemic fixes to prevent recurrence.
- Built a Python CLI integrating Jira and Ansible that automated 15+ of ~40 manual runbooks, reducing average alarm resolution time from 45+ minutes to under 10 minutes.
- Redesigned Prometheus alerting rules, cutting high-noise alert volume from 40+ per week to 3–5; built Grafana dashboards that became the team's primary incident response interface.
- Automated fleet recovery from hardware failures using Terraform taint/replace, eliminating manual node reprovisioning across distributed OCI environments.

### Associate Engineer · CtrlS Datacenters · Infrastructure Engineering
*Apr 2021 – Dec 2023 · Hyderabad*

- Owned reliability for 90+ enterprise private clouds across 2,500+ Linux nodes in a Tier IV datacenter — maintained 99.99% uptime SLA through proactive monitoring, structured incident workflows, and blameless post-mortems.
- Built an Ansible-based configuration management framework that enforced server baselines fleet-wide, eliminating environment drift and cutting remediation effort by ~60%.
- Deployed a fleet-wide observability stack using Zabbix with custom alerting rules and per-client dashboards — reduced MTTD for critical failures and accelerated cross-team escalation during incidents.
- Served as primary on-call for infrastructure incidents; triaged and resolved OS-level failures (kernel panics, NFS/LVM corruption, network degradation) using structured runbooks, coordinating across Network, DBA, and Application teams to drive RCA and resolution.
- Eliminated ~30% of repetitive team toil by writing Bash and Python tooling for user lifecycle management, credential rotation, log management, and patch orchestration.
- Tuned infrastructure for high-throughput enterprise workloads via NIC bonding, kernel parameter optimization, and LVM/NFS storage configuration, reducing infrastructure-layer incidents during peak load.

## Open Source Engineering

### Self-directed · Open Source
*Oct 2025 – Present*

*Deliberately stepped back from employment to build depth in cloud-native, AIOps, and observability engineering. Shipped production-grade projects independently, each designed to demonstrate real operational patterns — not toy demos.*

### [log-explainer](https://github.com/sharanch/log-explainer) — Python · Ollama · GitHub Actions · GHCR

- Built an AIOps CLI that tails live log files and uses a local LLM (Ollama, qwen2.5-coder:1.5b) to explain each line in real time — no data leaves the host, no API costs, fully privacy-preserving.
- Implemented a two-pass severity classifier (INFO/WARN/ERROR/CRITICAL) with sliding-window spike detection and automated incident summarization triggered on pattern anomalies.
- Shipped cross-platform installers (.deb, .rpm, .pkg, .msi) via a three-workflow GitHub Actions pipeline: lint → pytest (80%+ coverage gate) → Docker publish to GHCR → versioned releases on semver tags.

### [go-sre-observatory](https://github.com/sharanch/go-sre-observatory) — Go · Kubernetes · Prometheus · Grafana · Loki

- Built an end-to-end observability platform on Kubernetes around a Go microservice with full RED metrics instrumentation, SLI definitions, and deliberate SLO-breach simulation to keep the alerting pipeline continuously exercised.
- Implemented error budget tracking via PromQL recording rules; wired the full alert pipeline Prometheus → Alertmanager → Slack with severity routing and runbook-linked alert definitions.

### [chatops](https://github.com/sharanch/chatops) — React · Node.js · PostgreSQL · ArgoCD · Helm

- Deployed a production-grade 3-tier application on Kubernetes with full GitOps via ArgoCD, achieving sub-2-minute deploy cycles.
- Authored modular Helm charts with per-environment overrides; multi-stage Alpine builds reduced image size by ~60%, cutting deployment toil and improving release reliability.
- Implemented GitHub Actions CI/CD with path-based triggers so only affected services rebuild on commit; secured ingress via Cloudflare Tunnel for zero-trust access.

### [istio-mesh-demo](https://github.com/sharanch/istio-mesh-demo) — Istio · Kubernetes · FastAPI · Kiali · Grafana

- Deployed a service mesh on Kubernetes with full mTLS encryption via Envoy sidecars across distributed microservices — zero application code changes required.
- Validated SLO compliance under degraded conditions via a live canary pipeline (100/0 → 50/50 → 0/100) and fault injection (5s delay on 50% of requests).

### [postgresql-ha-lab](https://github.com/sharanch/postgres-ha-resiliency-lab) — CloudNativePG · Kubernetes

- Deployed an HA PostgreSQL cluster on Kubernetes achieving RPO < 5s and RTO < 30s, validated via chaos scenarios (pod kill, node drain) with zero data loss across 10+ failure events.
- Instrumented the full observability stack with kube-prometheus-stack; defined SLIs for replication lag and failover time, validated against SLO targets under simulated failure conditions.

## Education & Certifications

### Bachelor of Computer Applications · Kakatiya University
*2020 · 8.23 CGPA*

- **Active:** OCI Foundations Associate · OCI AI Foundations · LFS162 DevOps & SRE · GitHub Professional Certificate
- **In progress:** AWS Solutions Architect – Associate (SAA-C03)