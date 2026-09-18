# Casa Verde Competitive Intelligence Contract

## Goal and source of truth

Build an evidence-led picture of Austin and nearby Hill Country sustainable residential interior design so Elena Reyes and her team can make defensible positioning decisions for Casa Verde Studio. Compare actual residential work, material provenance, sustainability evidence, service scope, and budget fit. A natural-looking room alone is not evidence of sustainable practice.

Read these inputs before working:

- `brand/casa_verde_brand_bible.md`
- `docs/templates/competitor_research_schema.md`
- `.agents/skills/casa-verde/SKILL.md`
- `docs/reports/research_framework.md`, once created
- The relevant prompt file in `docs/prompts/`, using its contents rather than its filename to identify the stage.

The current user request takes precedence over older prompt examples. The framework is the research contract for prompts 2 through 4. Preserve its ten dimensions and evidence rules throughout research and publication. Do not silently change criteria to accommodate a preferred competitor or story.

For shell work, read and follow `~\.codex\RTK.md`. Prefix shell commands with `rtk`.

## Four-prompt build

| Stage | Work and completion requirements | Outputs |
|---|---|---|
| 1. Setup and framework | Read the inputs, establish this contract, and define discovery criteria and observable signals for every schema field. Do not populate firms or claim live market findings yet. | `AGENTS.md`; `docs/reports/research_framework.md` |
| 2a. Discover | Search for five qualifying Austin-area firms. Record inclusion evidence, budget uncertainty, and rejected candidates. Surface the shortlist and pause at the checkpoint required by prompt 2 before detailed capture. Never force five confirmed matches if evidence supports fewer. | `output/competitor_shortlist.md` |
| 2b. Browse, capture, synthesize | Inspect each shortlisted firm's live website and Instagram, save evidence, fill all ten fields with citations, and create a side-by-side comparison and positioning map. Record access failures. Apply the framework's map rules. | `output/competitors/<slug>.md`; `output/comparison.md`; screenshots at the paths below |
| 3. Internal positioning deck | Build the branded team deck from prompt 2 evidence. Include the landscape, five-firm overview when supported, per-firm findings, screenshots, map, opportunities, and recommendations. Preserve uncertainty in slide copy and source notes. | `output/casa_verde_positioning_deck.pptx`; `output/deck_summary.md` |
| 4. Public research artifacts | Create a 4 to 6 page branded white paper, a single-page infographic, and Instagram, email, and LinkedIn sharing copy. Present firms as landscape examples. Distinguish observations from outlook and recommendations. | `output/austin_sustainable_design_2026.pdf`; `output/austin_sustainable_design_infographic.png`; `output/sharing_blurbs.md` |

Execute only the stage requested. Future deliverable specifications do not authorize starting later stages or publishing, posting, or emailing artifacts.

## Paths and file conventions

- The canonical framework is `docs/reports/research_framework.md`, following the current request's explicit output list. Resolve legacy `output/research_framework.md` references to it. Do not create a second copy.
- The canonical schema is `docs/templates/competitor_research_schema.md`. Resolve older `templates/competitor_research_schema.md` references to it.
- Keep later-stage deliverables under `output/`, as specified above, unless a subsequent user request changes their paths.
- Store website captures in `assets/screenshots/websites/<slug>/` and Instagram captures in `assets/screenshots/instagram/<slug>/`.
- Use stable lowercase, hyphen-separated firm slugs across profiles, tables, and screenshot folders. Name captures `YYYY-MM-DD_<page-or-post>.png` and record their source URLs in the firm profile.
- Write Markdown as UTF-8. Use ISO dates, USD for prices, explicit price bases, and descriptive source links. Record access dates for live sources and publication dates where visible.
- Preserve source inputs and existing assets. Do not overwrite them to resolve uncertainty.

## Casa Verde voice and assets

Apply `.agents/skills/casa-verde/SKILL.md` to every customer-facing artifact, including white paper text, infographic cards, captions, alt text, email, and LinkedIn copy. Apply it to authored internal research and deck copy as well. Re-read it at each stage rather than relying on a shortened vocabulary list in a prompt.

