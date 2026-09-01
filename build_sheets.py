# -*- coding: utf-8 -*-
"""Traegt die Charakterdaten in den offiziellen Deadlands-Charakterbogen ein.

Quelle sind dieselben Markdown-Dateien wie fuer build_html.py: der ```build```-
Block liefert Attribute, Fertigkeiten, Handicaps und Talente, der optionale
```gear```-Block Ausruestung, Waffen und Kopfdaten, der optionale ```powers```-
Block die Maechte.

Die Wuerfel- und Kostenlogik wird aus build_html.py importiert -- sie lebt dort
und nur dort. Dieses Skript rechnet ausschliesslich das, was auf dem Bogen
steht und in build_html.py nichts zu suchen hat: die Dollarrechnung.

Aufruf:
    python build_sheets.py                 # rendert AUSWAHL
    python build_sheets.py 11-1 01-2       # rendert diese Figuren (Praefix)
    python build_sheets.py --alle          # rendert alle Charakterdateien

Abhaengigkeit: pip install pymupdf
"""
import io
import os
import re
import sys
import glob

import fitz  # PyMuPDF

import build_html as bh

REPO = os.path.dirname(os.path.abspath(__file__))
VORLAGE = os.path.join(REPO, "Deadlands_Character_Sheet.pdf")
AUSGABE = os.path.join(REPO, "CharacterSheetsPdf")

# Welche Figuren auf den Tisch kommen. Praefixe genuegen ("11-1"), der Rest
# des Dateinamens wird gesucht. Reihenfolge = Reihenfolge in Auswahl.pdf.
# Die sieben Einsteigerfiguren (siehe Charakterideen.md). Reihenfolge = Auswahl.pdf.
AUSWAHL = ["01-3", "02-3", "04-3", "05-1", "07-3", "12-3", "13-3"]

STARTGELD = 250.0        # Deadlands weicht hier von SWADE ab, Grundbuch S. 25
BENNIES = "3"
EDGE_ZEILEN = 5   # freie Zeilen der Talentspalte, danach die Aufstiegsspur

