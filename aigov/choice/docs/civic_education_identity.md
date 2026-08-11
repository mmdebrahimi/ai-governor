# Civic Education & Shared Martian Identity

Family `mars-gov-civic-education`. Goal — *avoid Earth-style divisions* — pursued via **thin shared civic
core + thick pluralism**, NOT an imposed single value-set. Code: `governance/civic_education.py`.

## The reframe (load-bearing)
"Instill one set of values" is structurally how you manufacture the worst division — a forced monoculture
creates an oppressed dissenting minority (a hidden fault line). The honest target is **"Martian" as a
*chosen civic* identity** (civic-nationalism analogue), not an imposed creed. **Thin unity, thick diversity.**

## Why Earth divides (target causes)
Material scarcity (zero-sum competition); evolved in-group/out-group tribalism; inherited grievance;
ascriptive markers (ethnicity/religion/nation); inequality/status hierarchy; information silos.

## The Mars reset — opportunity vs. risk
- **Opportunity:** no inherited borders; a single founding moment; a **built-in superordinate goal** — the
  environment is a common enemy (Robbers Cave / contact theory: shared survival threat unifies). Foreground
  **"we vs the planet,"** never "we vs them."
- **Risks:** founder-effect ideology (first ~100 imprint values on all who follow); **company-town capture**
  (single employer = economic coercion = value coercion → owner-vs-worker, the likeliest Mars division);
  "Little Earths" (imported nationalisms reconstitute); and **the unity project itself becoming the oppressor**.

## Evidence-based levers (build) vs. backfires (avoid)
| Build | Backfire |
|---|---|
| Foreground the superordinate survival goal | "we vs Earth/them" — a new enemy |
| Cross-cutting ties (mix crews/housing across origins) | Segregated origin enclaves |
| Thin civic core: common language, shared FACTS, the governance system, a pluralistically-authored founding story | Single-narrator curriculum → founder/corporate capture |
| Civic ritual + Mars-native symbols (sols, colony-milestone holidays) | Erasing origin cultures → resentment |
| Teach HOW to disagree (dissent as civic virtue) | Teach WHAT to believe (dissent as deviance) |

## The structural insight (reuse)
A curriculum that "instills values" **is agenda-setting at the identity level** — structurally identical to
the AI advisor curating a policy menu. So the **same anti-capture primitives** apply:

| Governance safeguard (built) | Education analogue (this family) |
|---|---|
| option-diversity predicate | curriculum spans multiple value-traditions (`pluralism_index`, `elective_traditions`) |
| exogenous (independent) steering audit | **curriculum-capture audit** (`capture_detected`) — one source owning the CORE, checked INDEPENDENTLY of cohesion so high cohesion can't mask it |
| "none-of-these" / dissent-preserved | `dissent_allowed` — reject the civic creed without penalty |
| resupplier-veto (connection-model) | **employer-veto** over education = company-town capture |

## The model (`governance/civic_education.py`)
- `CivicCurriculum(core_modules, elective_traditions, dissent_allowed, cross_cutting)`.
- `cohesion_index` (core present + cross-cutting), `pluralism_index` (elective breadth × dissent, penalized
  by an over-thick mandated core), `capture_detected` (core source-concentration > 50%).
- `classify` → **HEALTHY** / **FRAGMENTATION** (cohesion < 0.6 — *Little Earths*) / **MONOCULTURE**
  (capture, low pluralism, or no dissent — *Company Town*). Capture is checked FIRST (insidious, cohesion-masked).
- `division_risk(curr, scarcity)` — structural risk amplified by scarcity (couples to the resource/connection
  families: the import-dependent era is the highest-division-risk window).

## Validated behaviour (Stage-A model)
A thin-core/wide-elective/dissent/cross-cutting curriculum scores HEALTHY (risk ~0.06); a founder-captured
core scores MONOCULTURE **even at cohesion 0.95** (risk ~0.48); a no-core curriculum scores FRAGMENTATION
(risk ~0.57 under scarcity). Both failure modes are penalized; capture cannot hide behind high cohesion.

## Honest boundaries
Stage-A *model* only — the indices are designed proxies, not measured. The cohesion/pluralism/risk numbers
are parameter choices (not empirical); real validation needs Stage-B human study (do these proxies track
actual identity formation?). The model makes the *design tensions* explicit and checkable — it does not
prove a curriculum works on real humans.

## Deferred (phase-2)
Couple `division_risk(scarcity=...)` to the connection-model's import-dependent era; a curriculum
optimizer that searches the thin-core/wide-elective space; human-study instruments (Stage-B); the
founding-story authorship process (who writes it, contestably).
