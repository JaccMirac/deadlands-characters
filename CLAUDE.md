# CLAUDE.md

Handreichung für eine Sitzung, die dieses Repo zum ersten Mal sieht.

## Was das hier ist

Spielleiter-Vorbereitung für eine Runde **Deadlands: The Weird West** auf
**SWADE**. Kein Code-Projekt — der Inhalt sind Charaktere, der einzige Code ist
ein kleiner Renderer. 13 Archetypen, je 2 Figuren, dazu ein Einsteiger-Set aus
sechs weiteren Figuren, macht 32 Charaktere. Alles
auf Deutsch, weil am Tisch Deutsch gesprochen wird.

Einstieg zum Lesen: [`Charakterideen.md`](Charakterideen.md) — die Übersicht,
von der alles verlinkt ist.

| Pfad | Inhalt |
| --- | --- |
| `Charakterideen.md` | Inhaltsverzeichnis aller 32 Figuren, nach Archetyp |
| `Regelnotizen.md` | Regelkorrekturen, die für **alle** Builds gelten |
| `Bildprompts.md` | Ein Midjourney-Prompt je Figur + Stilklammer |
| `Charaktere/NN-N-slug.md` | Eine Datei je Figur — Hintergrund, Build, Aufhänger |
| `Archetypen/NN-slug.md` | Eine Datei je Archetyp — Voraussetzungen, Fallen |
| `Bilder/NN-N-slug.png` | Die Midjourney-Bilder, flach, benannt wie die Figuren |
| `build_html.py` | Rendert jede `.md` als `.html` daneben |
| `build_sheets.py` | Trägt Figuren in den offiziellen Charakterbogen ein |
| `build_dossier.py` | Deckblatt + Hintergrund + Regeltexte + Bogen als ein PDF |
| `CharacterSheetsPdf/` | Die fertig ausgefüllten Bögen (gitignoriert) |

## Regeln, die nicht verhandelbar sind

**Jede `.md` hat eine `.html` daneben.** Nach *jeder* Änderung an einer
Markdown-Datei:

```
python build_html.py
```

Beides wird zusammen committet. Eine `.md` ohne aktuelle `.html` gilt als
kaputt. Einzige Abhängigkeit: `pip install markdown`.

**Die PDFs gehören nicht ins Repo.** `Deadlands_Grundbuch.pdf`,
`SWADE_…_Core_Rules.pdf`, das deutsche `US85001PDF_Savage_Worlds_Abenteuer_
Edition…pdf`, `Deadlands_Character_Sheet.pdf`, `Pregens_Deadlands01.pdf`,
`DLR_Dead_Men_Walking.pdf` und die englische
`0-deadlands-the-weird-west…pdf` liegen lokal im Ordner und sind per `.gitignore`
(`*.pdf`) ausgeschlossen. Sie sind gekaufte, urheberrechtlich geschützte
Bücher — **nie stagen, nie committen, nie irgendwohin hochladen.** Sie dienen
ausschließlich zum Nachschlagen. Das Remote ist deshalb auch privat.

**Sprache.** Fließtext deutsch. Talente und Handicaps stehen **englisch**, mit
dem deutschen Buchbegriff in Klammern: `**Quick Draw** (*Schnell Ziehen*)`.
Seit das **deutsche SWADE-Grundregelwerk** vorliegt, ist jeder Begriff in der
`DE`-Tabelle von `build_sheets.py` belegt — Grundbuch für die Deadlands-eigenen
Talente, deutsches SWADE für den Rest, Seitenzahl je als Kommentar daneben.
**Nichts dort wird selbst übersetzt.** Wer ein neues Talent aufnimmt, schlägt
den gedruckten Begriff nach; findet er keinen, bleibt der Eintrag auf `False`
und die Klammer entfällt, statt eine Laienübersetzung zu erfinden.

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

