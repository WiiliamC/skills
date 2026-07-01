---
name: research-survey
description: Rigorous, evidence-first research workflow for comprehensive surveys of academic papers, open-source projects, software tools, benchmarks, methods, libraries, datasets, and technical ecosystems. Use only when the user explicitly invokes `$research-survey` or explicitly names this skill; do not use implicitly for ordinary research requests.
---

# Research Survey

## Overview

Conduct a broad, source-backed survey that favors recall over premature narrowing, then distill reliable information into a rigorous comparative report. Emphasize both classic/foundational objects and the newest credible objects, clearly separate evidence from inference, and mark uncertain or unknown items explicitly.

## Invocation Rule

Use this skill only after explicit invocation, such as `$research-survey`, "use research-survey", or "使用 research-survey". If the user asks for research without explicitly invoking this skill, do not apply these expanded requirements unless the active system has already loaded the skill.

## Workflow

1. Clarify scope only when necessary. If the topic is usable as written, proceed without asking. If the domain is broad, choose an inclusive scope and state it.
2. Search broadly before synthesizing. Cover academic literature, official project pages, repositories, documentation, release notes, benchmark leaderboards, standards/specs, datasets, surveys, and credible technical reports as applicable.
3. Prefer primary and authoritative sources. Use papers, official docs, repositories, benchmark pages, standards bodies, and maintainer announcements before blogs or secondary summaries. Use secondary sources mainly for discovery or historical context.
4. Include both classic and recent objects. Identify foundational/high-impact papers, projects, or tools, and also verify the newest credible developments with current sources.
5. Record evidence while searching. Track source URL, date or version, object name, category, claims supported by the source, and any missing information.
6. Compare objects using dimensions appropriate to the topic: task coverage, method/architecture, licensing, maturity, ecosystem, data requirements, deployment constraints, performance, cost, maintainability, community activity, and known limitations.
7. Quantify when reliable metrics exist. Prefer directly reported benchmark scores, reproducible evaluation results, adoption signals, release cadence, stars/downloads only when relevant, latency/throughput, cost, accuracy, memory, or dataset sizes. Do not fabricate numbers or normalize incompatible metrics without saying so.
8. Synthesize cautiously. Distinguish facts, source-backed trends, and clearly labeled hypotheses about future direction.

## Search Requirements

- Start with multiple query families rather than one query. Include synonyms, predecessor names, benchmark/task names, key authors/organizations, and implementation/tooling terms.
- Search for surveys and taxonomies early to avoid missing established categories, but verify final claims against primary sources.
- For academic topics, search paper databases or authoritative indices when available, plus arXiv, conference pages, project pages, and citation-linked work.
- For open-source projects, inspect the repository, releases/tags, README/docs, license, issue/discussion activity when relevant, and latest commit/release dates.
- For software tools, inspect official docs, changelogs/release notes, package registries, compatibility matrices, pricing/licensing pages when applicable, and benchmark or comparison pages.
- Expand the search when a source names additional important objects. Prefer "only more, not less" coverage until marginal new results are low quality or redundant.
- Verify recency-sensitive facts with live/current sources. Do not rely on model memory for latest versions, leaders, maintainers, licensing, pricing, or project status.

## Reliability Rules

- Do not assert unsupported facts. If evidence is absent, conflicting, or low confidence, write `unknown`, `uncertain`, or `conflicting evidence`, and briefly explain why.
- Cite sources for nontrivial claims, especially rankings, performance, dates, licensing, availability, and "latest" statements.
- Prefer conservative wording for comparisons. Use "reported", "in this benchmark", or "under these conditions" when metrics are context-bound.
- Keep benchmarks comparable. If objects are evaluated on different datasets, versions, hardware, or tasks, say they are not directly comparable.
- Do not convert popularity into quality. Treat stars, downloads, citations, and media attention as adoption signals, not proof of effectiveness.
- Note negative evidence: missing docs, stale releases, unclear license, unreproduced claims, small evaluation scope, or absent benchmarks.

## Report Structure

Produce the final report in the user's language unless asked otherwise. Include:

1. Executive summary: scope, major conclusions, and confidence level.
2. Search methodology: source types searched, query families, inclusion/exclusion criteria, and date of search.
3. Taxonomy: categories that organize the field.
4. Classic/foundational objects: key papers/projects/tools with why they matter.
5. Latest/current objects: recent credible developments with exact dates, versions, or publication venues when available.
6. Summary table: object, type, year/latest version, source, core idea/use case, strengths, weaknesses, maturity/status, key metrics, license/availability when relevant.
7. Comparative analysis: advantages, disadvantages, effectiveness, tradeoffs, and best-fit use cases.
8. Quantitative metrics: table of reliable metrics with dataset/benchmark, conditions, and caveats. If reliable metrics are unavailable, state that explicitly.
9. Gaps and unknowns: unresolved questions, missing evidence, conflicting claims, and weakly supported areas.
10. Development direction: cautious, evidence-based trends and possible future directions, labeled as inference rather than fact.
11. References: grouped by papers, projects/tools, benchmarks/docs, and secondary sources if used.

## Minimum Output Standards

- Include at least one comprehensive summary table when multiple objects are surveyed.
- Include a separate metrics table when any trustworthy quantitative results exist.
- Include source links or citations for each object in the summary table.
- State `unknown` rather than leaving important cells ambiguous.
- Give concise recommendations only after presenting evidence and tradeoffs.
- If the available evidence is insufficient for a rigorous conclusion, say so directly and explain what evidence would be needed.
