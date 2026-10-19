---
name: gsc-content-refresh
description: Analyze an existing article with Google Search Console comparison data, identify lost-impression recovery opportunities and high-value queries to protect, check overlap with similar site pages, and produce a safe content-refresh brief. Use for article updates, content decay, traffic or visibility drops, and requests to avoid removing important keywords. Do not use for broad technical SEO audits or net-new keyword research without an existing article.
---

# GSC Content Refresh

Create an evidence-backed refresh brief that recovers search visibility without damaging the article's current query coverage.

## Required inputs

Establish these from the request, active browser tab, connector, or supplied export:

- Exact article URL and site property.
- Comparison periods and search type.
- Page-filtered GSC query data containing clicks, impressions, CTR, and position for both periods.
- The current article content.

Do not ask the user to repeat information visible in the active GSC tab. If exact page-filtered data is unavailable, say what was checked and request only the missing export or access needed.

## Data acquisition

Prefer the cheapest exact source:

1. A supplied GSC comparison CSV or workbook.
2. A Search Console connector/API that supports the exact page filter and comparison.
3. The user's signed-in Chrome GSC report: verify the page filter and periods, then export CSV.

When the active tab is referenced, inspect it first. Keep browser actions read-only except downloading the report. Never change Search Console properties, filters, settings, or indexing state unless explicitly requested.

For a comparison CSV, run:

```bash
python scripts/analyze_gsc_queries.py <Queries.csv> --format markdown
```

Use `--format json` when structured output is easier to synthesize. The script ranks evidence; semantic relevance and page ownership still require judgment.

## Analysis workflow

1. Verify that the export belongs to the target article and periods.
2. Quantify page-level change: clicks, impressions, CTR, and average position.
3. Classify queries into:
   - **Recover:** relevant queries with material lost impressions, especially when position also worsened.
   - **Protect:** queries with high current impressions or clicks, plus growing queries whose coverage must remain.
   - **Monitor / exclude:** weakly related, accidental, seasonal, or misleading queries that should not drive the rewrite.
4. Group spelling variants and near-duplicate queries by search intent. Preserve the topic and answer, not every misspelling verbatim.
5. Diagnose each major loss:
   - Impressions down + position worse: likely ranking/coverage loss.
   - Impressions down + position stable or better: likely demand, seasonality, SERP, or data-mix change; label as a hypothesis.
   - Impressions up + clicks weak: CTR or rank opportunity, not a visibility loss.
6. Read [references/analysis-framework.md](references/analysis-framework.md) for prioritization, relevance, and similar-page analysis.
7. Read [references/output-template.md](references/output-template.md) before delivering the refresh brief.

## Similar-page and cannibalization check

Before recommending any change to Title, H1, meta description, canonical, URL, primary keyword ownership, deletion, merge, or redirect:

- Obtain query-to-page evidence for the priority query clusters when available.
- Identify related pages from the site's articles, sitemap/crawl, internal search, or `site:` results.
- Compare URL, Title, H1, intent, and topic coverage.
- Assign one owner page per primary intent and label other pages as supporting, overlapping, or unrelated.

If query-to-page evidence is unavailable, label cannibalization **not checked** and do not present Title/H1/URL ownership changes as confirmed recommendations.

## Writing brief rules

- Prioritize lost impressions first, then current visibility protection, clicks, position recovery potential, and business relevance.
- Never delete a section that supports a Protect cluster unless equivalent coverage remains elsewhere on the same owner page.
- Translate query clusters into useful H2/H3 sections and direct answers; do not stuff exact-match variants.
- Put a concise answer immediately after question-style headings, then add explanation, examples, and decision guidance.
- Separate confirmed GSC facts from hypotheses about causes.
- For health, finance, legal, or other YMYL topics, verify claims with current authoritative sources, avoid absolute promises, and require visible author/reviewer credentials and update date.
- Preserve the existing URL unless a redirect/consolidation plan is explicitly justified and authorized.

## Completion standard

The result must include:

- Executive snapshot and evidence/date range.
- Lost-impression table ranked by relevance and recoverability.
- Protection table for current and growing queries.
- Query clusters mapped to keep, strengthen, add, consolidate, or exclude actions.
- Similar-page relationship and owner-page map.
- Recommended article outline and writing notes.
- Risks, data gaps, and a 2- to 6-week measurement plan.

Match the user's language and keep the report practical.
