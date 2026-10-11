---
name: qwerty-report
description: List the newest SpinDoctor reports or show one
argument-hint: "[report name]"
disable-model-invocation: true
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" *)
---

Show SpinDoctor reports. With no argument list the newest ones; with a name show that TXT report:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" --workspace "${CLAUDE_PLUGIN_DATA}/workspace" report $ARGUMENTS
```

Give the matching PDF/JSON/CSV paths next to each TXT report.
