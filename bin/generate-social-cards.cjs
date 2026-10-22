// Rebuild the tutorial sharing images. See bin/README.md for temporary setup.
const { chromium } = require("playwright");
const fs = require("fs");
const path = require("path");
const outDir = path.resolve(__dirname, "../assets/img/research");
fs.mkdirSync(outDir, { recursive: true });
const cards = [
  {
    slug: "private-icl",
    topic: "PRIVATE LANGUAGE MODELS",
    title: "Privacy-preserving<br>in-context learning",
    subtitle: "Synthetic demonstrations<br>and privacy budgets",
    graphic: `<svg viewBox="0 0 330 330" aria-label="Private examples pass through a privacy mechanism to produce reusable demonstrations">
      <defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7" fill="#77d9c7"/></marker></defs>
      <g fill="#173c49" stroke="#77d9c7" stroke-width="2">
        <rect x="38" y="25" width="74" height="84" rx="8" transform="rotate(-9 75 67)"/><rect x="123" y="19" width="74" height="84" rx="8"/><rect x="208" y="25" width="74" height="84" rx="8" transform="rotate(9 245 67)"/>
      </g>
      <g stroke="#77d9c7" stroke-width="3" stroke-linecap="round" opacity=".65"><path d="M59 51h29m-29 13h35m-35 13h22M143 44h34m-34 13h34m-34 13h22M231 48l29 5m-31 8l35 6m-37 7l22 4"/></g>
      <path d="M160 117v30" stroke="#77d9c7" stroke-width="2" marker-end="url(#arrow)"/>
      <circle cx="160" cy="191" r="37" fill="#77d9c7"/>
      <text x="160" y="205" text-anchor="middle" font-size="43" fill="#092733" font-family="Georgia,serif">ε</text>
      <path d="M160 236v30" stroke="#77d9c7" stroke-width="2" marker-end="url(#arrow)"/>
      <rect x="75" y="277" width="170" height="43" rx="9" fill="#173c49" stroke="#77d9c7" stroke-width="2"/>
      <path d="M96 292h52m-52 12h90m15-14l6 7 13-14" fill="none" stroke="#77d9c7" stroke-width="3" stroke-linecap="round"/>
    </svg>`,
  },
  {
    slug: "private-muon",
    topic: "PRIVATE OPTIMIZATION",
    title: "Why gradient clipping<br>changes Muon’s geometry",
    subtitle: "A two-dimensional example",
    titleSize: "51px",
    graphic: `<svg viewBox="0 0 330 330" aria-label="Two vectors illustrate the change in direction after clipping">
      <defs><marker id="teal" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0 0L9 4.5L0 9z" fill="#77d9c7"/></marker><marker id="white" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0 0L9 4.5L0 9z" fill="#d9e8ec"/></marker></defs>
      <g fill="none" stroke="#355968" stroke-width="1"><path d="M35 45v255M85 45v255M135 45v255M185 45v255M235 45v255M285 45v255M25 50h275M25 100h275M25 150h275M25 200h275M25 250h275"/></g>
      <circle cx="110" cy="225" r="102" fill="none" stroke="#4d7c87" stroke-width="2" stroke-dasharray="6 7"/>
      <path d="M25 225h276M110 305V25" stroke="#89a7b2" stroke-width="2"/>
      <path d="M110 225L262 70" stroke="#d9e8ec" stroke-width="5" marker-end="url(#white)"/>
      <path d="M110 225L203 181" stroke="#77d9c7" stroke-width="5" marker-end="url(#teal)"/>
      <path d="M146 190a50 50 0 0 1 10 13" stroke="#77d9c7" stroke-width="3" fill="none"/>
      <circle cx="110" cy="225" r="6" fill="#77d9c7"/>
      <g font-family="Arial,sans-serif" font-size="17"><text x="195" y="51" fill="#d9e8ec">BEFORE</text><text x="205" y="213" fill="#77d9c7">AFTER</text></g>
    </svg>`,
  },
  {
    slug: "dipapprox-ccs25",
    topic: "ACM CCS 2025 · DIFFERENTIAL PRIVACY",
    title: "DipApprox: verifying<br>differential privacy<br>with Gaussian noise",
    subtitle: "Inside our ACM CCS 2025 paper",
    titleSize: "50px",
    graphic: `<svg viewBox="0 0 330 330" aria-label="Schematic Gaussian density with a shaded integral and certified lower and upper bounds">
      <defs><clipPath id="integral-region"><rect x="104" y="35" width="122" height="165"/></clipPath></defs>
      <text x="165" y="20" text-anchor="middle" font-size="16" fill="#d9e8ec" font-family="Arial,sans-serif" letter-spacing="1">GAUSSIAN NOISE</text>
      <path d="M28 195C70 194 90 183 110 135C132 75 145 49 165 49C185 49 198 75 220 135C240 183 260 194 302 195V200H28Z" fill="#77d9c7" opacity=".24" clip-path="url(#integral-region)"/>
      <path d="M28 200H302" stroke="#89a7b2" stroke-width="2"/>
      <path d="M104 200V147M226 200V147" stroke="#89a7b2" stroke-width="1.5" stroke-dasharray="4 5"/>
      <path d="M28 195C70 194 90 183 110 135C132 75 145 49 165 49C185 49 198 75 220 135C240 183 260 194 302 195" fill="none" stroke="#77d9c7" stroke-width="4" stroke-linecap="round"/>
      <g fill="#c0d2d9" font-size="19" font-family="Georgia,serif" font-style="italic" text-anchor="middle"><text x="104" y="224">a</text><text x="226" y="224">b</text></g>
      <text x="165" y="269" text-anchor="middle" fill="#77d9c7" font-size="28" font-family="Georgia,serif">L ≤ integral ≤ U</text>
      <text x="165" y="295" text-anchor="middle" fill="#d9e8ec" font-size="14" font-family="Arial,sans-serif" letter-spacing=".6">CERTIFIED INTEGRAL BOUNDS</text>
      <text x="165" y="324" text-anchor="middle" fill="#89a7b2" font-size="11" font-family="Arial,sans-serif" letter-spacing="1.4">SCHEMATIC</text>
    </svg>`,
  },
];
(async () => {
  const requestedSlug = process.argv[2];
  const selectedCards = requestedSlug ? cards.filter((card) => card.slug === requestedSlug) : cards;
  if (!selectedCards.length) {
    throw new Error(`Unknown card: ${requestedSlug}. Choose from ${cards.map((card) => card.slug).join(", ")}.`);
  }
  const browser = await chromium.launch({
    headless: true,
    ...(process.env.CHROME_EXECUTABLE ? { executablePath: process.env.CHROME_EXECUTABLE } : {}),
  });
  const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
  for (const card of selectedCards) {
    const html = `<!DOCTYPE html><html lang="en"><meta charset="UTF-8"><title>${card.slug} social card</title><style>
      *{box-sizing:border-box}body{margin:0;width:1200px;height:630px;overflow:hidden;background:#092733;color:#f3f7f8;font-family:Arial,Helvetica,sans-serif}.accent{position:absolute;top:0;left:0;width:1200px;height:7px;background:#77d9c7}.label{position:absolute;top:55px;left:64px;display:flex;align-items:center;gap:17px;font-size:16px;letter-spacing:2.3px;font-weight:600;color:#77d9c7}.label i{display:block;width:10px;height:10px;border-radius:50%;background:#77d9c7}.title{position:absolute;left:64px;top:142px;width:810px;margin:0;font-size:${
        card.titleSize || "60px"
      };line-height:1.14;font-weight:600;letter-spacing:-1.7px}.subtitle{position:absolute;left:66px;top:319px;font-size:28px;line-height:1.42;color:#c0d2d9;letter-spacing:-.3px}.graphic{position:absolute;right:34px;top:138px;width:304px;height:304px;opacity:.98}.footer{position:absolute;left:64px;right:64px;bottom:48px;border-top:1px solid #35515d;padding-top:25px;display:flex;align-items:center;justify-content:space-between}.author{font-size:26px;font-weight:600;letter-spacing:-.4px}.series{font-size:16px;color:#b9cbd3;margin-top:8px;letter-spacing:.2px}.domain{font-size:18px;color:#b9cbd3;letter-spacing:.3px}
    </style><body><div class="accent"></div><div class="label"><i></i>${card.topic}</div><h1 class="title">${card.title}</h1><div class="subtitle">${
      card.subtitle
    }</div><div class="graphic">${
      card.graphic
    }</div><div class="footer"><div><div class="author">Bishnu Bhusal</div><div class="series">Research tutorials</div></div><div class="domain">bishnubhusal.com.np</div></div></body></html>`;
    await page.setContent(html);
    await page.screenshot({ path: path.join(outDir, card.slug + ".png") });
    console.log(card.slug + ".png");
  }
  await browser.close();
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
