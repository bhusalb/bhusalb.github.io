# Research website maintenance

`generate-social-cards.cjs` contains the editable HTML, CSS, and SVG source for the three 1200 × 630 tutorial sharing images in `assets/img/research/`. The images are committed so normal Jekyll builds do not need Node or a browser.

To regenerate them with Node 20 or newer, install Playwright outside the repository and run the script with an installed Chrome executable:

```sh
npm install --prefix /tmp/site-social-card-tools playwright@1.64.1
NODE_PATH=/tmp/site-social-card-tools/node_modules \
  CHROME_EXECUTABLE="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  node bin/generate-social-cards.cjs
```

On other systems, set `CHROME_EXECUTABLE` to the Chrome/Chromium executable. Alternatively, install Playwright's Chromium in a temporary directory and omit `CHROME_EXECUTABLE`:

```sh
PLAYWRIGHT_BROWSERS_PATH=/tmp/site-social-card-browsers \
  /tmp/site-social-card-tools/node_modules/.bin/playwright install chromium
NODE_PATH=/tmp/site-social-card-tools/node_modules \
  PLAYWRIGHT_BROWSERS_PATH=/tmp/site-social-card-browsers \
  node bin/generate-social-cards.cjs
```

After changing a card, inspect the generated PNG at its original size to check title wrapping, diagram labels, and cropping. Keep the matching tutorial's `og_image`, `og_image_alt`, and `twitter_card` front matter in sync.
