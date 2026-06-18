# Firmware Analysis

## Objective

Analyze a compiled ECU firmware image and identify security weaknesses.

## Findings

### 1. Hardcoded Secret

TESLA_DIAGNOSTIC_2026

Impact: An attacker extracting firmware could recover embedded secrets and potentially gain access to diagnostic functionality.

### 2. Dormant Functions

- unlock_doors()
- diagnostic_mode()

Impact: Hidden functionality increases attack surface and may expose undocumented capabilities.

### 3. Unsafe Memory Operations

- Evidence: strcpy()
- Affected Funtion: process_input()

Impact: Potential stack-based buffer overflow leading to memory corruption or arbitrary code execution.

### 4. Debug Metadata Exposure

- vulnerable_firmware.c
- Source path information
- Symbol names

Impact: Reduces reverse engineering effort and exposes implementation details.

### Remediation

Remove hardcoded secrets
Replace strcpy with bounded alternatives
Strip symbols from release binaries
Remove debugging information before deployment

## Tools

- strings
- nm
- Ghidra