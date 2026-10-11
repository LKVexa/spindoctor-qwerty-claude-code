---
name: qwerty-folder
description: Run every supported command file in a project folder with q.folder
argument-hint: "<folder>"
disable-model-invocation: true
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" *)
---

Run the folder `$ARGUMENTS` with SpinDoctor's folder ingestion (top level only):

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" --workspace "${CLAUDE_PLUGIN_DATA}/workspace" run 'q.folder run path="<absolute folder path>"'
```

Rules to explain if something is rejected: .txt/.csv/.json/.qasm/.qasm2/.circuit/.pdf files at the top level, 1-128 supported
files, at most 4 MiB per file, 1-128 commands per file, 4096 characters per command, strict UTF-8, processed in ordinal name order;
other files are skipped and listed; the first failing file stops the job. Report the per-file results and the report paths.
