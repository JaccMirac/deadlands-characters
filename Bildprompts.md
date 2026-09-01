# Bildprompts (Midjourney 8.2)

Ein Prompt pro Figur, 32 Stück plus ein NSC, in derselben Reihenfolge wie
[`Charakterideen.md`](Charakterideen.md). Die Prompts sind englisch, weil
Midjourney englische Bildbegriffe deutlich zuverlässiger auflöst; die
Bildidee darüber steht auf Deutsch.

## Erst lesen, dann kopieren

**Es gibt kein `--v 8.2`.** Version 8.2 ist seit dem 24. Juli 2026 das
Standardmodell — jeder neue Prompt läuft ohnehin darauf, ganz ohne
Versions-Flag. Das `--preview`-Flag aus der Testphase wird nicht mehr
gebraucht. Wer *zurück* will, hängt `--v 8.1` an. Die Prompts unten sind
deshalb ohne Versionsangabe geschrieben — sie sind 8.2, weil alles 8.2 ist.

**Ein Deck, ein Look.** 33 Bilder sehen nur dann nach einem Satz
Charakterkarten aus, wenn sie eine gemeinsame Stilklammer haben. Der
Werkzeugkasten dafür in 8.2:

| Mittel | Wirkung |
| --- | --- |
| `--sref <code>` | Stil-Referenz. In 8.2 spürbar konsistenter als vorher. **Das ist der Hebel.** |
| `--profile <id>` | Dein Personalisierungsprofil; 8.2 wurde genau darauf optimiert. |
| `--stylize 150` | niedrig gehalten, damit die Prompt-Details überleben |
| `--ar 2:3` | Hochformat, passt auf eine Charakterkarte |
| `--hd` | größere Ausgabe, wenn gedruckt werden soll |

Praktisch: **einen** Prompt laufen lassen, das schönste Bild auswählen,
dessen `--sref`-Code ziehen und ihn an alle 33 anhängen. Der Stilblock
steht trotzdem in jedem Prompt ausgeschrieben, damit jeder einzeln
funktioniert.

**`--oref` funktioniert in der V8-Reihe nicht.** Omni Reference — das
Werkzeug für „dieselbe Person in mehreren Bildern" — wird von V8 (Stand
Juni 2026) nicht unterstützt. Für eine zweite Ansicht derselben Figur
bleiben also nur `--sref` plus ein sehr präzise wiederholter Prompt.