- No em-dashes, exclamation marks, banned vocabulary, adjective stacks, or sales hype in authored artifacts. Use the full banned list in the skill.
- Write in a warm, calm, specific voice. Material origins and concrete details carry the story. Keep research language factual and distinguish it from Elena's founder voice.
- Use `Design that breathes.` at most once per finished piece, and once across the entire deck. Sign founder-written emails and notes `Elena`.
- Use the skill's palette and typography for visual work. Document font substitutions if the specified fonts are unavailable.
- Use existing brand assets at their exact paths and inspect them before describing visible details. Do not regenerate brand imagery. For the infographic, use layout and rendering with existing assets rather than new brand image generation.
- Keep competitor screenshots as evidence, not as Casa Verde-authored copy. Do not alter captured wording. When a source contains prohibited wording or punctuation, use a faithful, explicitly labeled paraphrase with a source link in authored text. Never present edited wording as a direct quote. Review screenshot selections for suitability before public use.

## Evidence, missing data, and contradictions

Every substantive competitor field requires a source URL, access date, and evidence status. Use `observed`, `firm claim`, or `inference` for known material. A published company statement is evidence that the statement was made, not independent proof of its outcome.

Use the literal value `unknown` when a fact cannot be established. Add the attempted URL or source, access date, reason, and next useful check. Reasons include `not disclosed`, `login wall`, `site unavailable`, `insufficient sample`, and `conflicting sources`. Never replace missing information with zero, a guessed price, or a negative finding.

The ideal client persona and market opportunities may be labeled inferences grounded in cited evidence. This exception does not permit invented budgets, demographics, suppliers, certifications, environmental results, or client histories. The skill's allowance for plausible draft project copy does not apply to factual competitive research.

Keep conflicting source statements visible, with dates and scope. Prefer current, specific primary evidence for the relevant service, but do not silently resolve contradictions. For missing local inputs, record the missing path and continue only work that does not depend on it. Request clarification when the missing fact would change scope or a material conclusion.

An inaccessible Instagram account is an access limitation, not evidence of inactivity. Missing public sustainability proof is a communication gap, not proof of poor environmental practice. Treat Casa Verde's brand bible as stated brand intent, not an independently verified performance record.

## Verification before delivery

- Confirm all required stage outputs exist at their canonical paths and all ten schema dimensions survive into comparison and downstream synthesis.
- Check authored text, including captions, charts, notes, and alt text, against the complete skill vocabulary list and punctuation rules. Respect the signature phrase limit for each piece.
- Check that facts and figures have traceable sources, that inferences are labeled, and that unknown values retain their reasons.
- Render and inspect visual artifacts in prompts 3 and 4. Check readable labels, citations, screenshot fit, page or slide boundaries, and font substitutions.
- Finish each stage with a short report listing changed files, the main artifact path, and material evidence or access gaps. Do not claim checks that were not run.

## How the five firms get picked

You do not start with a list. In Phase 2a of prompt 2, Codex discovers 5 Austin-area firms that match Casa Verde's competitive set (sustainable residential interior design, honest materials, comparable budget range, Austin or nearby Hill Country). Codex writes the shortlist with rationale to `output/competitor_shortlist.md`. Then Phase 2b does the deep dive on those 5. Some sites or Instagram pages may be offline, slow, or private. Document what you cannot reach rather than guessing.

## If something breaks

- A firm site is offline: Codex captures the failure, notes it, continues with what is available
- Instagram is private: capture the wall, note it, do not log in
- Screenshot tool returns blank: retry once, then move on with a note
- Branded outputs sound generic: re-read the casa-verde skill at `.agents/skills/casa-verde/SKILL.md` and ask Codex to grep the avoid-word list against the deck or PDF, then rewrite any hits
- Brand colors look like generic gray: regenerate using the exact hex codes from `brand/casa_verde_brand_bible.md`
- "Design that breathes." appears in every section: the skill says once per piece. Tell Codex to grep and remove duplicates