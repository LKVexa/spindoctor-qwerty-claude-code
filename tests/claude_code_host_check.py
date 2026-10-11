# SpinDoctor Qwerty 1.1.0 - SpinDoctor Qwerty for Claude Code
# Copyright (C) 2026 RUSSELL PHILIP SMITHSON <russellsmithson77@outlook.com>
# SPDX-License-Identifier: GPL-3.0-or-later
# This program is free software: you can redistribute it and/or modify it under the terms of the GNU General
# Public License as published by the Free Software Foundation, either version 3 of the License, or (at your
# option) any later version. It is distributed WITHOUT ANY WARRANTY; see the LICENSE file for details.
"""Claude Code host check. Standard library only (Python 3.8+); no Anthropic account, no sign-in, no model calls.

1. Static checks (Claude Code plugin docs): .claude-plugin/plugin.json and marketplace.json, .mcp.json, the 7 slash-command
   skills (user-invoked: disable-model-invocation, argument-hint, and an allowed-tools Bash rule that matches EXACTLY the CLI
   command their body tells Claude to run, so it runs without a permission prompt), the main skill, the agent (tools, model),
   no hooks, no bin/, README 40+ words, LICENSE, text files only, examples/project-settings.json.
2. tools/set_python.py round trip on a scratch copy (python -> files rewritten consistently -> python3 restores byte-identical).
3. With the REAL Claude Code CLI (CLAUDE=/path/to/claude or `claude` on PATH), in a throw-away HOME: claude plugin validate
   (marketplace + manifest), marketplace add, install, list, details (8 skills, 1 agent, 1 MCP server, 0 hooks), mcp list
   (Connected).
4. CLI-first end-to-end: runs the exact command lines the slash commands use (`python3 "${CLAUDE_PLUGIN_ROOT}/.../spindoctor_cli.py"
   --workspace "${CLAUDE_PLUGIN_DATA}/workspace" ...`, placeholders filled in the way Claude Code substitutes them, against Claude
   Code's installed copy when available): run, script, preset, folder, report, functions (the `!` line), theory; checks the
   output, the reports and the PDFs.
5. MCP end-to-end: tests/e2e_mcp.py through the server declared in .mcp.json, resolved the way Claude Code documents it.
   Tool calls through Claude Code itself need a signed-in session, so steps 4-5 are host-simulated.

usage: python3 tests/claude_code_host_check.py [REPO_DIR]"""
import glob, json, os, re, shlex, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PLUGIN, MKT = "spindoctor-qwerty-code", "spindoctor-qwerty-code"
PLUGIN_ID = PLUGIN + "@" + MKT
CLI = 'python3 "${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_cli.py"'
WS = '--workspace "${CLAUDE_PLUGIN_DATA}/workspace"'
COMMANDS = ("qwerty-run", "qwerty-script", "qwerty-preset", "qwerty-folder", "qwerty-report", "qwerty-functions", "qwerty-theory")
TOOLS = ("spindoctor_functions", "spindoctor_list_presets", "spindoctor_report", "spindoctor_run_script", "spindoctor_run_preset", "spindoctor_test_theory")
TEXT = (".py", ".md", ".json", ".txt", ".csv", ".html", ".q", "")


def frontmatter(path):
    m = re.match(r"^---\n(.*?)\n---\n", open(path, encoding="utf-8").read(), re.S)
    return dict(re.findall(r"^([A-Za-z_-]+):\s*(.+)$", m.group(1), re.M)) if m else None


