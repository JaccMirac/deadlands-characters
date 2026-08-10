# CLAUDE.md

Handreichung für eine Sitzung, die dieses Repo zum ersten Mal sieht.

## Was das hier ist

Spielleiter-Vorbereitung für eine Runde **Deadlands: The Weird West** auf
**SWADE**. Kein Code-Projekt — der Inhalt sind Charaktere, der einzige Code ist
ein kleiner Renderer. 13 Archetypen, je 2 Figuren, macht 26 Charaktere. Alles
auf Deutsch, weil am Tisch Deutsch gesprochen wird.

Einstieg zum Lesen: [`Charakterideen.md`](Charakterideen.md) — die Übersicht,
von der alles verlinkt ist.

| Pfad | Inhalt |
| --- | --- |
| `Charakterideen.md` | Inhaltsverzeichnis aller 26 Figuren, nach Archetyp |
| `Regelnotizen.md` | Regelkorrekturen, die für **alle** Builds gelten |
| `Bildprompts.md` | Ein Midjourney-Prompt je Figur + Stilklammer |
| `Charaktere/NN-N-slug.md` | Eine Datei je Figur — Hintergrund, Build, Aufhänger |
| `Archetypen/NN-slug.md` | Eine Datei je Archetyp — Voraussetzungen, Fallen |
| `Bilder/NN-N-slug.png` | Die Midjourney-Bilder, flach, benannt wie die Figuren |
| `build_html.py` | Rendert jede `.md` als `.html` daneben |

## Regeln, die nicht verhandelbar sind

**Jede `.md` hat eine `.html` daneben.** Nach *jeder* Änderung an einer
Markdown-Datei:

```
python build_html.py
```

Beides wird zusammen committet. Eine `.md` ohne aktuelle `.html` gilt als
kaputt. Einzige Abhängigkeit: `pip install markdown`.

**Die PDFs gehören nicht ins Repo.** `Deadlands_Grundbuch.pdf`,
`SWADE_…_Core_Rules.pdf`, `Deadlands_Character_Sheet.pdf`,
`Pregens_Deadlands01.pdf` liegen lokal im Ordner und sind per `.gitignore`
(`*.pdf`) ausgeschlossen. Sie sind gekaufte, urheberrechtlich geschützte
Bücher — **nie stagen, nie committen, nie irgendwohin hochladen.** Sie dienen
ausschließlich zum Nachschlagen. Das Remote ist deshalb auch privat.

**Sprache.** Fließtext deutsch. Talente und Handicaps stehen **englisch**, mit
dem deutschen Grundbuch-Begriff in Klammern:
`**Quick Draw** (*Schnell Ziehen*)`. Die Klammer entfällt, wo das Grundbuch
keinen eigenen deutschen Begriff führt — siehe die Warnung am Ende von
`Regelnotizen.md`, die deutschen Namen sind nur für die Deadlands-*eigenen*
Neuzugänge belegt.

**Alle Builds sind Novize**, Standard-Erschaffung: 5 Attributspunkte,
12 Fertigkeitspunkte, bis zu 4 Handicap-Punkte, **250 Dollar** Startgeld
(Deadlands weicht hier von SWADE ab). Wer einen Build anfasst, liest vorher
`Regelnotizen.md` ganz — dort steht gesammelt, welche Talente entgegen der
üblichen Netzlisten erst ab Erfahren oder Fortgeschritten verfügbar sind.
Mehrere dieser Fallen wurden teuer gefunden; sie wieder einzubauen ist der
wahrscheinlichste Fehler.

**Dateinamen.** `NN-N-slug` — Archetypnummer, Figurnummer, Slug ohne Umlaute
und Sonderzeichen (`ü`→`u`, nicht `ue`; siehe
`06-2-delphine-della-tourneur-die-unterstutzungsschutzin.md`). Der Bildname ist
derselbe Name mit `.png`. Weitere Fassungen bekommen `-b`, `-c`; **der Name
ohne Buchstaben ist immer die gültige Fassung.**

## Fallen im Werkzeug

**`build_html.py` hat den Repo-Pfad fest verdrahtet** (`REPO = r"D:\DnD\…"`).
Auf einem anderen Rechner oder nach einem Umzug des Ordners muss die Zeile
angepasst werden, sonst schreibt das Skript ins Leere oder bricht ab. Der
Glob deckt nur `*.md` im Wurzelverzeichnis, `Archetypen/` und `Charaktere/` ab
— eine neue `.md` in einem *anderen* Unterordner bekommt still keine HTML.

**Smartypants frisst `--`.** Der Renderer läuft mit der `smarty`-Erweiterung,
die doppelte Bindestriche zu Halbgeviertstrichen macht. In Codeblöcken tut sie
das nachweislich *nicht*, und genau darauf verlassen sich die 26
Midjourney-Prompts, deren Parameter (`--ar 2:3 --stylize 150`) sonst lautlos
unbrauchbar würden. **Prompts gehören deshalb immer in einen Fenced Code
Block.** Nach Änderungen an `Bildprompts.md` gegenprüfen:

```
grep -c -- "--ar 2:3 --stylize 150" Bildprompts.html   # muss 26 sein
grep -c "&ndash;ar" Bildprompts.html                   # muss 0 sein
```

