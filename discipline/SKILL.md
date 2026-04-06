---
name: discipline
version: 1.0.0
description: Enforces Agent to only execute operations through predefined skills. Blocks all direct system calls, file operations, network requests, and code execution.
mode: enforce
priority: highest
---

# Discipline Skill

## Overview

This skill provides a behavioral guardrail and permission gateway for the Agent. When enabled, the Agent **cannot** directly execute any low-level operations. All external environment interactions must go through other skills.

## Use Cases

- Security-sensitive environments requiring strict Agent capability restrictions
- Multi-user shared Agent instances
- Production automation tasks
- Agent behavior auditing and tracing

## Core Restrictions

When `discipline` is enabled, the following operations are **completely prohibited**:

### 1. System Command Execution

- **Blocked**: `exec`, `system`, `subprocess`, `os.system`, `popen`, `spawn`, etc.
- **Reason**: Prevents arbitrary command execution security risks

### 2. File System Operations

- **Blocked**: Direct `open`, `os.remove`, `os.rename`, `shutil`, `pathlib` write operations
- **Reason**: Prevents unauthorized file reading, modification, deletion

### 3. Network Requests

- **Blocked**: `requests`, `urllib`, `socket`, `httpx`, `aiohttp`, etc.
- **Reason**: Prevents data exfiltration, internal network probing, malicious requests

### 4. Dynamic Code Execution

- **Blocked**: `eval`, `exec`, `compile`, `__import__`, `imp.load_module`
- **Reason**: Prevents code injection and runtime behavior escape

### 5. Process & System Information

- **Blocked**: `os.getpid`, `psutil`, `os.kill`, `multiprocessing`
- **Reason**: Prevents interfering with other processes or accessing unauthorized system info

## Allowed Operations

The Agent may **only** perform operations through:

- Calling whitelisted skills
- Pure text reasoning and conversation
- Reading its own existing context

## Whitelist Configuration

Default whitelist always includes the enabled skills of the Agent, additionally, you can add some skill in the following list:

```yaml
enabled_skills:
  - fast-dirpy
  - ...
```
