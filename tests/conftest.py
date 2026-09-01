"""Baut ein minimal gueltiges Foundation-Projekt als Testfixture."""

from __future__ import annotations

from pathlib import Path

import pytest

PROJECT_MD = """# Project

## Purpose
Ein Beispiel.

## Problem
Ein Problem.

## Target Users
Entwickler.

## Core Value
Nutzen.

## Scope

### MVP
Minimal.

### V1
Spaeter.

### Out of Scope
Alles andere.

## Functional Requirements
FR-1.

## Constraints
Keine.

## Open Decisions
Keine.
"""

ARCHITECTURE_MD = """# Architecture

| Bereich | Bewertung |
| --- | --- |
| Application Architecture | RELEVANT |
| Frontend | NOT REQUIRED |
| Backend | RELEVANT |
| Database | NOT REQUIRED |
| Data Model | NOT REQUIRED |
| Authentication | NOT REQUIRED |
| Authorization | NOT REQUIRED |
| APIs | NOT REQUIRED |
| External Services | NOT REQUIRED |
| Deployment | RELEVANT |
| Security | RELEVANT |
| Configuration | RELEVANT |
| Secrets | NOT REQUIRED |
"""

ADR_MD = """# ADR-0001: Beispielentscheidung

## Status
Accepted

## Context
Kontext.

## Decision
Entscheidung.

## Consequences
Folgen.
"""

STATUS_MD = """# Status

| Domain | Status |
| --- | --- |
| Project Definition | PASS |
| Architecture | PASS |
| Development Setup | PASS |
| AI Foundation | PASS |
| Documentation | PASS |
| Testing & Quality | PASS |
| CI/CD & Infrastructure | PASS |
| Security | PASS |
"""

MANIFEST_YML = """schema_version: 1
project:
  name: beispiel
  type: tool
  maturity: greenfield
stack:
  language: python
architecture:
  style: cli
ai_support:
  claude_md: true
  agents_md: false
  cursor_rules: false
testing:
  levels: [unit]
  command: pytest
infrastructure:
  ci: github-actions
quality_gates: [foundation, change]
foundation:
  status: READY
  blocking_issues: 0
  warnings: 0
"""


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """Ein Projekt, das alle strukturellen Pruefungen besteht."""
    (tmp_path / "docs" / "decisions").mkdir(parents=True)
    (tmp_path / "README.md").write_text("# Beispiel\n", encoding="utf-8")
    (tmp_path / "CLAUDE.md").write_text("# Regeln\n", encoding="utf-8")
    (tmp_path / "STATUS.md").write_text(STATUS_MD, encoding="utf-8")
    (tmp_path / ".project-foundation.yml").write_text(MANIFEST_YML, encoding="utf-8")
    (tmp_path / "docs" / "PROJECT.md").write_text(PROJECT_MD, encoding="utf-8")
    (tmp_path / "docs" / "ARCHITECTURE.md").write_text(ARCHITECTURE_MD, encoding="utf-8")
    (tmp_path / "docs" / "decisions" / "ADR-0001-beispiel.md").write_text(ADR_MD, encoding="utf-8")
    return tmp_path
