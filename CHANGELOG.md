# Changelog

## 1.1.0 (2026-10-10)

- Engine 1.1.0 at SpinDoctor 3.1.2 parity: 1-298 logical qubits (59 per factor), `mcx7`, wide basis-z sampling, `q.folder`
  (with .qasm2/.circuit and skipped-file listing), CSV report copies, measurement-CSV fitting, all 241 presets replayed
  against the updated 3.1.2 reference outputs.
- New: function table (`spindoctor_functions`, `/qwerty-functions`) and theory testing from files, pasted text and the chat
  history (`spindoctor_test_theory`, `/qwerty-theory`).
- Made Claude Code-specific and distinct from spindoctor-qwerty-claude: the plugin is now `spindoctor-qwerty-code`, so the
  two never clash. The repo is a single-plugin marketplace at the root, so `/plugin marketplace add LKVexa/...` works.
- Slash commands are now Claude Code skills (`skills/qwerty-*`, user-invoked) that run the bundled CLI with an `allowed-tools`
  rule matching exactly that command. Added `qwerty-script`, `qwerty-folder` and `qwerty-report`. `qwerty-functions`
  injects the table with `` !`...` `` when invoked.
- CLI and MCP server now share `${CLAUDE_PLUGIN_DATA}/workspace`.
- Agent `qwerty-helper`: Claude Code frontmatter (tools, `model: inherit`), CLI-driven.
- New `tools/set_python.py` (Windows `python`/`py`), with exact restore. New `examples/project-settings.json` (team marketplace,
  enabledPlugins, scoped MCP allow rules).
- Still no hooks (documented). Fixed the 1.0 limits text (29 -> 298 qubits).
- Tests: `tests/claude_code_host_check.py` with the real Claude Code CLI and a CLI-first end-to-end check of all seven commands.
- GPL-3.0-or-later licence, NOTICE, COPYRIGHT, SPDX headers; author RUSSELL PHILIP SMITHSON.

## 1.0.0

- Initial Claude Code plugin (`--plugin-dir` layout, 4 commands, agent, MCP server).
