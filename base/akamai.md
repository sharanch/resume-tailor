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
- Led transformation of manual OCI Compute runbook library into automated workflows, scaling team from 1 to 6 through structured onboarding and buddy system
- Managed 24×7 on-call for OCI Compute Control and Data Plane across thousands of nodes, leading triage of P0/P1 outages and driving systemic fixes
- Developed Python CLI integrating Jira and Ansible to automate 15 of 40 manual runbooks, reducing average alarm resolution time to under 10 minutes
- Revised Prometheus alerting rules to cut high-noise alerts from 40+ per week to 3–5, creating Grafana dashboards as primary incident response interface
- Automated fleet recovery from hardware failures using Terraform taint/replace, eliminating manual node reprovisioning across distributed OCI environments
### Associate Engineer · CtrlS Datacenters · Infrastructure Engineering
*Apr 2021 – Dec 2023 · Hyderabad*
- Reduced infrastructure downtime to 99.99% SLA across 2,500+ Linux nodes in Tier IV datacenters by implementing proactive monitoring, structured incident workflows, and blameless post-mortems.
- Established Ansible-based configuration management to enforce fleet-wide server baselines, eliminating environment drift and reducing remediation effort by 60%.
- Deployed Zabbix observability stack with custom alerting and per-client dashboards, improving MTTD for critical failures and accelerating incident escalation across teams.
- Led on-call infrastructure incident response, resolving OS-level failures like kernel panics and network degradation through structured runbooks and cross-team coordination.
- Automated 30% of repetitive team toil with Bash/Python tooling for user lifecycle, credential rotation, log management, and patch orchestration.
- Optimized high-throughput workloads via NIC bonding, kernel tuning, and LVM/NFS configuration, decreasing infrastructure-layer incidents during peak loads.
## Open Source Engineering
### Self-directed · Open Source
*Oct 2025 – Present*
*Deliberately stepped back from employment to build depth in cloud-native, AIOps, and observability engineering. Shipped production-grade projects independently, each designed to demonstrate real operational patterns — not toy demos.*
### [log-explainer](https://github.com/sharanch/log-explainer) — Python · Ollama · GitHub Actions · GHCR
- Built privacy-preserving AIOps CLI with local LLM (Ollama, qwen2.5-coder:1.5b) for real-time log explanation, ensuring no data leaves the host and eliminating API costs.
- Designed two-pass severity classifier with sliding-window spike detection and automated incident summarization for pattern anomalies, improving incident response accuracy.
- Established cross-platform installer pipeline with GitHub Actions for linting, pytest (80%+ coverage), Docker publishing to GHCR, and semver versioned releases.
### [go-sre-observatory](https://github.com/sharanch/go-sre-observatory) — Go · Kubernetes · Prometheus · Grafana · Loki
- Architected a Kubernetes-based observability system for a Go microservice, integrating RED metrics, SLI definitions, and SLO-breach simulations to maintain an active alerting pipeline.
- Established error budget tracking using PromQL recording rules, connecting Prometheus to Alertmanager and Slack with severity-based routing and runbook-integrated alert definitions.
### [chatops](https://github.com/sharanch/chatops) — React · Node.js · PostgreSQL · ArgoCD · Helm
- Built a 3-tier Kubernetes application with GitOps via ArgoCD, reducing deployment latency to under 2 minutes
- Created modular Helm charts with environment-specific overrides, decreasing image size by 60% through multi-stage Alpine builds
- Established GitHub Actions CI/CD with path-based triggers for targeted service rebuilds, securing ingress with Cloudflare Tunnel for zero-trust access
### [istio-mesh-demo](https://github.com/sharanch/istio-mesh-demo) — Istio · Kubernetes · FastAPI · Kiali · Grafana
- Built a service mesh on Kubernetes with full mTLS encryption using Envoy sidecars across distributed microservices without requiring application code changes.
- Validated SLO compliance under degraded conditions through a live canary pipeline and fault injection, simulating 5s delays on 50% of requests.
### [postgresql-ha-lab](https://github.com/sharanch/postgres-ha-resiliency-lab) — CloudNativePG · Kubernetes
- Built HA PostgreSQL cluster on Kubernetes, achieving sub-5s RPO and sub-30s RTO through chaos testing with zero data loss across 10+ failures.
- Designed observability stack with kube-prometheus-stack, defining SLIs for replication lag and failover time validated against SLO targets under simulated failures.

## Education & Certifications

### Bachelor of Computer Applications · Kakatiya University
*2020 · 8.23 CGPA*

- **Active:** OCI Foundations Associate · OCI AI Foundations · LFS162 DevOps & SRE · GitHub Professional Certificate
- **In progress:** AWS Solutions Architect – Associate (SAA-C03)