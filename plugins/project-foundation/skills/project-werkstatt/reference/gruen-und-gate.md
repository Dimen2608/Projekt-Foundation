# Grün-Definition und Gate

> Was „grün" heißt, wenn kein Mensch mehr jeden PR freigibt — und wie das KI-Gate blockiert.

## Die Leitfrage

Was muss „grün" umfassen, damit die Prüfungen den ganzen Schutz tragen, den vorher die
Einzelfreigabe getragen hat?

**Randbedingung:** Die Werkstatt setzt nichts voraus, was der Git-Host serverseitig erzwingt. Auf
einem Plan ohne Branch-Schutz, Pflicht-Checks und Merge-Queue hält ein roter Check einen Merge
technisch nicht auf.

**Antwort:** „Grün" ist keine Farbe auf der PR-Seite, sondern das Ergebnis **eines Merge-Skripts**,
das die Bau-Session als einzigen Weg zum Merge benutzt und das in der Fassung von `origin/main`
läuft: `git show origin/main:<pfad> | python -`. Das Skript führt Wächter und Listenprüfung
**selbst** aus `main` gegen den PR-Diff aus, statt dem gleichnamigen CI-Check zu glauben. Grund:
Bei `pull_request` nimmt GitHub die Workflow-Datei aus dem PR — ein PR könnte einen CI-Job durch
`exit 0` ersetzen.

## G-1 bis G-8

Ein PR ist grün, wenn **alle** acht Punkte zutreffen. Das Skript prüft in dieser Reihenfolge und
bricht beim ersten Fehlschlag ab; die Meldung nennt den Punkt.

| # | Bedingung | Schließt |
| --- | --- | --- |
| G-1 | Jeder Check der **Pflicht-Check-Liste** (Datei im Repo, gelesen aus `origin/main`) hat auf dem PR-Kopf `success`. `skipped`, `neutral`, `cancelled` und ein fehlender Check sind nicht grün. | Ein Job, der nicht lief, sieht in der Summe grün aus |
| G-2 | Die geprüfte SHA ist der PR-Kopf und wird gemergt (`gh pr merge --match-head-commit <sha>`). Testbericht trägt die SHA. | Geprüft wurde ein anderer Stand als der gemergte |
| G-3 | Der PR-Kopf enthält `origin/main` (`git merge-base --is-ancestor`). Sonst rebasen und neu laufen lassen. | Ohne Merge-Queue: zwei PRs, einzeln grün, zusammen kaputt |
| G-4 | Das Skript führt Wächter, Skip-Erlaubnisliste und Pflicht-Check-Liste selbst in der Fassung von `origin/main` aus. **Sperrpfade:** Jeder PR, der `.claude/agents/**`, `.claude/skills/**`, `.claude/hooks/**` oder `.claude/settings*.json` berührt, ist rot, ohne Ausnahme. Die geänderten Dateien kommen aus einem lokalen `git diff --no-renames --name-only origin/main...<sha>` (eine Umbenennung aus einem Sperrpfad heraus zählt am alten Pfad; die API-Dateiliste kann gekappt sein), verglichen ohne Unterschied der Groß- und Kleinschreibung. **Arbeitskopie-Abgleich:** Vor dem Merge prüft das Skript zusätzlich jeden Eintrag von `git worktree list` auf geänderte oder ungetrackte Dateien unter den Sperrpfaden und auf `disableAllHooks` ([leitplanken.md](leitplanken.md)). | Ein PR, der seinen eigenen Prüfer abschwächt; eine Session, die ihn in der Arbeitskopie abschwächt |
| G-5 | Jeder Pflicht-Check meldet ein **Lebenszeichen** mit Zahl > 0 (Tests gesammelt, Dateien geprüft). | Ein Wächter, der nichts geprüft hat |
| G-6 | Der letzte Lauf auf `main` ist grün. Steht `main` rot, mergt das Skript nur PRs mit dem Label `nacharbeit`. | Aufbau auf einem kaputten Stand |
| G-7 | **Werkstatt-PR:** (a) Ändert ein PR eine Datei der Werkstatt-Pfadliste (Workflows, Wächter, Listen, Merge-Skript), ändert er keine andere. (b) Eine Lockerung geht nur in einem Werkstatt-PR mit **genau einem** neuen Eintrag in der Abweichungsliste (gelockerte Stelle, welcher Fehler wieder möglich wird, Grund, Ersatz). (c) Ein Wert, den eine Entscheidung festlegt, ist nie so lockerbar. (d) Rechte, Agents und Hooks mergt das Skript nie. | Lockerung, die mit dem Code landet, der sie braucht; Lockerung ohne Begründung |
| G-8 | **Gate:** Zur PR-Kopf-SHA steht genau ein Gate-Marker, er sagt „ja" und hat einen Prüfumfang mit echtem Inhalt (nicht nur Satzzeichen oder Markup), stammt von einem Konto der Erlaubnisliste der Gate-Autoren, **und** im PR stehen über alle SHAs höchstens ein „nein". Zwei Marker zur selben SHA sind rot. Ausgenommen nur Dependabot-PRs (Login `dependabot[bot]` oder `app/dependabot`) außerhalb der Werkstatt-Pfadliste. | Ein PR, dessen Prüfung „nein" sagte oder nie lief; Neulauf bis „ja" |

