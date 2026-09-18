# Prompt 1: Setup and Research Framework

Copy and paste this into Codex from the project root:

```text
Context: We are running competitive intelligence for Elena Reyes, founder of Casa Verde Studio in Austin. Casa Verde does sustainable residential interior design with reclaimed wood, native plants, and honest materials. Before Elena does positioning work with her team, she wants a real read on the Austin sustainable interior design landscape. The casa-verde brand skill is pre-installed at `.agents/skills/casa-verde/SKILL.md` and Codex auto-loads it. The framework presented here is the contract for prompts 2-4.

Instruction: Read the inputs first. Then write `AGENTS.md` at the project root as the durable project contract: goal, the four-prompt build, conventions (output paths, casa-verde skill applies to every customer-facing artifact, no em-dashes, no exclamation marks, no banned vocabulary), and how missing data is handled. Then write `output/research_framework.md`. The framework opens with a Competitor Discovery section that defines who counts (sustainable residential interior design, honest materials, comparable budget range, Austin or nearby Hill Country), then expands every dimension from `templates/competitor_research_schema.md` into specific signals Codex will look for in prompt 2: positioning sentence, project types, signature materials, pricing range, geographic focus, sustainability claims, ideal client persona, social cadence, content quality, weakness or gap. Be opinionated. If a dimension feels weak for sustainable interior design, sharpen it before locking the framework.

Input:
- `brand/casa_verde_brand_bible.md`
- `docs/templates/competitor_research_schema.md`
- `.agents/skills/casa-verde/SKILL.md`

Output:
- `AGENTS.md` at the project root
- `docs/reports/research_framework.md` with Competitor Discovery criteria up front and every schema dimension expanded
- A short report listing changed files and the framework path
```
