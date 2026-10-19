# Analysis Framework

Use this reference after obtaining page-filtered comparison data.

## 1. Evidence normalization

For every query calculate:

- `impression_delta = current_impressions - previous_impressions`
- `click_delta = current_clicks - previous_clicks`
- `position_delta = current_position - previous_position` (positive means worse)
- current and previous CTR

Confirm whether GSC exported partial rows. Page totals and table-row sums may differ because anonymized queries are excluded from the table.

## 2. Lost-impression priority

Start with absolute lost impressions, then adjust qualitatively:

| Factor | Raise priority when | Lower priority when |
|---|---|---|
| Relevance | Query matches the article's main or supporting intent | Query is accidental, misleading, or belongs to another page type |
| Rank movement | Position deteriorated, especially from top 3/5/10 | Position held or improved |
| Recoverability | Current position remains near page one | Query has almost disappeared and intent no longer matches |
| Existing value | Query still has clicks or strong current impressions | It never produced meaningful engagement |
| Business value | It supports qualified next actions | It attracts unrelated informational demand |

Do not let a large impression loss override weak semantic relevance.

## 3. Protection priority

A Protect cluster includes one or more of:

- Top current impressions for the page.
- Top current clicks for the page.
- Positive impression or click growth.
- Top-3 or top-5 position with material visibility.
- A query that directly expresses the article's core intent.

Protection means retaining the answer, heading context, entities, examples, internal links, and useful media. It does not require keeping awkward wording or every spelling variant.

## 4. Cluster by intent

Group variants into practical clusters such as:

- Definition / what it is.
- Symptoms or signs.
- Causes or risk factors.
- Duration or timeline.
- Treatment or relief.
- Complications / danger signs.
- Comparison or type/location variants.
- Question clusters about related body areas, products, places, or audiences.

Name each cluster with natural language. Select one representative query and list important variants beneath it.

## 5. Diagnose the pattern

Use these labels:

- **Ranking loss:** impressions and position both worsened.
- **Demand/seasonality hypothesis:** impressions fell while position stayed stable or improved.
- **CTR opportunity:** impressions are healthy or growing but clicks/CTR lag.
- **Intent mismatch:** query is visible but the article does not answer it directly or the SERP favors a different page type.
- **Possible cannibalization:** multiple site pages receive the same query or have overlapping Titles/H1s and intent.
- **Data anomaly:** abrupt or implausible change requiring validation by dates, country, device, search appearance, or export settings.

## 6. Relationship with similar articles

Build a compact page map for the top query clusters:

| Page | Intended intent | Shared clusters | Evidence | Role | Action |
|---|---|---|---|---|---|
| Target article | Main intent | Core clusters | GSC + page content | Owner candidate | Keep/strengthen |
| Related page | Distinct or overlapping intent | Shared queries/headings | Query-page data + page review | Supporting/overlapping | Link, differentiate, consolidate, or leave |

Evidence preference:

1. GSC query + page performance for the same period.
2. Titles, H1s, URLs, canonicals, and actual page content.
3. Sitemap/crawl and internal links.
4. Search results as supporting evidence, not proof of ownership.

Classify relationships:

- **Owner:** best page for the primary intent.
- **Supporting:** covers a narrower subtopic and should link to the owner.
- **Overlapping:** competes on the same intent; requires differentiation or consolidation analysis.
- **Adjacent:** related but should not be merged.
- **Unrelated:** ignore for this refresh.

Do not infer cannibalization merely because two pages mention the same keyword.

## 7. Content action mapping

For each cluster choose one action:

- **Keep:** already strong and essential.
- **Strengthen:** relevant loss with existing coverage; improve answer depth, structure, evidence, or media.
- **Add:** relevant intent missing from the owner page.
- **Consolidate:** duplicate sections inside the same page, or cross-page overlap confirmed with evidence.
- **Internal link:** another page owns the intent but the relationship helps users.
- **Exclude:** irrelevant, unsafe, misleading, or low-value query.
- **Monitor:** insufficient evidence or likely demand shift.

## 8. Safety checks before final recommendations

- Do not change URL or canonical without an explicit migration rationale.
- Do not promise rankings or recovery amounts.
- Do not recommend exact-match repetition or hidden/manipulative tactics.
- Preserve high-value media, tables, FAQs, and internal links that support Protect clusters.
- For YMYL content, flag unsupported medical/legal/financial claims and require authoritative citations and expert review.
