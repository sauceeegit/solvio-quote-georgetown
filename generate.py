# -*- coding: utf-8 -*-
"""Quotation SV-2026-0144 - commercial rooftop, Georgetown, Guyana (GPL Tariff B)."""
import io, os

OUT = r"C:\Users\chady\AppData\Local\Temp\claude\C--Users-chady-OneDrive-Desktop-Claude-Code-stuff-Hotel-map\02b0fb74-a5d9-48ed-a4e8-394c55479b62\scratchpad\quote-georgetown"

# ---------------- inputs (bill + PVGIS model) ----------------
PRICE        = 3850000        # PLACEHOLDER (G$) - Option A, 34 panels, installed, grid-tied
PRICE_B      = 4400000        # PLACEHOLDER (G$) - Option B, 39 panels, installed, grid-tied
BAT10        = 1350000        # PLACEHOLDER (G$) - +10 kWh battery incl. hybrid inverter
BAT15        = 1900000        # PLACEHOLDER (G$) - +15 kWh battery incl. hybrid inverter
FX           = 208.50         # G$ per US$, GRA published rate effective 1 Sep 2026
PANELS       = 34
PANELS_B     = 39
PANEL_W      = 450
KWP          = PANELS * PANEL_W / 1000.0          # 15.3
YIELD_PER_KWP = 1524.79       # PVGIS Georgetown, 10 deg tilt, 14% losses
GEN_YR       = int(round(KWP * YIELD_PER_KWP))    # 23,329
GEN_MO       = int(round(GEN_YR / 12.0))          # 1,944
BILL_KWH     = 1699           # this cycle (12 May - 11 Jun 2026)
AVG3_KWH     = 1901.33        # previous 3-month average
CONS_YR      = int(round(AVG3_KWH * 12))          # 22,816
RATE         = 56.38          # G$/kWh, Tariff B
FIXED_MO     = 2467           # G$/month, unaffected by solar
OFFSET_YR    = int(round(min(GEN_YR, CONS_YR) * RATE / 1000.0)) * 1000   # capped at consumption
MARGIN_PCT   = (GEN_YR / float(CONS_YR) - 1) * 100
KWP_B        = PANELS_B * PANEL_W / 1000.0        # 17.55
GEN_YR_B     = int(round(KWP_B * YIELD_PER_KWP))  # 26,760
GEN_MO_B     = int(round(GEN_YR_B / 12.0))        # 2,230
SURPLUS_B    = GEN_YR_B - CONS_YR                 # ~3,944 kWh/yr banked as credits

def kwh_for(n): return int(round(n * PANEL_W / 1000.0 * YIELD_PER_KWP))

gfmt = lambda n: "G$" + format(int(n), ",")
usd  = lambda n: "US$" + format(int(round(n / FX / 100.0)) * 100, ",")