**Die Wortwahl ist Absicht.** Vier Figuren sind Gepeinigte, Büßer oder
Preisboxer, und die naheliegenden Wörter — Leiche, Blut, Wunde, Strang —
laufen bei Midjourney regelmäßig in den Filter. Die Prompts umschreiben
das durchgehend („a faint dark line above the collar", „an old healed
hollow above the left temple"). Wer sie umformuliert, sollte das im Kopf
behalten.

**Zweiter Stil.** Der Stilblock unten ist Nassplatten-Fotografie, also
periodenecht und einheitlich. Wer stattdessen Titelbild-Optik will,
ersetzt in jedem Prompt

> `wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws`

durch

> `moody oil painting, 1880s weird western, dramatic chiaroscuro, muted earth palette with a single rust-red accent, visible brushwork`

**Andere Einstellung.** Die Prompts sind Brustbild bis Halbfigur. Für eine
Ganzkörper-Variante `half-length portrait` durch `full length figure,
environmental shot` ersetzen; für Action `standing still` durch die
konkrete Handlung.

## Wohin die Bilder gehören

Alle Bilder liegen flach in **`Bilder/`** — kein Unterordner pro Figur. Der
Dateiname ist derselbe wie der der Charakterdatei, nur mit Bildendung, und
steht unter jedem Prompt als *Ablage* dabei. Weil die Namen mit der
Archetyp-Nummer beginnen, sortiert der Ordner sich von allein in dieselbe
Reihenfolge wie [`Charakterideen.md`](Charakterideen.md).

```
Charaktere/01-1-silas-deacon-crowe.md   →   Bilder/01-1-silas-deacon-crowe.png
```

Mehrere Fassungen derselben Figur bekommen einen Buchstaben angehängt —
`01-1-silas-deacon-crowe-b.png`, `-c.png` und so weiter. Der Name ohne
Buchstaben ist immer die Fassung, die gilt; dann muss nichts umbenannt
werden, wenn später Bilder in die Seiten eingebunden werden.

Midjourney-Downloads heißen `user_a_gaunt_hollow-cheeked_9f3c1a2b….png`.
Umbenennen ist kein Zierschritt: nach zwanzig Downloads weiß niemand mehr,
welcher Silas welcher ist.

---

## 01 · [GUNSLINGER (Revolverheld)](Archetypen/01-gunslinger.md)

### [Silas „Deacon" Crowe](Charaktere/01-1-silas-deacon-crowe.md)

*Neununddreißig und sieht aus wie sechzig. Der Prediger-Rock und die zwölf Kerben sind derselbe Beruf.*

```
half-length portrait of a gaunt hollow-cheeked white man of thirty-nine who looks sixty, consumptive grey pallor, sunken pale eyes, thin sandy hair, a worn black circuit preacher's frock coat gone green at the seams, a Colt revolver with twelve small notches filed into the backstrap riding in a cutaway holster, a folded grey handkerchief in one fist, standing perfectly still in the middle of a dusty street at high noon, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/01-1-silas-deacon-crowe.png`

### [Wilhelmina „Billie" Kessler](Charaktere/01-2-wilhelmina-billie-kessler.md)

*Preußische Büchsenmacherstochter auf dem Grat. Das Gewehr ist eine Nummer zu groß und sie weiß es.*

```
half-length portrait of a wind-burned white woman in her early twenties, blonde hair pinned flat under a low crowned hat, oversized canvas duck coat, cartridge belt, kneeling behind a rock ridge with an enormous single shot buffalo rifle braced across the stone, long brass telescopic sight, a cool contemptuous set to her mouth, prairie haze below her, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/01-2-wilhelmina-billie-kessler.png`

### [Hazel Quist — „Glass Hazel"](Charaktere/01-3-hazel-quist-die-trickschutzin.md)

*Mitten in der Nummer, nur gibt es die Schau nicht mehr: sie wirft selbst, und niemand sieht zu.*

```
full length figure, environmental shot of a lean fair-haired woman of twenty-one, Scandinavian features, wind-chapped cheeks, a fringed show costume with tarnished spangles worn over ordinary work clothes, one sleeve mended twice, caught mid-act: a single action revolver extended at arm's length and angled steeply upward, a thin plume of white powder smoke, high above her a glass ball bursting into a slow cloud of feathers and glass, her eyes already on the second ball still rising, the empty rutted lot behind a shuttered depot, no crowd, only a horse tied to the rail and a torn circus playbill nailed to the weathered boards, smoke and feathers smeared by the long exposure while she stands sharp, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/01-3-hazel-quist-die-trickschutzin.png`

---

## 02 · [BOUNTY HUNTER (Kopfgeldjäger)](Archetypen/02-bounty-hunter.md)

### [Absalom Freed](Charaktere/02-1-absalom-freed-genannt-the-long-sunday.md)

*Einundfünfzig, langsam im Reden, beunruhigend geduldig. Er bringt sie atmend zurück.*

```
half-length portrait of a Black man of fifty-one with a close greying beard and very still watchful eyes, weathered wide brim hat, plain trail coat over a collarless shirt, a coiled rawhide lariat over one shoulder, a lever action carbine cradled in the crook of his arm, iron handcuffs hanging at his belt, standing at the edge of a bottomland treeline at dusk, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/02-1-absalom-freed-genannt-the-long-sunday.png`

### [María Refugio Alvarado, „Cuca"](Charaktere/02-2-maria-refugio-alvarado-genannt-cuca.md)

*Sie legt die Flinte auf den Tresen, sagt den Namen laut und lässt den Raum entscheiden.*

```
half-length portrait of a Mexican woman of thirty-two, dark hair pulled back, a dead man's oversized stetson pushed back on her head with a small courtroom photograph tucked in the hat band, men's boots and a short riding jacket, a sawed off double barrel shotgun laid flat on a saloon bar in front of her, one hand resting on it, chin lifted, half the room behind her already turning to look, lamplit interior, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/02-2-maria-refugio-alvarado-genannt-cuca.png`

### [Ephraim Doak](Charaktere/02-3-ephraim-doak-der-leichenbestatter.md)

*Leichenbestatter, der Kopfgelder eintreibt, weil er die Fracht ohnehin fährt. Der Wagen ist die halbe Figur.*

```
half-length portrait of a narrow-shouldered white man of about forty in a black undertaker's suit and bowler hat, pale careful eyes, ink-stained fingers, a folded oilcloth ledger under one arm, standing beside a two-wheeled buckboard whose zinc-lined bed holds two plain pine coffins packed in sawdust, a block and tackle hanging from the cart frame, a revolver worn without display, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/02-3-ephraim-doak-der-leichenbestatter.png`

---

## 03 · [HARROWED (Gepeinigte)](Archetypen/03-harrowed.md)

### [Prudence „Pru" Mabry](Charaktere/03-1-prudence-pru-mabry.md)

*Zugeknöpft bei jedem Wetter. Der Kopf sitzt leicht falsch, und sie kann nicht nach oben blicken.*

```
half-length portrait of a pale white woman in her thirties with doughy bloodless skin, a broad flat hat pulled low, smoked glass spectacles, a high tightly buttoned collar worn in warm weather with a faint dark line just showing above it, long sleeves buttoned to the wrist, her head set very slightly wrong on her neck, a cut down lever action carbine held across her body, standing among cottonwoods at first light, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/03-1-prudence-pru-mabry.png`

### [Ezekiel „Zeke" Cornish](Charaktere/03-2-ezekiel-zeke-cornish-angekundigt-als-der-amboss-von-kentucky.md)

*Der Amboss von Kentucky, bei der Arbeit ohne Hut. Fünf Cent, um die Delle anzufassen.*

```
half-length portrait of an enormous barrel chested white prizefighter, no hat, shirt sleeves rolled over forearms like hams, an old healed hollow the size of a hand above his left temple with the hairline running into it, the left eye not quite tracking with the right, fine brass wire stitched along the jaw on that side, a heavy hickory wagon spoke carried at his hip, a fistful of printed handbills showing his own face, grinning crookedly at a crowd, carnival lamplight, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/03-2-ezekiel-zeke-cornish-angekundigt-als-der-amboss-von-kentucky.png`

---

## 04 · [TERRITORIAL RANGER (Territorialer Ranger)](Archetypen/04-territorial-ranger.md)

### [Amos Dell „Ledger" Ledbetter](Charaktere/04-1-amos-dell-ledbetter-genannt-ledger-der-institutionalist.md)

*Der Mann, der auf der Straße stehen bleibt. Und danach den Bericht schreibt.*

```
half-length portrait of a broad shouldered Black man in his late thirties with a stiff left shoulder, an armored riding duster buttoned to the throat, a five pointed star pinned to his chest, a pump action shotgun held muzzle down, an oilcloth wrapped field notebook and a stub pencil in his off hand, absolutely planted stance, standing alone in the middle of a rutted main street, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/04-1-amos-dell-ledbetter-genannt-ledger-der-institutionalist.png`

### [Adelaide „Addie" Kroll](Charaktere/04-2-adelaide-addie-kroll-die-wegen-der-akten-kam.md)

*Klein, tadellos, und mitten im Verhör. Der Mantel ist geschneidert, das Korsett gepanzert.*

```
half-length portrait of a small neat white woman of twenty-one, dark hair pinned severely, a well tailored grey travelling coat over a stiffened corset, a ranger's star worn openly at the lapel, a gold pocket watch on a chain, leaning slightly across a table toward someone unseen with an expression of patient friendly certainty, a stack of official papers under her hand, a jail office at night, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/04-2-adelaide-addie-kroll-die-wegen-der-akten-kam.png`

### [Tobias „Toby" Mullan](Charaktere/04-3-tobias-toby-mullan-der-junge-ranger.md)

*Neunzehn, in der Ausrüstung eines Toten. Alles an ihm ist zwei Nummern zu groß außer der Entschlossenheit.*

```
half-length portrait of a nineteen year old white ranch hand with a thin unshaven jaw and an unlined face, an oversized armored riding duster with the cuffs turned back twice, a lawman's five point star pinned slightly crooked to the chest, a single barrel shotgun held across the body, a battered stetson too large for him, morning light on an empty road behind him, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/04-3-tobias-toby-mullan-der-junge-ranger.png`

---

## 05 · [HUCKSTER (Taschenspieler)](Archetypen/05-huckster.md)

### [Cordelia „Cold Deck" Vance](Charaktere/05-1-cordelia-cold-deck-vance.md)

*Sie spielt nicht mit dem Teufel, sie hat ihn unter Vertrag. Die Karten in der Luft hält niemand.*

```
half-length portrait of a composed white woman of thirty in an immaculately tailored gambler's suit and standing collar, seated at a green baize faro table, a fan of playing cards hanging in the air in front of her dealt from a deck no one is holding, a battered leather bound book of games and a green ledger at her elbow, a derringer in a sleeve rig just visible, faint amused half smile, riverboat saloon lamplight, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/05-1-cordelia-cold-deck-vance.png`

### NSC · Mr. Pettibone

*Cordelias Manitou. Kein Monster — ein kahler Buchhalter mit Bleistift hinterm Ohr. Das Bild hat zwei Hälften: links sitzt er, rechts zeigt der Spiegel denselben Raum ohne ihn.*

```
half-length portrait of a bald courteous clerk of about fifty-five, a close fringe of grey hair above the ears, a carpenter's pencil tucked behind one ear, a plain dark suit twenty years out of fashion, celluloid cuffs, seated at a plain deal desk in a small rented office, a bowler hat and a closed green cloth ledger on the desk beside a kerosene lamp, a patient half-smile, looking straight into the camera; a tall mirror fills the right half of the frame, angled so that the man and the mirror stand side by side in the same photograph; the mirror shows the same desk, the same lamp, the same ledger, the same hat and an empty chair — the room exactly as it is, only without him; the mirror rendered in the same sharp focus and the same detail as the man, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/05-1-mr-pettibone.png`

### [Elijah Prosper Teague](Charaktere/05-2-elijah-prosper-teague.md)

*Der Chiffrierschreiber, der es geknackt hat und seither nicht mehr schläft.*

```
half-length portrait of a thin Black schoolteacher in his forties, wire rimmed spectacles, a threadbare dark suit and waistcoat, exhausted sleepless eyes, seated at a plank table by lamplight covered in stiff hand ruled index cards laid out in a grid, one card held upright between two fingers, an annotated leather book of games open beside three bound notebooks and a small brown bottle, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/05-2-elijah-prosper-teague.png`

---

## 06 · [HEXSLINGER (Runenschütze)](Archetypen/06-hexslinger.md)

### [Ezekiel „Deacon" Purefoy](Charaktere/06-1-ezekiel-deacon-purefoy-der-duellant.md)

*Zweiundzwanzig, mit der Pferdepistole seines Vaters. Die Runen sind seine eigene Arbeit — und tot.*

```
half-length portrait of a lean nervous white man of twenty-two with a preacher's son's haircut, plain dark coat, holding up an enormous old horse pistol with a very long barrel, four rows of hand filed norse rune staves cut along both barrel flats, silver wire hammered into the walnut grip in a card diagram pattern, the word AMEN filed into the backstrap, talking quietly to the gun, three dime novels rebound in oilcloth sticking out of his coat pocket, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/06-1-ezekiel-deacon-purefoy-der-duellant.png`

### [Delphine „Della" Tourneur](Charaktere/06-2-delphine-della-tourneur-die-unterstutzungsschutzin.md)

*Sie lädt am Lagerfeuer Patronen, eine nach der anderen, während die Waffe redet.*

```
half-length portrait of a Creole woman of twenty from New Orleans, dark curling hair under a plain kerchief, a river traveller's coat, sitting at a low campfire loading cartridges one at a time, a short sawed off double barrel shotgun across her knees with a cracked walnut stock bound in brass wire and a strip of red gambler's ribbon, a small crescent of neat tooth marks in the underside of the forestock, her head tilted as if listening to it, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/06-2-delphine-della-tourneur-die-unterstutzungsschutzin.png`

---

## 07 · [BLESSED (Gesegnete)](Archetypen/07-blessed.md)

### [„Rabbi" Feivel Zilber](Charaktere/07-1-rabbi-feivel-zilber.md)

*Der wärmste Mann am Tisch, mit den Papieren eines Toten in der Tasche.*

```
half-length portrait of a warm faced Ashkenazi Jewish peddler of thirty-five with a short dark beard, a much mended long coat, a heavy pack of needles thread spectacles tin cups and ribbons on his back, small leather phylactery boxes and straps held in both hands, a prayer shawl folded over one arm, a water stained folio volume under his elbow, a mule waiting behind him on an empty hill road, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/07-1-rabbi-feivel-zilber.png`

### [Hermano Sixto Trujillo y Vigil](Charaktere/07-2-hermano-sixto-trujillo-y-vigil.md)

*Sargmacher und Büßer. Kein Licht, kein Glühen — nur die Axt, die kalt wird.*

```
half-length portrait of a heavyset Nuevomexicano carpenter of forty with sawdust in his forearms and a closed exhausted face, coarse homespun shirt, a black cloth hood pushed back off his head, a broad coffin maker's broadaxe resting head down at his feet, a braided yucca fiber cord coiled at his belt, a thirty centimetre hand carved wooden saint in a real cloth robe held carefully in the crook of his arm, a piñon nut rosary around his wrist, adobe chapel wall behind, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/07-2-hermano-sixto-trujillo-y-vigil.png`

### [Patience Ludlow](Charaktere/07-3-patience-ludlow-die-quakerin.md)

*Quäkerin in ungefärbtem Grau. Kein Leuchten, kein Symbol — die Kraft ist an ihrer Ruhe zu erkennen.*

```
half-length portrait of a spare grey-haired woman of forty-three in undyed grey plain dress with a plain collar and hooks instead of buttons, no jewelry, no ornament, calm level eyes, hands folded over a heavy hickory wagon-tongue staff wound with wire at one end, a worn medical satchel at her feet, standing in the doorway of a plank building, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/07-3-patience-ludlow-die-quakerin.png`

---

## 08 · [SHAMAN (Schamanen)](Archetypen/08-shaman.md)

### [Asdzą́ą́ Łibáhí — „Grey Woman"](Charaktere/08-1-asdzaa-libahi-grey-woman.md)

*Einundsechzig, und in jedem der letzten zwanzig Jahre hat sie etwas aus dem Fluss getragen.*

```
half-length portrait of a Diné Navajo woman of sixty-one, deeply lined face and grey streaked hair tied in a traditional bun, a hand woven blanket with a spare geometric pattern over her shoulders, heavy silver and turquoise at her throat and wrists, holding a small knotted bundle of faded blue army blanket in both hands, a bow and quiver slung behind, standing on dry ground well back from a shallow river crossing, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/08-1-asdzaa-libahi-grey-woman.png`

### [Wewúkiye („Amos")](Charaktere/08-2-wewukiye-elk-bei-allen-amos.md)

*Zwanzig, Wollanzug und Internatshaarschnitt, und eine Elster auf dem Zaunpfahl.*

```
half-length portrait of a Nimiipuu Nez Perce man of twenty with a short boarding school haircut, a cheap wool suit under a cut down cadet uniform coat with the brass buttons snipped off, a lever action carbine across his back, standing at the head of an appaloosa mare, one black and white magpie tail feather tucked into his hatband as if grudgingly, a magpie watching him from a fence post, plains grass to the horizon, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/08-2-wewukiye-elk-bei-allen-amos.png`

---

## 09 · [MAD SCIENTIST (Verrückte Wissenschaftler)](Archetypen/09-mad-scientist.md)

### [Doktor Konstanze Hallweg](Charaktere/09-1-doktor-konstanze-hallweg.md)

*Elf Aufsätze, elf tote Studenten, und die Schuld lag beim Kessel.*

```
half-length portrait of a severe German woman scientist of forty, hair scraped back, a leather inventor's apron over a plain dark dress, a corset shaped riveted brass boiler strapped to her back feeding a braided copper hose, a metre long brass and dark steel lance carried on a leather shoulder yoke, its muzzle a fluted six petalled bell like a trumpet, a heavy armored hat and goggles pushed up on her forehead, an expression of total impatience, workshop clutter behind, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/09-1-doktor-konstanze-hallweg.png`

### [Obadiah „Pigeon" Tuck](Charaktere/09-2-obadiah-pigeon-tuck.md)

*Kann kein Wort lesen und hat es noch nie nicht wieder zum Laufen gebracht.*

```
half-length portrait of a grinning gap toothed river salvage tinker of thirty in a scorched leather apron, a brass fire extinguisher tank strapped across his chest on harness leather, its nozzle a sixty centimetre pelican beak soldered together out of hotel spoon handles, a cracked church table bell wrapped tight in copper wire hanging from a pole frame on his back, a canvas roll of mismatched tools, an evil looking grey mule beside him, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/09-2-obadiah-pigeon-tuck.png`

---

## 10 · [AGENT (Agenten)](Archetypen/10-agent.md)

### [Cordelia Ashgrove — „das Lächeln"](Charaktere/10-1-cordelia-ashgrove-das-lacheln.md)

*Ihr Verlust tut ihr sehr leid, und sie würde gern die Leiche sehen.*

```
half-length portrait of a pleasant looking white woman of thirty-four in a good grey travelling dress and small hat, notebook and pencil in hand, a flat leather document case held closed under one arm, a gold pocket watch, an entirely genuine sympathetic smile, standing in the burnt out doorway of a barn taking notes, ash still on the ground, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/10-1-cordelia-ashgrove-das-lacheln.png`

### [Ambrose Pettigrew Hale](Charaktere/10-2-ambrose-pettigrew-hale-der-aktenverwalter.md)

*Der Mann mit der Antwort und ohne Nerven.*

```
half-length portrait of a soft indoor white man of forty-five with thinning hair and thick spectacles, a rumpled book agent's suit, a large sample case open on a barrel in front of him showing an illustrated volume of engravings, a box camera and a plate holder beside it, one finger holding his place in the book, glancing anxiously off to the side, a mule tied behind him, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/10-2-ambrose-pettigrew-hale-der-aktenverwalter.png`

---

## 11 · [CHI MASTER (Chi-Meister)](Archetypen/11-chi-master.md)

### [Lam Ah-Yuen 林亞元](Charaktere/11-1-lam-ah-yuen.md)

*Nichts an ihm sieht nach Magie aus. Er tapt die Handgelenke und setzt sein Gewicht.*

```
half-length portrait of a Toisanese Chinese man of thirty-seven, calm and unhurried, queue coiled up under a plain felt hat, a dust coloured riding coat over a padded jacket, cloth wrapped wrists, a woven rattan ring worn as a bracelet on one forearm, a doctor's bag at his feet, standing relaxed and centred in the doorway of a small joss house, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/11-1-lam-ah-yuen.png`

### [Kuroda Sae 黒田 冴](Charaktere/11-2-kuroda-sae.md)

*Elf Namen auf dem Papier eines Toten, sieben durchgestrichen.*

```
half-length portrait of a Japanese woman of thirty-one with a hard flat stare, hair cut short and tied back, a man's riding coat with the sleeves pushed up showing heavy iron training rings on both forearms, an empty lacquered short sword scabbard with a cracked finish wrapped in oiled cloth carried at her side, a much folded piece of paper held in one fist, standing beside a railway freight car at dawn, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/11-2-kuroda-sae.png`

---

## 12 · [WARRIOR (Krieger)](Archetypen/12-warrior.md)

### [Wakȟíŋyaŋ Máni — „Walking Thunder"](Charaktere/12-1-wakhiya-mani-walking-thunder-oglala-lakota.md)

*Vertragsvollstrecker mit Klingenkeule. Er sammelt Beweise, keine Skalps.*

```
half-length portrait of an Oglala Lakota man of twenty-seven, long hair with a single wrapped braid, a trade cloth shirt and a plain blanket over one shoulder, holding a two handed bladed war club with a freshly wrapped haft, a bow case at his back, mounted bareback on a stocky buffalo pony with a rawhide bridle and a folded pad, black hills pine and mine tailings behind him, level unimpressed gaze, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/12-1-wakhiya-mani-walking-thunder-oglala-lakota.png`

### [Delia „Del" Cobb](Charaktere/12-2-delia-del-cobb-freigelassene-deserteurin-preisboxerin.md)

*Zwei Fäuste, ein Säbel, vierhundert Dollar auf ihren Kopf.*

```
half-length portrait of a strong shouldered Black woman of twenty-six in cut down cavalry trousers and braces over a man's shirt, horsehair wraps being wound around her knuckles, a cavalry sabre with the regimental number filed off the guard hanging from a peg behind her, a revolver and belt beside it, a broad unbothered grin, standing in a lamplit stable, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/12-2-delia-del-cobb-freigelassene-deserteurin-preisboxerin.png`

### [Owain „Owen" Tregarth](Charaktere/12-3-owain-owen-tregarth-der-bergmann.md)

*Walisischer Häuer, neun Tage verschüttet. Der Fäustel ist Werkzeug, Waffe und Andenken in einem.*

```
half-length portrait of a thickset dark-haired Welsh coal miner of thirty-five, heavy shoulders, coal dust ground permanently into the creases of his hands and eyelids, a broken nose, a short-hafted mining sledge resting on one shoulder, a pickaxe and coiled rope slung behind, standing at the mouth of a timbered adit in low evening light, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/12-3-owain-owen-tregarth-der-bergmann.png`

---

## 13 · [EXPLORER (Entdecker)](Archetypen/13-explorer.md)

### [Wilhelmina „Willa" Kerner](Charaktere/13-1-wilhelmina-willa-kerner-naturforscherin-der-akademie-der-entdecker.md)

*Sie kann das Ding auf Latein benennen und wird es publizieren, ob du überlebst oder nicht.*

```
half-length portrait of a German Texan naturalist woman of twenty-nine in a divided riding skirt and a many pocketed field jacket, spectacles pushed up into her hair, kneeling over an open collecting kit of killing jars insect pins plaster and arsenic soap, a field journal open on her knee with a precise anatomical drawing on the page, a heavy single shot rifle leaning nearby, a resentful pack mule behind her, salt flats, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/13-1-wilhelmina-willa-kerner-naturforscherin-der-akademie-der-entdecker.png`

### [Ambroise Ducharme](Charaktere/13-2-ambroise-ducharme-metis-fuhrer-vom-red-river.md)

*Er ist der, der weiß, wo das Wasser ist.*

```
half-length portrait of a Métis guide of thirty-six with a drooping moustache and long hair under a soft hat, a blue hooded wool capote coat, a finger woven red sash tied at the waist, a beaded fire bag hanging from it, a worn rosary looped around his hand, a heavy single shot rifle with a cut down forestock held loosely, reading the ground at the edge of an abandoned camp circle of two wheeled carts, montana river bottom in winter light, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/13-2-ambroise-ducharme-metis-fuhrer-vom-red-river.png`

### [Josephine „Jo" Pike](Charaktere/13-3-josephine-jo-pike-die-wanderfotografin.md)

*Wanderfotografin mit Atelierwagen. Sie sieht durch die Kamera mehr, als vor ihr gestanden hat.*

```
half-length portrait of a dark-haired woman of thirty in a plain traveling skirt and coat with chemical stains on the cuffs and fingertips, a box camera on a wooden tripod beside her, a glass plate held up against the light and examined closely, a two-wheeled buckboard with a light-tight box body behind her, wet plate collodion tintype, 1884 American West, natural daylight, shallow depth of field, warm sepia with cold slate shadows, fine silver grain, faint plate edge flaws --ar 2:3 --stylize 150
```

Ablage: `Bilder/13-3-josephine-jo-pike-die-wanderfotografin.png`

---

[Zur Übersicht](Charakterideen.md) · [Regelnotizen](Regelnotizen.md)
