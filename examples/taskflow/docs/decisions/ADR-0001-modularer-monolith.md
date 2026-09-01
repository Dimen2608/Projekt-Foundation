# ADR-0001: Modularer Monolith statt Services

## Status

Accepted — 2026-09-01

## Context

TaskFlow wird von einem Team betrieben, hat ein zusammenhängendes Datenmodell und maximal
20 gleichzeitige Nutzer. Die Frage war, ob die Anwendung von Beginn an in getrennte
Services geschnitten wird, um „später skalieren zu können".

## Decision

Ein einzelner Prozess mit klar getrennten Schichten (`routes → services → repositories`).
Die Trennung wird durch die Abhängigkeitsrichtung und die Repository-Signaturen erzwungen,
nicht durch Netzwerkgrenzen.

Verworfen: Aufteilung in Auth-Service und Task-Service. Sie würde bei dieser Größe
Netzwerkfehler, verteilte Transaktionen und zwei Deployments einführen — Kosten ohne
Gegenwert, da es keine getrennt skalierende Last gibt.

## Consequences

**Positiv**

- Ein Deployment, ein Log, eine Datenbanktransaktion.
- Refactoring über Modulgrenzen bleibt ein Compiler-Problem statt einer API-Migration.

**Negativ**

- Bei sehr ungleicher Last müsste später geschnitten werden. Die Schichtentrennung macht
  das möglich, aber nicht kostenlos.

**Grenze**

Neu bewerten, wenn ein Teil der Anwendung nachweislich eigene Skalierung braucht.
