# Deadlands Characters

Charaktere fuer Deadlands: The Weird West (Savage Worlds Adventure Edition).

## Aufbau

| Pfad | Inhalt |
| --- | --- |
| [`Charakterideen.md`](Charakterideen.md) | Übersicht: alle 13 Archetypen mit je 2 Figuren, dazu das Einsteiger-Set aus 6 weiteren |
| [`Regelnotizen.md`](Regelnotizen.md) | Regelkorrekturen und Novize-Fallen, die für alle Builds gelten |
| [`Bildprompts.md`](Bildprompts.md) | Ein Midjourney-8.2-Prompt pro Figur, plus Stilklammer für den ganzen Satz |
| `Charaktere/` | Eine Datei pro Figur (32) — Hintergrund, Build, Aufhänger |
| `Archetypen/` | Eine Datei pro Archetyp (13) — Voraussetzungen, archetyp-spezifische Regelnotizen |
| `Bilder/` | Die fertigen Midjourney-Bilder, flach, benannt wie die Charakterdateien |
| [`Abenteuer/`](Abenteuer/index.html) | Spielleiter-Abläufe zu One-Sheets, deutsch, Szene für Szene |
| `build_html.py` | Rendert jede `.md` als `.html` daneben |
| `build_sheets.py` | Füllt den offiziellen Deadlands-Charakterbogen aus |
| `build_dossier.py` | Deckblatt, Hintergrund, Regeltexte und Bogen als ein PDF |
| `CharacterSheetsPdf/` | Die fertigen Bögen, je Figur einer plus `Auswahl.pdf` |
| [`CLAUDE.md`](CLAUDE.md) | Konventionen, Werkzeugfallen und offene Punkte — für Claude Code |

Jede Markdown-Datei liegt zusätzlich als HTML daneben — gleicher Name, Endung
`.html`, interne Links sind mitgebogen. Die Seiten sind eigenständig (CSS
eingebettet, keine externen Ressourcen), hell/dunkel je nach Systemeinstellung
und drucken sauber, falls jemand am Tisch Papier bevorzugt. Einstieg zum
Blättern: [`Charakterideen.html`](Charakterideen.html).

Nach Änderungen an den Markdown-Dateien neu erzeugen mit:

```
python build_html.py
```

Einzige Abhängigkeit: `pip install markdown`.

## Charakterbögen zum Ausdrucken

Wer am Tisch Papier braucht, lässt die Figuren in den offiziellen Bogen
schreiben:

```
python build_sheets.py              # die Auswahl, die oben im Skript steht
python build_sheets.py 11-1 01-2    # einzelne Figuren
```

