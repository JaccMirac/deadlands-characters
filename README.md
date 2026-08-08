# Deadlands Characters

Charaktere fuer Deadlands: The Weird West (Savage Worlds Adventure Edition).

## Aufbau

| Pfad | Inhalt |
| --- | --- |
| [`Charakterideen.md`](Charakterideen.md) | Übersicht: alle 13 Archetypen mit je 2 Figuren, verlinkt |
| [`Regelnotizen.md`](Regelnotizen.md) | Regelkorrekturen und Novize-Fallen, die für alle Builds gelten |
| `Charaktere/` | Eine Datei pro Figur (26) — Hintergrund, Build, Aufhänger |
| `Archetypen/` | Eine Datei pro Archetyp (13) — Voraussetzungen, archetyp-spezifische Regelnotizen |
| `build_html.py` | Rendert jede `.md` als `.html` daneben |

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

Alle Builds sind **Novize** nach Standard-Erschaffung: 5 Attributspunkte,
12 Fertigkeitspunkte, bis zu 4 Handicap-Punkte, 250 Dollar Startgeld.
Talente und Handicaps sind englisch benannt, mit dem deutschen Begriff aus dem
Grundbuch in Klammern, wo das Grundbuch einen führt.

Regelbasis: `Deadlands_Grundbuch.pdf` (Ulisses, deutsch) und
`SWADE_Savage_Worlds_Adv_Ed_Core_Rules.pdf` (englisch) — beide liegen lokal im
Repo, sind aber per `.gitignore` ausgeschlossen.

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
