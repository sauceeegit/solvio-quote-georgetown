# -*- coding: utf-8 -*-
"""Quotation SV-2026-0144 - commercial rooftop, Georgetown, Guyana (GPL Tariff B)."""
import io, os

OUT = r"C:\Users\chady\AppData\Local\Temp\claude\C--Users-chady-OneDrive-Desktop-Claude-Code-stuff-Hotel-map\02b0fb74-a5d9-48ed-a4e8-394c55479b62\scratchpad\quote-georgetown"

# ---------------- inputs (bill + PVGIS model) ----------------
PRICE        = 3850000        # PLACEHOLDER (G$) - awaiting real price
PANELS       = 34
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

def kwh_for(n): return int(round(n * PANEL_W / 1000.0 * YIELD_PER_KWP))

gfmt = lambda n: "G$" + format(int(n), ",")

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
"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
'<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
'<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@700;800&family=DM+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">')

def chart_svg():
    """Horizontal bars: this bill, 3-month average, and modeled output of 34 panels."""
    rows = [("This bill (12 May - 11 Jun)", BILL_KWH, "rgba(9,50,27,.22)", "#09321B"),
            ("Your 3-month average", int(round(AVG3_KWH)), "rgba(9,50,27,.35)", "#09321B"),
            ("%d panels - modeled monthly output" % PANELS, GEN_MO, "#FF6700", "#FF6700")]
    W, H = 720, 190
    lx, x0, x1 = 16, 250, 690
    vmax = 2200.0
    s = []
    for i, (label, v, fill, tcol) in enumerate(rows):
        y = 22 + i * 52
        bw = (x1 - x0) * v / vmax
        s.append('<text x="%d" y="%d" font-family="DM Sans,sans-serif" font-size="13" fill="#09321B">%s</text>' % (lx, y + 17, label))
        s.append('<rect x="%d" y="%d" width="%.1f" height="26" rx="5" fill="%s"/>' % (x0, y, bw, fill))
        s.append('<text x="%.1f" y="%d" font-family="JetBrains Mono,monospace" font-size="12.5" font-weight="700" fill="%s">%s kWh</text>' % (x0 + bw + 8, y + 18, tcol, format(v, ",")))
    # dashed line at the 3-month average for the visual "match"
    ax = x0 + (x1 - x0) * AVG3_KWH / vmax
    s.append('<line x1="%.1f" y1="14" x2="%.1f" y2="%d" stroke="#C29848" stroke-width="2" stroke-dasharray="6 5"/>' % (ax, ax, H - 22))
    s.append('<text x="%.1f" y="%d" text-anchor="middle" font-family="JetBrains Mono,monospace" font-size="10" fill="#C29848">avg</text>' % (ax, H - 8))
    return '<svg viewBox="0 0 %d %d" role="img" style="width:100%%;max-width:800px;height:auto;display:block">%s</svg>' % (W, H, "".join(s))

def stat(v, lbl, color="var(--ink)"):
    return ('<div><div style="font-family:\'Space Grotesk\',sans-serif;font-weight:700;font-size:19px;color:%s">%s</div>'
            '<div style="font-size:12px;color:var(--text-muted)">%s</div></div>' % (color, v, lbl))

def warr(v, txt):
    return ('<div><div style="font-family:\'Space Grotesk\',sans-serif;font-weight:800;font-size:30px;color:var(--gold)">%s</div>'
            '<div style="font-size:14px;line-height:1.55;color:var(--text-body);margin-top:6px">%s</div></div>' % (v, txt))

def badge(v, lbl):
    return ('<div style="display:flex;flex-direction:column;gap:2px;background:var(--white);border:1px solid var(--border-hairline);border-radius:.75rem;padding:10px 14px;box-shadow:var(--shadow-soft)">'
            '<span style="font-family:\'Space Grotesk\',sans-serif;font-weight:700;font-size:17px;color:var(--gold)">%s</span>'
            '<span style="font-size:13px;color:var(--text-body)">%s</span></div>' % (v, lbl))

