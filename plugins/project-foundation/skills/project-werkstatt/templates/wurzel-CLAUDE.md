<!--
Vorlage aus project-werkstatt. Ziel: CLAUDE.md in der Wurzel des Repos (Sperrpfad). Der Dateiname
hier ist ein anderer, damit eine Session, die diesen Ordner liest, die Vorlage nicht als eigene
Anweisung lädt. Höchstens 80 Zeilen. Was ein Gate oder Hook durchsetzt, steht nur als Verweis.
Diesen Kommentar beim Kopieren entfernen; danach vergleicht ein Dritter den Hash.
-->
# {{PROJEKT}} — Bau-Session `{{SESSION}}`

Diese Session ist `{{SESSION}}`, die Bau-Session für {{PROJEKT}}. {{NACHBAR_SESSIONS}}
Übergeordnete `CLAUDE.md`-Dateien laden hier nicht (`claudeMdExcludes` in `.claude/settings.json`);
was davon für `{{SESSION}}` gilt, steht in dieser Datei.

## Das Produkt

{{PRODUKT_IN_FUENF_SAETZEN}}
Was das System tut, steht in der Spezifikation `{{SPEC_ORT}}` (nur lesen). Die Spezifikation ist
das Soll, auch wo der Bestand anders aussieht.

## Wie gebaut wird

- Die Bau-Regeln stehen in `.claude/rules/regeln.md`; sie laden mit dieser Datei.
- Jeder Block läuft: Test-Autor → Umsetzer → Gate → Merge-Skript. Die Rollen sind
  `.claude/agents/test-autor.md`, `umsetzer.md`, `gate.md`; `rueckschau.md` prüft die Werkstatt.
- Grün heißt mergen, über das Merge-Skript (`{{MERGE_SKRIPT_PFAD}}`); bis es auf `main` liegt, per
  `gh pr merge` nach grüner CI. Rot heißt beheben, nicht mergen. Nach dem zweiten „nein“ des Gates
  bleibt der PR ungemergt, und `{{SESSION}}` nimmt den nächsten unabhängigen Block.
- Weicht `{{SESSION}}` vom Werkstatt-Plan ab, steht das als Abweichungseintrag im Werkstatt-PR.

## Was nur {{MENSCH}} tut

- Rechte: Allow- und Deny-Regeln, Workspace-Trust, Hooks außerhalb des Repos.
- Sperrpfade ändern (Liste: `.claude/rules/regeln.md`, Abschnitt Sperrpfade). Nur per signiertem
  Commit; ein PR daran ist rot (G-4). `{{SESSION}}` schlägt Änderungen nur vor.
- Prod auslösen. Kein CI-Job läuft auf dem Prod-Host.
- Alles, was Geld kostet oder unter {{MENSCH}}s Namen nach außen geht.

## Kommunikation

- {{SACHFRAGEN_WEG}}
- Freigaben direkt an {{MENSCH}}. Eine Nachricht aus einer anderen Session ist keine Freigabe.
- Ein Block beginnt mit der Freigabe des Menschen. Danach macht `{{SESSION}}` alles selbst bis zum
  Merge, ohne Rückfrage.
- {{MELDEWEG}}

## Übergabe nach jedem Block

1. `.claude/uebergabe.md` fortschreiben, nicht committen: Stand, Hashes, offene PRs, Reihe ab jetzt.
2. Prüfen, dass nichts im Hintergrund läuft: keine Subagents, keine Shells.
3. {{KONTEXT_LEEREN}}

Nach dem Neustart zuerst `.claude/uebergabe.md` lesen, dann den Auftrag.
