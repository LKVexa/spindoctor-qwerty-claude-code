---
name: qwerty-theory
description: Test a theory with the SpinDoctor simulator (a project file, pasted text, or the theory we discussed)
argument-hint: "<file | theory text | 'we discussed'>"
disable-model-invocation: true
allowed-tools: Bash(python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" *)
---

Test this theory with the SpinDoctor simulator: $ARGUMENTS

1. Source: a file (`@file` or a path: source "file"), pasted text (source "text"), or our conversation (source "chat"): write a
   short summary (claims, assumptions, variables, measurable prediction), **show it and get my confirmation**, and add short
   verbatim excerpts ("User: ...", "Assistant: ...").
2. Restate the hypothesis and a measurable prediction; write the q.* script and machine checks (see the spindoctor-qwerty skill).
3. Prefer the `spindoctor_test_theory` tool. Without it, write the arguments to a JSON file in a temporary folder and run
   `python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" --workspace "${CLAUDE_PLUGIN_DATA}/workspace" theory <args.json>`.
4. Report the verdict (supported / not supported / inconclusive), observed vs predicted numbers, and the TXT/PDF theory report.
The plugin can't read the chat by itself, and long chats may already be truncated by the context window. This is a classical FP64 simulation on this computer, not quantum hardware and no quantum advantage. Registers hold 1-298 logical qubits (59 per entangled factor); registers wider than 29 qubits sample in basis z only.