Das Skript liest dieselben Markdown-Dateien — Attribute, Fertigkeiten,
Handicaps und Talente aus dem ` ```build `-Block, Ausrüstung und Waffen aus
` ```gear `, Mächte aus ` ```powers ` — und legt je Figur einen ausfüllbaren
Bogen in `CharacterSheetsPdf/` ab, dazu ein `Auswahl.pdf` mit allen Seiten zum
Ausdrucken. Das Startgeld rechnet es selbst nach und meldet, wenn eine Figur
über 250 Dollar liegt. Zusätzliche Abhängigkeit: `pip install pymupdf`.

Auf dem Bogen stehen Attribute, Fertigkeiten und Mächte englisch, Talente und
Handicaps englisch mit dem deutschen Begriff in Klammern, Ausrüstung und Waffen
deutsch.

## Dossiers

Für den Spieltisch gibt es je Figur eine komplette Mappe in einem PDF —
Deckblatt mit Porträt und Namen in Western-Schrift, danach die
Hintergrundgeschichte mit dem wörtlichen Regeltext zu jedem Talent und
Handicap (samt Buch und Seitenzahl), zuletzt der ausgefüllte Charakterbogen:

```
python build_dossier.py
```

Die Regeltexte werden bei jedem Lauf aus den lokalen Regelwerk-PDFs gelesen und
liegen nicht im Repo.

Wie dicht gesetzt wird, entscheidet das Skript je Figur: Es nimmt den größten
Satzfaktor, der noch mit der kleinsten Seitenzahl auskommt. So bleibt keine
fast leere Seite übrig, die im Druck ein volles Blatt kosten würde — der Lauf
meldet den Faktor hinter der Seitenzahl, wenn er von 100 % abweicht.

Alle Builds sind **Novize** nach Standard-Erschaffung: 5 Attributspunkte,
12 Fertigkeitspunkte, bis zu 4 Handicap-Punkte, 250 Dollar Startgeld.
Talente und Handicaps sind englisch benannt, mit dem **gedruckten** deutschen
Begriff in Klammern — aus dem Grundbuch für die Deadlands-eigenen, aus dem
deutschen SWADE-Grundregelwerk für den Rest. Jeder dieser Begriffe ist mit
Seitenzahl belegt (`Regelnotizen.md`); selbst übersetzt wird nichts.

Regelbasis: `Deadlands_Grundbuch.pdf` (Ulisses, deutsch), das deutsche
`Savage Worlds Abenteuer Edition` Grundregelwerk (Ulisses) und
`SWADE_Savage_Worlds_Adv_Ed_Core_Rules.pdf` (englisch) — alle liegen lokal im
Repo, sind aber per `.gitignore` ausgeschlossen.

## Abenteuer

Im Ordner [`Abenteuer/`](Abenteuer/index.html) liegen Spielleiter-Abläufe zu
englischen One-Sheets, aufbereitet für den deutschen Tisch: Szene für Szene,
Vorlesetexte übersetzt, Statblocks dort abgedruckt, wo die Szene sie braucht,
Regelverweise auf *Der Unheimliche Westen* und die *Abenteuer-Edition* mit
Seitenzahl. Eigene Ergänzungen sind als solche markiert.

- [**Dead Men Walkin'**](Abenteuer/Dead-Men-Walking_SL-Ablauf.html) von Shane Lacy
  Hensley — sieben Szenen auf den High Plains, mit geplantem TPK in den ersten
  20 Minuten und einem Runde für Runde durchgespielten Beispielkampf.
- [**… bist das du?**](Abenteuer/Is-That-You_SL-Ablauf.html) von Matthew Cutter —
  sechs Szenen in Roswell: eine Sturmnacht, ein Gestaltwandler am Ofen und eine
  Sturzflut. Kein Kampf bis zum Schluss.

Diese Seiten sind von Hand geschrieben, nicht aus Markdown erzeugt —
`build_html.py` fasst sie nicht an. Die Quell-PDFs der One-Sheets bleiben per
`.gitignore` draußen.

## Vor Sitzung eins besprechen

Zwei Punkte im Grundbuch, die eine Tischabsprache verdienen:

- **Sitting Bull** ist im Setting der heimliche Anführer der Ravenites (S. 131) —
  eine reale, verehrte historische Person mit lebenden Nachfahren, zum Verräter
  umgedeutet. Ein fiktiver Ravenite-Anführer ist trivial einzusetzen.
- **Kriegsherr Kang** (S. 119 ff.) ist Fu Manchu mit Eisenbahnkonzession. Wenn
  die einzigen NSCs gleicher Herkunft für einen chinesischen SC Kangs Leute
  sind, hat das Spiel den Archetyp still zur Verwandtschaft des Bösewichts
  gemacht. Gegengewichte stehen im Buch: China Mary in Tombstone (S. 137),
  Deadwoods Chinatown (S. 132), Olympia (S. 123).

Details dazu stehen in den jeweiligen Archetyp-Dateien
([Schamanen](Archetypen/08-shaman.md), [Chi-Meister](Archetypen/11-chi-master.md),
[Krieger](Archetypen/12-warrior.md)).

