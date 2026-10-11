# End-to-end results: spindoctor-qwerty-claude-code 1.1.0

Run on 2026-10-10 (PT) by `tests/claude_code_host_check.py` in a clean-room copy (empty folder, empty HOME, minimal PATH,
no access to engine development folders), following only this README.

**Mode:** real Claude Code CLI **2.1.296** (npm `@anthropic-ai/claude-code`, throw-away home folder, never signed in, no API
key) for validate / marketplace / install / list / details / `mcp list`. Tool calls through Claude Code itself need a
signed-in session, so the CLI-first and MCP end-to-end steps are **host-simulated (tool calls)**: they use the exact command
lines and server that Claude Code's installed copy would run, with `${CLAUDE_PLUGIN_ROOT}` / `${CLAUDE_PLUGIN_DATA}` filled
in as Claude Code documents.

**Parity target:** the updated SpinDoctor 3.1.2. Publishing was approved by Russell on the basis of the updated 3.1.2
passing its own suite 18/18, with the three 29-qubit test checks adapted to the 298-qubit limit.

## Host check (clean room)

```
PASS plugin.json: name spindoctor-qwerty-code (distinct from the claude repo's spindoctor-qwerty), version 1.1.0, author, GPL-3.0-or-later
PASS marketplace.json: name, owner, one entry at the repo root (source ./), same version
PASS .mcp.json: stdio server, plain plugin file under ${CLAUDE_PLUGIN_ROOT}, workspace under ${CLAUDE_PLUGIN_DATA}
PASS 7 slash-command skills: user-invoked, argument-hint, allowed-tools rule = the exact CLI command each body runs
PASS main skill: model-invocable, description <= 1536 chars
PASS agent qwerty-helper: description, tools include Bash, model inherit
PASS no hooks, no top-level bin/
PASS README 40+ words outside code, links the claude repo; LICENSE; text files only
PASS examples/project-settings.json: marketplace + enabledPlugins + allow rules named mcp__plugin_<plugin>_<server>__<tool>
PASS tools/set_python.py: 'python' rewrites .mcp.json + 9 skill/agent files consistently; 'python3' restores byte-identical
PASS 2.1.296 (Claude Code): claude plugin validate passes (marketplace + manifest)
PASS claude plugin marketplace add <repo>
PASS claude plugin install spindoctor-qwerty-code@spindoctor-qwerty-code
PASS claude plugin list: 1.1.0, enabled
PASS claude plugin details: 8 skills (7 slash commands + main skill), agent qwerty-helper, 1 MCP server, 0 hooks
PASS claude mcp list: plugin:spindoctor-qwerty-code:spindoctor-qwerty Connected
PASS CLI-first end-to-end: the 7 slash commands' exact command lines (qwerty-run, qwerty-script, qwerty-preset, qwerty-folder, qwerty-report, qwerty-functions (! line), qwerty-theory) + 27 valid PDFs in ${CLAUDE_PLUGIN_DATA}/workspace
PASS initialize (server spindoctor-qwerty 1.1.0)
PASS tools/list exposes the 6 tools
PASS function table (Markdown, 19 sections, 298-qubit limits listed)
PASS 241 presets listed
PASS one script per command family (16 families, every table example)
PASS 298-qubit circuit with mcx7 (prepared-factor-Born-Z)
PASS q.folder on mixed .txt/.csv/.json/.qasm folder (+ .md skipped)
PASS theory from a file -> supported, TXT+PDF report
PASS theory from a chat summary + quoted excerpts -> supported
PASS theory from an exported chat transcript -> supported
PASS presets qc-001..qc-025 match the updated 3.1.2 reference (20 identical, 5 documented differences)
PASS TXT+PDF reports valid (255 PDFs, 255 TXT twins)
SUMMARY 12/12 passed in 12.2s
PASS MCP end-to-end through the server declared in .mcp.json (plugin root: Claude Code's installed copy)
HOST-CHECK (real Claude Code (tool calls host-simulated)) PASS
```

## Notes

- The plugin is named `spindoctor-qwerty-code` (the claude repo's is `spindoctor-qwerty`), so both can coexist without
  command clashes; the README tells users to enable only one.
- `claude plugin details` reports 8 skills (7 user-invoked slash commands + the main skill), 1 agent, 1 MCP server, 0 hooks.
- `!` dynamic context injection in `qwerty-functions` and the `allowed-tools` pre-approval are documented Claude Code
  behaviour. Both were checked statically and by running the exact command line, not inside a signed-in session.
- The five documented preset differences are the engine's known, accepted ones (CPU-only reference instead of OpenCL GPU
  fields, tranche checkpoint text, state file name), as in every SpinDoctor Qwerty repo.
