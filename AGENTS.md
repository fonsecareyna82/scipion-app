# scipion-app — developer manual for AI agents

Read this before making changes here. Written for an AI coding agent, not end users — see `README.rst` for that.

For deeper, less-frequently-needed context, see:
- [`.ai/tech-debt.md`](.ai/tech-debt.md) — known problem areas, with file:line
- [`.ai/roadmap.md`](.ai/roadmap.md) — planned/likely future work (draft, pending team review)

## What this repo is

The Scipion installer/launcher/plugin-manager. Top of the core dependency chain: `scipion-pyworkflow` ← `scipion-em` ← **`scipion-app`** ← external plugins. Depends on both lower layers directly (`requirements.txt`: `scipion-em`, `scipion-pyworkflow>=3.11.2`). Notably, the dependency for *GUI discovery* runs the other way: pyworkflow finds scipion-app's GUI via the `pyworkflow.guiplugin` entry point (`pyproject.toml`), not via a direct import.

## Architecture map

- `scipion/install/funcs.py` (1455 lines, the biggest file here) — a declarative builder DSL for install scripts: `Command`/`Target`/`Environment` (target-dependency bookkeeping, `addTarget`/`_addTargetDeps` with real validation - raises on duplicate targets or missing deps), `CommandDef`/`CondaCommandDef` (chainable command-string builders — `.append()`/`.cd()`/`.touch()`), `InstallHelper` (higher-level wrapper for plugin install scripts, has extensive docstrings with worked examples — read those before guessing behavior).
- `scipion/install/plugin_funcs.py`, `plugin_manager.py`, `install_plugin.py`, `inspect_plugins.py`, `update_manager.py` — plugin discovery/install/update machinery. `plugin_manager.py` (1153 lines) is Tkinter-based.
- `scipion/scripts/` — `kickoff.py` (588 lines, Tkinter startup GUI), `fontbrowser.py` (Tkinter), `config.py` (config file checking/creation, not GUI), `tutorial.py`.
- `scipion/utils.py` — small path helpers (`getScipionHome`, `getScipionAppPath`, etc.) and `getModuleFolder` (resolves a module's on-disk folder via `importlib.util.find_spec` — has a real Python-3.11+ gotcha, see below).
- `scipion/__main__.py` — the `scipion` console-script entry point (`pyproject.toml`'s `[project.scripts]`).

## Conventions actually used here

- camelCase throughout, matching pyworkflow/scipion-em.
- GPL header block on every file.
- Test deps live in `pyproject.toml`'s `[project.optional-dependencies] test`, not a separate `requirements-dev.txt` — same pattern as the other 2 core repos, matching the convention already established in `I2PC/xmipp3-installer`. Versions are pinned conditionally on `python_version` since pytest/pytest-cov's newer major versions raise their own Python floor (verified against PyPI metadata, not assumed).

## Testing

- `scipion/tests/` — pytest-native (`test_*` functions). Originally had exactly one test (`installation.py`, wrong filename for pytest's default discovery — renamed to `test_installation.py` and modernized; verified via GitHub code search there's no external reuse risk, unlike scipion-em's `BaseTest`).
- Real coverage was near-zero as of the last pass — `test_funcs.py`/`test_utils.py`/`test_find_deps.py` cover the pure builder-DSL logic and path helpers. `plugin_funcs.py`'s real-network-calling paths and the lower-traffic install modules (`install_plugin.py`, `inspect_plugins.py`, `update_manager.py`, `change_rpath.py`, `clean.py`) are **not yet covered** — see `.ai/roadmap.md`.
- CI: `test` job (pytest) + `gui` job (import-smoke only on the tkinter-backed modules — no behavioral GUI testing, since Tkinter is slated for removal). Matrix: Python 3.8–3.12.
- Run locally: `pip install -e .[test]` then `pytest`.

## Known gotchas

- **`getModuleFolder` (`scipion/utils.py`) had a real Python-3.11+ bug**, found and fixed via this repo's own test suite: `os` (and other stdlib modules) are "frozen" on Python ≥3.11 — `importlib.util.find_spec("os").origin == "frozen"`, a sentinel string, not a real path. The fix excludes `"frozen"`/`"built-in"` from the direct-origin fast path so it falls through to the robust `import + __file__` fallback. If you're resolving module locations anywhere else in this ecosystem, expect the same trap.
- `publish_and_tag.yml` used to call `python setup.py sdist` with **no `setup.py` in the repo** — fixed to `python -m build --sdist` (this repo builds purely from `pyproject.toml`). If you see `setup.py` referenced anywhere else in this ecosystem, verify it actually exists before assuming it works.
- Tkinter imports (`plugin_manager.py`, `kickoff.py`, `fontbrowser.py`, `guiplugin.py`) work fine without a real display for import-only purposes — a display is only needed once a `Tk()` root window is actually instantiated. Don't assume you need `xvfb-run` just to import these.
