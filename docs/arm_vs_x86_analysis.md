# ARM vs x86 Firmware Analysis

## x86 Firmware

Architecture:
x86_64

Findings:
- Hardcoded Secret
- Unsafe strcpy
- Debug Symbols

## ARM Firmware

Architecture:
ARM

Findings:
- Hardcoded Secret
- Unsafe strcpy
- Debug Symbols

## Observation

The same security flaws persisted across architectures.

Changing CPU architecture does not eliminate firmware vulnerabilities.

## Security Impact

Firmware security must be addressed through secure coding practices, not architecture changes alone.