**Der fest verdrahtete Repo-Pfad ist weg.** Beide Skripte leiten `REPO` aus
`__file__` ab und laufen damit dort, wo sie liegen. Geblieben ist die zweite
Hälfte der Falle: der Glob deckt nur `*.md` im Wurzelverzeichnis, `Archetypen/`
und `Charaktere/` ab — eine neue `.md` in einem *anderen* Unterordner bekommt
still keine HTML.

**In der Talentspalte des Bogens sind nur die ersten fünf Zeilen frei.** Ab der
sechsten beginnt die vorgedruckte Aufstiegsspur (`N N N S S S S V V V V …`),
die dem Spieler gehört. `build_sheets.py` kappt dort und schiebt den Rest zur
Ausrüstung, statt über die Spur zu drucken (`EDGE_ZEILEN`).

**Die Deadlands-Bände setzen ihre Einträge als GROSSBUCHSTABEN-Überschrift.**
Wer in den PDFs nach einem Talent sucht, muss ohne Rücksicht auf Groß- und
Kleinschreibung suchen (`re.I`). Eine Suche nach `Galgenhumor` findet
`GALGENHUMOR` **nicht** — das hat schon einmal dazu geführt, ein völlig
korrektes Talent für erfunden zu halten. `build_dossier.py` sucht deshalb
grundsätzlich `re.I`.

**Der PDF-Textextrakt bricht Überschriften auf zwei Arten kaputt.** Erstens
schiebt er in manchen SWADE-Überschriften ein Leerzeichen hinter das ß —
gedruckt steht *Außenseiter (leicht oder schwer)*, extrahiert kommt
`Auß enseiter`. Zweitens brechen lange Grundbuch-Überschriften mitten im Namen
um: `ARKANER HINTERGRUND (VERRÜCKTER` / `WISSENSCHAFTLER)`. Beide Fälle lassen
eine wörtliche Zeilensuche ins Leere laufen und den Eintrag still auf die
englische Quelle zurückfallen. `suche_eintrag` erlaubt deshalb ein optionales
Leerzeichen hinter ß und einen Zeilenumbruch an jeder Lücke im Namen.

**Der Name über einem Werteblock ist kein Regeleintrag.** Im Grundbuch steht
auf S. 148 der NSC-Archetyp `KAMPFKÜNSTLER` — die Suche nach dem Talent
*Kampfkünstler* landete dort und zog Attribute und Ausrüstung eines
Statisten ins Dossier. `suche_eintrag` bevorzugt darum Funde mit
Voraussetzungen-Zeile (Talente) oder Schweregrad in Klammern (Handicaps) und
meldet es, wenn sie auf einen Fund ohne beides zurückfallen muss.

**Die gedruckte Seitenzahl ist nicht der PDF-Index.** Grundbuch und deutsches
SWADE ±0, aber englisches SWADE und die englische Deadlands-Ausgabe liegen um
−1 daneben. Die Offsets stehen in
`QUELLEN` in `build_dossier.py`; wer eine Seitenzahl von Hand zitiert, prüft
sie am Fuß der Seite nach.

**Die Formularfelder sind Helvetica/WinAnsi.** Chinesische oder japanische
Schrift im Titel (`林亞元`) kann dort nicht stehen; sie wird entfernt und
gemeldet. Für den Bogen zählt der lateinische Name.

**Smartypants frisst `--`.** Der Renderer läuft mit der `smarty`-Erweiterung,
die doppelte Bindestriche zu Halbgeviertstrichen macht. In Codeblöcken tut sie
das nachweislich *nicht*, und genau darauf verlassen sich die 33
Midjourney-Prompts, deren Parameter (`--ar 2:3 --stylize 150`) sonst lautlos
unbrauchbar würden. **Prompts gehören deshalb immer in einen Fenced Code
Block.** Nach Änderungen an `Bildprompts.md` gegenprüfen:

