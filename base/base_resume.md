<!-- links
me@sharanch.dev | mailto:me@sharanch.dev
LinkedIn | https://www.linkedin.com/in/sharanchenna/
GitHub | https://github.com/sharanch/
log-explainer | https://github.com/sharanch/log-explainer
go-sre-observatory | https://github.com/sharanch/go-sre-observatory
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

### [go-sre-observatory](https://github.com/sharanch/go-sre-observatory) — Go · Kubernetes · Prometheus · Grafana · Loki

- Built a production-instrumented Go microservice (RED metrics via `prometheus/client_golang` — request counter, error counter, p99 latency histogram with custom buckets, in-flight gauge) and deployed it to Kubernetes alongside a load generator producing a 16 req/s baseline and 40 RPS periodic spikes — deliberately triggering SLO-breach conditions to keep the full alert pipeline exercised at all times.
- Wired Prometheus → Alertmanager → Slack end to end with severity routing and runbook-linked alert annotations; centralized logs via Promtail → Loki, queryable alongside metrics in a Grafana dashboard built as the primary incident interface. Error budget tracked via PromQL recording rules. Full stack deploys or tears down in a single command.

### [postgresql-ha-lab](https://github.com/sharanch/postgres-ha-resiliency-lab) — CloudNativePG · Kubernetes · Prometheus · Grafana

- Deployed a 3-replica CloudNativePG cluster on Kubernetes and validated RPO = 0 rows and RTO of 2.2–4.5s across 10+ automated chaos scenarios — pod kill, node drain, and write-during-failover durability runs with a concurrent writer verifying zero data loss throughout each failover event.
- Defined SLIs for replication lag and failover time; tracked a 99.9% / 30-day error budget via PromQL recording rules and a custom Grafana SLO dashboard — confirmed budget exhaustion and Prometheus alert firing under a looped chaos scenario, producing screenshots used as validation evidence.

### [log-explainer](https://github.com/sharanch/log-explainer) — Python · Ollama · ELK · GitHub Actions · GHCR

- AIOps CLI that tails live log files and pipes each line through a locally running LLM (Ollama) for real-time plain-English incident explanation — fully air-gapped, zero API costs, with an optional ELK pipeline mode that ships LLM-enriched JSON to Elasticsearch so Kibana incident views show the raw log and its AI explanation side by side.
- Two-pass severity classifier (explicit keyword first, regex fallback for bare tracebacks and OOM events) with sliding-window spike detection and auto-generated incident summaries; ships as `.deb`/`.rpm` installers via a three-stage GitHub Actions pipeline — lint → pytest with 80%+ coverage gate → Docker publish to GHCR.

### [inkwell](https://github.com/sharanch/inkwell) — Go · React · Kubernetes · Prometheus · Loki

- Built a 5-service Go microservices platform (Chi router, sqlx, golang-jwt, go-redis) using interface-based repository and client abstractions throughout — each service depends on interfaces, not concrete types, keeping unit tests independent of real database or Redis connections.
- Implemented passwordless OTP auth: 6-digit codes generated via `crypto/rand`, stored in Redis with 10-minute TTL and per-email rate limiting, delivered by a dedicated notify-service over SMTP — JWT validated at the API gateway with `X-User-ID` header injection so downstream services trust the gateway without re-validating tokens. Instrumented the gateway with Prometheus RED metrics and centralized logs via Loki + Promtail; path-based GitHub Actions CI rebuilds only the service whose code changed on each commit.

## Education & Certifications

### Bachelor of Computer Applications · Kakatiya University
*2020 · 8.23 CGPA*

- **Active:** OCI Foundations Associate · OCI AI Foundations · LFS162 DevOps & SRE · GitHub Professional Certificate
- **In progress:** AWS Solutions Architect – Associate (SAA-C03)