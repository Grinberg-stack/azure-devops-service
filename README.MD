# Azure DevOps Work Items Automation Service

## Overview
This service helps streamline your Azure DevOps workflows by automating some repetitive tasks. Here's what it does:
- **Fetches Work Items** created in the past three days.
- **Updates titles** of Work Items (types `PBI`, `Feature`,`Bug`) by appending today's date.
- **Creates child tasks** for every `PBI` Work Item.

---

## Prerequisites
Before you start, make sure you have the following set up:
1. An **Azure DevOps organization and project** ready to go.
2. A **Personal Access Token (PAT)** with these permissions:
   - Work Items: Read & Write
   - Project and Team: Read
3. **Docker** installed on your system.

---

## Configuration
Before running the service, update the `config.py` file:
1. Update `<organization>` in `AZURE_DEVOPS_API` with your Azure DevOps organization name.
2. Replace `<project>` in `AZURE_DEVOPS_API` with your project name.
3. Add your **Personal Access Token (PAT)** value.

---

