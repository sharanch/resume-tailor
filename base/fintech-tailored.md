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
- Established automated workflows for OCI Compute CloudOps SRE team, scaling team from 1 to 6 through structured onboarding and buddy system
- Led 24×7 on-call for OCI Compute Control and Data Plane, resolving P0/P1 outages across thousands of nodes and implementing systemic fixes to prevent recurrence
- Developed Python CLI integrating Jira and Ansible, automating 15+ of 40 manual runbooks and reducing alarm resolution time to under 10 minutes
- Revised Prometheus alerting rules to reduce high-noise alerts from 40+ per week to 3–5, creating Grafana dashboards as primary incident response interface
- Automated fleet recovery from hardware failures using Terraform taint/replace, eliminating manual node reprovisioning across distributed OCI environments
### Associate Engineer · CtrlS Datacenters · Infrastructure Engineering
*Apr 2021 – Dec 2023 · Hyderabad*
- Implemented reliability strategies across 90+ enterprise private clouds spanning 2,500+ Linux nodes in a Tier IV datacenter, achieving 99.99% uptime SLA through proactive monitoring and structured incident workflows.
- Designed an Ansible-based configuration management framework to enforce server baselines fleet-wide, eliminating environment drift and reducing remediation effort by ~60%.
- Deployed a Zabbix-based observability stack with custom alerting rules and per-client dashboards, improving MTTD for critical failures and accelerating cross-team incident escalation.
- Served as primary on-call for infrastructure incidents, resolving OS-level failures like kernel panics and network degradation using structured runbooks and coordinating cross-team RCA and resolution.
- Automated ~30% of repetitive team toil by developing Bash and Python tooling for user lifecycle management, credential rotation, and log management.
- Optimized infrastructure for high-throughput workloads through NIC bonding, kernel parameter tuning, and LVM/NFS storage configuration, reducing infrastructure-layer incidents during peak load.
## Open Source Engineering
### Self-directed · Open Source
*Oct 2025 – Present*
*Deliberately stepped back from employment to build depth in cloud-native, AIOps, and observability engineering. Shipped production-grade projects independently, each designed to demonstrate real operational patterns — not toy demos.*
### [log-explainer](https://github.com/sharanch/log-explainer) — Python · Ollama · GitHub Actions · GHCR
- Architected a privacy-first AIOps CLI that streams live logs to a local LLM (Ollama, qwen2.5-coder:1.5b) for real-time explanations without data exfiltration or API costs
- Engineered a severity classification system with sliding-window anomaly detection and automated incident summaries triggered by pattern deviations
- Delivered cross-platform installers (.deb, .rpm, .pkg, .msi) through a GitHub Actions pipeline with linting, pytest (80%+ coverage), Docker publishing, and semver versioned releases
### [go-sre-observatory](https://github.com/sharanch/go-sre-observatory) — Go · Kubernetes · Prometheus · Grafana · Loki
- Designed a Kubernetes-based observability platform for a Go microservice, integrating RED metrics, SLI definitions, and SLO-breach simulations to maintain an active alerting pipeline.
- Established error budget tracking using PromQL recording rules, connecting Prometheus to Alertmanager and Slack with severity-based routing and runbook-integrated alerts.
### [chatops](https://github.com/sharanch/chatops) — React · Node.js · PostgreSQL · ArgoCD · Helm
- Built a production-grade 3-tier application on Kubernetes with GitOps via ArgoCD, achieving sub-2-minute deploy cycles for improved reliability.
- Designed modular Helm charts with per-environment overrides, reducing image size by ~60% through multi-stage Alpine builds to enhance release reliability.
- Established GitHub Actions CI/CD with path-based triggers for targeted service rebuilds and secured ingress via Cloudflare Tunnel to enforce zero-trust access.
### [istio-mesh-demo](https://github.com/sharanch/istio-mesh-demo) — Istio · Kubernetes · FastAPI · Kiali · Grafana
- Built a service mesh with mTLS encryption across microservices using Envoy sidecars, achieving zero code changes required for deployment
- Validated SLO compliance through canary testing and fault injection, simulating degraded conditions from 100/0 to 50/50 to 0/100 with 5s delays on 50% of requests
### [postgresql-ha-lab](https://github.com/sharanch/postgres-ha-resiliency-lab) — CloudNativePG · Kubernetes
- Built HA PostgreSQL cluster on Kubernetes, achieving sub-5s RPO and sub-30s RTO through chaos testing with zero data loss across 10+ failures
- Instrumented kube-prometheus-stack for observability, defined SLIs for replication lag and failover time, validated SLOs under simulated failures

## Education & Certifications

### Bachelor of Computer Applications · Kakatiya University
*2020 · 8.23 CGPA*

- **Active:** OCI Foundations Associate · OCI AI Foundations · LFS162 DevOps & SRE · GitHub Professional Certificate
- **In progress:** AWS Solutions Architect – Associate (SAA-C03)