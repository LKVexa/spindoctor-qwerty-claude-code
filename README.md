# SpinDoctor Qwerty for Claude Code

A **Claude Code** plugin for the SpinDoctor 3.1.2 quantum-circuit **simulator**, built for working in the terminal: seven
slash commands that run the bundled engine's CLI directly (pre-approved, so no permission prompt for the engine itself), a
`qwerty-helper` subagent for multi-step experiments, a local MCP server with the six `spindoctor_*` tools, a one-line fix for
Windows Python, and a ready-made project settings file for teams.

Engine: SpinDoctor Qwerty 1.1.0 (SpinDoctor 3.1.2 parity), bundled under `skills/spindoctor-qwerty/`. Standard-library
Python 3.8+ only, NumPy optional, no network, no installs.

## Which repository should I use?

| You use... | Choose |
| --- | --- |
| Claude Code in a terminal or IDE, and want slash commands, a subagent and a CLI that works even without the MCP server | **this repo**, `spindoctor-qwerty-claude-code` |
| claude.ai chat or Cowork (upload a `.plugin` file), or one plugin that works across claude.ai, Cowork and Claude Code | [spindoctor-qwerty-claude](https://github.com/LKVexa/spindoctor-qwerty-claude) |
| Claude Desktop chat, tools only, one-click install (Settings > Extensions, `.mcpb`) | [spindoctor-qwerty-claude-desktop](https://github.com/LKVexa/spindoctor-qwerty-claude-desktop) |

Both bundle the same engine and give the same results. Install **one** of them in Claude Code: both start the same six tools,
so having both enabled just duplicates them. The plugins have different names (`spindoctor-qwerty-code` here,
`spindoctor-qwerty` there), so their commands never clash.

## Install

You need Claude Code and Python 3.8 or newer.

In Claude Code:

```
/plugin marketplace add LKVexa/spindoctor-qwerty-claude-code
/plugin install spindoctor-qwerty-code@spindoctor-qwerty-code
```

On Claude Code 2.1.275 or later this also works in one step:

```
/plugin install spindoctor-qwerty-code --marketplace LKVexa/spindoctor-qwerty-claude-code
```

From a shell (same result):

```bash
claude plugin marketplace add LKVexa/spindoctor-qwerty-claude-code
claude plugin install spindoctor-qwerty-code@spindoctor-qwerty-code
```

Run `/reload-plugins` (or restart Claude Code), then check `/mcp`: `plugin:spindoctor-qwerty-code:spindoctor-qwerty` should
show as connected. To try it without installing, clone this repo and start `claude --plugin-dir ./spindoctor-qwerty-claude-code`.

### Windows: `python` instead of `python3`

The plugin starts Python as `python3`. The python.org installer on Windows provides `python` and `py`, not `python3`. Clone the
repo, point the plugin at your Python once, then install from the clone:

```bash
git clone https://github.com/LKVexa/spindoctor-qwerty-claude-code
cd spindoctor-qwerty-claude-code
python tools/set_python.py python          # or: py   |   "C:/Path To/python.exe"
claude plugin marketplace add .
claude plugin install spindoctor-qwerty-code@spindoctor-qwerty-code
```

`set_python.py` rewrites the command in `.mcp.json`, in the slash commands (and their pre-approved rules) and in the agent, and
prints each change. `python tools/set_python.py python3` restores the original files exactly. If `/mcp` shows the server as
failed, this is almost always the cause.

## Slash commands

All commands are user-invoked (Claude doesn't trigger them on its own) and are namespaced by the plugin name.

| Command | What it does | Example |
| --- | --- | --- |
| `/spindoctor-qwerty-code:qwerty-functions` | Shows the full function table. The engine prints it when you invoke the command, so it costs no tool call | `/spindoctor-qwerty-code:qwerty-functions gates` |
| `/spindoctor-qwerty-code:qwerty-run` | Runs q.* commands | `/spindoctor-qwerty-code:qwerty-run q.circuit new bell 2; q.circuit add h 0; q.circuit add cx 0 1; q.circuit run shots 1000 basis z` |
| `/spindoctor-qwerty-code:qwerty-script` | Runs a script file from your project (one command per line) | `/spindoctor-qwerty-code:qwerty-script experiments/ghz.q` |
| `/spindoctor-qwerty-code:qwerty-preset` | Runs one of the 241 presets, with overrides | `/spindoctor-qwerty-code:qwerty-preset qc-061 shots=500` |
| `/spindoctor-qwerty-code:qwerty-folder` | Runs a folder of command files with `q.folder` | `/spindoctor-qwerty-code:qwerty-folder runs/batch1` |
| `/spindoctor-qwerty-code:qwerty-report` | Lists the newest reports or shows one | `/spindoctor-qwerty-code:qwerty-report` |
| `/spindoctor-qwerty-code:qwerty-theory` | Tests a theory from a file, pasted text or the conversation | `/spindoctor-qwerty-code:qwerty-theory @notes/theory.md` |

**Claude Code specifics.** Each command's `allowed-tools` pre-approves exactly one Bash command: the bundled CLI,
`python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py" ...`. Nothing else runs without your
normal permission prompt, and the grant ends with that turn. The CLI and the MCP server share one workspace,
`${CLAUDE_PLUGIN_DATA}/workspace`, so circuits and reports from either are visible to both. Claude Code fills in both paths.

## The `qwerty-helper` subagent

`agents/qwerty-helper.md` is a subagent for multi-step jobs, such as running a batch of presets, sweeping a parameter or testing
several theories, without filling your main conversation. Ask Claude to "use the qwerty-helper agent to ...", or pick it from
`/agents`. It inherits your model and uses Bash, Read, Glob, Grep and Write to drive the CLI.

## CLI-first workflow

The engine is an ordinary command-line program, so you can use it with or without Claude:

```bash
S=skills/spindoctor-qwerty/scripts/spindoctor_cli.py
python3 $S functions                                   # the function table
python3 $S run "q.circuit new bell 2" "q.circuit add h 0" "q.circuit add cx 0 1" "q.circuit run shots 1000 basis z"
python3 $S script my_experiment.q                      # one command per line, lines starting with # are comments
python3 $S preset qc-061 shots=500
python3 $S run 'q.folder run path="runs/batch1"'
python3 $S report                                      # newest reports
python3 $S theory theory_args.json                     # same fields as the spindoctor_test_theory tool
```

Add `--workspace DIR` before the subcommand to choose where reports go (default `~/spindoctor-workspace`). The slash commands
use `--workspace "${CLAUDE_PLUGIN_DATA}/workspace"`. The CLI keeps working when the MCP server is disabled, not yet approved, or
blocked by your organisation's MCP policy. Scripts you write by hand in your project run unchanged through `qwerty-script`
or `q.folder`. Headless runs such as `claude -p "/spindoctor-qwerty-code:qwerty-preset qc-001"` work too, but need a signed-in
Claude Code and were not tested here.

## Sharing it with a team

Copy `examples/project-settings.json` into your project's `.claude/settings.json` (merge it if the file exists). Teammates
who trust the folder are offered the marketplace and the plugin, and the six MCP tools run without a prompt. The allow rules
use Claude Code's scoped names, `mcp__plugin_spindoctor-qwerty-code_spindoctor-qwerty__<tool>`. Remove any you'd rather
approve each time.

## Hooks

None, on purpose. A session hook would start Python in every Claude Code session whether or not you use SpinDoctor, and the
rules for this project don't allow hooks that run the engine or touch the network. Nothing in this plugin runs until you
call a command, a tool or the agent.

## Function table

Ask "what can SpinDoctor do?" or run `/spindoctor-qwerty-code:qwerty-functions`. The full table (every command family with
runnable examples, the gates, the six tools and all 241 presets) is in [FUNCTIONS.md](FUNCTIONS.md).

| Tool | What it does |
| --- | --- |
| `spindoctor_functions` | The function table (Function, What it does, Command to type), by section with an optional filter |
| `spindoctor_run_script` | Runs q.* commands; returns results plus TXT/PDF/JSON/CSV report paths |
| `spindoctor_run_preset` | Runs one of the 241 presets (qc-001..qc-241) with optional overrides |
| `spindoctor_list_presets` | Lists or filters the presets |
| `spindoctor_report` | Lists or reads reports in the workspace |
| `spindoctor_test_theory` | Tests a theory from a file, pasted text or the chat, and writes a theory test report |

## Theory testing

Say "test the theory in @notes/theory.md", paste the theory, or say "test the theory we discussed". For the last one, Claude
writes a short summary (claims, assumptions, variables, a measurable prediction), asks you to confirm it, and records short
quoted excerpts under "Source: chat history". Files can be .txt, .md, .pdf, .py, .json, .csv or .q, and exported chat
transcripts (.txt, .md, .json, .html) also work. The report (TXT + JSON + PDF) gives the hypothesis, the script, the raw
results, a verdict (supported, not supported or inconclusive) and the limits. Samples are in
`skills/spindoctor-qwerty/examples/theory/`. The plugin can't read your chat by itself, and very long chats may already be
cut by the context window.

## Honest limits

- SpinDoctor is a **classical FP64 simulator** running on your computer. It is not a quantum computer and gives no quantum
  speed-up or advantage.
- 1-298 logical qubits per register. An entangled block (factor) is capped at 59 qubits, and memory grows as 2^n x 16 bytes
  for an n-qubit dense block, so a memory budget applies. Registers wider than 29 qubits sample in basis z only.
- `q.compile synthesize` (preset qc-198) is not available, as in SpinDoctor 3.1.2.
- Python 3.8 or newer is required. NumPy is used if present, but nothing is installed.
- `q.folder` reads only the top level of a folder: 1-128 supported files, 4 MiB per file, 1-128 commands per file, 4096
  characters per command, strict UTF-8, and it stops at the first failing file.

## Testing

`python3 tests/claude_code_host_check.py` (set `CLAUDE=/path/to/claude` to include the real CLI). It checks the manifests,
the slash commands' pre-approved rules against the exact commands they run, the agent, the absence of hooks, the team
settings file and the Windows switcher. With the real Claude Code CLI (2.1.296, in a throw-away home folder, never signed
in) it runs `claude plugin validate`, marketplace add, install, list, details and `claude mcp list` (Connected). It then
runs the seven slash commands' exact command lines and the full MCP end-to-end suite against Claude Code's installed copy.
Calling tools through Claude Code itself needs a signed-in session, so those two steps are **host-simulated**: the same
commands, paths and server Claude Code would use, started directly. See [E2E_RESULTS.md](E2E_RESULTS.md).

## Layout

```
.claude-plugin/plugin.json        plugin manifest (name spindoctor-qwerty-code)
.claude-plugin/marketplace.json   single-plugin marketplace (this repo)
.mcp.json                         local stdio MCP server
skills/spindoctor-qwerty/         main skill + bundled engine, presets, examples
skills/qwerty-*/                  the seven slash commands
agents/qwerty-helper.md           subagent
examples/project-settings.json    team settings for .claude/settings.json
tools/set_python.py               Windows Python switcher
tests/                            host check and end-to-end suite
```

## Author and license

Author: RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>

Copyright (C) 2026 RUSSELL PHILIP SMITHSON. Licensed under the GNU General Public License v3.0 or later
(`GPL-3.0-or-later`); see [LICENSE](LICENSE), [NOTICE](NOTICE) and [COPYRIGHT](COPYRIGHT).
