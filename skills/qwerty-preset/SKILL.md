---
name: qwerty-preset
description: Run one of the 241 SpinDoctor presets (qc-001..qc-241), with optional name=value overrides
argument-hint: "<qc-NNN> [name=value ...]"
disable-model-invocation: true
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" *)
---

Run SpinDoctor preset $ARGUMENTS:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" --workspace "${CLAUDE_PLUGIN_DATA}/workspace" preset qc-NNN name=value ...
```

To find a preset first: `python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" presets <filter>`. Summarise each step and give the TXT/PDF report paths. This is a classical FP64 simulation on this computer, not quantum hardware and no quantum advantage. Registers hold 1-298 logical qubits (59 per entangled factor); registers wider than 29 qubits sample in basis z only.