Ebenfalls schon repariert und nicht wieder kaputtmachen: das `re.sub` auf
`&lsquo;(?=\d)`, das aus Jahreszahlen wie ’84 wieder einen Apostroph macht.

## Der Baukasten-Block (Charakterbogen)

Jede Figurendatei trägt direkt vor `**Hintergrund.**` einen Fenced Block
` ```build `, aus dem `build_html.py` eine Charakterbogen-Karte rendert
(Attribut- und Fertigkeitstabelle mit **berechneten Punktkosten**, abgeleitete
Werte, Handicap-/Talent-Kontobuch). Format:

```
Attributes: Agility d6, Smarts d4, Spirit d8, Strength d6, Vigor d6
Skills: Faith d8, Fighting d8, Athletics d6, Notice d6, Shooting d4, Occult d4
Hindrances: Vow (Major), Outsider (Minor), Talisman (Minor)
Edges: Arcane Background (Blessed) [free: Human] | Champion [Hindrance] | Grit [Hindrance]
```

Die mechanischen Begriffe stehen **englisch** (SWADE-Terminologie, passend zum
englischen Regelwerk in `Referenzen/`). Der Renderer normalisiert allerdings auch
deutsche Eingaben — `Geschicklichkeit`, `Kämpfen`, `(schwer)` usw. werden erkannt
und trotzdem englisch angezeigt; die Schlüssel gehen deutsch (`Attribute`,
`Fertigkeiten`, `Handicaps`, `Talente`) wie englisch. Neue Blöcke bitte trotzdem
gleich englisch schreiben.

Wichtig — **der Block transkribiert nur Würfel, er rechnet nicht.** Die gesamte
Kostenlogik (Attributskosten, die „2 Punkte je Stufe über dem Attribut"-Regel,
Kernfertigkeiten gratis, Parry/Toughness) lebt zentral in `build_html.py`.
Das ist Absicht: frühere Audits scheiterten reihenweise an Handrechnung. Regeln:

- **Attribute** immer alle fünf, in fester Reihenfolge: Agility, Smarts, Spirit,
  Strength, Vigor.
- **Würfel effektiv vs. gekauft:** trage den *mit Punkten gekauften* Basiswürfel
  ein, nicht den durch ein Talent erhöhten (z.B. Harrowed mit „Supernatural
  Attribute": Basis `Strength d6`, nicht `d10`).
- **Optionale Zeilen** im selben Block: `Bonus: N` (zusätzliche
  Fertigkeitspunkte, z.B. +5 aus *Elderly* oder +1 aus einem Handicap-Punkt),
  `Pace: N`, `Armor: N` (hebt Toughness), sowie `Parry:`/`Toughness:` als
  Freitext-Override für Boni, die *keine* Punktkäufe sind (Undead +2, Size +1).
- Der Renderer **warnt** beim Bauen über unbekannte Fertigkeitsnamen und
  fehlende Attribute; das Punkte-Badge wird **rot**, wenn ein Budget
  *überzogen* ist (Unterschreiten ist erlaubt und bleibt neutral). Neue
  Fertigkeitsnamen gehören in die `SKILL_LINK`-Tabelle in `build_html.py`.

## Was als Nächstes ansteht

Erledigt: alle 26 Bilder liegen in `Bilder/`, und `build_html.py` setzt beim
Rendern von `Charaktere/X.md` ein vorhandenes `Bilder/X.png` als Porträt unter
den Titel (`figure.portrait`).

1. **Die Stilklammer ist noch nicht gesetzt.** Der Plan steht in
   `Bildprompts.md`: einen Prompt laufen lassen, vom schönsten Ergebnis den
   `--sref`-Code ziehen, ihn an *alle* 26 anhängen. Solange das nicht passiert
   ist, sind die Bilder 26 Einzelstücke statt eines Kartensatzes. Ob die
   vorhandenen Bilder danach neu gezogen werden müssen, ist eine offene
   Entscheidung.
2. **Zwei Tischabsprachen sind offen**, beschrieben am Ende von `README.md`:
   die Sitting-Bull-Umdeutung im Grundbuch und Kriegsherr Kang als einziger
   prominenter chinesischer NSC. Beide brauchen eine Entscheidung des
   Spielleiters, keine Datei.

## Arbeitsweise

Die Charakterdateien sind dicht und eigenwillig geschrieben — konkrete
Gegenstände statt Adjektive (ein Wagenspeichen-Knüppel, sechs Löffelstiele zu
einem Pelikanschnabel gelötet, Kerben im Rückenriemen). Wer etwas ergänzt,
trifft diesen Ton, statt zu erklären. Der Aufbau je Figur ist immer gleich:
Zitat, ` ```build `-Block, Hintergrund, **Build**, **Aufhänger**,
**Warum es Spaß macht**.

Was regeltechnisch behauptet wird, muss aus dem Grundbuch oder den Core Rules
belegbar sein; im Zweifel im PDF nachschlagen, nicht aus dem Gedächtnis
schreiben. Falsche Voraussetzungen sind hier der teuerste Fehler, weil sie erst
am Spieltisch auffallen.

Committet wird auf `master`, Remote ist `origin`
(github.com/JaccMirac/deadlands-characters, privat).