# ---------------------------------------------------------------------------
# Deutsche Bezeichnungen fuer Talente und Handicaps.
#
# Der Wert ist (deutscher Begriff, belegt?). "belegt" heisst: der Begriff steht
# so im deutschen Grundbuch -- entweder im Talent-/Handicap-Kapitel oder in den
# Werteblöcken der Archetypen ab S. 145. Alles andere stammt aus dem
# allgemeinen deutschen SWADE, das hier nicht als PDF vorliegt; solche Begriffe
# werden zwar gesetzt, aber beim Bauen als unbelegt gemeldet. Siehe die Warnung
# am Ende von Regelnotizen.md.
# ---------------------------------------------------------------------------
# GB = Deadlands-Grundbuch, SW = deutsches SWADE-Grundregelwerk. Jeder Begriff
# steht so gedruckt im angegebenen Buch — nichts hier ist selbst übersetzt.
DE = {
    # -- Arkane Hintergründe, alle Deadlands-eigen ----------------------
    u"Arcane Background (Blessed)":      (u"Arkaner Hintergrund (Gesegneter)", True),            # GB S. 17
    u"Arcane Background (Chi Master)":   (u"Arkaner Hintergrund (Chi-Meister)", True),           # GB S. 17
    u"Arcane Background (Huckster)":     (u"Arkaner Hintergrund (Taschenspieler)", True),        # GB S. 18
    u"Arcane Background (Shaman)":       (u"Arkaner Hintergrund (Schamane)", True),              # GB S. 18
    u"Arcane Background (Mad Scientist)": (u"Arkaner Hintergrund (Verrückter Wissenschaftler)", True), # GB S. 18
    # -- weitere Deadlands-eigene Talente ---------------------------------
    u"Gallows Humor":                    (u"Galgenhumor", True),                                 # GB S. 18
    u"Guts":                             (u"Mumm", True),                                        # GB S. 21
    u"Grit":                             (u"Schneid", True),                                     # GB S. 22 — VETERAN, nicht Novize
    u"Quick Draw":                       (u"Schnell Ziehen", True),                              # GB S. 19
    u"Territorial Ranger":               (u"Territorialer Ranger", True),                        # GB S. 21
    u"Don't Get 'im Riled!":             (u"Mach ihn nicht wütend!", True),                      # GB S. 19
    u"Duelist":                          (u"Duellant", True),                                    # GB S. 19
    u"Card Sharp":                        (u"Falsch Spielen", True),                              # GB S. 20
    u"Harrowed":                         (u"Gepeinigt", True),                                   # GB S. 22
    u"Superior Kung Fu":                 (u"Überlegenes Kung Fu", True),                         # GB S. 56
    u"Supernatural Attribute":           (u"Übernatürliches Attribut", True),                    # GB S. 61
    u"Ore Eater":                        (u"Erzfresser", True),                                  # GB S. 73
    # -- Deadlands-eigene Handicaps ---------------------------------------
    u"Grim Servant o' Death":            (u"Grimmiger Diener des Todes", True),                  # GB S. 15
    u"Night Terrors":                    (u"Nachtängste", True),                                 # GB S. 16
    u"Talisman":                         (u"Talisman", True),                                    # GB S. 16
    # -- Talente aus SWADE ------------------------------------------------
    u"Alertness":                        (u"Aufmerksamkeit", True),                              # SW S. 38
    u"Ambidextrous":                     (u"Beidhändig", True),                                  # SW S. 38
    u"Brawny":                           (u"Kräftig", True),                                     # SW S. 39
    u"Charismatic":                      (u"Charismatisch", True),                               # SW S. 38
    u"Two-Fisted":                       (u"Beidhändiger Kampf", True),                          # SW S. 41
    u"Martial Artist":                   (u"Kampfkünstler", True),                               # SW S. 42
    u"Trademark Weapon":                 (u"Lieblingswaffe", True),                              # SW S. 42
    u"Steady Hands":                     (u"Ruhige Hände", True),                                # SW S. 43
    u"Mr. Fix It":                       (u"Bastler", True),                                     # SW S. 45
    u"Power Points":                     (u"Machtpunkte", True),                                 # SW S. 46
    u"Scholar":                          (u"Gelehrter", True),                                   # SW S. 49
    u"Woodsman":                         (u"Naturbursche", True),                                # SW S. 49
    u"Menacing":                         (u"Bedrohlich", True),                                  # SW S. 50
    u"Champion":                         (u"Auserwählter", True),                                # SW S. 51
    u"Reliable":                         (u"Verlässlich", True),                                 # SW S. 51
    u"Elan":                             (u"Elan", True),                                        # SW S. 39
    u"Quick":                            (u"Schnell", True),                                     # SW S. 40
    u"Luck":                             (u"Glück", True),                                       # SW S. 39
    u"Brave":                            (u"Mutig", True),                                       # SW S. 40
    u"Fleet-Footed":                     (u"Flink", True),                                       # SW S. 39
    u"Rich":                             (u"Reich", True),                                       # SW S. 40
    u"Healer":                           (u"Heiler", True),                                      # SW S. 52
    u"Sweep":                            (u"Rundumschlag", True),                                # SW S. 43
    u"Danger Sense":                     (u"Sechster Sinn", True),                               # SW S. 52
    # -- Handicaps aus SWADE ----------------------------------------------
    u"Illiterate":                       (u"Analphabet", True),                                  # SW S. 22
    u"Habit":                            (u"Angewohnheit", True),                                # SW S. 22
    u"Arrogant":                         (u"Arrogant", True),                                    # SW S. 23
    u"Outsider":                         (u"Außenseiter", True),                                 # SW S. 23
    u"Thin Skinned":                     (u"Dünnhäutig", True),                                  # SW S. 23
    u"Wanted":                           (u"Gesucht", True),                                     # SW S. 24
    u"Greedy":                           (u"Gierig", True),                                      # SW S. 24
    u"Big Mouth":                        (u"Große Klappe", True),                                # SW S. 25
    u"Loyal":                            (u"Loyal", True),                                       # SW S. 26
    u"Curious":                          (u"Neugierig", True),                                   # SW S. 26
    u"Pacifist":                         (u"Pazifist", True),                                    # SW S. 26
    u"Vengeful":                         (u"Rachsüchtig", True),                                 # SW S. 26
    u"Vow":                              (u"Schwur", True),                                      # SW S. 27, nicht „Gelübde“
    u"Cautious":                         (u"Vorsichtig", True),                                  # SW S. 28
    u"Doubting Thomas":                  (u"Zweifler", True),                                    # SW S. 28
    u"Driven":                           (u"Angetrieben", True),                                 # SW S. 22
    u"Overconfident":                    (u"Übermütig", True),                                   # SW S. 28, nur schwer
    u"Quirk":                            (u"Tick", True),                                        # SW S. 28
    u"Heroic":                           (u"Heldenhaft", True),                                  # SW S. 25, nur schwer
    u"Poverty":                          (u"Arm", True),                                         # SW S. 23
    u"Hard of Hearing":                  (u"Schwerhörig", True),                                 # SW S. 27
    u"Stubborn":                         (u"Stur", True),                                        # SW S. 28
}

