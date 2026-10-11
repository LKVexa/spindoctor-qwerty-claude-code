---
name: qwerty-run
description: Run SpinDoctor q.* commands with the bundled CLI and summarise the results
argument-hint: "<q.* commands, one per line or separated by ;>"
disable-model-invocation: true
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" *)
---

Run these SpinDoctor q.* commands:

$ARGUMENTS

Put each command in its own double-quoted argument (split on new lines or `;`) and run exactly:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" --workspace "${CLAUDE_PLUGIN_DATA}/workspace" run "q.circuit new bell 2" "q.circuit add h 0" ...
```

Then summarise each step: the exact probabilities next to the sampled counts, any error verbatim, and the TXT/PDF report paths
from the output. This is a classical FP64 simulation on this computer, not quantum hardware and no quantum advantage. Registers hold 1-298 logical qubits (59 per entangled factor); registers wider than 29 qubits sample in basis z only.