**Nach dem Merge** läuft dieselbe Pipeline auf `main`. Sie prüft zusätzlich jeden neuen Commit der
First-Parent-Linie: Er muss ein Merge-Commit mit der Zeile `Gemergt-durch: merge-gruen <sha>` sein
(Merge-Vermerk), und `<sha>` muss sein zweiter Elternteil sein (`$c^2`, der gemergte PR-Kopf).
Ein direkter Push, ein Squash- oder Rebase-Merge, ein fehlender oder abweichender Vermerk machen
den Lauf rot. Beim ersten Push (`before` = Nullen) beginnt die Prüfung am Startpunkt: dem Vorgänger
des letzten Setup-Commits, mit dem der Aufsetz-Block die Prüfung scharf schaltet. Das erkennt
einen Merge am Skript vorbei, den eine Deny-Regel allein nicht verhindert (`gh api -X PUT …/merge`
oder ein Subprozess umgehen ein Befehlsmuster). Einzige Ausnahme: ein direkter Commit des Menschen
an den Sperrpfaden, signiert mit seinem Schlüssel ([schutz-und-deploy.md](schutz-und-deploy.md)).

**Wie das Skript seine eigene Änderung erlebt:** Ein PR, der Skript, Liste oder Wächter ändert,
wird noch nach der alten Fassung aus `main` geprüft. Die Schärfung wirkt ab dem Merge. Im ersten
Werkstatt-Block ist `main` leer, dort gilt die Regel noch nicht.

## Wächter gegen aufgeweichte Tests

Teil von G-4. Er vergleicht den PR-Diff mit `origin/main` und ist rot bei: neuem `skip`/`skipif`/
`xfail` außerhalb der Erlaubnisliste; neuem `noqa`, `type: ignore`, `pragma: no cover`; einer
gelöschten Testfunktion (Vergleich über den Namen, nicht die Zahl); einer Testfunktion, deren
Asserts auf null sinken; einer gesenkten Schwelle; einer Lockerung in `.github/workflows/**`
(Pflicht-Job oder Schritt entfernt, `continue-on-error`, `if:` an einem Pflicht-Job, `runs-on`
außerhalb der Erlaubnisliste); jeder Änderung an den Sperrpfaden.

Wie er eine Lockerung in einer Workflow-Datei oder ein entferntes Assert erkennt (AST oder Text),
ist **offen** — die Probe-PRs sind das Abnahmekriterium, nicht das Verfahren.

## Das Gate: blockierend mit SHA-Bindung

**Warum blockierend:** Kosten sind gleich, ob das Skript das Urteil verlangt oder nicht — das Gate
läuft ohnehin. Ein Urteil ohne Wirkung wäre ein Nachweis ohne Wirkung auf das Gate selbst.

**SHA-Bindung:** Das Urteil gilt für genau eine SHA. Ein neuer Push macht es wertlos. Ein
LLM-Urteil ist nicht reproduzierbar; es gilt als Artefakt der SHA, und pro SHA zählt genau ein
Marker.

**Die Regel „zwei Nein":** Ein „nein" zur Kopf-SHA ist rot — beheben, neuer Push, neues Urteil. Ab
dem zweiten „nein" im selben PR ist der PR rot, auch wenn danach ein „ja" kommt. Kein Neulauf bis
„ja". Weiter geht es nur mit einem neuen PR mit neuem Zuschnitt.