WARNUNGEN = []


def warn(msg):
    WARNUNGEN.append(msg)


# ---------------------------------------------------------------------------
# Textaufbereitung
# ---------------------------------------------------------------------------
def lat1(s):
    """Die Formularfelder des Bogens sind Helvetica/WinAnsi -- alles, was dort
    nicht hineinpasst (chinesische Schrift im Titel etwa), wird entfernt."""
    out, weg = [], []
    for ch in s:
        try:
            ch.encode("cp1252")
            out.append(ch)
        except UnicodeEncodeError:
            weg.append(ch)
    if weg:
        warn(u"nicht darstellbare Zeichen entfernt: %s" % u"".join(weg))
    return re.sub(r"\s{2,}", " ", u"".join(out)).strip()


def entmarkup(s):
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)   # [Text](link)
    s = re.sub(r"[*_`]+", "", s)
    return s.strip()


# Geldrechnung, Preis- und Blockparser leben in build_html.py, damit die
# HTML-Karte und der PDF-Bogen garantiert dasselbe lesen und rechnen.
geld = bh.geld
preis = bh.preis
parse_sections = bh.parse_sections


# ---------------------------------------------------------------------------
# Bloecke aus der Markdown-Datei
# ---------------------------------------------------------------------------
def block(raw, name):
    m = re.search(r"(?ms)^```%s[ \t]*\n(.*?)\n```[ \t]*$" % name, raw)
    return m.group(1) if m else None


def titel_und_beiname(raw):
    m = re.search(r"^#\s+(.+)$", raw, re.M)
    voll = entmarkup(m.group(1)) if m else u"Deadlands"
    beiname = u""
    q = re.search(u"[„“\"]([^“”\"]+)[“”\"]", voll)
    if q:
        beiname = q.group(1).strip()
        voll = re.sub(u"[„“\"][^“”\"]+[“”\"]", "", voll)
    return lat1(voll), lat1(beiname)


def archetyp(raw):
    m = re.search(r"^\*Archetyp:\s*(.+?)\*\s*$", raw, re.M)
    if not m:
        return u""
    t = entmarkup(m.group(1))
    t = re.sub(r"\s*\(.*?\)\s*$", "", t).strip()   # "GUNSLINGER (Revolverheld)"
    return t.title()


# ---------------------------------------------------------------------------
# Build-Block auswerten (Wuerfel und Kosten kommen aus build_html)
# ---------------------------------------------------------------------------
def attribute(d):
    aus = {}
    for x in (d.get("attribute") or d.get("attributes", "")).split(","):
        if x.strip():
            nm, die = bh._split_die(x)
            aus[bh.ATTR_EN.get(nm, nm)] = die
    return aus


