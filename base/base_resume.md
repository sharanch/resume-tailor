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

SRE with 4+ years building and operating large-scale Linux and OCI Compute infrastructure. First hire on Oracle OCI's CloudOps SRE team, automated 15+ manual runbooks via a Python CLI, cutting resolution time from 45+ minutes to under 10. Ramped a team of 6 and personally owned 24×7 P0/P1 response. Currently on a deliberate sabbatical shipping production-grade open source tooling in AIOps, Kubernetes observability, and cloud-native reliability engineering.

## Skills

**Infrastructure:** OCI, AWS, Kubernetes, Terraform, Linux, Docker, Helm, ArgoCD, KVM
**Observability:** Prometheus, Grafana, Alertmanager, Loki, Zabbix
**Automation/CICD:** Python, Bash, Go, GitHub Actions, Jenkins, Ansible, Boto3, Terraform
**Reliability:** Incident command (P0/P1), post-mortems, SLO design, chaos engineering, on-call operations

## Experience

### Cloud Operations Engineer · Oracle · OCI Compute
*Feb 2024 – Sep 2025 · Hyderabad*

- First hire on the CloudOps SRE team for OCI Compute (serving millions of daily API requests across the control and data plane); inherited manual runbooks and transformed them into automated workflows — onboarded 2 engineers and established a buddy system that scaled the team to 6.
- Owned 24×7 on-call for OCI Compute Control and Data Plane across a fleet of thousands of bare-metal and VM nodes. Led triage and resolution of P0/P1 outages; authored post-mortems and drove systemic follow-through to prevent recurrence.
- Built a Python CLI integrating Jira and Ansible that automated 15+ of ~40 manual runbooks — reduced average alarm resolution time from 45+ minutes to under 10 minutes for automated workflows.
- Redesigned Prometheus alerting rules, cutting alert volume on high-noise alarm types from 40+ per week to 3–5. Built Grafana dashboards used as the team's primary incident response interface.
- Automated fleet recovery from hardware failures using Terraform taint/replace, eliminating manual node reprovisioning across distributed OCI environments.

### Associate Engineer · CtrlS Datacenters · Infrastructure Engineering
*Apr 2021 – Dec 2023 · Hyderabad*

- Designed and owned end-to-end infrastructure reliability for 90+ enterprise private clouds across 2,500+ Linux nodes in a Tier IV datacenter — maintained 99.99% uptime SLA by establishing proactive monitoring, incident workflows, and systematic post-incident reviews.
- Built and scaled an Ansible-based configuration management framework to enforce server baselines across the full fleet, eliminating environment drift and cutting manual remediation effort by ~60% across repeated provisioning tasks.
- Designed and deployed a fleet-wide observability stack using Zabbix — authored custom alerting rules, thresholds, and per-client dashboards that reduced mean time to detect (MTTD) critical failures and enabled faster cross-team escalation during incidents.
- Acted as primary on-call responder for infrastructure incidents — triaged and resolved OS-level failures (kernel panics, NFS/LVM corruption, network degradation) with structured runbooks, coordinating across Network, DBA, and Application teams to drive rapid RCA and resolution.
- Automated routine operational toil — wrote Bash and Python tooling for user lifecycle management, credential rotation, log management, and patch orchestration using YUM/DNF — freeing ~30% of team bandwidth previously spent on repetitive manual tasks.
- Implemented NIC bonding, kernel tuning, and storage configuration (LVM/NFS) for high-throughput enterprise workloads, supporting seamless application deployments and reducing infrastructure-layer incidents during peak load windows.

## Open Source Engineering

### Self-directed · Open Source
*Oct 2025 – Present*

*Deliberately stepped back from employment to build depth in cloud-native, AIOps, and observability engineering. Shipped production-grade projects independently, each designed to demonstrate real operational patterns — not toy demos.*

### [log-explainer](https://github.com/sharanch/log-explainer) — Python · Ollama · GitHub Actions · GHCR

- AIOps CLI that tails live log files and uses a locally running LLM (Ollama, qwen2.5-coder:1.5b) to explain each line in real time — no data leaves the host, no API costs, fully privacy-preserving.
- Two-pass severity classifier (INFO/WARN/ERROR/CRITICAL) with sliding-window spike detection and automated incident summarization triggered on pattern anomalies.
- Ships as cross-platform installers (.deb, .rpm, .pkg, .msi) via a three-workflow GitHub Actions pipeline with lint → pytest (80%+ coverage gate) → Docker publish to GHCR → versioned releases on semver tags.

### [go-sre-observatory](https://github.com/sharanch/go-sre-observatory) — Go · Kubernetes · Prometheus · Grafana · Loki

- End-to-end observability platform on Kubernetes — metrics, logs, and alerting built around a Go microservice with full RED metrics instrumentation, SLI definition, and deliberate SLO-breach simulation to keep the alerting pipeline continuously exercised.
- Error budget tracking via PromQL recording rules; alert pipeline wired end to end: Prometheus → Alertmanager → Slack with severity routing and runbook-linked definitions. Single-command deploy and teardown via raw Kubernetes manifests.

### [chatops](https://github.com/sharanch/chatops) — React · Node.js · PostgreSQL · ArgoCD · Helm

- Production-grade 3-tier application on Kubernetes with full GitOps via ArgoCD — sub-2-minute deploy cycles demonstrating reliability engineering and operational maturity.
- Modular Helm charts with per-environment overrides; multi-stage Alpine builds reduced image size by ~60%, improving deployment reliability and reducing toil in release management.
- GitHub Actions CI/CD with path-based triggers — only affected services rebuild on commit. Cloudflare Tunnel for zero-trust ingress.

### [istio-mesh-demo](https://github.com/sharanch/istio-mesh-demo) — Istio · Kubernetes · FastAPI · Kiali · Grafana

- Service mesh on Kubernetes with full mTLS encryption via Envoy sidecars across distributed microservices — zero application code changes required.
- Live canary pipeline shifting traffic 100/0 → 50/50 → 0/100; fault injection (5s delay on 50% of requests) validates frontend resilience and SLO compliance under degraded conditions.

### [postgresql-ha-lab](https://github.com/sharanch/postgres-ha-resiliency-lab) — CloudNativePG · Kubernetes

- HA PostgreSQL cluster on Kubernetes — RPO < 5s, RTO < 30s, validated via chaos scenarios (pod kill, node drain). Zero data loss across 10+ failure events.
- Instrumented full observability stack with kube-prometheus-stack; SLIs defined for replication lag and failover time, validated against SLO targets under simulated failure conditions.

## Education & Certifications

### Bachelor of Computer Applications · Kakatiya University
*2020 · 8.23 CGPA*

- **Active:** OCI Foundations Associate · OCI AI Foundations · LFS162 DevOps & SRE · GitHub Professional Certificate
- **In progress:** AWS Solutions Architect – Associate (SAA-C03)