CSS = """
:root{
--orange:#FF6700;--orange-deep:#A3550F;--ink:#09321B;--pine-900:#0C1E1A;
--surface:#E3F1FF;--white:#FFFFFF;--slate-500:#5A6B62;
--price-green:#117238;--gold:#C29848;
--text-body:rgba(9,50,27,.75);--text-muted:var(--slate-500);--text-faint:rgba(9,50,27,.55);
--border-hairline:rgba(9,50,27,.07);--border-soft:rgba(9,50,27,.10);
--on-dark-body:rgba(255,255,255,.65);
--shadow-soft:0 2px 14px rgba(9,50,27,.05);
}
*{box-sizing:border-box}
body{margin:0;background:var(--surface);color:var(--ink);font-family:'DM Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--orange);text-decoration:none}
h1,h2,h3{font-family:'Space Grotesk',sans-serif;letter-spacing:-.01em}
.mono{font-family:'JetBrains Mono',ui-monospace,monospace}
.wrap{max-width:1200px;margin:0 auto;padding-left:clamp(16px,4vw,40px);padding-right:clamp(16px,4vw,40px)}
.eyebrow{font-family:'JetBrains Mono',monospace;font-size:12px;letter-spacing:.15em;text-transform:uppercase;color:var(--orange);margin-bottom:14px}
.card{background:var(--white);border:1px solid var(--border-hairline);border-radius:1.25rem;box-shadow:var(--shadow-soft)}
.grid-dots{background-image:radial-gradient(rgba(255,255,255,.08) 1px,transparent 1px);background-size:22px 22px}
.check li{display:flex;gap:10px;margin:0}
.check li span:first-child{color:var(--orange)}
.num li{display:flex;gap:12px;margin:0;align-items:flex-start}
.num li b{flex:0 0 26px;height:26px;border-radius:999px;background:var(--surface);color:var(--ink);font-family:'JetBrains Mono',monospace;font-size:12px;display:inline-flex;align-items:center;justify-content:center}
.legend{display:flex;flex-wrap:wrap;gap:14px 24px;font-size:13px;color:var(--text-body);margin-top:14px}
.legend span{display:inline-flex;align-items:center;gap:8px}
table.sens{width:100%;border-collapse:collapse;font-size:14px}
table.sens th{font-family:'JetBrains Mono',monospace;font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-muted);text-align:left;padding:8px 10px;border-bottom:1px solid var(--border-soft)}
table.sens td{padding:11px 10px;border-bottom:1px solid var(--border-hairline);color:var(--text-body)}
table.sens tr.hi td{background:rgba(255,103,0,.06);color:var(--ink);font-weight:600}
table.sens td:first-child{font-family:'Space Grotesk',sans-serif;font-weight:700;color:var(--ink)}
.batbtn{flex:1;text-align:left;padding:10px 12px;border-radius:.75rem;cursor:pointer;font-family:inherit;transition:all .2s cubic-bezier(.4,0,.2,1);background:#fff;border:1px solid rgba(9,50,27,.15);color:rgba(9,50,27,.6)}
.batbtn.sel{background:#FF6700;border:1px solid #FF6700;color:#fff;font-weight:600;box-shadow:0 2px 8px rgba(255,103,0,.28)}
.batbtn b{display:block;font-weight:600;font-size:13px}
.batbtn i{display:block;font-style:normal;font-size:11px;opacity:.75}
.tile{background:var(--surface);border-radius:.75rem;padding:12px 14px}
.tile .v{font-family:'Space Grotesk',sans-serif;font-weight:700;font-size:20px;color:var(--ink)}
.tile .l{font-size:12px;color:var(--text-muted);margin-top:2px}
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
'<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">')

def chart_svg():
    rows = [("This bill (12 May - 11 Jun)", BILL_KWH, "rgba(9,50,27,.22)", "#09321B"),
            ("Your 3-month average", int(round(AVG3_KWH)), "rgba(9,50,27,.35)", "#09321B"),
            ("Option A - %d panels, monthly output" % PANELS, GEN_MO, "#FF6700", "#FF6700"),
            ("Option B - %d panels, monthly output" % PANELS_B, GEN_MO_B, "#C29848", "#A3550F")]
    W, H = 720, 242
    lx, x0, x1 = 16, 250, 690
    vmax = 2500.0
    s = []
    for i, (label, v, fill, tcol) in enumerate(rows):
        y = 22 + i * 52
        bw = (x1 - x0) * v / vmax
        s.append('<text x="%d" y="%d" font-family="DM Sans,sans-serif" font-size="13" fill="#09321B">%s</text>' % (lx, y + 17, label))
        s.append('<rect x="%d" y="%d" width="%.1f" height="26" rx="5" fill="%s"/>' % (x0, y, bw, fill))
        s.append('<text x="%.1f" y="%d" font-family="JetBrains Mono,monospace" font-size="12.5" font-weight="700" fill="%s">%s kWh</text>' % (x0 + bw + 8, y + 18, tcol, format(v, ",")))
    ax = x0 + (x1 - x0) * AVG3_KWH / vmax
    s.append('<line x1="%.1f" y1="14" x2="%.1f" y2="%d" stroke="#C29848" stroke-width="2" stroke-dasharray="6 5"/>' % (ax, ax, H - 22))
    s.append('<text x="%.1f" y="%d" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="10" fill="#C29848">avg</text>' % (ax, H - 8))
    return '<svg viewBox="0 0 %d %d" role="img" style="width:100%%;max-width:800px;height:auto;display:block">%s</svg>' % (W, H, "".join(s))

def sun_svg():
    """Daily sunshine hours by month, Georgetown (weather-and-climate.com), wet months shaded."""
    hrs = [6.2, 6.9, 7.1, 7.0, 6.3, 5.3, 6.1, 6.8, 7.5, 7.9, 7.0, 6.1]
    wet = {1, 5, 6, 7, 8, 11, 12}
    months = ["J","F","M","A","M","J","J","A","S","O","N","D"]
    W, H = 720, 200
    x0, x1, y0, y1 = 36, 700, 18, 160
    vmax, ph = 9.0, y1 - y0
    slot = (x1 - x0) / 12.0; bw = slot * 0.6
    s = []
    for g in (3, 6, 9):
        gy = y1 - g / vmax * ph
        s.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="rgba(9,50,27,.08)"/>' % (x0, gy, x1, gy))
        s.append('<text x="%d" y="%.1f" text-anchor="end" font-family="JetBrains Mono,monospace" font-size="10" fill="#5A6B62">%dh</text>' % (x0 - 6, gy + 3.5, g))
    for i, h in enumerate(hrs):
        bx = x0 + slot * i + (slot - bw) / 2
        by = y1 - h / vmax * ph
        fill = "rgba(9,50,27,.22)" if (i + 1) in wet else "#FF6700"
        s.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="%s"/>' % (bx, by, bw, y1 - by, fill))
        s.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="10" fill="#09321B">%.1f</text>' % (bx + bw / 2, by - 4, h))
        s.append('<text x="%.1f" y="%d" text-anchor="middle" font-family="DM Sans,sans-serif" font-size="11.5" fill="#5A6B62">%s</text>' % (bx + bw / 2, y1 + 18, months[i]))
    s.append('<text x="%d" y="%d" text-anchor="end" font-family="JetBrains Mono,monospace" font-size="10" fill="#5A6B62">avg daily sunshine hours, Georgetown</text>' % (x1, H - 4))
    return '<svg viewBox="0 0 %d %d" role="img" style="width:100%%;max-width:800px;height:auto;display:block">%s</svg>' % (W, H, "".join(s))

def stat(v, lbl, color="var(--ink)"):
    return ('<div><div style="font-family:\'Space Grotesk\',sans-serif;font-weight:700;font-size:19px;color:%s">%s</div>'
            '<div style="font-size:12px;color:var(--text-muted)">%s</div></div>' % (color, v, lbl))

def tile(v, lbl):
    return '<div class="tile"><div class="v">%s</div><div class="l">%s</div></div>' % (v, lbl)

def warr(v, txt):
    return ('<div><div style="font-family:\'Space Grotesk\',sans-serif;font-weight:800;font-size:30px;color:var(--gold)">%s</div>'
            '<div style="font-size:14px;line-height:1.55;color:var(--text-body);margin-top:6px">%s</div></div>' % (v, txt))

def badge(v, lbl):
    return ('<div style="display:flex;flex-direction:column;gap:2px;background:var(--white);border:1px solid var(--border-hairline);border-radius:.75rem;padding:10px 14px;box-shadow:var(--shadow-soft)">'
            '<span style="font-family:\'Space Grotesk\',sans-serif;font-weight:700;font-size:17px;color:var(--gold)">%s</span>'
            '<span style="font-size:13px;color:var(--text-body)">%s</span></div>' % (v, lbl))

def checklist(n, kwp, inv):
  return [
    "%d &times; %d Wp Solvio all-black panels (%.2f kWp DC)" % (n, PANEL_W, kwp),
    "~%s kW AC grid-tied inverter &mdash; hybrid inverter if a battery is chosen; string design finalised at site survey" % inv,
    "Low-tilt roof mounting engineered to your roof type &mdash; confirmed at survey",
    "GPL net-billing interconnection &mdash; we prepare the GPL request and GEI inspection",
    "Wiring, commissioning &amp; production monitoring",
  ]

def option_card(o):
    checks = "".join('<li><span>&#10003;</span><span>%s</span></li>' % c for c in o["checks"])
    # short values so three stats fit one row on a 375px phone without wrapping
    stats = stat("~%.1fk" % (o["gen"] / 1000.0), "kWh modeled / year") + \
            stat("~G$%.2fM" % (OFFSET_YR / 1e6), "energy charges offset / year", "var(--price-green)") + \
            ('<div><div id="pay-%s" style="font-family:\'Space Grotesk\',sans-serif;font-weight:700;font-size:19px;color:var(--ink)">~%.1f yrs</div>'
             '<div style="font-size:12px;color:var(--text-muted)">payback</div></div>' % (o["key"], o["price"] / float(OFFSET_YR)))
    chip = ('<span class="mono" style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#fff;background:var(--orange);border-radius:999px;padding:6px 13px">%s</span>' % o["chip"]
            if o["solid"] else
            '<span class="mono" style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:var(--text-body);border:1px solid var(--border-soft);border-radius:999px;padding:5px 12px">%s</span>' % o["chip"])
    note = ('<p style="font-size:12.5px;color:var(--text-body);margin:0 0 22px;line-height:1.5">%s</p>' % o["note"]) if o["note"] else ""
    return """
    <div class="card" style="padding:clamp(24px,4vw,36px);display:flex;flex-direction:column">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
        <span class="mono" style="font-size:12px;letter-spacing:.15em;text-transform:uppercase;color:var(--text-muted)">%(label)s</span>
        %(chip)s
      </div>
      <h2 style="font-weight:700;font-size:30px;margin:0 0 6px">%(kwp)s kWp system <span style="display:block;margin-top:8px"><span class="mono" style="display:inline-block;background:var(--orange);color:#fff;font-size:12px;letter-spacing:.08em;text-transform:uppercase;border-radius:.5rem;padding:5px 12px">%(n)d Panels</span></span></h2>
      <p style="margin:0 0 22px;font-size:15px;color:var(--text-body)">%(desc)s</p>
      <ul class="check" style="list-style:none;margin:0 0 24px;padding:0;display:grid;gap:11px;font-size:15px;color:var(--text-body)">
        %(checks)s
      </ul>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;border-top:1px solid var(--border-hairline);border-bottom:1px solid var(--border-hairline);padding:16px 0;margin-bottom:%(stats_mb)s">
        %(stats)s
      </div>%(note)s
      <div class="mono" style="display:flex;align-items:center;gap:8px;font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase;margin-bottom:10px">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#FF6700" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="16" height="10" rx="2"></rect><line x1="22" y1="11" x2="22" y2="13"></line><line x1="6" y1="11" x2="6" y2="13"></line><line x1="10" y1="11" x2="10" y2="13"></line></svg>Add battery storage
      </div>
      <div style="display:flex;gap:8px;margin-bottom:8px">
        <button class="batbtn sel" data-card="%(key)s" data-k="none" onclick="pick('%(key)s','none')"><b>None</b><i>grid-tied only</i></button>
        <button class="batbtn" data-card="%(key)s" data-k="b10" onclick="pick('%(key)s','b10')"><b>+10 kWh</b><i>+%(bat10)s</i></button>
        <button class="batbtn" data-card="%(key)s" data-k="b15" onclick="pick('%(key)s','b15')"><b>+15 kWh</b><i>+%(bat15)s</i></button>
      </div>
      <p style="font-size:12px;color:var(--text-muted);margin:0 0 24px;line-height:1.5">Battery options include a hybrid inverter in place of the grid-tied unit. Keeps essential loads running through outages and shifts daytime surplus into the evening.</p>
      <div style="margin-top:auto">
        <div style="font-size:12px;color:var(--text-muted);margin-bottom:2px">Total, installed</div>
        <div id="total-%(key)s" style="font-family:'Space Grotesk',sans-serif;font-weight:800;font-size:38px;letter-spacing:-.02em;color:var(--price-green)">%(price)s</div>
        <div style="font-size:14px;color:var(--ink);font-weight:600;margin-top:2px">&asymp; <span id="total-usd-%(key)s">%(price_usd)s</span> <span style="font-size:11.5px;color:var(--text-muted);font-weight:400">at G$%(fx)s / US$ (GRA rate, 1 Sep 2026)</span></div>
        <div id="totalsub-%(key)s" style="font-size:12px;color:var(--text-muted);margin-top:4px">grid-tied, no battery &middot; preliminary, confirmed after site survey</div>
      </div>
    </div>""" % dict(o, checks=checks, stats=stats, chip=chip, note=note,
                     bat10=gfmt(BAT10), bat15=gfmt(BAT15), price=gfmt(o["price"]), price_usd=usd(o["price"]),
                     fx=("%.2f" % FX), stats_mb=("10px" if o["note"] else "22px"))

OPTIONS = [
    dict(key="a", label="Option A", chip="Annual match", solid=True, n=PANELS, kwp="%.1f" % KWP, gen=GEN_YR,
         desc="Modeled to produce what you use over a year &mdash; %s kWh against %s kWh consumed." % (format(GEN_YR, ","), format(CONS_YR, ",")),
         checks=checklist(PANELS, KWP, "15"), price=PRICE, note=""),
    dict(key="b", label="Option B", chip="Wet-season cover", solid=False, n=PANELS_B, kwp="%.2f" % KWP_B, gen=GEN_YR_B,
         desc="Covers your %s kWh average even in a June-like low-sun month &mdash; no need to draw on banked credits." % format(int(round(AVG3_KWH)), ","),
         checks=checklist(PANELS_B, KWP_B, "17"), price=PRICE_B,
         note="Plus ~%s kWh a year of surplus into your GPL Energy Credits Bank &mdash; paid at 90%% of tariff if unused after 12 months. Not counted in the figure above." % format(SURPLUS_B, ",")),
]
NEXT_STEPS = [
    "Twelve consecutive GPL bills, to confirm the seasonal pattern",
    "Roof dimensions, orientation and shading assessment",
    "Structural check of the roof for the array load",
    "Daytime vs. night-time consumption profile",
    "Final panel electrical specifications and inverter string calculations",
    "GPL interconnection approval and GEI Certificate of Inspection",
]

HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>Solvio - Quotation SV-2026-0144</title>
{fonts}
<style>{css}</style>
</head>
<body>

<div class="wrap" style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;padding-top:18px">
  <div class="mono" style="font-size:11.5px;letter-spacing:.1em;color:var(--text-muted);text-transform:uppercase;line-height:1.9">
    Quote SV-2026-0144 &nbsp;&middot;&nbsp; Issued 3 Sep 2026 &nbsp;&middot;&nbsp; Valid until 3 Oct 2026
  </div>
  <div class="mono" style="font-size:11.5px;letter-spacing:.1em;color:var(--text-muted);text-transform:uppercase">Preliminary &mdash; subject to site survey</div>
</div>

<section class="wrap" style="padding-top:16px">
  <div class="grid-dots" style="background-color:var(--ink);border-radius:1.25rem;padding:clamp(28px,5vw,52px) clamp(22px,4vw,48px)">
    <div class="eyebrow">Commercial Rooftop Solar &mdash; Quotation</div>
    <h1 style="font-weight:800;font-size:clamp(30px,6.5vw,52px);line-height:1.1;margin:0;color:#fff;max-width:760px">Solar for Your Business. Sized to Your GPL Bill.</h1>
  </div>
  <div style="display:flex;flex-wrap:wrap;gap:20px 40px;align-items:center;justify-content:space-between;margin-top:22px">
    <p style="font-size:clamp(15px,2vw,17px);line-height:1.6;color:var(--text-body);margin:0;flex:1 1 340px;max-width:560px">Prepared for <strong style="font-weight:600;color:var(--ink)">Moonkally Baburam</strong> &mdash; a {kwp} kWp grid-tied system for your premises at 97 Chandra Nagar, Prashad Nagar, Georgetown, sized to match your annual GPL consumption.</p>
    <div style="display:grid;grid-template-columns:repeat(2,1fr);gap:10px;flex:1 1 300px;max-width:360px">
      {badges}
    </div>
  </div>
</section>

<section class="wrap" style="padding-top:40px">
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px;align-items:stretch">
    {opt_cards}
  </div>
</section>

<section class="wrap" style="padding-top:24px">
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px;align-items:stretch">
    <div class="card" style="padding:clamp(24px,4vw,36px)">
      <div class="eyebrow">What changes on your bill</div>
      <h2 style="font-weight:700;font-size:28px;margin:0 0 12px">Energy Charges Down. Fixed Charge Stays.</h2>
      <p style="font-size:15px;line-height:1.65;color:var(--text-body);margin:0 0 22px">Your monthly bill has two parts. Solar works on one of them.</p>
      <div style="display:grid;gap:10px">
        <div style="display:flex;justify-content:space-between;gap:12px;padding:12px 14px;border-radius:.75rem;background:rgba(255,103,0,.07);border:1px solid rgba(255,103,0,.25)">
          <div><div style="font-weight:600">Energy charge &mdash; {bill_kwh} kWh @ G${rate}</div><div style="font-size:13px;color:var(--text-body)">This is what the array offsets, month after month.</div></div>
          <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;white-space:nowrap;color:var(--price-green)">G$95,790</div>
        </div>
        <div style="display:flex;justify-content:space-between;gap:12px;padding:12px 14px;border-radius:.75rem;border:1px solid var(--border-hairline)">
          <div><div style="font-weight:600">Fixed charge (Tariff B)</div><div style="font-size:13px;color:var(--text-body)">A standing charge from GPL &mdash; unchanged by solar.</div></div>
          <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;white-space:nowrap">{fixed}</div>
        </div>
      </div>
      <p style="font-size:13.5px;line-height:1.6;color:var(--text-body);margin:20px 0 0">At your 3-month average of {avg3} kWh, energy charges run to about <strong style="color:var(--ink)">{offset_yr} a year</strong> (&asymp; {offset_usd}). The recommended array is modeled to generate slightly more than that over twelve months.</p>
    </div>
  </div>
  <p style="font-size:12.5px;color:var(--text-faint);margin:16px 4px 0;max-width:820px;line-height:1.6">Generation modeled with PVGIS for Georgetown: 10&deg; tilt, south-facing, crystalline-silicon modules, 14% system losses, terrain horizon enabled &mdash; {yield_kwp} kWh per installed kWp per year. Savings assume energy charges at G${rate}/kWh and are capped at your metered consumption; surplus is banked as GPL energy credits rather than valued here. US$ figures use the Guyana Revenue Authority rate of G${fx} per US$ effective 1 Sep 2026 and are indicative only. Actual output varies with weather, shading and roof orientation.</p>
</section>

<section class="wrap" style="padding-top:48px">
  <div class="card" style="padding:clamp(22px,4vw,36px) clamp(22px,4vw,40px)">
    <div class="eyebrow">Why these sizes</div>
    <h2 style="font-weight:700;font-size:28px;margin:0 0 12px">Sized to Match a Year, Not a Month.</h2>
    <p style="font-size:15px;line-height:1.65;color:var(--text-body);margin:0 0 26px;max-width:820px">Your bill gives two consumption figures: {bill_kwh} kWh for this cycle and a {avg3} kWh average over the previous three months. Annualised, that's about {cons_yr} kWh. One 450 Wp panel in Georgetown produces roughly {per_panel} kWh a year, so {cons_yr} &divide; {per_panel} &asymp; 33.3 panels. Option A rounds that up to {panels}; Option B adds five more so a wet month is covered on its own.</p>
    <div style="overflow-x:auto">{chart}</div>
    <div class="legend">
      <span><span style="width:22px;height:12px;border-radius:3px;background:rgba(9,50,27,.3);display:inline-block"></span>Your consumption (kWh/month)</span>
      <span><span style="width:22px;height:12px;border-radius:3px;background:#FF6700;display:inline-block"></span>Option A &mdash; {panels} panels, annual average</span>
      <span><span style="width:22px;height:12px;border-radius:3px;background:#C29848;display:inline-block"></span>Option B &mdash; {panels_b} panels, annual average</span>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:26px">
      <div style="border-left:3px solid var(--orange);padding-left:16px">
        <h3 style="font-size:17px;font-weight:700;margin:0 0 6px">Option A &mdash; {panels} panels, sized to the year</h3>
        <p style="font-size:14.5px;line-height:1.65;color:var(--text-body);margin:0">Generates {gen_yr} kWh a year against {cons_yr} kWh consumed &mdash; a {margin}% margin. This bill covers mid-May to mid-June, a lower-yield stretch; GPL's Energy Credits Bank lets a sunny September carry a wet June, so sizing to the year rather than the weakest month avoids paying for capacity that over-produces most of the time. The PVGIS model already deducts 14% for real-world losses, so nothing is double-counted.</p>
      </div>
      <div style="border-left:3px solid var(--gold);padding-left:16px">
        <h3 style="font-size:17px;font-weight:700;margin:0 0 6px">Option B &mdash; {panels_b} panels, sized to the wettest month</h3>
        <p style="font-size:14.5px;line-height:1.65;color:var(--text-body);margin:0">Averages {gen_mo_b} kWh a month and still produces around {avg3} kWh in a June-like month, so even the wettest weeks are covered without touching banked credits. Over a year it runs about {surplus_b} kWh ahead of consumption; that surplus accrues in your credits bank and is paid at 90% of tariff if unused after twelve months. The right choice if you expect load to grow, or once GPL confirms your net-billing account and the surplus has a guaranteed value.</p>
      </div>
    </div>
  </div>
</section>

<section class="wrap" style="padding-top:48px">
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px;align-items:stretch">

    <div class="card" style="padding:clamp(22px,4vw,36px)">
      <div class="eyebrow">The sun in Georgetown</div>
      <h2 style="font-weight:700;font-size:28px;margin:0 0 12px">A Strong, Steady Resource.</h2>
      <p style="font-size:15px;line-height:1.65;color:var(--text-body);margin:0 0 20px">At 6.8&deg;N the sun sits high all year, so there is no winter dip &mdash; only the wet seasons (May&ndash;July and December&ndash;January) trim the output.</p>
      <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-bottom:22px">
        {sun_tiles}
      </div>
      <div style="overflow-x:auto">{sun_chart}</div>
      <div class="legend" style="margin-top:8px">
        <span><span style="width:18px;height:12px;border-radius:3px;background:#FF6700;display:inline-block"></span>Drier months</span>
        <span><span style="width:18px;height:12px;border-radius:3px;background:rgba(9,50,27,.22);display:inline-block"></span>Wetter months</span>
      </div>
      <p style="font-size:13px;line-height:1.6;color:var(--text-body);margin:16px 0 0">June, the month on your bill, is Georgetown's wettest and lowest-sun month. A system sized to a June bill alone would over-produce for the other ten.</p>
    </div>

    <div class="card" style="padding:clamp(22px,4vw,36px)">
      <div class="eyebrow">Selling surplus to GPL</div>
      <h2 style="font-weight:700;font-size:28px;margin:0 0 12px">GPL Buys Back Your Surplus.</h2>
      <p style="font-size:15px;line-height:1.65;color:var(--text-body);margin:0 0 20px">Guyana's Grid-Tied &amp; Net-Billing Programme lets approved customers &mdash; GPL calls them <em>prosumers</em> &mdash; export surplus to the national grid under a Standard Offer Contract. Section C of your bill, &ldquo;Customer Energy Credits&rdquo;, is where it shows up.</p>
      <ul class="check" style="list-style:none;margin:0 0 20px;padding:0;display:grid;gap:11px;font-size:14.5px;color:var(--text-body)">
        <li><span>&#10003;</span><span><strong style="color:var(--ink)">Systems under 100 kW AC</strong> are allowed regardless of consumption, subject to GPL's interconnection requirements &mdash; yours is 15.3 kW.</span></li>
        <li><span>&#10003;</span><span><strong style="color:var(--ink)">Surplus goes into an Energy Credits Bank</strong> and offsets energy charges on later bills &mdash; a sunny September pays for a wet June.</span></li>
        <li><span>&#10003;</span><span><strong style="color:var(--ink)">Unused credit after 12 months is paid out</strong> at 90% of the tariff at the time, less anything owed to GPL.</span></li>
        <li><span>&#10003;</span><span><strong style="color:var(--ink)">Approval path:</strong> interconnection request to GPL with a one-line diagram and inverter specs, then a GEI Certificate of Inspection. Equipment must meet NEC 2014 (Arts. 690/705), IEEE 1547 and UL 1741 &mdash; standard for what we install.</span></li>
      </ul>
      <p style="font-size:13px;line-height:1.6;color:var(--text-body);margin:0">Over 290 properties in Guyana were already exporting under the programme by mid-2025. We handle the paperwork; we don't count export income in this quote until GPL approves your account.</p>
    </div>
  </div>
</section>

<section class="wrap" style="padding-top:48px">
  <div class="card" style="padding:clamp(22px,4vw,36px) clamp(22px,4vw,40px)">
    <div class="eyebrow">Before final design</div>
    <h2 style="font-weight:700;font-size:28px;margin:0 0 12px">What We Confirm at Site Survey.</h2>
    <p style="font-size:15px;line-height:1.65;color:var(--text-body);margin:0 0 22px;max-width:820px">This quotation is a preliminary annual-energy match from one bill. It is not a final design or a guaranteed production figure. The final proposal follows once we have:</p>
    <ol class="num" style="list-style:none;margin:0;padding:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(300px,1fr));gap:12px 28px;font-size:15px;color:var(--text-body)">
      {next_steps}
    </ol>
  </div>
</section>

<section class="wrap" style="padding-top:48px">
  <div class="card" style="padding:clamp(22px,4vw,36px) clamp(22px,4vw,40px)">
    <h2 style="font-weight:700;font-size:28px;margin:0 0 26px">Built to Last. Backed by Warranty.</h2>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:28px">
      {warranties}
    </div>
  </div>
</section>

<section class="wrap" style="padding-top:48px;padding-bottom:56px">
  <div class="grid-dots" style="background-color:var(--ink);border-radius:1.25rem;padding:clamp(24px,5vw,48px);display:flex;justify-content:space-between;align-items:center;gap:32px;flex-wrap:wrap">
    <div style="max-width:520px">
      <h2 style="font-weight:700;font-size:clamp(24px,4vw,34px);margin:0 0 10px;color:#fff">Ready for the next step?</h2>
      <p style="font-size:15px;line-height:1.65;color:var(--on-dark-body);margin:0">Reply to book the site survey. We'll confirm roof, shading and the inverter design, then issue the final proposal and start the GPL net-billing application.</p>
    </div>
    <div style="display:flex;gap:14px;flex-wrap:wrap">
      <a href="mailto:sales@solvio.solar?subject=Site%20survey%20-%20quote%20SV-2026-0144" style="display:inline-block;background:var(--orange);color:#fff;font-weight:600;font-size:16px;padding:14px 32px;border-radius:999px;text-align:center">Book the site survey</a>
    </div>
  </div>
  <div style="display:flex;justify-content:space-between;gap:24px;flex-wrap:wrap;margin-top:28px;font-size:12.5px;color:var(--text-muted);line-height:1.7">
    <div>Solvio Solar &middot; <a href="mailto:sales@solvio.solar">sales@solvio.solar</a></div>
    <div>Quote SV-2026-0144 &middot; valid 30 days from issue &middot; prices in Guyanese dollars (G$), installed &middot; US$ indicative</div>
  </div>
  <p style="font-size:11.5px;color:var(--text-faint);margin:14px 0 0;line-height:1.6">Sources: GPL Grid-Tie &amp; Net-Billing Programme (gplinc.com); Guyana Energy Agency (gea.gov.gy); Guyana Revenue Authority exchange rates (gra.gov.gy); PVGIS (EU JRC); Georgetown sunshine climatology (weather-and-climate.com).</p>
</section>

<script>
var BASE={{a:{price_raw},b:{price_b_raw}}},BAT={{none:0,b10:{bat10_raw},b15:{bat15_raw}}},FX={fx},OFFSET={offset_raw};
var SUBS={{none:'grid-tied, no battery \\u00b7 preliminary, confirmed after site survey',
          b10:'incl. 10 kWh battery + hybrid inverter \\u00b7 preliminary, confirmed after site survey',
          b15:'incl. 15 kWh battery + hybrid inverter \\u00b7 preliminary, confirmed after site survey'}};
function pick(c,k){{
  document.querySelectorAll('.batbtn[data-card="'+c+'"]').forEach(function(b){{b.classList.toggle('sel',b.dataset.k===k);}});
  var g=BASE[c]+BAT[k];
  document.getElementById('total-'+c).textContent='G$'+g.toLocaleString('en-US');
  document.getElementById('total-usd-'+c).textContent='US$'+(Math.round(g/FX/100)*100).toLocaleString('en-US');
  document.getElementById('totalsub-'+c).textContent=SUBS[k];
  document.getElementById('pay-'+c).textContent='~'+(g/OFFSET).toFixed(1)+' yrs';
}}
</script>
</body>
</html>"""

