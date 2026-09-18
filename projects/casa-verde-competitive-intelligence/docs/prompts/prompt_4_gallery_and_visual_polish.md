# Prompt 4: White Paper PDF and Shareable Infographic

Copy and paste this into Codex after Prompt 3 is complete:

```text
Context: Continue the Casa Verde competitive intelligence project. Prompt 3 produced the internal branded positioning deck. This final prompt produces two customer-facing artifacts that share the prompt 2 research and a single brand pass: a 4 to 6 page Casa Verde branded white paper PDF that Elena hands to prospects, and a single-page shareable branded infographic that works as a website lead magnet or Instagram carousel cover. Long-form is where brand voice drift sneaks in, so the casa-verde skill applies to every line. Use HTML/CSS to PDF (or the pdf skill) for the white paper and image generation (or HTML/CSS render to PNG) for the infographic.

Instruction: Read the inputs first. Write `output/austin_sustainable_design_2026.pdf` as a 4 to 6 page Casa Verde branded white paper covering: introduction in Elena's voice, the Austin sustainable design landscape, what honest materials means in 2026, five firm snapshots without naming them as competitors (positioning, materials, gap), where the market is heading, and how Casa Verde sits in that picture. Apply the Casa Verde palette and typography (GT Sectra for headings, Söhne for body, sans fallbacks if missing). Generate `output/austin_sustainable_design_infographic.png` as a single-page shareable visual sized to work both as a website lead magnet and an Instagram carousel cover, using the same palette and one tight headline plus 4 to 6 short cards. Write `output/sharing_blurbs.md` with an Instagram caption, an email subject and body, and a LinkedIn post that point to the white paper. Before saving each artifact, grep the text for em-dashes, exclamation marks, and the casa-verde banned vocabulary (luxury, premium, elevated, curated, bespoke, transform, stunning, gorgeous, wow factor, dream home). Rewrite any hits. Use "Design that breathes." at most once per piece.

Input:
- `output/research_framework.md`
- `output/competitors/<slug>.md` (all five)
- `output/comparison.md`
- `output/casa_verde_positioning_deck.pptx`
- `brand/casa_verde_brand_bible.md`
- `.agents/skills/casa-verde/SKILL.md`

Output:
- `output/austin_sustainable_design_2026.pdf` (4 to 6 page branded white paper)
- `output/austin_sustainable_design_infographic.png` (single-page branded visual)
- `output/sharing_blurbs.md` with Instagram, email, and LinkedIn copy
- A short report listing changed files and any banned-word hits that were rewritten
```
