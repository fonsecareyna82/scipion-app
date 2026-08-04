# Roadmap — scipion-app

**Status: draft, pending review with Yunior (repo co-owner).** Seeded from a rough team Google Doc plus findings surfaced while doing the test/CI/Python-3.8-3.12 work on this repo (2026-08-04). Treat as a starting point, not a committed plan.

## This repo specifically

- Extend test coverage to `plugin_funcs.py`'s network-calling paths (needs `requests` mocking to do properly) and the lower-traffic install modules (`install_plugin.py`, `inspect_plugins.py`, `update_manager.py`, `change_rpath.py`, `clean.py`) — see `.ai/tech-debt.md`.
- `scipion/install/find_deps.py:111`'s hardcoded i386-architecture filter could use a real fix instead of the noted `# FIXME: something nicer`.

## Ecosystem-wide (applies to all 5 repos, not just this one)

- **Branch/release cleanup**: drop the redundant `master` branch, rename `devel` → `main`, replace push-triggered publish with a manual `workflow_dispatch` release gated by a protected GitHub deployment environment. `I2PC/scipion-em-xmipp`'s `.github/workflows/release.yml` is a concrete reference — this repo's own `publish_and_tag.yml` was already partially fixed this session (broken `setup.py sdist` → `python -m build --sdist`), but still auto-publishes on push to `master` rather than requiring manual approval.
- **Remove Tkinter entirely** (`plugin_manager.py`, `kickoff.py`, `fontbrowser.py`, `guiplugin.py`) once ScipionAPI + ScipionWeb fully replace it (ScipionWeb replaces both the legacy Tkinter GUI and an intermediate NiceGUI attempt).
- **Convert buildbot to a GitHub Actions self-hosted runner.**
- **Set up a dependency manager (Renovate)** across all 5 repos.
