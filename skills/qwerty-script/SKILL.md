---
name: qwerty-script
description: Run a q.* script file from the project (one command per line; lines starting with a hash are comments)
argument-hint: "<path/to/file.q>"
disable-model-invocation: true
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" *)
---

Run the SpinDoctor script file `$ARGUMENTS` (relative to the project, or absolute). Read it first if it is short, then run:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" --workspace "${CLAUDE_PLUGIN_DATA}/workspace" script "<absolute path of the file>"
```

Summarise the results step by step and give the TXT/PDF report paths. If a command fails, show the engine error verbatim and point
to the line. This is a classical FP64 simulation on this computer, not quantum hardware and no quantum advantage. Registers hold 1-298 logical qubits (59 per entangled factor); registers wider than 29 qubits sample in basis z only.
