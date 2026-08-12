# V15 — Persona databases, expert councils, and whether any of it produces independent judgment

> Five research rounds, 2026-08-12. Prompted by a concrete design proposal: build a council of expert
> personas, drawn from an open persona database, backed by several different models, that confers and
> brings recommendations to the principal.
>
> **Verdict up front.** The persona database exists and is enormous. The council design, as usually
> imagined, does not work — but the *specific* variant proposed (different models behind the seats) is
> the one lever with real evidence behind it. The fix is to differentiate on **model, information and
> accountability**, never on personality.

---

## 1. The persona database exists

**[PersonaHub](https://github.com/tencent-ailab/persona-hub)** (Tencent AI Lab, [arXiv 2406.20094](https://arxiv.org/abs/2406.20094)):
**one billion personas**, roughly 13% of the world's population, automatically curated from web text
via Text-to-Persona and Persona-to-Persona. Open on GitHub and
[Hugging Face](https://huggingface.co/datasets/proj-persona/PersonaHub).

| Resource | Adds |
|---|---|
| [OpenCharacter](https://arxiv.org/html/2501.15427v1) | PersonaHub personas expanded to full profiles + dialogues |
| [DeepPersona](https://openreview.net/forum?id=3eN8zaMN8G) | ~1 MB narrative per persona — two orders of magnitude deeper |
| [Persona Generators](https://arxiv.org/html/2602.03545v2) | Evolutionary search over generator code; committing to open-source |
| PersonaCite (CHI EA '26) | Source attribution + explicit knowledge-gap recognition |
| [RoleBench](https://github.com/Neph0s/awesome-llm-role-playing-with-persona) | 100 profiles, 168K dialogues — evaluation only |

**Constraints.** PersonaHub is **research-licensed**; the authors warn that querying a target model at
scale with it risks replicating that model's capabilities. PersonaChat-style sets are shallow
crowd-sourced trait sentences, not professional profiles.

**Where the gap actually is.** Not "a CSV of personas" — that ground is taken at a scale hard to
compete with. The unoccupied niche is **elicited, role-accountable, decision-linked profiles**: who
decides what, what they can see, what they answer for. Nobody has that, and it is much closer to what
this project needs than a persona list.

---

## 2. The finding that breaks the naive council

**Persona prompts change style, tone and formatting. They do not reliably change judgment — and on
knowledge-heavy tasks they degrade it.**

- ["When 'A Helpful Assistant' Is Not Really Helpful"](https://arxiv.org/abs/2311.10054): **162
  personas × 4 model families × 2,410 factual questions** → **no improvement over no persona at all**.
  Which persona helped on a given question was **essentially random** — unpredictable better than chance.
- [Hu & Collier](https://aclanthology.org/2024.acl-long.554/): persona variables account for **under
  10% of the variance** in subjective annotation tasks.
- [Later work](https://arxiv.org/pdf/2603.18507): expert personas **improve alignment** — the answer
  *sounds* more expert — while **damaging factual accuracy**.
- Systematic persona-steering analysis: reasoning-benchmark effects peak around 7B and **attenuate to
  noise by 14B**. Larger models are *less* steerable by persona, not more.

**Consequence for the design.** Fifty personas on one model give fifty voices delivering one model's
opinion. Worse than useless, because the surface variety reads as corroboration.

---

## 3. Model heterogeneity IS the lever — this part of the proposal is right

The user proposed different backbones (Qwen, DeepSeek, GPT, Kimi) behind the seats. The literature
supports this as the single most reliable decorrelation mechanism.

- ["Stop Overvaluing Multi-Agent Debate"](https://www.alphaxiv.org/overview/2502.08788v3): having
  agents draw from a pool of **different** LLMs improved **every** debate framework tested (up to
  **+5.8%** over CoT-average). With **identical** debaters, **all** multi-agent methods
  **underperformed a single agent**.
- **2 diverse agents can match or exceed 16 homogeneous ones** — an information-theoretic result:
  homogeneous agents saturate early because outputs are strongly correlated.
- Error reduction is highest when models come from **different organisations**.

**Different training data beats different prompts, and it is not close.**

---

## 4. But heterogeneity is not free

- Heterogeneous groups still [converge on wrong answers together](https://arxiv.org/html/2509.05396);
  debate sometimes *harms* group performance.
- A negative-results paper: the mixed team **underperformed the best homogeneous member in 6 of 8**
  condition–task pairs; Qwen+Llama on GSM-Hard fell **25.1 pp** below homogeneous Qwen. Capability
  gaps matter — a weak member drags a strong one down.
- **Theoretical ceiling:** homogeneous debate behaves like a martingale over expressed beliefs and
  **provably cannot exceed majority-vote accuracy in expectation**.
- Much of the measured benefit attributed to debate is explained by **voting, not deliberation**.

**Design consequence: baseline against plain heterogeneous voting at matched cost before building any
debate mechanism.** If deliberation does not beat independent votes, the chamber is decoration.

---

## 5. Failure modes specific to a *council*

- LLM agents **struggle to recognise and discard low-quality contributions**, so in group discussion
  **noise propagates rather than dissipating** — the opposite of the human-committee assumption.
- Conformity, sycophancy, authority bias and bandwagon effects are **amplified** in multi-agent
  settings; discussion-level biases layer on top of interaction-level ones.
- **"Minority Truth":** across heterogeneous debates on six benchmarks, roughly **one in four**
  divergent cases had the **minority holding the correct answer**, suppressed by majority voting.

> The literature's own summary: apparent agreement is **social convergence, not epistemic
> convergence**. Consensus is a poor proxy for accuracy.

---

## 6. What actually worked: interviews, not personas

[Park et al. (2024)](https://arxiv.org/pdf/2411.10109) built agents of **1,052 real people**, each
from a **two-hour interview**. Agents reproduced those individuals' survey answers at **85% of the
humans' own two-week self-consistency** — close to ceiling, since people do not fully agree with
themselves.

The decisive contrast:

| Agent specification | Normalized accuracy |
|---|---|
| Demographics only | **74%** |
| Interview-based | **85%** |

**The interview carried the signal; the persona label did not.** This is the same principle as the
decision inventory (`aigov/decisions.py`): elicit from the real person, then compute.

---

## 7. Silicon-sampling validity caveats

Relevant because a persona panel is a silicon sample by another name.

- **Variance compression** — synthetic responses show less variation than human ones; regression
  coefficients sometimes **flip sign** versus real survey estimates.
- **Tail truncation** — [Bisbee et al.] overfit to majority opinion, systematically under-representing
  extremes and minority subgroups.
- **Caricature** — the mirror failure: exaggerating between-group differences.
- **"Potemkin personas"** — one review found generated personas were **86% US-based** despite no
  geographic constraint in the prompt.
- Even [Argyle et al.](https://arxiv.org/abs/2209.06899), who coined the approach, hedged: silicon
  samples do not emulate individual responses, only aggregate patterns where algorithmic fidelity
  holds — and fidelity must be checked per domain.

For a **multi-country** land enterprise, the US-default bias is precisely the wrong one to inherit.

---

## 8. Design consequences

| # | Rule | Source |
|---|---|---|
| 1 | Differentiate seats by **base model**, never by personality | §3 |
| 2 | Differentiate by **what each seat can see** — disagreement about evidence is signal | prior design |
| 3 | Differentiate by **accountability** — score each seat against outcomes | §5 |
| 4 | **Baseline against plain heterogeneous voting** before building deliberation | §4 |
| 5 | **Never treat consensus as confirmation**; log dissent — minority right ~25% of the time | §5 |
| 6 | Use **interviews** wherever the goal is a real person's judgment | §6 |
| 7 | Watch **capability gaps** — a weak seat can drag the panel below its best member | §4 |
| 8 | Personas generate **questions and cases**, never **judgments to trust** | §2 |

**Where personas genuinely earn their place:** synthetic data at scale (PersonaHub's actual purpose,
and it worked — 79.4% in-distribution on generated maths, matching gpt-4-turbo on MATH), coverage
checks ("how would a neighbour / regulator / tenant see this?"), and adversarial input generation.

---

## 9. Honest limits of this memo

- Every result is **benchmark evidence**, not evidence about *our* problems. The design consequences
  are priors to test, not conclusions. Rule 4 exists precisely to test them cheaply.
- A real four-model panel requires **paid API access** — a money action, and therefore a hard gate.
  Nothing here has been run against live models.
- The multi-agent literature is young and moves fast; several cited results are 2025–2026 preprints
  whose replication status is unknown.
