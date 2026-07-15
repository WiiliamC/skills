---
name: research-general
description: Comprehensive, evidence-first workflow for general information gathering, background research, fact-checking, topic overviews, timelines, entity profiles, policy and social issue research, multi-source synthesis, and sourced briefing reports across non-specialist domains. Use when Codex is asked to 搜集资料、搜索并汇总、做背景调查、一般性调研、专题研究、事实核查、梳理来龙去脉、形成资料综述, investigate a topic broadly, build a sourced brief, or find as much relevant information as practical. Do not use for competitor or market landscape work covered by research-competitor, or for systematic surveys of papers, open-source projects, technical tools, benchmarks, methods, libraries, datasets, or technical ecosystems when research-tech is explicitly invoked.
---

# Research General

Conduct broad, traceable research across heterogeneous sources, then turn the evidence into a clear synthesis. Favor recall during discovery and precision during reporting. Adapt the structure to the question instead of forcing every topic into a comparison report.

## Core workflow

1. **Frame the question.** Extract the subject, decisions to support, time range, geography, audience, requested dimensions, output format, and research cutoff date. Proceed with an inclusive stated scope when ambiguity is low. Ask only when a missing choice would materially change the result.
2. **Inspect available context.** Check user-provided files, local resources, connected sources, requested output paths, and repository instructions before browsing. Treat supplied material as evidence to verify, not automatically as ground truth.
3. **Map the topic.** Define key concepts, boundaries, subquestions, entities, events, stakeholders, aliases, translations, disputed terms, and likely information gaps. Separate easily confused concepts before searching.
4. **Design multiple query families.** Search the main question plus synonyms, local-language terms, official terminology, dates, organizations, people, locations, causes, effects, controversies, criticism, data, and source-specific queries. Do not rely on one broad query.
5. **Search in passes.** First establish vocabulary and a provisional map; then locate primary and authoritative sources; then broaden across perspectives, regions, languages, and source types; then run gap, contradiction, negative-evidence, and recency checks.
6. **Maintain an evidence ledger.** For each material claim record the claim, source, URL or local location, publisher or author, event date, publication date, geography, source type, relevant excerpt or data definition, confidence, and conflicts. Keep search notes temporary unless requested.
7. **Follow useful leads.** Expand named entities, citations, references, linked documents, predecessor events, alternate spellings, and newly discovered subtopics. Use secondary sources for discovery, then verify important claims against the most direct available evidence.
8. **Test coverage.** Check the topic across time, geography, stakeholders, source types, languages, supportive and critical views, and known unknowns as applicable. Continue until repeated searches mostly yield duplicates, circular citations, low-quality sources, or details outside scope.
9. **Resolve and preserve disagreement.** Compare definitions, dates, jurisdictions, populations, methods, and incentives. Prefer the source closest to the underlying fact, but show credible conflicting accounts when they cannot be reconciled. Never silently average incompatible figures.
10. **Synthesize around the question.** Lead with the answer, then organize evidence by themes, chronology, actors, causes, consequences, or another structure suited to the topic. Separate sourced fact, source characterization, analysis, and inference.
11. **Cite and validate.** Put direct citations near nontrivial claims. Check that links support the exact claim, dates and units are consistent, quotes are accurate and short, requested dimensions are covered, and uncertainty is explicit.

## Search breadth rules

- Use current browsing or authoritative connected sources whenever facts may have changed or the user requests comprehensive research.
- Begin with at least three meaningfully different query families. Vary vocabulary and source targets, not just word order.
- Search in relevant local languages for region-specific topics. Record translated names and transliteration variants.
- Include primary records, authoritative syntheses, credible reporting, specialist analysis, and first-person or community evidence when each adds a distinct perspective. Do not mistake diversity of URLs for diversity of evidence.
- Search for disconfirming information with terms such as criticism, correction, audit, limitation, dispute, lawsuit, retraction, failure, or the domain-specific equivalent.
- Trace important statistics and quotations back to their origin. Treat repeated copies of one claim as one evidence chain.
- For “尽可能全面”, “只多不少”, or equivalent requests, bias toward recall: expand adjacent subtopics and lower-priority findings, placing them in appendices or a source inventory rather than deleting them.
- Stop only after coverage checks and diminishing returns. State the research boundary, inaccessible sources, and important searches that produced no reliable evidence.

