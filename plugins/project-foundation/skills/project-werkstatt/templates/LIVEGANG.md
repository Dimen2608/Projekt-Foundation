# Release-Prüfung und Livegang-Liste — {{PROJEKT}}

> Vorlage aus project-werkstatt. Ziel: `docs/werkstatt/LIVEGANG.md`. Eine Liste **vor dem ersten
> Prod-Deploy**, nicht je PR; den Prod-Deploy löst nur der Mensch aus. Abgehakt wird mit Datum und
> Beleg. Herleitung: [git-und-dod.md](../reference/git-und-dod.md), Abschnitt Release-Prüfung.

## Achsen der Release-Prüfung

Gliederung nach der Production Readiness Review (Google SRE Book, Kap. 32). Je Achse steht der
Träger im Plan; eine Achse ohne Träger ist eine Lücke und wird so benannt.

| Achse | Träger im Plan | Stand |
| --- | --- | --- |
| Architektur, Abhängigkeiten | {{ARCHITEKTUR_TRAEGER}} (Threat Model eingeschlossen) | |
| Monitoring, Notfallreaktion | {{BETRIEB_TRAEGER}} | |
| Kapazität, Performance | {{BETRIEB_TRAEGER}}; Messwerte aus Staging | |
| Änderungsmanagement | Deploy-Weg der Werkstatt (Staging automatisch, Prod nur der Mensch) | |
| Konformität | {{KONFORMITAET}} (etwa eine Konformitätssuite gegen die Spezifikation) | |
| Livegang-Pflichten | Tabelle unten | |

## Livegang-Liste

Jede Zeile hat eine Quelle: eine Entscheidung, eine Rechtspflicht oder einen Vertrag. Eine Zeile
ohne Quelle kommt nicht hinein. Gefunden werden sie mit einer ausgeführten Maske über das
Entscheidungsprotokoll, etwa `grep -n -i 'go-live\|livegang\|vor dem start' <entscheidungen>`, mit
Positivkontrolle; die Maske und ihr Ergebnis stehen unter der Tabelle.

| # | Vor dem Livegang | Wer | Nachweis | Beleg | Erledigt (Datum, Beleg) |
| --- | --- | --- | --- | --- | --- |
| LG-1 | {{PFLICHT}} | {{WER}} | {{NACHWEIS}} | {{QUELLE}} | |

Typische Zeilen, je nur mit eigener Quelle aufzunehmen: Anlage zu den technischen und
organisatorischen Maßnahmen; Statusseite außerhalb der eigenen Infrastruktur und Incident-Runbook
mit Meldeweg; externer Pentest mit Pflichtziel (etwa Mandantentrennung), Bericht ohne offenen
kritischen Fund; SPF, DKIM und DMARC der Absenderdomain; Auftragsverarbeitungsverträge mit den
Anbietern; Restore-Probe gegen das Backup mit Datum und Ergebnis; rechtliche Prüfung offener
Wortlaute; Schalter, die zu einem Stichtag im Betrieb stehen müssen.

**Maske:** `{{MASKE}}` → {{ERGEBNIS}}. Positivkontrolle: {{POSITIVKONTROLLE}}.
