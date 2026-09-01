# Projekt-Definition — TaskFlow

> Beispielprojekt. Zeigt, wie eine ausgefüllte Projektdefinition aussieht.

## Purpose

Ein interner Aufgaben-Tracker, mit dem ein Team von bis zu 20 Personen Aufgaben anlegen,
zuweisen und im Status verfolgen kann — ohne die Einrichtungskosten und den
Funktionsumfang großer Ticketsysteme.

## Problem

Aufgaben werden aktuell in einer geteilten Tabelle und in Chat-Nachrichten geführt.
Zuständigkeiten sind nicht nachvollziehbar, der Stand ist nur nach Rückfrage bekannt, und
abgeschlossene Aufgaben verschwinden nicht aus der Ansicht. Bestehende Ticketsysteme
lösen das, kosten aber Einrichtung und Schulung, die für die Teamgröße unverhältnismäßig ist.

## Target Users

- **Primär:** Teammitglieder, die Aufgaben annehmen und deren Status pflegen.
- **Sekundär:** Teamleitung, die den Gesamtstand sehen will.

## Core Value

Auf einen Blick sehen, wer woran arbeitet und was liegen bleibt.

## Scope

### MVP

- Anmeldung mit E-Mail und Passwort
- Aufgaben anlegen, bearbeiten, löschen
- Zuweisung an ein Teammitglied
- Status: `offen`, `in Arbeit`, `erledigt`
- Listenansicht mit Filter nach Zuständigkeit und Status

### V1

- Kommentare an Aufgaben
- Fälligkeitsdaten und Erinnerungen
- Aktivitätsverlauf je Aufgabe

### Out of Scope

- Mehrere Organisationen in einer Installation (kein Multi-Tenancy, siehe ADR-0003)
- Zeiterfassung, Reporting, Dashboards
- Mobile Apps — die Weboberfläche ist responsiv, mehr nicht
- Single Sign-On und externe Identity Provider
- Öffentliche API für Drittsysteme

## Functional Requirements

| ID | Anforderung |
| --- | --- |
| FR-1 | Nutzer melden sich mit E-Mail und Passwort an. |
| FR-2 | Angemeldete Nutzer legen Aufgaben mit Titel und Beschreibung an. |
| FR-3 | Eine Aufgabe kann genau einem Teammitglied zugewiesen sein. |
| FR-4 | Der Status einer Aufgabe ist genau einer aus `offen`, `in Arbeit`, `erledigt`. |
| FR-5 | Die Listenansicht filtert nach Zuständigkeit und Status. |
| FR-6 | Nutzer sehen ausschließlich Aufgaben ihres eigenen Teams. |

## Non-Functional Requirements

| ID | Anforderung |
| --- | --- |
| NFR-1 | Die Listenansicht lädt bei 5.000 Aufgaben in unter 500 ms. |
| NFR-2 | Passwörter werden mit Argon2id gehasht. |
| NFR-3 | Die Anwendung läuft auf einem einzelnen Container ohne externe Dienste außer PostgreSQL. |

## Constraints

- Betrieb auf vorhandener interner Container-Plattform; kein Cloud-Budget.
- Node 22 und PostgreSQL 16 sind gesetzt (bestehende Betriebserfahrung im Team).
- Nur interne Nutzer, kein öffentlicher Zugang.

## Open Decisions

| ID | Frage | Status |
| --- | --- | --- |
| OD-1 | Ob Kommentare Markdown unterstützen sollen | vertagt bis V1 |
