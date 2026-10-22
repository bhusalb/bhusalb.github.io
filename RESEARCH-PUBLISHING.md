# Publishing research on this site

The site connects papers, tutorials, software, and citation downloads. All substantive content is rendered into HTML at build time; reading it does not require JavaScript. `llms.txt` and the structured exports are additional discovery formats, not guarantees of indexing or recommendations.

## Sources of truth

- `_bibliography/papers.bib`: titles, author order, venues, dates, identifiers, abstracts, PDFs, and code links. Preserve the published title and author list. Identify preprints by their actual repository and update the record when a published version appears.
- `_data/research.yml`: topic groupings and concise explanations of contributions and relevance. Keep claims within the paper's stated assumptions and evaluation.
- `_posts/`: original research tutorials. Include `description`, `author`, `date`, `related_papers` (bibliography keys), and `sitemap: true` in front matter. Link to the original paper and distinguish teaching examples from experimental results.
- `_examples/posts/`: archived al-folio examples, excluded from the published site and feed.

The generator preserves `/publications/<key>/` URLs and creates `/publications.json`, `/publications.bib`, and per-paper `cite.bib` / `cite.ris` files. `/llms.txt` lists research pages and tutorials; `/llms-full.txt` adds the complete abstracts, summaries, and citation information. These outputs are generated from the bibliography instead of being maintained separately.

## Before publishing

Run the build and the integration checks:

```sh
bundle install
JEKYLL_ENV=production bundle exec jekyll build --lsi
bundle exec ruby bin/validate_research_site.rb
python3 assets/code/clipping_polar_geometry.py
npm ci
npx prettier _config.yml _pages _posts _includes/metadata.liquid _includes/head.liquid --check
```

The deployment workflow checks rendered metadata, local links, publication exports, sitemap entries, feed content, and the CV download on pull requests and before publishing. This replaces the old raw-Markdown link checker (which treated Liquid expressions as broken URLs) and the redundant post-deployment rebuild. It also submits the sitemap's URLs to IndexNow after deployment. A successful submission is a notification, not proof of indexing.

## Search visibility and measurement

Submit `https://bishnubhusal.com.np/sitemap.xml` in Google Search Console and Bing Webmaster Tools using the owner's accounts. Inspect the homepage, a tutorial, and a paper URL after substantial changes. If domain verification is unavailable, the theme supports verification tokens through `_config.yml`. Never put account credentials in the repository.

Google Scholar discovers articles independently of regular web search. Paper pages expose Highwire citation tags and full-text links when available. Check the Scholar profile for duplicate versions, correct publication metadata, and links to self-hosted PDFs. Only host full text when the version may be shared.

Track search impressions and queries, visits to tutorials and paper pages, PDF/code interest where measurement is configured, and citations over time. Analytics is currently disabled; the old Universal Analytics identifier is not an active measurement system. Do not claim a traffic or citation increase without measurements.

For sustained reach, publish a focused explanation when a paper, artifact, or substantial revision is ready. Link from the corresponding project README and relevant scholarly profiles when those accounts are available. Share tutorials with communities where the research answers a real question, and cite other researchers' contributions accurately. This repository's deployment does not post to social accounts or contact other people.
