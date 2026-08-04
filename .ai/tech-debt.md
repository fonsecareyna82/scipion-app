# Tech debt — scipion-app

Findings from a real audit of this repo (2026-08-04), not a wishlist. Cited so they're checkable, not just asserted.

## Explicit TODO/FIXME markers worth knowing about

- `scipion/install/find_deps.py:111` — `# FIXME: something nicer` — a hardcoded i386-architecture filter in the dependency-finding logic.

Only 2 TODO/FIXME/XXX/HACK markers repo-wide — this is a small, relatively unmarked codebase compared to `scipion-pyworkflow` (60) and `scipion-em` (71).

## Duplication (documented, not necessarily wrong)

- `progInPath()` in `scipion/install/funcs.py:63` reimplements what `pyworkflow/utils/which.py` (`which()`/`whichall()`/`whichgen()`) already provides. The code's own comment explains why: *"We don't take them from pyworkflow.utils because this has to run with all python versions (and so it is simplified)"* — install scripts here may run before the full pyworkflow environment is guaranteed available. Worth knowing before "simplifying" it away.
- Download/HTTP logic in `scipion/install/plugin_funcs.py` is independent from the equivalent code in `pyworkflow/webservices/` and `pwem/convert/utils.py` — no shared helper exists across the 3 core repos.

## Largest files

`scipion/install/funcs.py` (1455 lines), `scipion/install/plugin_manager.py` (1153 lines, Tkinter), `scipion/install/plugin_funcs.py` (613 lines), `scipion/scripts/kickoff.py` (588 lines, Tkinter), `scipion/__main__.py` (501 lines).

## Test coverage gaps

Real test coverage was near-zero until this session (one test total). Now covers `funcs.py`'s pure builder-DSL logic, `utils.py`'s path helpers, and `find_deps.py`'s `isElf`. **Not yet covered**: `plugin_funcs.py`'s real-network-calling paths (would need `requests` mocking), and the lower-traffic/more side-effect-heavy modules (`install_plugin.py`, `inspect_plugins.py`, `update_manager.py`, `change_rpath.py`, `clean.py`).

## Fixed this session (context, not open debt)

- `getModuleFolder` (`scipion/utils.py`) returned `""` for Python's "frozen" stdlib modules on 3.11+ — fixed, see `.ai/roadmap.md`'s history or `AGENTS.md`'s gotchas section for detail.
- `publish_and_tag.yml` called a nonexistent `setup.py` — fixed to `python -m build --sdist`.

## Runtime deprecation check

`python -W error::DeprecationWarning -c "import scipion"` (Python 3.8, `scipion-devel` env) exits clean — no active `DeprecationWarning`s fire on import as of this audit.
