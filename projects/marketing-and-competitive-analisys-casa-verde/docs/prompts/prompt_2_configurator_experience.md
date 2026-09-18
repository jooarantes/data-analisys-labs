# Prompt 2: Discover, Browse, Capture, and Synthesize

**Important: You will need to enable the Playwright and the Playwright Interactive Skills in Codex**

Copy and paste this into Codex after Prompt 1 is complete:

```text
Context: This prompt is the long stretch and runs in two phases inside one prompt. Phase 2a discovers the 5 Austin firms that match the criteria. Phase 2b visits each shortlisted firm's site and Instagram, captures evidence, fills the schema, and synthesizes a positioning map. Use Playwright (or Chrome MCP, whichever browser automation is connected) for live browsing. Failures and login walls are data, not bugs.

Instruction: Read the inputs first. Phase 2a: use web search to find 5 Austin-area firms that fit the Competitor Discovery criteria from the framework. Write `reports/competitor_shortlist.md` with one row per firm (name, url, instagram handle, one-line rationale tied back to the criteria) plus a short list of candidates rejected and why. Pause and surface the shortlist in the report before moving on. Phase 2b: for each shortlisted firm, open the live website (homepage, about, portfolio) and Instagram grid in the browser, capture screenshots to `assets/screenshots/websites/<slug>/` and `assets/screenshots/instagram/<slug>/`, and fill `docs/reports/competitors/<slug>.md` against every dimension in the framework. Cite the source for each cell. Where pricing or sustainability claims are not disclosed, write "unknown" with the source you tried. Never guess. After all five firms are filled, write `docs/reports/comparison.md` with a side-by-side table across the framework dimensions plus a positioning map. Choose axes that matter for Casa Verde (honest materials versus showroom luxury on x, residential intimate versus commercial scale on y, or sharper alternatives if the data suggests them).

Input:
- `reports/research_framework.md`
- `brand/casa_verde_brand_bible.md`
- `templates/competitor_research_schema.md`
- `.agents/skills/casa-verde/SKILL.md`
- Live web access through the connected browser automation skill

Output:
- `docs/reports/competitor_shortlist.md` with 5 firms and rejected candidates
- `docs/reports/competitors/<slug>.md` for each of the 5 firms, fully filled against the framework
- Screenshots in `assets/screenshots/websites/<slug>/` and `assets/screenshots/instagram/<slug>/`, with documented gaps for any offline site or login wall
- `docs/reports/comparison.md` with the side-by-side table and positioning map
- A short report listing changed files and any sites that failed or hit a login wall
```