def sens_rows():
    rows = [(34, "Matches your annual consumption (+%.1f%%)" % MARGIN_PCT, True),
            (35, "Matches this bill's month in a low-sun period", False),
            (36, "About 8% headroom - only if 12 months of bills show higher demand", False),
            (39, "Covers 1,901 kWh even in a low-sun month - likely over-produces annually", False)]
    out = []
    for n, note, hi in rows:
        out.append('<tr%s><td>%d panels</td><td>%.2f kWp</td><td>%s kWh/yr</td><td>%s</td></tr>'
                   % (' class="hi"' if hi else "", n, n * PANEL_W / 1000.0, format(kwh_for(n), ","), note))
    return "".join(out)

CHECKLIST = [
    "%d &times; %d Wp Solvio all-black panels (%.1f kWp DC)" % (PANELS, PANEL_W, KWP),
    "~15 kW AC grid-tied inverter &mdash; string design finalised at site survey",
    "Low-tilt roof mounting engineered to your roof type &mdash; confirmed at survey",
    "GPL net-billing interconnection &mdash; we prepare the GPL and GEI applications",
    "Wiring, commissioning &amp; production monitoring",
]
NEXT_STEPS = [
    "Twelve consecutive GPL bills, to confirm the seasonal pattern",
    "Roof dimensions, orientation and shading assessment",
    "Structural check of the roof for the array load",
    "Daytime vs. night-time consumption profile",
    "Final panel electrical specifications and inverter string calculations",
    "GPL and GEI interconnection approval for net-billing",
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
    <p style="font-size:clamp(15px,2vw,17px);line-height:1.6;color:var(--text-body);margin:0;flex:1 1 340px;max-width:560px">Prepared for <strong style="font-weight:600;color:var(--ink)">Moonkally Baburam</strong> &mdash; a {kwp} kWp grid-tied system for your premises in Prashad Nagar, Georgetown, sized to match your annual GPL consumption.</p>
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:10px;flex:1 1 380px;max-width:520px">
      {badges}
    </div>
  </div>
</section>

<section class="wrap" style="padding-top:40px">
  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:24px;align-items:stretch">

    <div class="card" style="padding:clamp(24px,4vw,36px);display:flex;flex-direction:column">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px">
        <span class="mono" style="font-size:12px;letter-spacing:.15em;text-transform:uppercase;color:var(--text-muted)">Recommended system</span>
        <span class="mono" style="font-size:11px;letter-spacing:.1em;text-transform:uppercase;color:#fff;background:var(--orange);border-radius:999px;padding:6px 13px">Annual match</span>
      </div>
      <h2 style="font-weight:700;font-size:30px;margin:0 0 6px">{kwp} kWp system <span style="display:block;margin-top:8px"><span class="mono" style="display:inline-block;background:var(--orange);color:#fff;font-size:12px;letter-spacing:.08em;text-transform:uppercase;border-radius:.5rem;padding:5px 12px">{panels} Panels</span></span></h2>
      <p style="margin:0 0 22px;font-size:15px;color:var(--text-body)">Modeled to produce what you use over a year &mdash; {gen_yr} kWh against {cons_yr} kWh consumed.</p>
      <ul class="check" style="list-style:none;margin:0 0 24px;padding:0;display:grid;gap:11px;font-size:15px;color:var(--text-body)">
        {checklist}
      </ul>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;border-top:1px solid var(--border-hairline);border-bottom:1px solid var(--border-hairline);padding:16px 0;margin-bottom:22px">
        {stats}
      </div>
      <div style="margin-top:auto">
        <div style="font-size:12px;color:var(--text-muted);margin-bottom:2px">Total, installed</div>
        <div style="font-family:'Space Grotesk',sans-serif;font-weight:800;font-size:38px;letter-spacing:-.02em;color:var(--price-green)">{price}</div>
        <div style="font-size:12px;color:var(--text-muted)">grid-tied, no battery &middot; preliminary, confirmed after site survey</div>
      </div>
    </div>

    <div class="card" style="padding:clamp(24px,4vw,36px)">
      <div class="eyebrow">What changes on your bill</div>
      <h2 style="font-weight:700;font-size:28px;margin:0 0 12px">Energy Charges Down. Fixed Charge Stays.</h2>
      <p style="font-size:15px;line-height:1.65;color:var(--text-body);margin:0 0 22px">Your June bill splits into three parts. Solar works on one of them.</p>
      <div style="display:grid;gap:10px">
        <div style="display:flex;justify-content:space-between;gap:12px;padding:12px 14px;border-radius:.75rem;background:rgba(255,103,0,.07);border:1px solid rgba(255,103,0,.25)">
          <div><div style="font-weight:600">Energy charge &mdash; {bill_kwh} kWh @ G${rate}</div><div style="font-size:13px;color:var(--text-body)">This is what the array offsets, month after month.</div></div>
          <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;white-space:nowrap;color:var(--price-green)">G$95,790</div>
        </div>
        <div style="display:flex;justify-content:space-between;gap:12px;padding:12px 14px;border-radius:.75rem;border:1px solid var(--border-hairline)">
          <div><div style="font-weight:600">Fixed charge (Tariff B)</div><div style="font-size:13px;color:var(--text-body)">A standing charge from GPL &mdash; unchanged by solar.</div></div>
          <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;white-space:nowrap">{fixed}</div>
        </div>
        <div style="display:flex;justify-content:space-between;gap:12px;padding:12px 14px;border-radius:.75rem;border:1px solid var(--border-hairline)">
          <div><div style="font-weight:600">Balance brought forward</div><div style="font-size:13px;color:var(--text-body)">Arrears from earlier bills &mdash; not a monthly cost, and not something solar can reduce.</div></div>
          <div style="font-family:'Space Grotesk',sans-serif;font-weight:700;white-space:nowrap">G$113,197</div>
        </div>
      </div>
      <p style="font-size:13.5px;line-height:1.6;color:var(--text-body);margin:20px 0 0">At your 3-month average of {avg3} kWh, energy charges run to about <strong style="color:var(--ink)">{offset_yr} a year</strong>. The recommended array is modeled to generate slightly more than that over twelve months.</p>
    </div>
  </div>
  <p style="font-size:12.5px;color:var(--text-faint);margin:16px 4px 0;max-width:820px;line-height:1.6">Generation modeled with PVGIS for Georgetown: 10&deg; tilt, south-facing, crystalline-silicon modules, 14% system losses, terrain horizon enabled &mdash; {yield_kwp} kWh per installed kWp per year. Savings assume energy charges at G${rate}/kWh and are capped at your metered consumption; exported energy is not assigned a value until GPL confirms this account's net-billing eligibility. Actual output varies with weather, shading and roof orientation.</p>
</section>

<section class="wrap" style="padding-top:48px">
  <div class="card" style="padding:clamp(22px,4vw,36px) clamp(22px,4vw,40px)">
    <div class="eyebrow">Why {panels} panels</div>
    <h2 style="font-weight:700;font-size:28px;margin:0 0 12px">Sized to Match a Year, Not a Month.</h2>
    <p style="font-size:15px;line-height:1.65;color:var(--text-body);margin:0 0 26px;max-width:820px">Your bill gives two consumption figures: {bill_kwh} kWh for this cycle and a {avg3} kWh average over the previous three months. Annualised, that's about {cons_yr} kWh. One 450 Wp panel in Georgetown produces roughly {per_panel} kWh a year, so {cons_yr} &divide; {per_panel} &asymp; 33.3 panels &mdash; rounded up to {panels}.</p>
    <div style="overflow-x:auto">{chart}</div>
    <div class="legend">
      <span><span style="width:22px;height:12px;border-radius:3px;background:rgba(9,50,27,.3);display:inline-block"></span>Your consumption (kWh/month)</span>
      <span><span style="width:22px;height:12px;border-radius:3px;background:#FF6700;display:inline-block"></span>Modeled output of {panels} panels, annual average</span>
    </div>
    <div style="overflow-x:auto;margin-top:28px">
      <table class="sens">
        <thead><tr><th>Array</th><th>Capacity</th><th>Modeled output</th><th>What it means</th></tr></thead>
        <tbody>{sens}</tbody>
      </table>
    </div>
    <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:20px;margin-top:26px">
      <div style="border-left:3px solid var(--orange);padding-left:16px">
        <h3 style="font-size:17px;font-weight:700;margin:0 0 6px">Why not more</h3>
        <p style="font-size:14.5px;line-height:1.65;color:var(--text-body);margin:0">The PVGIS model already deducts 14% for real-world losses. Adding panels on top for soiling or degradation would count those losses twice. Until twelve months of bills or new loads show higher demand, extra capacity is money spent producing energy you can't yet be paid for.</p>
      </div>
      <div style="border-left:3px solid var(--gold);padding-left:16px">
        <h3 style="font-size:17px;font-weight:700;margin:0 0 6px">Why annual, not monthly</h3>
        <p style="font-size:14.5px;line-height:1.65;color:var(--text-body);margin:0">This bill covers mid-May to mid-June, a lower-yield stretch of the year. GPL's net-billing programme banks surplus energy as credits for approved systems, so a sunny month can carry a cloudy one. Sizing to the year, rather than the weakest month, avoids paying for an array that over-produces most of the time.</p>
      </div>
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
    <div>Quote SV-2026-0144 &middot; valid 30 days from issue &middot; prices in Guyanese dollars (G$), installed</div>
  </div>
</section>
</body>
</html>"""

html = HTML.format(
    fonts=FONTS, css=CSS,
    kwp=("%.1f" % KWP), panels=PANELS,
    gen_yr=format(GEN_YR, ","), cons_yr=format(CONS_YR, ","),
    bill_kwh=format(BILL_KWH, ","), avg3=format(int(round(AVG3_KWH)), ","),
    rate=("%.2f" % RATE), fixed=gfmt(FIXED_MO), offset_yr=gfmt(OFFSET_YR),
    yield_kwp=("%.0f" % YIELD_PER_KWP), per_panel=("%.0f" % (PANEL_W / 1000.0 * YIELD_PER_KWP)),
    price=gfmt(PRICE),
    badges="".join(badge(*b) for b in [("25 yrs", "performance warranty"), ("10 yrs", "product warranty"), ("100%", "annual energy match")]),
    checklist="".join('<li><span>&#10003;</span><span>%s</span></li>' % c for c in CHECKLIST),
    stats=stat("~%sk kWh" % ("%.1f" % (GEN_YR / 1000.0)), "modeled yield / year") +
          stat("~" + gfmt(OFFSET_YR), "energy charges offset / year", "var(--price-green)"),
    chart=chart_svg(), sens=sens_rows(),
    next_steps="".join('<li><b>%d</b><span>%s</span></li>' % (i + 1, t) for i, t in enumerate(NEXT_STEPS)),
    warranties="".join(warr(v, t) for v, t in [
        ("25 yrs", "Panel performance warranty &mdash; guaranteed output for a quarter century."),
        ("10 yrs", "Product warranty on panel materials and workmanship &mdash; defects covered, parts and labour."),
        ("5 yrs", "Comprehensive coverage on the inverter, mounting and workmanship."),
        ("Lifetime", "Support from Solvio's solar engineers &mdash; whenever you need us.")]),
)

if not os.path.isdir(OUT):
    os.makedirs(OUT)
p = OUT + r"\index.html"
io.open(p, "w", encoding="utf-8", newline="\n").write(html)
print("index.html  %.1f KB" % (os.path.getsize(p) / 1024.0))
print("kWp=%.1f gen=%d cons=%d margin=%.2f%% offset/yr=%s price=%s" % (KWP, GEN_YR, CONS_YR, MARGIN_PCT, gfmt(OFFSET_YR), gfmt(PRICE)))