def fertigkeiten(d):
    """[(Anzeigename, Wuerfel)] -- die fuenf Kernfertigkeiten zuerst und
    immer vollzaehlig, denn ungekaufte Kernfertigkeiten stehen auf W4."""
    gekauft, unbekannt = {}, []
    for eintrag in (d.get("fertigkeiten") or d.get("skills", "")).split(","):
        if not eintrag.strip():
            continue
        name, die = bh._split_die(eintrag)
        lookup = re.sub(r"\s*\(.*?\)\s*$", "", name).strip()
        link = bh.SKILL_LINK.get(lookup)
        if not link:
            unbekannt.append(name)
            continue
        klammer = re.search(r"\((.*?)\)\s*$", name)
        anzeige = link[0] + (u" (%s)" % klammer.group(1) if klammer else u"")
        gekauft[anzeige] = die
    for n in unbekannt:
        warn(u"unbekannte Fertigkeit: %s" % n)

    kern = [e for e, _a, core, _al in bh.SKILLS_DEF if core]
    reihe = []
    for k in kern:
        treffer = [n for n in gekauft if n.split(" (")[0] == k]
        reihe.append((k, gekauft.pop(treffer[0]) if treffer else u"d4"))
    for n, die in gekauft.items():
        reihe.append((n, die))
    return reihe


def handicaps(d):
    aus = []
    for h in (d.get("handicaps") or d.get("hindrances", "")).split(","):
        h = h.strip()
        if not h:
            continue
        m = re.search(r"\((schwer|leicht|Major|Minor)\)", h)
        schwere = bh.SEVERITY[m.group(1)][1] if m else u""
        name = re.sub(r"\s*\((schwer|leicht|Major|Minor)\)\s*", "", h).strip()
        aus.append((name, schwere))
    return aus


def talente(d):
    aus = []
    for t in (d.get("talente") or d.get("edges", "")).split("|"):
        t = re.sub(r"\[[^\]]*\]", "", t).strip()   # [free: Human], [Hindrance]
        if t:
            aus.append(t)
    return aus


def mit_deutsch(name):
    """"Martial Artist" -> "Martial Artist (Kampfkuenstler)". Der Zusatz in
    Klammern am Original bleibt stehen: "Superior Kung Fu: Wing Tsun"."""
    kopf, rest = name, u""
    m = re.match(r"^(.*?)\s*:\s*(.+)$", name)          # "Superior Kung Fu: Wing Tsun"
    if m and m.group(1) in DE:
        kopf, rest = m.group(1), u": " + m.group(2)
    eintrag = DE.get(kopf)
    if not eintrag:
        warn(u"keine deutsche Bezeichnung hinterlegt: %s" % kopf)
        return name
    de, belegt = eintrag
    if not belegt:
        warn(u"deutscher Begriff nicht aus dem Grundbuch belegt: %s (%s)"
             % (kopf, de))
    # Traegt der englische Name schon eine Klammer, wuerde eine zweite
    # ineinandergeschachtelt unlesbar -- dann trennt ein Mittelpunkt.
    if de.lower() == kopf.lower():        # "Arrogant (Arrogant)" ist albern
        return kopf + rest
    fuge = u"%s · %s%s" if kopf.endswith(u")") else u"%s (%s)%s"
    return fuge % (kopf, de, rest)


# ---------------------------------------------------------------------------
# Bogen fuellen
# ---------------------------------------------------------------------------
DIE_STATES = {"4": "4", "6": "6", "8": "8", "10": "10", "12": "12"}


def wuerfelzahl(die):
    m = re.search(r"\d+", die or "")
    return m.group() if m else None