```
grep -c -- "--ar 2:3 --stylize 150" Bildprompts.html   # muss 33 sein
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
Edges: Arcane Background (Blessed) [free: Human] | Champion [Hindrance] | Guts [Hindrance]
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

## Der Ausrüstungsblock und der PDF-Bogen

Neben ` ```build ` trägt eine Figur, die auf einen Bogen soll, zwei weitere
optionale Blöcke. `build_sheets.py` schreibt daraus den offiziellen
`Deadlands_Character_Sheet.pdf` voll, `build_html.py` hängt dieselben Daten als
Tabellen unter die Charakterbogen-Karte. Beide lesen denselben Parser
(`parse_sections` in `build_html.py`) und rechnen mit derselben Geldfunktion —
**der Block listet Preise, das Skript summiert sie.**

```
Start: 250
Nickname: Uncle Lam
Ausrüstung:
- Arzttasche | $10 | 3 | freie Wiederholung auf Heilen, 5 Anwendungen
- Maultier | $50 | –
Waffen:
- Messer | 3/6/12 | Stä+W4 | – | 1 | 0,5 | $2 | auch als Wurfwaffe
Notizen:
- Wing Tsun: +1 Parade, –2 auf jeden erlittenen Nahkampfschaden
```

Spalten: Ausrüstung ist `Name | Kosten | Gewicht in kg | Anmerkung`, Waffen sind
`Name | Reichweite | Schaden | PB | FR | Gewicht | Kosten | Anmerkung`. Das
Gewicht trägt der Bogen nicht, es steht nur zur Kontrolle da. `Start:` ist
optional und steht sonst auf 250. Der ` ```powers `-Block sieht genauso aus:

```
Machtpunkte: 15
Mächte:
- Deflection | 3 | Self | 5 | attackers –2, –4 with a raise
```

**Sprachen auf dem Bogen**, so gewollt: Attribute, Fertigkeiten und Mächte
englisch, Talente und Handicaps englisch mit dem deutschen Begriff in Klammern
(`Vow (Schwur) — Major`), Ausrüstung und Waffen deutsch. Die deutschen Begriffe
stehen in der `DE`-Tabelle in `build_sheets.py`, jeder mit einem Flag, ob er im
Grundbuch **belegt** ist; unbelegte werden beim Bauen gemeldet, aber trotzdem
gesetzt. Neue Talente gehören dort ergänzt, mit Seitenzahl im Kommentar.

Aufruf:

```
python build_sheets.py              # die Liste AUSWAHL oben im Skript
python build_sheets.py 11-1 01-2    # diese Figuren (Präfix des Dateinamens)
python build_sheets.py --alle
```

Es entstehen ein ausfüllbarer Bogen je Figur und ein `Auswahl.pdf` über alle,
in dem die Formularfelder in die Seite gebacken sind — gleichnamige Felder auf
mehreren Seiten wären im AcroForm sonst *ein* Feld und würden sich gegenseitig
überschreiben. Zusätzliche Abhängigkeit: `pip install pymupdf`.

## Das Dossier (`build_dossier.py`)

Ein Dossier ist alles, was eine Figur am Tisch braucht, in **einem** PDF:

1. **Deckblatt** — das Porträt aus `Bilder/` groß, der Name in Playbill, der
   Archetyp und das Zitat. Trägt der Titel chinesische Schrift (`林亞元`),
   bekommt sie eine eigene Zeile in der CJK-Schrift, die PyMuPDF mitbringt.
2. **Hintergrund und Regeltexte** — die Abschnitte aus `ABSCHNITTE`, danach zu
   jedem Talent und Handicap der **wörtliche Eintrag aus dem Regelwerk**, mit
   Buch und gedruckter Seitenzahl darüber. Läuft über so viele Seiten, wie
   nötig.
3. **Der ausgefüllte Charakterbogen**, weiterhin ausfüllbar.

```
python build_dossier.py            # AUSWAHL aus build_sheets.py
python build_dossier.py 11-1
python build_dossier.py --en       # Regeltexte durchgehend englisch
```

**`ABSCHNITTE` ist die Gästeliste des Spielerhandouts.** Gedruckt werden
*Hintergrund*, *Die Rechnung*, *Am Tisch*, *Warum es Spaß macht* und
*Die Machtliste* — in dieser Reihenfolge, Nachschlageteile also hinten.
Ein Abschnitt, der nicht in der Liste steht, erscheint nur in der `.md`
und ihrer `.html`; genau das ist der Ablageort für Marshal-Material
(`**Mr. Pettibone.**` bei 05-1). Die Überschrift muss dafür exakt so
heißen wie der Eintrag in `ABSCHNITTE` — `**Am Tisch.**`, nicht
`**Am Tisch — in fünf Schritten.**`, sonst greift der Abgleich nicht.
Aufzählungszeilen (`- …`) in diesen Abschnitten setzt `md_zu_html` als
echte Punkte.

**`**Aufhänger**` steht bewusst nicht in `ABSCHNITTE`.** Dort stehen die
Enthüllungen und ausdrückliche Marshal-Hinweise; das Dossier ist als
Spielerhandout gedacht. Wer eine Marshal-Mappe will, trägt ihn dort ein.

**Kein Regeltext und keine Schrift liegen im Repo.** Die Einträge werden bei
*jedem* Lauf frisch aus den lokalen PDFs gezogen, Playbill wird aus
`C:\Windows\Fonts` gelesen. Das ist Absicht und gehört zur PDF-Regel oben:
was hier entsteht, ist gitignoriert (`*.pdf`), und im Repo landet nur der Code,
der es erzeugt. Fehlt eine Quelle, sagt das Skript das, statt still etwas
anderes zu setzen — ein nicht gefundener Eintrag wird auf der Seite rot als
fehlend markiert und nicht erfunden.

**Sprache der Regeltexte:** `SPRACHE = "quellentreu"` nimmt den deutschen
Buchtext, wo es einen gibt — das sind genau die Deadlands-*eigenen* Einträge
(Arkaner Hintergrund (Chi-Meister), Überlegenes Kung Fu, Galgenhumor) — und
sonst den englischen aus SWADE. `--en` schaltet auf durchgehend englisch.

## Was als Nächstes ansteht

Erledigt: 31 der 32 Figurenbilder liegen in `Bilder/` (dazu das NSC-Porträt
`05-1-mr-pettibone.png`), und `build_html.py` setzt beim Rendern von
`Charaktere/X.md` ein vorhandenes `Bilder/X.png` als Porträt unter den Titel
(`figure.portrait`). **Es fehlen noch zwei:** `07-3-patience-ludlow-die-quakerin`
und `13-3-josephine-jo-pike-die-wanderfotografin`; die Prompts stehen bereit.

1. **Die Stilklammer ist noch nicht gesetzt.** Der Plan steht in
   `Bildprompts.md`: einen Prompt laufen lassen, vom schönsten Ergebnis den
   `--sref`-Code ziehen, ihn an *alle* 33 anhängen. Solange das nicht passiert
   ist, sind die Bilder Einzelstücke statt eines Kartensatzes. Ob die
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
Zitat, ` ```build `-Block (bei Figuren mit Bogen gefolgt von ` ```gear ` und
ggf. ` ```powers `), Hintergrund, **Build**, **Aufhänger**,
**Warum es Spaß macht**.

Was regeltechnisch behauptet wird, muss aus dem Grundbuch oder den Core Rules
belegbar sein; im Zweifel im PDF nachschlagen, nicht aus dem Gedächtnis
schreiben. Falsche Voraussetzungen sind hier der teuerste Fehler, weil sie erst
am Spieltisch auffallen.

Committet wird auf `master`, Remote ist `origin`
(github.com/JaccMirac/deadlands-characters, privat).
