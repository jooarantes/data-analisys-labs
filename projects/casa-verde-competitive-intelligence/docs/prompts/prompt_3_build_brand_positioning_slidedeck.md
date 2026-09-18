# Prompt 3: Build the Branded Internal Positioning Deck

**Important: Try GPT-5.5 High Model and ensure that @presentation skill is enabled and called at the start of the prompt** 

Copy and paste this into Codex after Prompt 2 is complete:

```text
Context: Continue the Casa Verde competitive intelligence project. Prompt 2 produced the shortlist, five filled competitor files, screenshots, and the comparison with positioning map. Five files of research do not equal a positioning story. This prompt forces Codex to apply the casa-verde skill to every line of slide copy, embed the prompt 2 screenshots, and produce an internal deck Elena can walk through with her team on Monday. Use the pptx skill (or python-pptx) for the build. The casa-verde skill at `.agents/skills/casa-verde/SKILL.md` shapes every line.

Instruction: Read the inputs first. Build `output/casa_verde_positioning_deck.pptx` using the pptx skill. Apply the Casa Verde palette (Clay #B27F5C, Olive #6B7A4C, Limestone #E5DFD3, Charcoal #2C2A26, Moss #4A5D3A, Off White #F8F4ED) and the casa-verde skill voice to every slide. Slides should cover: title and one-line thesis; the Austin sustainable design landscape in plain language; the five firms in a grid with one screenshot each; per-firm positioning, materials, and weakness in tight bullets; the positioning map with axes labeled; gaps Casa Verde can own; recommendations for the team; closing sign-off "Design that breathes." (used at most once across the deck). Pull screenshots from `assets/screenshots/websites/` and `assets/screenshots/instagram/` rather than regenerating them. Write `output/deck_summary.md` with slide titles and the key takeaway per slide. Before saving, grep the deck text for em-dashes, exclamation marks, and the banned vocabulary in the casa-verde skill (luxury, premium, elevated, curated, bespoke, transform, stunning, gorgeous, wow factor, dream home). Rewrite any hits.

Input:
- `output/research_framework.md`
- `output/competitor_shortlist.md`
- `output/competitors/<slug>.md` (all five)
- `output/comparison.md`
- `assets/screenshots/websites/` and `assets/screenshots/instagram/`
- `brand/casa_verde_brand_bible.md`
- `.agents/skills/casa-verde/SKILL.md`

Output:
- `output/casa_verde_positioning_deck.pptx` with embedded screenshots and the positioning map
- `output/deck_summary.md` listing slide titles and key takeaways
- A short report listing changed files and any banned-word hits that were rewritten
```
