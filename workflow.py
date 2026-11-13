"""Lesson-specific workflow. Read this file before the execution adapter."""
from __future__ import annotations
import asyncio
import json
from pathlib import Path
from runtime import atomic_json, contained_path, in_process_tool

async def run(agent, data):
    project = contained_path(agent.root, data['project'])
    files = sorted(project.rglob('*.py'))
    inventory = [{'path': str(p.relative_to(agent.root)), 'lines': len(p.read_text(encoding='utf8').splitlines())} for p in files]
    report = await agent.ask('audit', 'Use Glob, Grep and Read to inspect the project. Describe its Python files with evidence; do not execute code.',
        {'project': str(project), 'inventory': inventory}, 'The project has calculator.py, which defines add(a, b).',
        sdk={'tools': ['Glob', 'Grep', 'Read'], 'allowed_tools': ['Glob', 'Grep', 'Read']})
    (agent.output / 'project_report.md').write_text(report, encoding='utf8')
    return {'inventory': inventory, 'report': report}