def fuelle(pfad_md, ziel):
    raw = io.open(pfad_md, encoding="utf-8").read()
    basis = os.path.splitext(os.path.basename(pfad_md))[0]
    b = block(raw, "build")
    if not b:
        warn(u"%s: kein ```build```-Block, uebersprungen" % basis)
        return None
    d = bh._parse_build(b)
    g_skalar, g_abschnitt = parse_sections(block(raw, "gear"))
    p_skalar, p_abschnitt = parse_sections(block(raw, "powers"))

    attr = attribute(d)
    skills = fertigkeiten(d)

    # -- abgeleitete Werte: dieselbe Rechnung wie in der HTML-Karte --------
    fight = dict(skills).get(u"Fighting")
    ruest = re.match(r"\d+", d.get("rüstung") or d.get("armor") or "0")
    ruest = int(ruest.group()) if ruest else 0
    parry = d.get("parade") or d.get("parry") or str(
        2 + (bh._half(fight) if fight else 0))
    tough = d.get("robustheit") or d.get("toughness") or str(
        2 + (bh._half(attr[u"Vigor"]) if attr.get(u"Vigor") else 0) + ruest)
    pace = d.get("tempo") or d.get("pace") or "6"

    # -- Dollarrechnung ----------------------------------------------------
    start = float(g_skalar.get("start", STARTGELD))
    ausruestung = g_abschnitt.get(u"ausrüstung", []) or g_abschnitt.get("ausruestung", [])
    waffen = g_abschnitt.get("waffen", [])
    ausgegeben = sum(preis(r[1]) for r in ausruestung if len(r) > 1)
    ausgegeben += sum(preis(r[6]) for r in waffen if len(r) > 6)
    rest = start - ausgegeben
    if rest < 0:
        warn(u"%s: Startgeld ueberzogen -- %s von %s ausgegeben"
             % (basis, geld(ausgegeben), geld(start)))

    # -- Felder ------------------------------------------------------------
    name, beiname = titel_und_beiname(raw)
    if g_skalar.get("name"):
        name = lat1(g_skalar["name"])
    if g_skalar.get("nickname"):
        beiname = lat1(g_skalar["nickname"])
    info = g_skalar.get("info") or u" · ".join(
        [x for x in (archetyp(raw), u"Novize",
                     (u"%s Machtpunkte" % p_skalar["machtpunkte"])
                     if p_skalar.get("machtpunkte") else u"") if x])

    text = {
        "Name": name,
        "Nickname": beiname,
        "Bennies": g_skalar.get("bennies", BENNIES),
        "Info": info,
        "Pace": pace,
        "Parry": parry,
        "Toughness": tough,
    }

    for i, (nm, _die) in enumerate(skills, 1):
        if i > 20:
            warn(u"%s: mehr als 20 Fertigkeiten, %s faellt weg" % (basis, nm))
            break
        text["Skills %d" % i] = nm

    for i, (nm, schwere) in enumerate(handicaps(d), 1):
        if i > 4:
            warn(u"%s: mehr als 4 Handicaps, %s faellt weg" % (basis, nm))
            break
        text["Hindrances %d" % i] = mit_deutsch(nm) + (
            u" — %s" % schwere if schwere else u"")

    zeilen = [mit_deutsch(t) for t in talente(d)]
    for notiz in g_abschnitt.get("notizen", []):
        zeilen.append(u" | ".join(notiz))
    # Nur die ersten fuenf Zeilen dieser Spalte sind frei. Ab der sechsten
    # beginnt die vorgedruckte Aufstiegsspur (N N N S S S S V V V V H H H H
    # L L L L), die dem Spieler gehoert und nicht bedruckt werden darf.
    ueberlauf = zeilen[EDGE_ZEILEN:]
    for i, z in enumerate(zeilen[:EDGE_ZEILEN], 1):
        text["Edges & Advancements %d" % i] = z
    if ueberlauf:
        warn(u"%s: %d Talent-/Notizzeile(n) passen nicht in die Talentspalte "
             u"und stehen jetzt bei der Ausruestung" % (basis, len(ueberlauf)))

    # Ausruestung: Name, Kosten und die Anmerkung; das Gewicht traegt der
    # Bogen nicht, es dient nur der Kontrolle in der Markdown-Datei.
    gear = []
    for r in ausruestung:
        nm = r[0]
        anm = r[3] if len(r) > 3 and r[3] else u""
        p = r[1] if len(r) > 1 else u""
        gear.append(u"%s%s%s" % (nm,
                                 u" (%s)" % p if p and preis(p) else u"",
                                 u" — %s" % anm if anm else u""))
    gear.append(u"Bargeld: %s" % geld(rest))
    gear.extend(ueberlauf)
    for i, z in enumerate(gear, 1):
        if i > 18:
            warn(u"%s: mehr als 18 Ausruestungszeilen" % basis)
            break
        text["Gear %d" % i] = z

    SPALTEN = ["Weapons %d", "Weapons Range %d", "Weapons Damage %d",
               "Weapons AP %d", "Weapons ROF %d", "Weapons WT %d",
               "Weapons Notes %d"]
    for i, r in enumerate(waffen, 1):
        if i > 8:
            warn(u"%s: mehr als 8 Waffen" % basis)
            break
        # Blockformat: Name|Reichw.|Schaden|PB|FR|Gewicht|Kosten|Notiz
        werte = (r[:6] + [r[7] if len(r) > 7 else u""])
        for feld, wert in zip(SPALTEN, werte):
            text[feld % i] = wert

    for i, r in enumerate(p_abschnitt.get(u"mächte", []) or
                          p_abschnitt.get("maechte", []), 1):
        if i > 8:
            warn(u"%s: mehr als 8 Maechte" % basis)
            break
        for feld, wert in zip(["Power %d", "PP %d", "Power Range %d",
                               "Duration %d", "Effect %d"], r):
            text[feld % i] = wert

    # -- schreiben ---------------------------------------------------------
    haken = {}
    for a, die in attr.items():
        haken["%s CHECK" % a] = wuerfelzahl(die)
    for i, (_nm, die) in enumerate(skills[:20], 1):
        haken["Skills %d CHECK" % i] = wuerfelzahl(die)

    doc = fitz.open(VORLAGE)
    seite = doc[0]
    for w in seite.widgets():
        fn = w.field_name
        if fn in text:
            w.field_value = lat1(text[fn])
            w.update()
        elif fn in haken:
            an = w.button_states()["normal"][0]
            w.field_value = (an == haken[fn])
            w.update()
    doc.save(ziel, garbage=3, deflate=True)
    doc.close()
    return {"name": name, "ausgegeben": ausgegeben, "rest": rest,
            "waffen": len(waffen), "gear": len(ausruestung)}


