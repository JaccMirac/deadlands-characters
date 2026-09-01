# -*- coding: utf-8 -*-
"""Baut je Figur ein dreiteiliges Dossier als ein einzelnes PDF.

    Seite 1  Titelbild -- das Portraet gross, der Name in Western-Schrift
    Seite 2  Hintergrundgeschichte, danach der Regeltext zu jedem Talent
             und Handicap, woertlich aus dem Regelwerk
    Seite 3  der ausgefuellte Charakterbogen (aus build_sheets.py)

Seite 2 kann auf mehrere Seiten laufen, wenn die Regeltexte lang sind; der
Bogen ist immer die letzte Seite.

WICHTIG -- Urheberrecht: die Regeltexte werden bei *jedem* Lauf frisch aus
den lokalen PDFs gezogen und liegen **nirgends** im Repo. Ebenso die
Western-Schrift: PLAYBILL.TTF wird aus dem Windows-Schriftenordner gelesen,
nicht mitgeliefert. Fehlt eine der Quellen, sagt das Skript das und benutzt
einen Ersatz, statt still etwas anderes zu drucken.

Aufruf:
    python build_dossier.py                # AUSWAHL aus build_sheets.py
    python build_dossier.py 11-1 01-2
    python build_dossier.py --alle

Abhaengigkeit: pip install pymupdf
"""
import io
import os
import re
import sys
import glob

import fitz

import build_html as bh
import build_sheets as bs

REPO = os.path.dirname(os.path.abspath(__file__))
AUSGABE = os.path.join(REPO, "CharacterSheetsPdf")
BILDER = os.path.join(REPO, "Bilder")

# Western-Schrift. Playbill ist die klassische Steckbrief-Schrift und liegt
# auf jedem Windows mit Office bei. Sie wird gelesen, nicht ins Repo kopiert.
WESTERN = r"C:\Windows\Fonts\PLAYBILL.TTF"

# Welche Abschnitte der Markdown-Datei auf Seite 2 landen. **Aufhaenger** ist
# bewusst nicht dabei: dort stehen die Enthuellungen und ausdrueckliche
# Marshal-Hinweise ("Dunkler, wenn der Marshal ein Messer will"). Wer das
# Dossier als Marshal-Mappe statt als Spielerhandout will, traegt ihn hier ein.
ABSCHNITTE = [u"Hintergrund", u"Die Rechnung", u"Am Tisch",
              u"Warum es Spaß macht", u"Die Machtliste"]

# Reihenfolge der Nachschlagewerke. (Kuerzel, Datei, Sprache, Folio-Offset) --
# der Offset rechnet den PDF-Index auf die gedruckte Seitenzahl um.
QUELLEN = [
    (u"Grundbuch",      "Deadlands_Grundbuch.pdf",                    "de",  0),
    (u"SWADE (dt.)",    "US85001PDF_Savage_Worlds_Abenteuer_Edition_"
                        "LZ_meta_Vierte_Auflage.pdf",                 "de",  0),
    (u"Deadlands: TWW", "0-deadlands-the-weird-westpdf_compress-2.pdf", "en", -1),
    (u"SWADE",          "SWADE_Savage_Worlds_Adv_Ed_Core_Rules.pdf",   "en", -1),
]

# "quellentreu" = deutscher Buchtext, wo es einen gibt, sonst englischer.
# "en" ueberspringt das Grundbuch und nimmt ueberall den englischen Text.
SPRACHE = "quellentreu"

WARNUNGEN = []
UEBERLAUF = [False]   # setzt _seiten(einseitig=True), liest titelseite()
_CACHE = {}


def warn(m):
    WARNUNGEN.append(m)


