# -*- coding: utf-8 -*-
"""Rendert alle Markdown-Dateien des Repos als eigenstaendige HTML-Seiten."""
import os, re, io, glob
import markdown

REPO = os.path.dirname(os.path.abspath(__file__))

CSS = u"""
:root{
  --bg:#f4efe4; --panel:#fbf8f1; --ink:#241d16; --muted:#6b5d4c;
  --rule:#d8cdb8; --accent:#8c2f1d; --accent-soft:#b5563f;
  --quote-bg:#efe7d6; --code-bg:#e9e0cd; --link:#7a3b12;
}
@media (prefers-color-scheme:dark){
  :root:not([data-theme="light"]){
    --bg:#17140f; --panel:#1f1b15; --ink:#ece4d6; --muted:#a2937d;
    --rule:#3a3227; --accent:#e0755c; --accent-soft:#c9634c;
    --quote-bg:#241f18; --code-bg:#2a241c; --link:#e2a06f;
  }
}
:root[data-theme="dark"]{
  --bg:#17140f; --panel:#1f1b15; --ink:#ece4d6; --muted:#a2937d;
  --rule:#3a3227; --accent:#e0755c; --accent-soft:#c9634c;
  --quote-bg:#241f18; --code-bg:#2a241c; --link:#e2a06f;
}
*{box-sizing:border-box}
body{
  margin:0; background:var(--bg); color:var(--ink);
  font:16px/1.65 "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  -webkit-text-size-adjust:100%;
}
.wrap{max-width:44rem;margin:0 auto;padding:2.5rem 1.25rem 5rem}
nav.top{
  font:600 .72rem/1 ui-sans-serif,system-ui,"Segoe UI",sans-serif;
  letter-spacing:.09em;text-transform:uppercase;
  padding-bottom:1.5rem;margin-bottom:2rem;border-bottom:1px solid var(--rule);
  display:flex;gap:1.25rem;flex-wrap:wrap;
}
nav.top a{color:var(--muted);text-decoration:none}
nav.top a:hover{color:var(--accent)}
h1{
  font-size:2rem;line-height:1.15;margin:0 0 1.5rem;
  font-weight:700;letter-spacing:-.01em;
}
h2{
  font-size:1.05rem;margin:2.75rem 0 .9rem;color:var(--accent);
  font:700 .82rem/1.3 ui-sans-serif,system-ui,"Segoe UI",sans-serif;
  letter-spacing:.12em;text-transform:uppercase;
}
h3{font-size:1.12rem;margin:2rem 0 .6rem;font-weight:700}
p,ul,ol{margin:0 0 1.05rem}
ul,ol{padding-left:1.35rem}
li{margin-bottom:.4rem}
li>ul,li>ol{margin-top:.4rem}
a{color:var(--link);text-decoration:none;border-bottom:1px solid var(--rule)}
a:hover{color:var(--accent);border-bottom-color:var(--accent-soft)}
strong{font-weight:700}
em{font-style:italic}
hr{border:0;border-top:1px solid var(--rule);margin:2.5rem 0}
blockquote{
  margin:1.5rem 0;padding:.9rem 1.25rem;background:var(--quote-bg);
  border-left:3px solid var(--accent-soft);border-radius:0 4px 4px 0;
  font-size:1.05rem;
}
blockquote p:last-child{margin-bottom:0}
blockquote h3{margin-top:0;font-size:1rem;color:var(--accent)}
code{
  background:var(--code-bg);padding:.12em .38em;border-radius:3px;
  font:.86em/1.4 ui-monospace,"Cascadia Mono",Consolas,monospace;
}
pre{background:var(--code-bg);padding:1rem;border-radius:5px;overflow-x:auto}
pre code{background:none;padding:0}
.tablewrap{overflow-x:auto;margin:0 0 1.25rem}
table{border-collapse:collapse;width:100%;font-size:.94rem}
th,td{padding:.5rem .7rem;text-align:left;border-bottom:1px solid var(--rule);
      vertical-align:top}
th{
  font:700 .72rem/1.3 ui-sans-serif,system-ui,sans-serif;
  letter-spacing:.09em;text-transform:uppercase;color:var(--muted);
}
tbody tr:last-child td{border-bottom:0}
figure.portrait{margin:0 0 2rem}
figure.portrait img{
  display:block;width:100%;max-width:22rem;margin:0 auto;height:auto;
  border-radius:6px;border:1px solid var(--rule);
}
footer{
  margin-top:3.5rem;padding-top:1.25rem;border-top:1px solid var(--rule);
  color:var(--muted);font-size:.85rem;
}
footer a{color:var(--muted)}

/* ---- Baukasten / Charakterbogen ---- */
.charsheet{
  margin:0 0 2.5rem;padding:1.15rem 1.35rem 1.35rem;
  background:var(--panel);border:1px solid var(--rule);border-radius:8px;
}
.charsheet h3{
  margin:0 0 .55rem;font:700 .72rem/1.3 ui-sans-serif,system-ui,"Segoe UI",sans-serif;
  letter-spacing:.11em;text-transform:uppercase;color:var(--accent);
  display:flex;justify-content:space-between;align-items:baseline;gap:1rem;
}
.charsheet .cs-pts{
  font:700 .68rem/1 ui-sans-serif,system-ui,sans-serif;letter-spacing:.05em;
  color:var(--muted);border:1px solid var(--rule);border-radius:999px;
  padding:.22em .6em;white-space:nowrap;
}
.charsheet .cs-pts.bad{color:#fff;background:var(--accent);border-color:var(--accent)}
.cs-cols{display:grid;grid-template-columns:1fr 1.5fr;gap:1.75rem}
@media(max-width:36rem){.cs-cols{grid-template-columns:1fr;gap:1.4rem}}
.charsheet table{width:100%;font-size:.9rem;border-collapse:collapse}
.charsheet td,.charsheet th{padding:.26rem .45rem;border:0;vertical-align:baseline}
.charsheet tbody tr:not(:last-child) td{border-bottom:1px solid var(--rule)}
.charsheet .die{font-weight:700;white-space:nowrap}
.charsheet .lnk{color:var(--muted);font-size:.82em}
.charsheet .num{text-align:right;font-variant-numeric:tabular-nums;
  color:var(--muted);white-space:nowrap}
.charsheet .free{color:var(--muted);font-style:italic}
.cs-derived{
  margin:1.2rem 0 0;padding-top:.95rem;border-top:1px solid var(--rule);
  font:.82rem/1.5 ui-sans-serif,system-ui,sans-serif;letter-spacing:.03em;
  display:flex;flex-wrap:wrap;gap:.45rem 1.75rem;
}
.cs-derived span{color:var(--muted)}
.cs-derived b{color:var(--ink);font-weight:700}
.cs-ledger{margin-top:1.2rem;padding-top:.95rem;border-top:1px solid var(--rule);
  display:grid;grid-template-columns:1fr 1fr;gap:1.75rem}
@media(max-width:36rem){.cs-ledger{grid-template-columns:1fr;gap:1.4rem}}
.cs-ledger ul{margin:0;padding-left:1.15rem;font-size:.9rem}
.cs-ledger li{margin-bottom:.3rem}
.cs-ledger .tag{color:var(--muted);font-size:.82em}
.cs-kit{margin-top:1.2rem;padding-top:.95rem;border-top:1px solid var(--rule)}
.cs-kit h4{
  margin:0 0 .5rem;font:700 .68rem/1.3 ui-sans-serif,system-ui,sans-serif;
  letter-spacing:.11em;text-transform:uppercase;color:var(--muted);
}
.cs-kit + .cs-kit{margin-top:1.1rem}
.cs-kit ul{margin:0;padding-left:1.15rem;font-size:.9rem}
.cs-kit li{margin-bottom:.25rem}
.cs-kit .note{color:var(--muted);font-size:.88em}
.cs-kit .cost{color:var(--muted);font-variant-numeric:tabular-nums}
.cs-purse{margin-top:.55rem;font:.82rem/1.5 ui-sans-serif,system-ui,sans-serif;
  color:var(--muted);letter-spacing:.03em}
.cs-purse b{color:var(--ink)}
.cs-purse.bad b{color:var(--accent)}
@media print{
  body{background:#fff;color:#000;font-size:11pt}
  nav.top{display:none}
  .wrap{max-width:none;padding:0}
  a{color:#000;border:0}
}
"""