## Source and reliability rules

Prefer sources in this order when they directly address the claim:

1. **Primary records:** laws, regulations, court or government records, official statistics, original datasets, filings, transcripts, speeches, contemporaneous documents, direct announcements, and original research.
2. **Authoritative syntheses:** government or institutional reviews, standards bodies, reputable reference works, systematic reviews, and transparent expert reports.
3. **Credible secondary reporting and analysis:** established newsrooms, specialist publications, and named experts whose methods and sourcing are visible.
4. **Discovery or perspective sources:** aggregators, social media, forums, anonymous posts, and unsourced summaries.

Match source type to claim. Official sources are strongest for what an institution says or records, but independent sources may be necessary for impact, criticism, or verification. First-person accounts can establish a person's stated experience, not prevalence. Search-result snippets and AI summaries are leads, not evidence.

- Verify volatile facts as of an exact date. Distinguish event date, effective date, announcement date, and publication date.
- Cite every nontrivial factual claim, especially numbers, dates, rankings, causal claims, legal or policy status, and claims about named people or organizations.
- Use `unknown`, `uncertain`, `not found`, or `conflicting evidence` when warranted. Explain the search boundary for important missing facts.
- Qualify estimates with owner, population, geography, period, definition, and method. Keep differently defined figures separate.
- Treat source silence as absence of evidence unless the source is demonstrably complete for that field.
- Label allegations, opinions, forecasts, and institutional claims; do not rewrite them as established fact.
- Prefer paraphrase. Quote only when the exact wording matters, and preserve context.

## Output design

Use the user's requested format and language. For substantial research, include the following when relevant:

- Executive answer with major findings, confidence, and the most important caveats.
- Scope and method, including research date, query families, source types, and inclusion or exclusion rules.
- A topic map, taxonomy, timeline, stakeholder map, or comparison table when it materially clarifies the evidence.
- Thematic findings with citations next to claims.
- A source-backed table for multiple entities, events, claims, or options; use `unknown` for material missing fields.
- Conflicts, limitations, negative evidence, and open questions.
- Clearly labeled implications or inference after the evidence.
- A compact source index grouped by role or source type when the report is long.

Do not manufacture a fixed report shape for a narrow request. A fact-check may use claim-by-claim verdicts; a historical investigation may center a timeline; an entity brief may center actors and relationships; a broad topic review may use themes and a source inventory.

## Boundary with neighboring skills

- Use **research-competitor** when commercial competitors, products, vendors, market size or share, pricing, channels, customer segments, business models, or strategic opportunities are central.
- Use **research-tech** when the user explicitly invokes it for a rigorous survey of academic papers, open-source projects, software tools, technical methods, benchmarks, libraries, datasets, or a technical ecosystem.
- Use this skill for the surrounding general context or for mixed-domain research whose core is neither commercial competition nor a systematic technical survey. If a task spans boundaries, apply the specialist skill to its specialist section and this workflow to the remainder without duplicating searches.

## Quality gates

Before completion, verify:

- The answer addresses the user's actual questions, not merely the easiest available sources.
- Important synonyms, languages, time periods, stakeholders, and counterevidence were searched where relevant.
- Major claims trace to direct sources and repeated reports are not counted as independent confirmation.
- Citations support the exact adjacent claims and no search-results pages are cited.
- Conflicting definitions, numbers, dates, and accounts remain visible and explained.
- Facts, source claims, analysis, and inference are distinguishable.
- Material gaps say `unknown` or explain why evidence was not found.
- The final structure is readable; extensive lower-priority evidence is retained in appendices rather than overwhelming the main answer.