# ---------------------------------------------------------------------------
# Regeltexte aus den Buechern holen
# ---------------------------------------------------------------------------
# Eine Ueberschrift ist entweder eine Zeile in GROSSBUCHSTABEN (so setzen die
# Deadlands-Baende ihre Eintraege), eine Zeile direkt vor VORAUSSETZUNGEN/
# REQUIREMENTS, oder eine Handicap-Zeile mit Schweregrad -- englisch
# "Name (Major or Minor)", deutsch "Name (leicht oder schwer)".
#
# Der Schweregrad steht als (?i:), weil das Grundbuch ihn mitversalisiert:
# "TALISMAN (LEICHT ODER SCHWER)". Ohne das passt keines der Muster auf so
# eine Zeile -- die Versalien-Regel unten erlaubt keine Klammern --, und der
# Eintrag davor liest ueber sein Ende hinaus weiter. So zog "Nachtaengste"
# die drei folgenden Handicaps mit: 2906 Zeichen statt 390.
_HEAD = [
    re.compile(r"^[^\n]{2,60}\n(?=REQUIREMENTS|VORAUSSETZUNGEN)", re.M),
    re.compile(r"^[A-Z][A-Za-z'\u2019 \-]{2,40}"
               r"\((?i:Major|Minor)[^)]*\)[ \t]*$", re.M),
    re.compile(r"^[A-Z\u00c4\u00d6\u00dc][A-Za-z\u00c4\u00d6\u00dc"
               r"\u00e4\u00f6\u00fc\u00df'\u2019 \-]{2,40}"
               r"\((?i:leicht|schwer)[^)]*\)[ \t]*$", re.M),
    re.compile(r"^[A-Z\u00c4\u00d6\u00dc][A-Z\u00c4\u00d6\u00dc0-9'\u2019 .\-!?]{3,50}[ \t]*$", re.M),
]


def _naechste_ueberschrift(text, ab):
    treffer = []
    for pat in _HEAD:
        m = pat.search(text, ab)
        if m:
            treffer.append(m.start())
    return min(treffer) if treffer else len(text)