**Stillstand statt Rückfrage:** Nach dem zweiten „nein" fragt die Bau-Session niemanden. Der PR
bleibt ungemergt, sie nimmt den nächsten Block, der nicht von ihm abhängt, und führt den PR in
ihrer Übergabe. Hängt der nächste Block davon ab, steht der Bau, bis der Mensch von außen
eingreift. Neu aufzumachen, wenn der Stillstand in der Rückschau mehr als einen Block je Woche
kostet (Bedingung der Quelle).

**Was das Gate prüft, in dieser Reihenfolge:** 0. das Protokoll der Umsetzer-Kette zum
Endstand-Baum-Hash; 1. Redundanz gegen den Bestand; 2. tote Pfade; 3. Abstraktionshöhe; 4. Layer
und Musterbruch; 5. Verstoß gegen eine Entscheidung oder Regel des Repos; 6. den
Sicherheitsbericht — jeder Befund behoben oder mit tragendem Vermerk, sonst blockierend. Es liest
PR-Beschreibung und Diff (`gh pr view`, `gh pr diff`), den Bericht des Umsetzers nicht zuerst, und
den Sicherheitsbericht zuletzt. Es urteilt und ändert nichts.

**Gate nicht in der CI:** Ein Claude-Lauf je PR kostet Geld, das beim Menschen liegt.

## Grenzen, offen benannt

- **Gate-Marker sind Selbstauskunft.** Den PR-Kommentar schreibt meist dieselbe Identität, die
  mergt. Die Erlaubnisliste der Gate-Autoren fängt nur Kommentare fremder Konten; schreibt das Gate
  unter dem Konto der Bau-Session, bleibt der Marker Selbstauskunft.
  Das Skript prüft Form, SHA und Zahl der Marker, nicht, dass ein unabhängiger Lauf stattfand.
  Marker sind löschbar; ob `main` gelöschte Marker eines gemergten PR nachträglich erkennen kann,
  ist nicht belegt.
- **Ein neuer PR beginnt die Nein-Zählung von vorn.** „Nein" zählt je PR. Ein neuer PR mit
  gleichem Diff beginnt bei null. Die Rückschau sucht gemergte PRs, deren Diff einem PR mit zwei
  „nein" gleicht (Vorschlag: gleiche `git patch-id --stable` oder gleiche Dateimenge mit
  überlappenden Hunks).
- **Stillstand ist das Risiko.** Ein Gate, das fälschlich blockiert, hält den Bau an.
- **Abweichungseinträge sind Selbstauskunft.** Eine Lockerung in einer Workflow-Datei, die der
  Wächter nicht als solche erkennt, landet mit einem Werkstatt-PR. Das fangen Merge-Vermerk,
  Rework Rate und Rückschau; eine Sperre ist das nicht.
- **Abnick-Risiko.** Ein Gatekeeper kann abnicken. Gegenmittel: nichtleerer Prüfumfang, Probe-PRs,
  Rückschau, Rework Rate.

## Feuert-Nachweis des Merge-Skripts

Je G-Punkt eine Probe, die den Merge verweigert: fehlender Check (G-1), veraltete SHA (G-2), Kopf
ohne aktuellen `main` (G-3), PR lockert den Wächter oder berührt einen Sperrpfad (G-4), Check mit
null geprüften Einheiten (G-5), `main` rot und PR ohne Label (G-6), Werkstatt-PR mit Produktdatei
oder Lockerung ohne Eintrag (G-7), Gate-Urteil fehlt, zu alter SHA, „nein", ohne Prüfumfang,
zweimal „nein" dann „ja", zwei Marker zur selben SHA (G-8). Negativkontrolle: ein sauberer PR mit
„ja" wird gemergt. Die Proben laufen in einem Wegwerf-Repo mit dem Skript im Prüfmodus ohne Merge.

## Kennzahl: Rework Rate

Anteil gemergter PRs mit Label `nacharbeit`, die einen Fehler eines schon gemergten PR beheben.
Trend, kein Benchmark. Sie ist der Beleg dafür, ob „grün heißt mergen" trägt. Das Label setzt der
Umsetzer selbst — auch das ist Selbstauskunft.