PAGE = u"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<style>%(css)s</style>
</head>
<body>
<div class="wrap">
<nav class="top">%(nav)s</nav>
%(body)s
<footer>Deadlands: The Weird West &middot; SWADE &middot; erzeugt aus %(src)s</footer>
</div>
</body>
</html>
"""


def nav_for(depth):
    up = "../" * depth
    return ("<a href=\"%sREADME.html\">Repo</a>"
            "<a href=\"%sCharakterideen.html\">Charaktere</a>"
            "<a href=\"%sRegelnotizen.html\">Regelnotizen</a>"
            "<a href=\"%sAbenteuer/index.html\">Abenteuer</a>") % (up, up, up, up)


def first_h1(md_text):
    m = re.search(r"^#\s+(.+)$", md_text, re.M)
    if not m:
        return "Deadlands"
    t = m.group(1)
    t = re.sub(r"\*+", "", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", t)
    return t.strip()


# --------------------------------------------------------------------------
# Baukasten: berechnet die Punktkosten aus den Wuerfeln und rendert den
# Charakterbogen. Die Kostenlogik lebt NUR hier -- die Bloecke in den
# Charakterdateien transkribieren blosse Wuerfelwerte, keine Arithmetik.
# --------------------------------------------------------------------------
DIE_STEPS = {4: 1, 6: 2, 8: 3, 10: 4, 12: 5}   # Wuerfeltyp -> Stufen ab W4/d4
AGI, SMA, SPI = u"Agility", u"Smarts", u"Spirit"
ATTR_ORDER = [AGI, SMA, SPI, u"Strength", u"Vigor"]

# Attribut-Alias -> englischer Anzeigename (dt. Eingabe wird normalisiert)
ATTR_EN = {
    u"Geschicklichkeit": AGI, u"Agility": AGI,
    u"Verstand": SMA, u"Smarts": SMA,
    u"Geist": SPI, u"Willenskraft": SPI, u"Spirit": SPI,
    u"Stärke": u"Strength", u"Strength": u"Strength",
    u"Konstitution": u"Vigor", u"Vigor": u"Vigor",
}

# (englischer Anzeigename, verknuepftes Attribut, Kernfertigkeit?, [dt. Aliasse])
SKILLS_DEF = [
    (u"Athletics", AGI, True, [u"Athletik"]),
    (u"Common Knowledge", SMA, True, [u"Allgemeinwissen"]),
    (u"Notice", SMA, True, [u"Bemerken"]),
    (u"Persuasion", SPI, True, [u"Überreden"]),
    (u"Stealth", AGI, True, [u"Heimlichkeit"]),
    (u"Fighting", AGI, False, [u"Kämpfen"]),
    (u"Shooting", AGI, False, [u"Schießen"]),
    (u"Riding", AGI, False, [u"Reiten"]),
    (u"Driving", AGI, False, [u"Fahren"]),
    (u"Boating", AGI, False, [u"Booten"]),
    (u"Piloting", AGI, False, [u"Fliegen"]),
    (u"Thievery", AGI, False, [u"Fingerfertigkeit", u"Schlösser knacken",
                               u"Diebeshandwerk"]),
    (u"Faith", SPI, False, [u"Glaube"]),
    (u"Focus", SPI, False, [u"Fokus"]),
    (u"Intimidation", SPI, False, [u"Einschüchtern"]),
    (u"Performance", SPI, False, [u"Auftreten", u"Aufführen"]),
    (u"Taunt", SMA, False, [u"Provozieren", u"Verspotten", u"Spotten", u"Spott"]),
    (u"Healing", SMA, False, [u"Heilen", u"Heilkunde"]),
    (u"Occult", SMA, False, [u"Okkultismus"]),
    (u"Research", SMA, False, [u"Nachforschungen", u"Nachforschung",
                               u"Nachforschen", u"Recherche"]),
    (u"Science", SMA, False, [u"Wissenschaft", u"Naturwissenschaften"]),
    (u"Academics", SMA, False, [u"Bildung", u"Gelehrsamkeit"]),
    (u"Survival", SMA, False, [u"Überleben"]),
    (u"Gambling", SMA, False, [u"Glücksspiel"]),
    (u"Language", SMA, False, [u"Sprache", u"Sprachen"]),
    (u"Repair", SMA, False, [u"Reparieren", u"Handwerk"]),
    (u"Weird Science", SMA, False, [u"Seltsame Wissenschaft",
                                    u"Verrückte Wissenschaft"]),
    (u"Spellcasting", SMA, False, [u"Zaubern", u"Hexerei", u"Zauberei"]),
    (u"Alchemy", SMA, False, [u"Alchemie"]),
]

# Alias (engl. + dt.) -> (Anzeigename, Attribut, Kern?)
SKILL_LINK = {}
for _en, _at, _core, _al in SKILLS_DEF:
    SKILL_LINK[_en] = (_en, _at, _core)
    for _a in _al:
        SKILL_LINK[_a] = (_en, _at, _core)

# Handicap-Schwere: Eingabe -> (Punkte, Anzeige)
SEVERITY = {u"schwer": (2, u"Major"), u"Major": (2, u"Major"),
            u"leicht": (1, u"Minor"), u"Minor": (1, u"Minor")}

WARNINGS = []


def parse_sections(text):
    """Ein Fenced Block aus Skalarzeilen (``Start: 250``) und Abschnitten
    (``Waffen:`` gefolgt von ``- a | b | c``-Zeilen). Rueckgabe:
    (skalare, abschnitte) -- beide Schluessel kleingeschrieben."""
    skalar, abschnitte, aktuell = {}, {}, None
    for line in (text or "").splitlines():
        if not line.strip():
            continue
        m = re.match(r"^\s*-\s*(.+)$", line)
        if m and aktuell is not None:
            abschnitte[aktuell].append([c.strip() for c in m.group(1).split("|")])
            continue
        m = re.match(r"^\s*([^:]+):\s*(.*)$", line)
        if m:
            key, val = m.group(1).strip().lower(), m.group(2).strip()
            if val:
                skalar[key] = val
                aktuell = None
            else:
                aktuell = key
                abschnitte[aktuell] = []
    return skalar, abschnitte


def preis(tok):
    """``$12,50`` / ``$1.50`` / ``50¢`` / ``-`` -> float."""
    tok = (tok or "").strip()
    if not tok or tok in (u"-", u"—", u"–"):
        return 0.0
    m = re.match(r"^(\d+(?:[.,]\d+)?)\s*¢$", tok)
    if m:
        return float(m.group(1).replace(",", ".")) / 100.0
    m = re.match(r"^\$?\s*(\d+(?:[.,]\d+)?)$", tok)
    if m:
        return float(m.group(1).replace(",", "."))
    WARNINGS.append(u"Preis nicht lesbar: %r" % tok)
    return 0.0


def geld(betrag):
    """0.5 -> ``50¢``, 12.5 -> ``$12,50``, 50.0 -> ``$50``."""
    if abs(betrag - round(betrag)) < 0.005:
        return u"$%d" % int(round(betrag))
    return (u"$%.2f" % betrag).replace(".", ",")


ABSCHNITT = {u"ausrüstung": "gear", u"ausruestung": "gear", u"gear": "gear",
             u"waffen": "weapons", u"weapons": "weapons",
             u"notizen": "notes", u"notes": "notes",
             u"mächte": "powers", u"maechte": "powers", u"powers": "powers"}


def _sections(text):
    skalar, roh = parse_sections(text)
    return skalar, dict((ABSCHNITT.get(k, k), v) for k, v in roh.items())


def _die_step(tok):  # akzeptiert d8 (engl.) wie W8 (dt.)
    m = re.search(r"\d+", tok or "")
    return DIE_STEPS.get(int(m.group())) if m else None


def _half(die):  # halber Wuerfeltyp: d8 -> 4
    return int(re.search(r"\d+", die).group()) // 2


def _split_die(entry):
    m = re.match(r"^(.*?)\s+([WwDd]\d+(?:[+-]\d+)?)$", entry.strip())
    return (m.group(1).strip(), m.group(2)) if m else (entry.strip(), None)


def _attr_cost(die):
    return _die_step(die) - 1


def _skill_cost(die, attr_die, core):
    s, a = _die_step(die), _die_step(attr_die)
    start = 2 if core else 1          # Kernfertigkeit besitzt W4 gratis
    return sum(1 if lv <= a else 2 for lv in range(start, s + 1))


def _parse_build(text):
    d = {}
    for line in text.splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            d[k.strip().lower()] = v.strip()
    return d


def _pts_badge(got, want):
    # Ueberziehen ist regelwidrig (rot); Unterschreiten ist erlaubt (neutral)
    cls = " bad" if got > want else ""
    return '<span class="cs-pts%s">%d / %d</span>' % (cls, got, want)


def render_build(text, base):
    d = _parse_build(text)
    esc = lambda s: (s.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;"))

    # -- Attributes ------------------------------------------------------
    attr_die = {}
    for x in (d.get("attribute") or d.get("attributes", "")).split(","):
        if not x.strip():
            continue
        nm, die = _split_die(x)
        attr_die[ATTR_EN.get(nm, nm)] = die
    arows, acost = [], 0
    for name in ATTR_ORDER:
        die = attr_die.get(name)
        if not die:
            WARNINGS.append("%s: Attribut fehlt: %s" % (base, name))
            continue
        c = _attr_cost(die)
        acost += c
        arows.append('<tr><td>%s</td><td class="die">%s</td>'
                     '<td class="num">%d</td></tr>' % (esc(name), die, c))
    attr_html = (
        '<div class="cs-block"><h3>Attributes %s</h3><table><tbody>%s</tbody>'
        '</table></div>' % (_pts_badge(acost, 5), "".join(arows)))

    # -- Fertigkeiten ----------------------------------------------------
    bonus = int(re.match(r"\d+", d.get("bonus", "0") or "0").group() or 0) \
        if re.match(r"\d+", d.get("bonus", "0") or "0") else 0
    srows, scost, fight = [], 0, None
    for entry in [x for x in (d.get("fertigkeiten") or
                              d.get("skills", "")).split(",") if x.strip()]:
        name, die = _split_die(entry)
        lookup = re.sub(r"\s*\(.*?\)\s*$", "", name).strip()  # "Language (English)"
        link = SKILL_LINK.get(lookup)
        if not link:
            WARNINGS.append("%s: unbekannte Fertigkeit: %s" % (base, name))
            srows.append('<tr><td>%s</td><td class="lnk">?</td>'
                         '<td class="die">%s</td><td class="num">?</td></tr>'
                         % (esc(name), die or "?"))
            continue
        disp, latt, lcore = link
        if disp == u"Fighting":
            fight = die
        paren = re.search(r"\((.*?)\)\s*$", name)
        show = disp + (" (%s)" % paren.group(1) if paren else "")
        adie = attr_die.get(latt)
        c = _skill_cost(die, adie, lcore)
        scost += c
        cost_txt = ('<span class="free">core</span>' if (lcore and c == 0)
                    else str(c))
        srows.append('<tr><td>%s</td><td class="lnk">%s</td>'
                     '<td class="die">%s</td><td class="num">%s</td></tr>'
                     % (esc(show), latt[:3], die, cost_txt))
    want = 12 + bonus
    hdr = "Skills" + (" (12&#8202;+&#8202;%d bonus)" % bonus if bonus else "")
    skill_html = (
        '<div class="cs-block"><h3>%s %s</h3><table><thead><tr>'
        '<th>Skill</th><th>Attr.</th><th>Die</th>'
        '<th class="num">Pts.</th></tr></thead><tbody>%s</tbody></table></div>'
        % (hdr, _pts_badge(scost, want), "".join(srows)))

    # -- Derived stats ---------------------------------------------------
    pace = d.get("tempo") or d.get("pace") or "6"
    armraw = d.get("rüstung") or d.get("armor") or "0"
    armor = int(re.match(r"\d+", armraw).group()) if re.match(r"\d+", armraw) else 0
    parry = 2 + (_half(fight) if fight else 0)
    vig = attr_die.get(u"Vigor")
    tough = 2 + (_half(vig) if vig else 0) + armor
    tough_txt = str(tough) + (" (%d+%d)" % (tough - armor, armor) if armor else "")
    # Vorlagen-Boni (Untot, Groesse ...) sind keine Punktkaeufe -> Override
    parry_txt = d.get("parade") or d.get("parry") or str(parry)
    tough_txt = d.get("robustheit") or d.get("toughness") or tough_txt
    derived = ('<div class="cs-derived"><span>Pace</span> <b>%s</b>'
               '<span>Parry</span> <b>%s</b>'
               '<span>Toughness</span> <b>%s</b></div>'
               % (esc(pace), esc(parry_txt), esc(tough_txt)))

    # -- Handicaps & Talente (Kontobuch) --------------------------------
    def _hind_items(raw_):
        items, tot = [], 0
        for h in [x.strip() for x in raw_.split(",") if x.strip()]:
            m = re.search(r"\((schwer|leicht|Major|Minor)\)", h)
            if m:
                pts, label = SEVERITY[m.group(1)]
                tot += pts
                disp = re.sub(r"\((schwer|leicht|Major|Minor)\)",
                              "(%s)" % label, h)
                items.append('<li>%s <span class="tag">%d</span></li>'
                             % (esc(disp), pts))
            else:
                items.append('<li>%s</li>' % esc(h))
        return items, tot

    # dt. Schluessel (Handicaps/Talente) und engl. (Hindrances/Edges) erlaubt
    hitems, htot = _hind_items(d.get("handicaps") or d.get("hindrances", ""))
    edges_raw = d.get("talente") or d.get("edges", "")
    # Edges durch " | " getrennt; [Anmerkung] wird zu einem Tag
    titems = ['<li>%s</li>' % re.sub(r"\[([^\]]*)\]",
                                     r'<span class="tag">\1</span>', esc(t.strip()))
              for t in edges_raw.split("|") if t.strip()]
    ledger = (
        '<div class="cs-ledger"><div class="cs-block">'
        '<h3>Hindrances %s</h3><ul>%s</ul></div>'
        '<div class="cs-block"><h3>Edges</h3><ul>%s</ul></div></div>'
        % (_pts_badge(htot, 4), "".join(hitems), "".join(titems)))

    return ('<section class="charsheet"><div class="cs-cols">%s%s</div>%s%s'
            '</section>' % (attr_html, skill_html, derived, ledger))


def render_kit(gear_text, powers_text, base):
    """Rendert ```gear``` und ```powers``` als Anhang der Charakterbogen-Karte.
    Die Dollarrechnung passiert hier -- der Block listet nur Preise."""
    esc = lambda s: (s.replace("&", "&amp;").replace("<", "&lt;")
                     .replace(">", "&gt;"))
    g_sk, g_ab = _sections(gear_text)
    p_sk, p_ab = _sections(powers_text)
    teile = []

    ausr, waffen = g_ab.get("gear", []), g_ab.get("weapons", [])
    if ausr or waffen:
        items = []
        for r in ausr:
            kosten = r[1] if len(r) > 1 else u""
            note = r[3] if len(r) > 3 and r[3] else u""
            items.append(
                '<li>%s%s%s</li>'
                % (esc(r[0]),
                   ' <span class="cost">%s</span>' % esc(kosten)
                   if kosten and preis(kosten) else "",
                   ' <span class="note">&mdash; %s</span>' % esc(note)
                   if note else ""))
        start = float(g_sk.get("start", 250))
        weg = (sum(preis(r[1]) for r in ausr if len(r) > 1)
               + sum(preis(r[6]) for r in waffen if len(r) > 6))
        purse = ('<div class="cs-purse%s">%s ausgegeben von %s &middot; '
                 '<b>%s</b> Bargeld</div>'
                 % (" bad" if weg > start else "", geld(weg), geld(start),
                    geld(start - weg)))
        if weg > start:
            WARNINGS.append("%s: Startgeld ueberzogen (%s von %s)"
                            % (base, geld(weg), geld(start)))
        teile.append('<div class="cs-kit"><h4>Gear</h4><ul>%s</ul>%s</div>'
                     % ("".join(items), purse))

    if waffen:
        kopf = ["Weapon", "Range", "Damage", "AP", "RoF", "Wt.", "Cost"]
        rows = []
        for r in waffen:
            zellen = (r + [""] * 8)[:7]
            note = r[7] if len(r) > 7 and r[7] else ""
            rows.append("<tr>%s</tr>" % "".join(
                "<td>%s</td>" % esc(c) for c in zellen)
                + ('<tr><td colspan="7" class="note">%s</td></tr>' % esc(note)
                   if note else ""))
        teile.append(
            '<div class="cs-kit"><h4>Weapons</h4><table><thead><tr>%s</tr>'
            '</thead><tbody>%s</tbody></table></div>'
            % ("".join("<th>%s</th>" % h for h in kopf), "".join(rows)))

    maechte = p_ab.get("powers", [])
    if maechte:
        kopf = ["Power", "PP", "Range", "Dur.", "Effect"]
        rows = ["<tr>%s</tr>" % "".join("<td>%s</td>" % esc(c)
                                        for c in (r + [""] * 5)[:5])
                for r in maechte]
        pp = p_sk.get("machtpunkte") or p_sk.get("power points")
        teile.append(
            '<div class="cs-kit"><h4>Powers%s</h4><table><thead><tr>%s</tr>'
            '</thead><tbody>%s</tbody></table></div>'
            % (" (%s PP)" % esc(pp) if pp else "",
               "".join("<th>%s</th>" % h for h in kopf), "".join(rows)))

    for note in g_ab.get("notes", []):
        teile.append('<div class="cs-kit"><p class="note">%s</p></div>'
                     % esc(u" · ".join(note)))
    return "".join(teile)


def main():
    targets = (glob.glob(os.path.join(REPO, "*.md"))
               + glob.glob(os.path.join(REPO, "Archetypen", "*.md"))
               + glob.glob(os.path.join(REPO, "Charaktere", "*.md")))

    md = markdown.Markdown(extensions=["extra", "sane_lists", "smarty"],
                           extension_configs={"smarty": {"substitutions": {
                               "left-double-quote": "\u201e",
                               "right-double-quote": "\u201c"}}})

    count = 0
    for src in sorted(targets):
        raw = io.open(src, encoding="utf-8").read()

        # Baukasten-Block herausloesen und durch Platzhalter ersetzen
        base = os.path.splitext(os.path.basename(src))[0]
        card_html = ""
        gear_txt = powers_txt = None
        for nm in ("gear", "powers"):
            m = re.search(r"(?ms)^```%s[ \t]*\n(.*?)\n```[ \t]*$" % nm, raw)
            if m:
                if nm == "gear":
                    gear_txt = m.group(1)
                else:
                    powers_txt = m.group(1)
                raw = raw[:m.start()] + raw[m.end():]
        bm = re.search(r"(?ms)^```build[ \t]*\n(.*?)\n```[ \t]*$", raw)
        if bm:
            card_html = render_build(bm.group(1), base)
            if gear_txt or powers_txt:
                card_html = card_html.replace(
                    "</section>", render_kit(gear_txt, powers_txt, base)
                    + "</section>")
            raw = raw[:bm.start()] + "\nBUILDCARDPLACEHOLDER\n" + raw[bm.end():]

        md.reset()
        html = md.convert(raw)
        if card_html:
            html = html.replace("<p>BUILDCARDPLACEHOLDER</p>", card_html)

        # interne .md-Links auf .html umbiegen
        html = re.sub(r'(href="[^"]*?)\.md(?=("|#))', r"\1.html", html)
        # smartypants macht aus Jahreszahlen wie '84 ein oeffnendes Anfuehrungs-
        # zeichen; es ist ein Apostroph (Auslassung des Jahrhunderts)
        html = re.sub(r"&lsquo;(?=\d)", "&rsquo;", html)
        # breite Tabellen horizontal scrollbar machen
        html = html.replace("<table>", '<div class="tablewrap"><table>')
        html = html.replace("</table>", "</table></div>")

        # Charakterseiten: gleichnamiges Portraet aus Bilder/ unter den Titel setzen
        base = os.path.splitext(os.path.basename(src))[0]
        if (os.path.basename(os.path.dirname(src)) == "Charaktere"
                and os.path.exists(os.path.join(REPO, "Bilder", base + ".png"))):
            fig = ('<figure class="portrait"><img src="../Bilder/%s.png" '
                   'alt="%s"></figure>' % (base, first_h1(raw)))
            html = html.replace("</h1>", "</h1>\n" + fig, 1)

        rel = os.path.relpath(src, REPO)
        depth = rel.count(os.sep)
        out = os.path.splitext(src)[0] + ".html"
        io.open(out, "w", encoding="utf-8", newline="\n").write(PAGE % {
            "title": first_h1(raw), "css": CSS, "nav": nav_for(depth),
            "body": html, "src": os.path.basename(src)})
        count += 1

    # GitHub-Pages-Einstieg: index.html leitet auf die Charakteruebersicht,
    # .nojekyll verhindert Jekyll-Verarbeitung (Dateien werden 1:1 ausgeliefert).
    io.open(os.path.join(REPO, ".nojekyll"), "w", encoding="utf-8").write(u"")
    io.open(os.path.join(REPO, "index.html"), "w", encoding="utf-8",
            newline="\n").write(
        u'<!doctype html>\n<html lang="de">\n<head>\n<meta charset="utf-8">\n'
        u'<meta name="viewport" content="width=device-width,initial-scale=1">\n'
        u'<meta http-equiv="refresh" content="0; url=Charakterideen.html">\n'
        u'<title>Deadlands: The Weird West — Charaktere</title>\n'
        u'<style>body{margin:0;min-height:100vh;display:flex;align-items:center;'
        u'justify-content:center;background:#17140f;color:#ece4d6;'
        u'font:16px/1.6 "Iowan Old Style",Palatino,Georgia,serif}'
        u'a{color:#e2a06f}</style>\n</head>\n<body>\n'
        u'<p><a href="Charakterideen.html">Deadlands-Charaktere &rarr;</a></p>\n'
        u'</body>\n</html>\n')

    print("HTML-Dateien geschrieben: %d" % count)
    if WARNINGS:
        print("\nBaukasten-Warnungen (%d):" % len(WARNINGS))
        for w in WARNINGS:
            print("  ! " + w)


if __name__ == "__main__":
    main()