def _saeubern(text):
    # Die Deadlands-Baende setzen Aufzaehlungspunkte als C1-Steuerzeichen
    # (U+0084). Keine Schrift stellt die dar -- sie werden zu echten
    # Absatzmarken, damit aus der Bleiwueste eine Liste wird.
    text = re.sub(u"[\u0080-\u009f]", u"\u2022", text)
    text = text.replace(u"\u00ad", "")                      # weiches Trennzeichen
    text = re.sub(r"(\w)[-\u2010\u2011]\n([a-z\u00e4\u00f6\u00fc\u00df])", r"\1\2", text)
    text = re.sub(r"[ \t]*\n[ \t]*", " ", text)
    text = re.sub(u"[\u0000-\u0008\u000b\u000c\u000e-\u001f]", "", text)
    text = re.sub(u"[ \\t]*\u2022[ \\t]*", u"\u2022", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def _voraussetzungen(koerper):
    """Schneidet die REQUIREMENTS-/VORAUSSETZUNGEN-Zeile ab. Sie laeuft im
    Satz oft ueber zwei Zeilen ("Novice, skill with chosen / weapon of d8+"),
    darf aber nicht die erste Textzeile mitnehmen. Fortgesetzt wird nur, wenn
    die bisherige Zeile mit Komma endet oder die naechste klein anfaengt."""
    m = re.match(r"\s*(?:REQUIREMENTS|VORAUSSETZUNGEN):[ \t]*", koerper)
    if not m:
        return u"", koerper
    zeilen = koerper[m.end():].split("\n")
    genommen, i = [zeilen[0]], 1
    while i < len(zeilen) and i < 3:
        vorige, naechste = genommen[-1].rstrip(), zeilen[i].lstrip()
        if vorige.endswith(",") or (naechste[:1].islower() if naechste else False):
            genommen.append(zeilen[i]); i += 1
        else:
            break
    return (_saeubern("\n".join(genommen)),
            "\n".join(zeilen[i:]))

def _seiten_text(doc, i):
    schluessel = (id(doc), i)
    if schluessel not in _CACHE:
        _CACHE[schluessel] = doc[i].get_text()
    return _CACHE[schluessel]


def _kandidat(t, m, doc, i, kuerzel, offset):
    """Schneidet den Eintrag ab der Fundstelle bis zur naechsten Ueberschrift."""
    rest = t[m.end():]
    ende = _naechste_ueberschrift(rest, 0)
    koerper = rest[:ende]
    # Laeuft der Eintrag bis ans Seitenende, wird auf der naechsten Seite
    # weitergelesen -- aber NUR, wenn er dort ueberhaupt weitergehen kann.
    # Endet er mit einem vollstaendigen Satz, ist er fertig. Ohne diese
    # Pruefung zog "Zweifler" (SWADE S. 28, letzter Eintrag der Seite) das
    # halbe Kapitel "Eigenschaften" von S. 29 hinterher: 5302 Zeichen statt
    # 400, weil dessen Ueberschriften auf keines der Muster passen.
    if (ende >= len(rest) - 2 and i + 1 < doc.page_count
            and koerper.rstrip()[-1:] not in u".!?“”\")"):
        f = _seiten_text(doc, i + 1)
        koerper += "\n" + f[:_naechste_ueberschrift(f, 0)]
    vor, koerper = _voraussetzungen(koerper.strip("\n"))
    return vor, _saeubern(koerper), kuerzel, i + offset


_SCHWERE = re.compile(r"\((?:leicht|schwer|Major|Minor)", re.I)


def suche_eintrag(begriff, sprachen):
    """Liefert (Voraussetzungen, Text, Quelle, Seite) oder None.

    Der Name steht in den Buechern auch ueber Werteblocks von NSCs --
    "Kampfkuenstler" etwa als Archetyp im Grundbuch, S. 148. Ein echter
    Regeleintrag verraet sich durch die Voraussetzungen-Zeile (Talente) oder
    den Schweregrad in Klammern (Handicaps); der wird bevorzugt, ein Fund
    ohne beides nur als Notnagel genommen und gemeldet."""
    # Der PDF-Textextrakt schiebt in manchen Ueberschriften ein Leerzeichen
    # hinter das ss ("Auss enseiter (leicht oder schwer)", SWADE S. 23) --
    # deshalb darf dort eines stehen.
    # Lange Ueberschriften brechen um ("ARKANER HINTERGRUND (VERRUECKTER /
    # WISSENSCHAFTLER)", Grundbuch S. 18) -- jede Luecke im Namen darf
    # deshalb ein Zeilenende sein.
    kern = re.escape(begriff).replace(u"\u00df", u"\u00df\\s?")
    kern = kern.replace(u"\\ ", u"[ \\t]*\\n?[ \\t]*")
    muster = re.compile(r"^[ \t]*" + kern
                        + r"[ \t]*(\([^)\n]*\))?[ \t]*$", re.M | re.I)
    treffer = ersatz = None
    for kuerzel, datei, sprache, offset in QUELLEN:
        if treffer:
            break
        if sprache not in sprachen:
            continue
        pfad = os.path.join(REPO, datei)
        if not os.path.exists(pfad):
            continue
        doc = _CACHE.setdefault("doc:" + datei, fitz.open(pfad))
        for i in range(doc.page_count):
            m = muster.search(_seiten_text(doc, i))
            if not m:
                continue
            k = _kandidat(_seiten_text(doc, i), m, doc, i, kuerzel, offset)
            if k[0] or _SCHWERE.search(m.group(0)):
                treffer = k
                break
            if ersatz is None:
                ersatz = k
    if not treffer and ersatz:
        warn(u"%s: Eintrag ohne Voraussetzungen und ohne Schweregrad "
             u"(%s, S. %d) — womoeglich ein Werteblock"
             % (begriff, ersatz[2], ersatz[3]))
        treffer = ersatz
    if treffer and len(treffer[1]) < 40:
        warn(u"%s: Regeltext verdaechtig kurz (%d Zeichen)"
             % (begriff, len(treffer[1])))
    # Gegenprobe nach oben. Der laengste legitime Eintrag in den vorliegenden
    # Buechern ist UEBERLEGENES KUNG FU mit rund 3100 Zeichen, weil er alle
    # sechs Stile auflistet. Wird es deutlich mehr, hat die Suche ueber das
    # Ende des Eintrags hinaus weitergelesen.
    if treffer and len(treffer[1]) > 3500:
        warn(u"%s: Regeltext verdaechtig lang (%d Zeichen, %s S. %d) -- "
             u"vermutlich ist ein Kapitel mitgelesen worden"
             % (begriff, len(treffer[1]), treffer[2], treffer[3]))
    return treffer


def regeltext(englisch, deutsch):
    """Sucht den Eintrag -- erst unter dem deutschen Namen, wenn der Modus
    quellentreu ist, sonst gleich englisch."""
    versuche = []
    if SPRACHE == "quellentreu" and deutsch:
        versuche.append((deutsch, ("de",)))
    versuche.append((englisch, ("en",)))
    if deutsch:
        versuche.append((deutsch, ("de",)))
    for begriff, sprachen in versuche:
        treffer = suche_eintrag(begriff, sprachen)
        if treffer:
            return treffer
    warn(u"kein Regeltext gefunden: %s" % englisch)
    return None


# ---------------------------------------------------------------------------
# Markdown auswerten
# ---------------------------------------------------------------------------
def abschnitte(raw):
    """{'Hintergrund': 'Text', ...} aus den **Ueberschrift.**-Absaetzen."""
    schnitt = re.search(r"(?m)^---\s*$", raw)
    if schnitt:
        raw = raw[:schnitt.start()]
    aus = {}
    for m in re.finditer(r"(?ms)^\*\*(.+?)\.\*\*\s*(.*?)(?=^\*\*|\Z)", raw):
        aus[m.group(1).strip()] = m.group(2).strip()
    return aus


def voller_name(raw):
    """Der H1-Titel, Beiname inbegriffen -- fuer Deckblatt und Kopfzeile."""
    m = re.search(r"^#\s+(.+)$", raw, re.M)
    t = m.group(1) if m else u"Deadlands"
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    return bs.lat1(re.sub(r"[*_`]+", "", t))

def cjk_teil(raw):
    """Der chinesische/japanische Anteil des H1-Titels. Playbill kann ihn
    nicht setzen, deshalb bekommt er auf dem Deckblatt eine eigene Zeile in
    der CJK-Schrift, die PyMuPDF mitbringt -- statt ihn wegzuwerfen."""
    m = re.search(r"^#\s+(.+)$", raw, re.M)
    if not m:
        return u""
    return u"".join(c for c in m.group(1)
                    if u"\u3000" <= c <= u"\u9fff")

def zitat(raw):
    m = re.search(r"^>\s*(.+)$", raw, re.M)
    return re.sub(r"[*_]", "", m.group(1)).strip() if m else u""


def md_zu_html(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*([^*]+?)\*(?!\*)", r"<i>\1</i>", text)
    text = (text.replace("&", "&amp;").replace("<b>", "\x01").replace("</b>", "\x02")
            .replace("<i>", "\x03").replace("</i>", "\x04"))
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    text = (text.replace("\x01", "<b>").replace("\x02", "</b>")
            .replace("\x03", "<i>").replace("\x04", "</i>"))
    # "- Eintrag" wird zum Aufzaehlungspunkt -- sonst stuende der Bindestrich
    # als Zeichen im Fliesstext (Machtlisten, Merkzettel).
    aus = []
    for z in text.split("\n"):
        z = z.strip()
        if not z:
            continue
        if z.startswith("- "):
            aus.append('<p class="bullet">&#8226; %s</p>' % z[2:])
        else:
            aus.append("<p>%s</p>" % z)
    return "".join(aus)


def absatz_html(text):
    """Aus einem Regeltext mit Aufzaehlungspunkten werden echte Absaetze."""
    stuecke = [t.strip() for t in text.split(u"•") if t.strip()]
    if len(stuecke) < 2:
        return u'<p class="rule">%s</p>' % esc(text)
    aus = [u'<p class="rule">%s</p>' % esc(stuecke[0])]
    aus += [u'<p class="bullet">• %s</p>' % esc(t) for t in stuecke[1:]]
    return u"".join(aus)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


# ---------------------------------------------------------------------------
# Satz
# ---------------------------------------------------------------------------
PAPIER = fitz.paper_rect("letter")
RAND = fitz.Rect(56, 54, PAPIER.x1 - 56, PAPIER.y1 - 54)
CREME = (0.957, 0.937, 0.894)
TINTE = "#241d16"
ROT = "#6b1d12"

CSS = u"""
body   {font-family: Georgia, serif; font-size: 10.5px; color: %(ink)s;}
h1     {font-family: Western; font-size: 33px; color: %(red)s;
        margin: 0 0 2px 0; line-height: 1.1;}
h2     {font-family: Western; font-size: 17px; color: %(red)s;
        margin: 16px 0 6px 0;}
h3     {font-family: Georgia, serif; font-size: 11px; color: %(ink)s;
        margin: 11px 0 1px 0;}
p      {margin: 0 0 7px 0; line-height: 1.45; text-align: justify;}
.sub   {font-size: 10px; color: #6b5d4c; font-style: italic;
        margin: 0 0 14px 0;}
.quote {font-size: 12px; font-style: italic; color: #6b5d4c;
        text-align: center; margin: 0;}
.src   {font-size: 8.5px; color: #8a7860; margin: 0 0 3px 0;}
.req   {font-size: 9px; color: #6b5d4c; margin: 0 0 3px 0;}
.rule  {margin: 0 0 4px 0; font-size: 10px; line-height: 1.4;
        text-align: left;}
.bullet {margin: 0 0 3px 14px; font-size: 10px; line-height: 1.4;
        text-align: left;}
.chosen {font-size: 10px; color: #6b1d12; margin: 0 0 4px 0;}
.miss  {font-size: 10px; color: %(red)s; margin: 0 0 4px 0;}
.cover-name {font-family: Western; font-size: 40px; color: %(red)s;
        text-align: center; margin: 0;}
.cover-cjk  {font-family: CJK; font-size: 22px; color: %(red)s;
        text-align: center; margin: 2px 0 0 0;}
.cover-sub  {font-size: 11px; color: #6b5d4c; text-align: center;
        letter-spacing: 1px; margin: 4px 0 0 0;}
""" % {"ink": TINTE, "red": ROT}


def archiv(bild=None, cjk=False):
    """Liefert (Archiv, @font-face-Block). Eine Schrift wird nur deklariert,
    wenn sie auch im Archiv liegt -- sonst bricht MuPDF den Satz ab und der
    Umbruch verschiebt sich stillschweigend."""
    a = fitz.Archive()
    faces = []
    if cjk:      # 3,5 MB -- nur laden, wenn die Figur wirklich CJK im Namen hat
        a.add(fitz.Font("china-t").buffer, "CJK.TTF")
        faces.append("@font-face {font-family: CJK; src: url(CJK.TTF);}")
    if os.path.exists(WESTERN):
        a.add(io.open(WESTERN, "rb").read(), "WESTERN.TTF")
        faces.append("@font-face {font-family: Western; src: url(WESTERN.TTF);}")
    if bild:
        a.add(io.open(bild, "rb").read(), os.path.basename(bild))
    return a, ("\n".join(faces) + "\n") if faces else ""


def _seiten(html, arch_css, rect=RAND, einseitig=False):
    """Rendert HTML in so viele Letter-Seiten, wie noetig, und gibt ein
    fertiges fitz.Document zurueck."""
    puffer = io.BytesIO()
    arch, faces = arch_css
    story = fitz.Story(html=html, user_css=faces + CSS, archive=arch)
    schreiber = fitz.DocumentWriter(puffer)
    weiter = 1
    while weiter:
        dev = schreiber.begin_page(PAPIER)
        weiter, _ = story.place(rect)
        story.draw(dev)
        schreiber.end_page()
        if einseitig:      # das Deckblatt ist per Definition eine Seite
            UEBERLAUF[0] = bool(weiter)
            break
    schreiber.close()
    doc = fitz.open("pdf", puffer.getvalue())
    for seite in doc:                       # Pergamentgrund unter den Text
        seite.draw_rect(PAPIER, color=None, fill=CREME, overlay=False)
    return doc


# 2:3-Portraet, so gross wie es neben Titel und Zitat passt. Lange Zitate
# brauchen mehr Platz, also wird das Bild notfalls kleiner statt das Zitat
# abgeschnitten.
BILDGROESSEN = [(330, 495), (300, 450), (270, 405), (240, 360)]


def titelseite(name, archetyp, spruch, bild, cjk=u""):
    hat_bild = bool(bild and os.path.exists(bild))
    if not hat_bild:
        warn(u"kein Portraet: %s" % bild)
    rumpf = (u'<div><p class="cover-name">%s</p>'
             + (u'<p class="cover-cjk">%s</p>' % esc(cjk) if cjk else u'')
             + u'<p class="cover-sub">%s</p></div>'
             u'<div style="text-align:center;margin:16px 0 14px 0">%s</div>'
             u'<p class="quote">%s</p>')
    # ohne Portraet darf der Pfad nicht ins Archiv -- sonst bricht das Oeffnen ab
    arch = archiv(bild if hat_bild else None, cjk=bool(cjk))
    seite = None
    for breite, hoehe in (BILDGROESSEN if hat_bild else [(0, 0)]):
        img = ('<img src="%s" width="%d" height="%d">'
               % (os.path.basename(bild), breite, hoehe)) if hat_bild else ""
        html = rumpf % (esc(name.upper()), esc(archetyp.upper()), img, esc(spruch))
        seite = _seiten(html, arch, einseitig=True)
        if not UEBERLAUF[0]:
            return seite
    warn(u"%s: Deckblatt laeuft ueber, auch beim kleinsten Bild — Zitat kuerzen"
         % name)
    return seite


def regelseiten(name, raw, d_build, reste=None):
    teile = [u'<h1>%s</h1>' % esc(name)]
    zeile = zitat(raw)
    if zeile:
        teile.append(u'<p class="sub">%s</p>' % esc(zeile))

    abs_ = abschnitte(raw)
    for titel in ABSCHNITTE:
        if titel in abs_:
            teile.append(u"<h2>%s</h2>%s" % (esc(titel), md_zu_html(abs_[titel])))

    for ueberschrift, eintraege in ((u"Talente", bs.talente(d_build)),
                                    (u"Handicaps", bs.handicaps(d_build))):
        if not eintraege:
            continue
        teile.append(u"<h2>%s</h2>" % ueberschrift)
        for e in eintraege:
            nm, schwere = (e if isinstance(e, tuple) else (e, u""))
            kopf = nm
            zusatz = u""
            m = re.match(r"^(.*?)\s*:\s*(.+)$", nm)
            if m and m.group(1) in bs.DE:
                kopf, zusatz = m.group(1), m.group(2)
            de = bs.DE.get(kopf, (None, False))[0]
            treffer = regeltext(kopf, de)
            titelzeile = bs.mit_deutsch(nm) + (u" — %s" % schwere if schwere else u"")
            teile.append(u"<h3>%s</h3>" % esc(titelzeile))
            if treffer:
                vor, text, quelle, seite = treffer
                teile.append(u'<p class="src">%s, S. %d</p>' % (esc(quelle), seite))
                if vor:
                    teile.append(u'<p class="req">Voraussetzungen: %s</p>' % esc(vor))
                # Die gewaehlte Variante gehoert vor den Regeltext -- bei
                # Ueberlegenes Kung Fu stehen sonst sechs Stile davor, von denen
                # die Figur nur einen beherrscht.
                if zusatz:
                    teile.append(u'<p class="chosen">Gewählt: %s</p>' % esc(zusatz))
                teile.append(absatz_html(text))
            else:
                teile.append(u'<p class="miss">Kein Regeltext in den vorliegenden '
                             u'Büchern gefunden — bitte nachtragen.</p>')

    # Notizenblatt: erst der Abschnitt **Notizen.** aus der Figurendatei --
    # dort steht, wie sich Talente und Handicaps bei dieser Figur konkret
    # zeigen --, danach alles, was auf dem Bogen keinen Platz mehr hatte.
    # So verschwindet nichts stillschweigend zwischen Markdown und Formular.
    notiz = abschnitte(raw).get(u"Notizen", u"")
    nachtrag = []
    if reste:
        if reste.get("gekuerzt"):
            nachtrag.append(u"**Auf dem Bogen ohne ihre Anmerkung:** "
                            + u"; ".join(reste["gekuerzt"]))
        if reste.get("weggefallen"):
            nachtrag.append(u"**Hat nicht mehr auf den Bogen gepasst:**")
            nachtrag += [u"- " + z for z in reste["weggefallen"]]
    if notiz or nachtrag:
        teile.append(u"<h2>Notizen</h2>")
        if notiz:
            teile.append(md_zu_html(notiz))
        if nachtrag:
            teile.append(md_zu_html(u"\n".join(nachtrag)))
    return _seiten(u"".join(teile), archiv())


# ---------------------------------------------------------------------------
def dossier(pfad_md, ziel):
    raw = io.open(pfad_md, encoding="utf-8").read()
    basis = os.path.splitext(os.path.basename(pfad_md))[0]
    b = bh_block(raw, "build")
    if not b:
        warn(u"%s: kein ```build```-Block" % basis)
        return None
    d_build = bh._parse_build(b)

    name = voller_name(raw)
    arche = bs.archetyp(raw)
    bild = os.path.join(BILDER, basis + ".png")

    # Der Bogen wird zuerst gefuellt: erst dadurch ist bekannt, was auf ihm
    # keinen Platz gefunden hat, und genau das kommt auf das Notizenblatt.
    bogen = os.path.join(AUSGABE, basis + ".pdf")
    info = bs.fuelle(pfad_md, bogen) or {}

    doc = fitz.open()
    t = titelseite(name, arche, zitat(raw), bild, cjk_teil(raw))
    doc.insert_pdf(t); t.close()
    r = regelseiten(name, raw, d_build, info)
    doc.insert_pdf(r); r.close()

    # Verkleinern MUSS vor dem Bogen passieren. Die CJK-Schrift, derentwegen
    # ueberhaupt verkleinert wird, steckt nur im Deckblatt; der offizielle
    # Charakterbogen bringt dagegen fuenf eingebettete Zierschriften mit
    # (TheDeadSaloon, WildCards ...), und subset_fonts zerlegt deren
    # Glyphenbreiten -- aus ATTRIBUTES wird dann "AT", aus SKILLS "KB".
    # Deshalb: erst Deckblatt und Regelseiten verkleinern, dann den Bogen
    # unangetastet anhaengen.
    try:
        doc.subset_fonts()
    except Exception as e:
        warn(u"Schriften nicht verkleinert: %s" % e)

    s = fitz.open(bogen)
    doc.insert_pdf(s); s.close()

    doc.save(ziel, garbage=4, deflate=True)
    seiten = doc.page_count
    doc.close()
    return seiten


def bh_block(raw, name):
    m = re.search(r"(?ms)^```" + name + r"[ \t]*\n(.*?)\n```[ \t]*$", raw)
    return m.group(1) if m else None


def main(argv):
    global SPRACHE
    argv = list(argv)
    for flag in ("--en", "--englisch"):
        if flag in argv:
            argv.remove(flag)
            SPRACHE = "en"
    if not os.path.exists(WESTERN):
        warn(u"Western-Schrift nicht gefunden (%s) — es wird die "
             u"Standardschrift gesetzt" % WESTERN)
    if argv and argv[0] == "--alle":
        dateien = sorted(glob.glob(os.path.join(REPO, "Charaktere", "*.md")))
    else:
        dateien = [f for f in (bs.finde(a) for a in (argv or bs.AUSWAHL)) if f]
    if not os.path.isdir(AUSGABE):
        os.makedirs(AUSGABE)

    fertig = []
    for src in dateien:
        basis = os.path.splitext(os.path.basename(src))[0]
        ziel = os.path.join(AUSGABE, basis + "-dossier.pdf")
        n = dossier(src, ziel)
        if n:
            fertig.append(ziel)
            print(u"  %-46s %d Seiten" % (basis, n))

    if len(fertig) > 1:
        sammel = fitz.open()
        for z in fertig:
            e = fitz.open(z)
            e.bake()
            sammel.insert_pdf(e)
            e.close()
        pfad = os.path.join(AUSGABE, "Dossiers.pdf")
        try:
            sammel.subset_fonts()
        except Exception:
            pass
        sammel.save(pfad, garbage=4, deflate=True)
        print(u"\nSammelmappe: %s (%d Seiten)"
              % (os.path.basename(pfad), sammel.page_count))
        sammel.close()

    WARNUNGEN.extend(bs.WARNUNGEN)
    WARNUNGEN.extend(bh.WARNINGS)
    print(u"\nDossiers geschrieben: %d" % len(fertig))
    if WARNUNGEN:
        print(u"\nWarnungen (%d):" % len(WARNUNGEN))
        for w in WARNUNGEN:
            print(u"  ! " + w)


if __name__ == "__main__":
    main(sys.argv[1:])
