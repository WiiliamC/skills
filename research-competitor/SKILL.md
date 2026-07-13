---
name: research-competitor
description: Evidence-first workflow for comprehensive competitor research and market research covering product landscapes, feature and specification comparisons, pricing, launch dates, availability, sales and shipments, market size and share, customer segments, use cases, interaction models, channels, business models, risks, and strategic opportunities. Use when Codex is asked to conduct 竞品调研、市场调研、行业扫描、产品对标、竞争格局分析、market landscape、competitive analysis、benchmark commercial products, compare vendors, build a competitor matrix, or write a sourced research report. Especially use when facts are current or volatile and must be verified from live sources.
---

# Research Competitor

Conduct broad, current, source-backed commercial research, normalize unlike claims into comparable fields, and produce a decision-ready report. Favor coverage and traceability over premature narrowing.

## Core workflow

1. **Frame the assignment.** Extract the subject, geography, customer segment, time horizon, product boundary, required dimensions, output language, and destination file. Proceed with an inclusive, stated scope when ambiguity is low. Ask only when a missing choice would materially change the study.
2. **Inspect local context.** Check the requested output path, existing reports, templates, and repository instructions before researching. Preserve unrelated files and edits.
3. **Define a taxonomy before comparing.** Separate product types that solve different jobs or have incompatible architectures. State inclusion and exclusion rules. Add adjacent substitutes or prototypes only in a clearly labeled benchmark or roadmap section.
4. **Build a field schema.** Start from the user's requested fields, then select relevant optional fields from [references/field-catalog.md](references/field-catalog.md). Keep `unknown`, `not applicable`, `announced`, `preorder`, and `shipping` distinct.
5. **Search broadly in query families.** Search product lineups, official specifications, launch announcements, pricing, regional availability, sales or shipment evidence, market reports, customer use cases, interaction methods, reviews, failures, privacy, regulation, and roadmap. Use local authoritative resources or connectors when available; otherwise browse the web for current facts.
6. **Create an evidence ledger while searching.** For every material claim record the object, normalized value, raw wording, unit and conditions, event date, publication date, geography, source URL, source tier, and confidence. A working ledger may remain temporary unless the user requests it.
7. **Research in passes.** First establish the category and major players; then collect primary product facts; then market and sales evidence; then fill gaps and contradictions; finally search for challengers, discontinued products, substitutes, negative evidence, and recent announcements.
8. **Normalize carefully.** Convert units only when lossless. Preserve currencies and dates; add converted values only with an exchange-rate date. Do not compare standby, mixed-use, continuous audio, continuous recording, display-on time, and charging-case total as one battery metric. Do not combine shipment, sell-in, sell-through, activation, orders, crowdfunding backers, and revenue.
9. **Resolve conflicts.** Prefer a newer first-party specification for the current product, but retain the older launch value when discussing launch history. Prefer audited or named research data for market metrics. If credible sources still disagree, show both values, their definitions, and why they differ.
10. **Synthesize after coverage.** Separate sourced facts from analysis and inference. Explain strategic causes, tradeoffs, best-fit scenarios, barriers, white spaces, and risks. Avoid declaring a winner without specifying the user, scenario, metric, and evidence.
11. **Write the report.** Use the user's format or copy [assets/report-template.md](assets/report-template.md) as a starting structure. Put citations next to supported claims and direct links in comparison rows. Write to the requested file rather than only returning chat text.
12. **Validate before handoff.** Check table consistency, units, dates, price regions, duplicated products, broken or indirect citations, unsupported superlatives, missing requested fields, status labels, and report existence. Report limitations explicitly.

## Search and coverage rules

- Use live/current sources whenever price, availability, leadership, specifications, sales, laws, versions, or roadmaps may have changed.
- Start with at least three query families rather than a single broad query. Use local-language searches for each important market.
- Expand aliases: company name, brand, product family, model number, predecessor, translated name, and common misspellings.
- Search both leaders and challengers. Include regional specialists, new entrants, adjacent substitutes, discontinued products that shaped the category, and announced products when strategically relevant.
- Continue until new searches mostly return duplicates or low-quality objects. For a request such as “尽可能充分/只多不少,” bias toward recall and use appendices for lower-priority objects.
- For each priority competitor, seek at least: one primary product source, one commercial-status or price source, and one independent market/adoption source when such evidence exists.
- Do not fabricate missing values. Write `未披露/unknown` and state the search boundary when the omission matters.

## Source hierarchy

1. **Tier A — primary:** official product pages, manuals, support pages, launch posts, regulatory filings, financial statements, investor releases, standards, government data, and named raw datasets.
2. **Tier B — authoritative research:** established research firms, trade bodies, peer-reviewed research, retailer sell-through datasets, and transparent benchmark organizations.
3. **Tier C — reputable secondary:** major media, specialist publications with hands-on testing, established retailers, and analyst reports that name their methodology or sources.
4. **Tier D — discovery only:** aggregators, SEO comparison pages, anonymous posts, forums, social media, and unsourced reposts.

Use Tier D to discover leads or document user-reported problems, not as the sole support for specifications, sales, market share, or launch status. Label manufacturer claims and crowdfunding numbers as such. Never turn preorders, backers, production capacity, downloads, or “sold out” into unit sales without evidence.

## Citation and claim rules

- Cite every volatile or nontrivial fact: price, date, specification, availability, sales, share, ranking, policy, compatibility, and roadmap.
- Link to the page that directly supports the claim, not a search-results page.
- Keep quotes short; paraphrase by default.
- Place citations in the same paragraph or table cell as the claim whenever readable.
- Use exact event dates when available and distinguish them from article publication dates.
- Identify the metric owner and scope in prose or table headers, for example “IDC shipment estimate, China, 2025.”
- Qualify comparisons with conditions: `reported`, `under the vendor's test`, `online retail channel`, or `not directly comparable`.

## Required report properties

Unless the user specifies otherwise, include:

- Executive summary with conclusions and confidence.
- Scope, taxonomy, methodology, inclusion/exclusion rules, and research cutoff date.
- Market size, growth, share, and adoption evidence with definitions.
- A broad competitor landscape and normalized comparison tables.
- Separate functional/use-case and hardware/commercial views when one table would be too wide.
- Pricing, availability, launch status, and sales evidence.
- Application scenarios, customer segments, interaction or workflow comparison.
- Competitive advantages, weaknesses, business models, channels, and ecosystem dependencies.
- Strategic opportunities, risks, gaps, and near-term watchlist.
- Unknowns and conflicting evidence.
- Source index or bibliography.

For a large study, lead with conclusions and use appendices rather than deleting useful coverage. Prefer multiple readable tables over one extremely wide table.

## Quality gates

Before declaring completion, verify:

- Every user-requested dimension appears in the schema or is explicitly marked unavailable.
- Products from different categories are not ranked as if directly substitutable.
- All battery, performance, market, and sales figures retain their conditions and units.
- Launch, announcement, preorder, on-sale, delivery, and discontinuation dates are not conflated.
- Current price is not silently substituted for launch price, and regional taxes or subsidies are labeled.
- Market numbers from different firms are not combined without explaining scope differences.
- Important rows have direct citations and missing cells say `unknown` rather than remaining ambiguous.
- Conclusions follow from the evidence and clearly labeled inference.
- The requested output file exists and renders as valid Markdown or the requested format.

## Resource use

- Read [references/field-catalog.md](references/field-catalog.md) when designing a new comparison schema or when the user's requested fields are incomplete.
- Copy and adapt [assets/report-template.md](assets/report-template.md) for a new Markdown report. Remove irrelevant sections rather than filling them with generic text.