def main():
    repo = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.dirname(HERE)
    ok = True; mode = "host-simulated"

    def T(name, cond, detail=""):
        nonlocal ok
        ok = ok and bool(cond); print(("PASS " if cond else "FAIL ") + name + ("" if cond else "  -- " + str(detail)[:700])); sys.stdout.flush()

    load = lambda *p: json.load(open(os.path.join(*p), encoding="utf-8"))
    pj = load(repo, ".claude-plugin", "plugin.json"); mk = load(repo, ".claude-plugin", "marketplace.json"); mj = load(repo, ".mcp.json")
    T("plugin.json: name spindoctor-qwerty-code (distinct from the claude repo's spindoctor-qwerty), version 1.1.0, author, GPL-3.0-or-later",
      pj.get("name") == PLUGIN and pj.get("version") == "1.1.0" and pj.get("author", {}).get("name") == "RUSSELL PHILIP SMITHSON" and pj.get("license") == "GPL-3.0-or-later" and pj.get("homepage", "").startswith("https://"), pj)
    e = (mk.get("plugins") or [{}])[0]
    T("marketplace.json: name, owner, one entry at the repo root (source ./), same version", mk.get("name") == MKT and mk.get("owner", {}).get("name") and e.get("name") == PLUGIN and e.get("source") in ("./", ".") and e.get("version") == "1.1.0", mk)
    s = mj["mcpServers"]["spindoctor-qwerty"]
    T(".mcp.json: stdio server, plain plugin file under ${CLAUDE_PLUGIN_ROOT}, workspace under ${CLAUDE_PLUGIN_DATA}", s.get("type") == "stdio" and s["args"] == ["${CLAUDE_PLUGIN_ROOT}/skills/spindoctor-qwerty/scripts/spindoctor_mcp.py"] and s["env"]["SPINDOCTOR_WORKSPACE"] == "${CLAUDE_PLUGIN_DATA}/workspace", s)
    bad = []
    for c in COMMANDS:
        p = os.path.join(repo, "skills", c, "SKILL.md"); fm = frontmatter(p) or {}; body = open(p, encoding="utf-8").read().split("\n---\n", 1)[-1]
        rule = fm.get("allowed-tools", ""); m = re.match(r"^Bash\((.*) \*\)$", rule)
        lines = [l.strip().lstrip("!`").rstrip("`") for l in body.splitlines() if "spindoctor_cli.py" in l and l.strip().startswith(("python3", "!`python3", "`python3"))]
        if not (fm.get("name") == c and fm.get("description") and fm.get("argument-hint") and fm.get("disable-model-invocation") == "true" and m and m.group(1) == CLI
                and lines and all(l.startswith(CLI + " ") for l in lines)):
            bad.append((c, fm, lines[:2]))
    T("7 slash-command skills: user-invoked, argument-hint, allowed-tools rule = the exact CLI command each body runs", not bad, bad)
    fm = frontmatter(os.path.join(repo, "skills", "spindoctor-qwerty", "SKILL.md")) or {}
    T("main skill: model-invocable, description <= 1536 chars", fm.get("name") == "spindoctor-qwerty" and "disable-model-invocation" not in fm and 0 < len(fm.get("description", "")) <= 1536, fm)
    ag = frontmatter(os.path.join(repo, "agents", "qwerty-helper.md")) or {}
    T("agent qwerty-helper: description, tools include Bash, model inherit", ag.get("description") and "Bash" in ag.get("tools", "") and ag.get("model") == "inherit", ag)
    T("no hooks, no top-level bin/", not os.path.exists(os.path.join(repo, "hooks")) and not os.path.exists(os.path.join(repo, "bin")) and "hooks" not in pj)
    readme = re.sub(r"```.*?```", "", open(os.path.join(repo, "README.md"), encoding="utf-8").read(), flags=re.S)
    binf = [os.path.relpath(os.path.join(r, f), repo) for r, ds, fs in os.walk(repo) if not {".git", "dist", "__pycache__"} & set(r.split(os.sep))
            for f in fs if os.path.splitext(f)[1].lower() not in TEXT and not (f.endswith(".pdf") and r.endswith(os.path.join("examples", "theory")))]
    T("README 40+ words outside code, links the claude repo; LICENSE; text files only", len(readme.split()) >= 40 and "spindoctor-qwerty-claude)" in readme and os.path.isfile(os.path.join(repo, "LICENSE")) and not binf, binf)
    ex = load(repo, "examples", "project-settings.json")
    T("examples/project-settings.json: marketplace + enabledPlugins + allow rules named mcp__plugin_<plugin>_<server>__<tool>",
      ex["extraKnownMarketplaces"][MKT]["source"] == {"source": "github", "repo": "LKVexa/spindoctor-qwerty-claude-code"} and ex["enabledPlugins"] == {PLUGIN_ID: True}
      and sorted(ex["permissions"]["allow"]) == sorted("mcp__plugin_%s_spindoctor-qwerty__%s" % (PLUGIN, t) for t in TOOLS), ex)

    scratch = os.path.join(tempfile.mkdtemp(prefix="sdq_setpy_"), "r"); shutil.copytree(repo, scratch, ignore=shutil.ignore_patterns(".git", "dist", "__pycache__", "*.pdf"))
    snap = lambda d: {os.path.relpath(os.path.join(r, f), d): open(os.path.join(r, f), "rb").read() for r, _, fs in os.walk(d) for f in fs}
    before = snap(scratch)
    subprocess.run([sys.executable, os.path.join(scratch, "tools", "set_python.py"), "python"], check=True, stdout=subprocess.DEVNULL)
    mid = snap(scratch); changed = [k for k in before if before[k] != mid[k]]
    alls = b"".join(mid[k] for k in changed)
    subprocess.run([sys.executable, os.path.join(scratch, "tools", "set_python.py"), "python3"], check=True, stdout=subprocess.DEVNULL)
    T("tools/set_python.py: 'python' rewrites .mcp.json + %d skill/agent files consistently; 'python3' restores byte-identical" % (len(changed) - 1),
      ".mcp.json" in changed and len(changed) >= 9 and b'python "${CLAUDE_PLUGIN_ROOT}' in alls and b'python3 "${CLAUDE_PLUGIN_ROOT}' not in alls and snap(scratch) == before, changed)

    root = repo
    claude = os.environ.get("CLAUDE") or shutil.which("claude")
    if claude:
        mode = "real Claude Code (tool calls host-simulated)"
        home = tempfile.mkdtemp(prefix="sdq_claude_home_"); env = dict(os.environ, HOME=home)
        run = lambda *a: subprocess.run([claude] + list(a), env=env, cwd=home, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=180)
        v = run("--version").stdout.strip().splitlines()[-1]
        rs = [run("plugin", "validate", p) for p in (repo, os.path.join(repo, ".claude-plugin", "plugin.json"))]
        T("%s: claude plugin validate passes (marketplace + manifest)" % v, all(r.returncode == 0 and "Validation passed" in r.stdout for r in rs), [r.stdout[-300:] for r in rs])
        r = run("plugin", "marketplace", "add", repo); T("claude plugin marketplace add <repo>", r.returncode == 0 and MKT in r.stdout, r.stdout)
        r = run("plugin", "install", PLUGIN_ID); T("claude plugin install " + PLUGIN_ID, r.returncode == 0 and "Successfully installed" in r.stdout, r.stdout)
        r = run("plugin", "list"); T("claude plugin list: 1.1.0, enabled", PLUGIN_ID in r.stdout and "Version: 1.1.0" in r.stdout and "enabled" in r.stdout, r.stdout)
        r = run("plugin", "details", PLUGIN_ID)
        T("claude plugin details: 8 skills (7 slash commands + main skill), agent qwerty-helper, 1 MCP server, 0 hooks",
          "Skills (8)" in r.stdout and all(c in r.stdout for c in COMMANDS) and re.search(r"Agents \(1\)\s+qwerty-helper", r.stdout) and re.search(r"MCP servers \(1\)\s+spindoctor-qwerty", r.stdout) and "Hooks (0)" in r.stdout, r.stdout)
        r = run("mcp", "list")
        T("claude mcp list: plugin:%s:spindoctor-qwerty Connected" % PLUGIN, re.search(r"plugin:%s:spindoctor-qwerty: python3 \S+spindoctor_mcp\.py - \S* ?Connected" % PLUGIN, r.stdout), r.stdout)
        inst = load(home, ".claude", "plugins", "installed_plugins.json")
        paths = [x.get("installPath") for v_ in inst.get("plugins", {}).values() for x in (v_ if isinstance(v_, list) else [v_]) if isinstance(x, dict)]
        root = next((p for p in paths if p and os.path.isdir(p)), repo)
    else:
        print("SKIP real Claude Code CLI not found (set CLAUDE=/path/to/claude)")

    data = tempfile.mkdtemp(prefix="sdq_plugin_data_"); work = tempfile.mkdtemp(prefix="sdq_cli_")
    sub = lambda x: x.replace("${CLAUDE_PLUGIN_ROOT}", root).replace("${CLAUDE_PLUGIN_DATA}", data)
    py = os.environ.get("SPINDOCTOR_PYTHON")
    def cli(extra, ws=True):
        cmd = shlex.split(sub(CLI + (" " + WS if ws else ""))) + extra
        if py: cmd[0] = py
        return subprocess.run(cmd, cwd=work, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=300)
    fold = os.path.join(work, "folder"); os.makedirs(fold)
    open(os.path.join(fold, "01_bell.txt"), "w").write("q.circuit new fbell 2\nq.circuit add h 0\nq.circuit add cx 0 1\nq.circuit run shots 64 basis z\n")
    open(os.path.join(fold, "02_ghz.qasm"), "w").write('OPENQASM 2.0;\ninclude "qelib1.inc";\nqreg q[3];\nh q[0];\ncx q[0],q[1];\ncx q[1],q[2];\n')
    open(os.path.join(fold, "notes.md"), "w").write("# skipped\n")
    ex_dir = os.path.join(root, "skills", "spindoctor-qwerty", "examples", "theory")
    args = os.path.join(work, "theory.json")
    json.dump({"action": "run", "source": "text", "text": "A Hadamard on |0> gives 0 and 1 with probability 1/2 each.", "hypothesis": "H|0> is a 50/50 superposition",
               "prediction": "P(0) = P(1) = 0.5 within shot noise", "script": "q.circuit new th 1\nq.circuit add h 0\nq.circuit run shots 4000 basis z",
               "checks": [{"kind": "probability", "outcome": "0", "expected": 0.5, "tolerance": 0.05}]}, open(args, "w"))
    cases = [("qwerty-run", ["run", "q.circuit new bell 2", "q.circuit add h 0", "q.circuit add cx 0 1", "q.circuit run shots 1000 basis z"], True, ["bell"]),
             ("qwerty-script", ["script", os.path.join(ex_dir, "xbasis.q")], True, []),
             ("qwerty-preset", ["preset", "qc-001"], True, ["qc-001"]),
             ("qwerty-folder", ["run", 'q.folder run path="%s"' % fold.replace("\\", "/")], True, ["notes.md"]),
             ("qwerty-report", ["report"], True, [".txt"]),
             ("qwerty-functions (! line)", ["functions"], False, ["| Function |", "298"]),
             ("qwerty-theory", ["theory", args], True, ["supported"])]
    res = []
    for name, extra, ws, needles in cases:
        r = cli(extra, ws); out = r.stdout
        good = r.returncode == 0 and all(n in out for n in needles) and '"ok": false' not in out and "Traceback" not in out
        res.append((name, good, out[-300:] if not good else ""))
    pdfs = glob.glob(os.path.join(data, "workspace", "**", "*.pdf"), recursive=True)
    pdf_ok = pdfs and all(open(p, "rb").read(5) == b"%PDF-" and b"%%EOF" in open(p, "rb").read()[-1024:] for p in pdfs)
    T("CLI-first end-to-end: the 7 slash commands' exact command lines (%s) + %d valid PDFs in ${CLAUDE_PLUGIN_DATA}/workspace" % (", ".join(n for n, g, _ in res if g), len(pdfs)),
      all(g for _, g, _ in res) and pdf_ok, [x for x in res if not x[1]])

    cmd = [py or sub(s["command"])] + [sub(a) for a in s["args"]]
    env2 = dict(os.environ, **{k: sub(v) for k, v in s.get("env", {}).items()}); env2.update(CLAUDE_PLUGIN_ROOT=root, CLAUDE_PLUGIN_DATA=data)
    r = subprocess.run([sys.executable, os.path.join(HERE, "e2e_mcp.py"), "--server"] + cmd + ["--examples", ex_dir, "--out", os.path.join(work, "e2e_results.json")], env=env2)
    T("MCP end-to-end through the server declared in .mcp.json (plugin root: %s)" % ("Claude Code's installed copy" if root != repo else "repo"), r.returncode == 0)
    print("HOST-CHECK (%s)" % mode, "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
