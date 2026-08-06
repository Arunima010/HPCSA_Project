## HPC-Based Distributed Fraud Detection and Monitoring Platform

<img width="1898" height="970" alt="Screen Recording 2026-08-05 211729" src="https://github.com/user-attachments/assets/614ccc17-f121-4157-8076-dbf9f8340a2b" />


A High Performance Computing (HPC) based fraud detection system that uses a virtual cluster to process financial transactions in parallel using machine learning.

## Features

- HPC cluster with Headnode and Compute Nodes
- PXE Boot provisioning
- LDAP-based centralized authentication
- NFS shared storage
- SLURM job scheduling
- XGBoost fraud detection model
- PostgreSQL database
- Grafana monitoring dashboard

## Tech Stack

- Ubuntu Server 24.04
- VMware Workstation
- SLURM
- LDAP
- NFS
- Python
- XGBoost
- PostgreSQL
- Grafana

## Architecture

```
Transactions
      │
      ▼
 Headnode (SLURM)
      │
      ▼
 Compute Nodes
      │
      ▼
 ML Fraud Detection
      │
      ▼
 PostgreSQL
      │
      ▼
 Grafana Dashboard
```

## Current Status

- ✅ Virtual HPC Cluster Setup
- ✅ PXE Boot Configuration
- ✅ LDAP Server Setup
- ✅ NFS & SLURM Configuration
- ✅ Fraud Detection Pipeline
- ✅ Dashboard & Monitoring

---

**Author:** Arunima Mukhopadhyay  
**Course:** PG-DAC HPCSA, C-DAC Pune