# ---------------------------------------------------------------------------
def finde(praefix):
    treffer = sorted(glob.glob(os.path.join(REPO, "Charaktere",
                                            praefix + "*.md")))
    if not treffer:
        treffer = sorted(glob.glob(os.path.join(REPO, "Charaktere",
                                                "*%s*.md" % praefix)))
    if not treffer:
        warn(u"keine Charakterdatei zu %r" % praefix)
        return None
    if len(treffer) > 1:
        warn(u"%r ist mehrdeutig: %s" % (praefix,
                                         ", ".join(os.path.basename(t)
                                                   for t in treffer)))
    return treffer[0]


def main(argv):
    if not os.path.exists(VORLAGE):
        sys.exit(u"Vorlage fehlt: %s" % VORLAGE)
    if argv and argv[0] == "--alle":
        dateien = sorted(glob.glob(os.path.join(REPO, "Charaktere", "*.md")))
    else:
        dateien = [f for f in (finde(a) for a in (argv or AUSWAHL)) if f]

    if not os.path.isdir(AUSGABE):
        os.makedirs(AUSGABE)

    fertig = []
    for src in dateien:
        basis = os.path.splitext(os.path.basename(src))[0]
        ziel = os.path.join(AUSGABE, basis + ".pdf")
        info = fuelle(src, ziel)
        if info:
            fertig.append((ziel, info))
            print(u"  %-46s %s ausgegeben, %s Bargeld"
                  % (basis, geld(info["ausgegeben"]), geld(info["rest"])))

    # Sammelbogen zum Ausdrucken. Die Formularfelder werden dabei in den
    # Seiteninhalt gebacken -- gleichnamige Felder auf mehreren Seiten waeren
    # im AcroForm sonst ein einziges Feld und wuerden sich gegenseitig
    # ueberschreiben.
    if len(fertig) > 1:
        sammel = fitz.open()
        for ziel, _ in fertig:
            e = fitz.open(ziel)
            e.bake()
            sammel.insert_pdf(e)
            e.close()
        pfad = os.path.join(AUSGABE, "Auswahl.pdf")
        sammel.save(pfad, garbage=3, deflate=True)
        sammel.close()
        print(u"\nSammelbogen: %s (%d Seiten)"
              % (os.path.basename(pfad), len(fertig)))

    WARNUNGEN.extend(bh.WARNINGS)
    print(u"\nBoegen geschrieben: %d" % len(fertig))
    if WARNUNGEN:
        print(u"\nWarnungen (%d):" % len(WARNUNGEN))
        for w in WARNUNGEN:
            print(u"  ! " + w)


if __name__ == "__main__":
    main(sys.argv[1:])