html = HTML.format(
    fonts=FONTS, css=CSS,
    kwp=("%.1f" % KWP), panels=PANELS, panels_b=PANELS_B, gen_mo_b=format(GEN_MO_B, ","),
    surplus_b=format(SURPLUS_B, ","), margin=("%.1f" % MARGIN_PCT),
    opt_cards="".join(option_card(o) for o in OPTIONS), price_b_raw=PRICE_B, offset_raw=OFFSET_YR,
    gen_yr=format(GEN_YR, ","), cons_yr=format(CONS_YR, ","),
    bill_kwh=format(BILL_KWH, ","), avg3=format(int(round(AVG3_KWH)), ","),
    rate=("%.2f" % RATE), fixed=gfmt(FIXED_MO),
    offset_yr=gfmt(OFFSET_YR), offset_usd=usd(OFFSET_YR),
    yield_kwp=("%.0f" % YIELD_PER_KWP), per_panel=("%.0f" % (PANEL_W / 1000.0 * YIELD_PER_KWP)),
    price_raw=PRICE,
    bat10=gfmt(BAT10), bat15=gfmt(BAT15), bat10_raw=BAT10, bat15_raw=BAT15,
    fx=("%.2f" % FX),
    badges="".join(badge(*b) for b in [("30 yrs", "performance warranty"), ("10 yrs", "product warranty")]),
    chart=chart_svg(),
    sun_tiles="".join(tile(v, l) for v, l in [
        ("5.0 kWh/m&sup2;", "average daily irradiation"),
        ("4.2 &ndash; 5.8", "seasonal range, kWh/m&sup2;/day"),
        ("~1,800 kWh/m&sup2;", "annual irradiation"),
        ("~2,470 h", "sunshine hours / year"),
        ("7.9 h/day", "October, sunniest"),
        ("5.3 h/day", "June, wettest")]),
    sun_chart=sun_svg(),
    next_steps="".join('<li><b>%d</b><span>%s</span></li>' % (i + 1, t) for i, t in enumerate(NEXT_STEPS)),
    warranties="".join(warr(v, t) for v, t in [
        ("30 yrs", "Panel performance warranty &mdash; guaranteed output for three decades."),
        ("10 yrs", "Product warranty on panel materials and workmanship &mdash; defects covered, parts and labour."),
        ("5 yrs", "Comprehensive coverage on the inverter, battery, mounting and workmanship."),
        ("Lifetime", "Support from Solvio's solar engineers &mdash; whenever you need us.")]),
)

if not os.path.isdir(OUT):
    os.makedirs(OUT)
p = OUT + r"\index.html"
io.open(p, "w", encoding="utf-8", newline="\n").write(html)
print("index.html  %.1f KB" % (os.path.getsize(p) / 1024.0))
print("A %s (%s) | B %s (%s) | B gen %d kWh/yr, surplus %d | offset/yr %s"
      % (gfmt(PRICE), usd(PRICE), gfmt(PRICE_B), usd(PRICE_B), GEN_YR_B, SURPLUS_B, gfmt(OFFSET_YR)))
