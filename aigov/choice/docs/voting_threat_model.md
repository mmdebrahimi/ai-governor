# Voting Threat Model & Mechanism-Selection Plan (family `mars-gov-voting-verification`)

Gating artifact for the voting-verification family (umbrella `mars-governance`). Written before any
prototype code per the 2026-06-05 brainstorm + review. Electorate **N = 100–500**, isolated colony,
intermittent connectivity, close physical quarters (coercion risk), **no trusted external election
authority**. Phase-1 deliverable = an Earth-tested, evidence-based mechanism *selection*, reversible.

## 1. Construct-validity bridge (Earth rig → Mars claim)
The Earth rig represents **mechanism attack-surface differences** under a documented threat model. It does
**not** represent Mars-specific environment (comms latency beyond "intermittent", radiation/hardware
faults, real colonist social dynamics). Per-channel attack-success-rates are **modeled parameter
estimates**, not field data — they are falsifiability levers. A selection is therefore valid *conditional
on the documented parameters*; transfer to Mars is asserted only for the attack-surface ordering, not for
absolute rates. The narrower real testable question: *"for N=100–500, no external authority, proximity
coercion, which complete mechanism best satisfies tamper-evidence + ballot secrecy + eligibility?"*

## 2. Requirements & adversary classes
Requirements: **tamper-evidence** (no undetected add/alter/drop), **ballot secrecy** (no party — incl.
insiders — links voter→vote), **eligibility** (only eligible colonists, exactly once).
Adversaries: malicious insider/admin with full logs; compromised voter/terminal device; coercer using
observation or receipts; timing/metadata attacker; **colluding faction** (incl. up to k−1 trustees); a
social-graph-aware attacker exploiting small-cell/unanimous results; **the RESUPPLIER-AS-COERCER (added
2026-06-06 from the Earth↔Mars connection analysis)** — during the import-dependent (mid-term "tether")
phase, whoever controls Earth→Mars resupply holds a **survival veto**: withholding a resupply window
coerces governance outcomes regardless of the in-colony voting mechanism. This breaks the "no trusted
external authority" premise *for as long as the colony cannot feed itself*. The veto's reach is quantified
by `governance/connection.py:resupplier_veto_survivable` (False while import-dependent → veto live; True
once self-sufficient → veto void). Mitigation is not cryptographic — it is **self-sufficiency** (closing
the food/O2 loop locally) plus a strategic-reserve buffer that survives ≥1 missed window.

## 3. Eligibility lifecycle & root of trust
Eligibility is a **lifecycle**, not one-time issuance: enrollment → credential activation → replacement
(lost creds) → revocation (death/incapacity/quarantine/role-change) → post-election audit.
**Root of trust = the colony membership/residency/life-support registry** (the authority that already
governs oxygen/habitat access) made **auditable + contestable**: public change-logs, challenge periods,
threshold-approved changes. **The k-of-n trustee board is IN-SCOPE as a potential adversary** (decision,
§7-Q2): honest-majority assumption with an explicit collusion threshold k; any ≤k−1 subset must not be
able to forge eligibility or link votes. Registry tamper-evidence and pre-board-window compromise are
explicit risks (a compromise predating the logging window is unaudited — phase-2 must address bootstrap).

## 4. Casting model
**Decision: supervised private terminals (for E2E) / private paper booths — NOT remote voting.** Remote +
a compromised personal device defeats both secrecy and receipt non-transferability, and E2E crypto does
not fix endpoint compromise. Residual: a supervised terminal/booth reintroduces a physical-observation
channel ("who watches the supervisor") — modeled in §6.

## 5. Candidates (complete systems = eligibility | private casting | public tally verification)
- **paper_rla** — paper private casting + risk-limiting audit + public bulletin board. *Front-runner.*
- **e2e_supervised** — in-person E2E-verifiable (ElectionGuard/Benaloh-style) on supervised terminals.
  *(Spec/package/schema pinning deferred to phase-2 build.)*
- **blockchain — DROPPED as a complete candidate.** Drop criterion: it provides only append-only
  publication; it supplies no eligibility, secrecy, coercion-resistance, or tally correctness by itself.
  It may re-enter ONLY as the bulletin-board *substrate* inside another candidate, never as a standalone
  system. H2 needs only two complete systems.

## 6. Secrecy test battery (social + physical channels, scored by attack-success-rate)
Controllable per-mechanism channels: insider logs, device compromise, coercer receipt, physical
observation, timing. Shared (mechanism-independent) channel: **small-cell/unanimous-bloc inference**, a
function of published tally granularity — mitigation (result aggregation / minimum cell size) is **deferred
to phase-2** and reported, not used as a differentiator. Ground truth comes from a **seeded synthetic
electorate** (`generate_electorate`) with social blocs + correlated preferences, so inference accuracy is
measured against known true ballots.

## 7. Selection decision rule (closes "which failure is worst")
**Hard constraints (eliminate on any failure):** `secrecy_leak ≤ 0.30`, `tamper_detection ≥ 0.99`,
`double_vote_block = 1.0`. **Tiebreak among survivors:** lower secrecy_leak, then higher understandability.
Worst-failure ordering (most→least unacceptable): **vote-choice revealed > ineligible vote allowed >
result not understandable/contestable > eligible vote blocked > turnout revealed.** Secrecy and eligibility
are therefore hard constraints; understandability is a tiebreak; turnout handling is procedural (§8).

### Open authority decisions resolved 2026-06-05 (defaults; ratify or redirect)
- **Q1 understandability** → *deferred-qualitative*: a documented tiebreak constant now (paper 0.90 /
  e2e 0.50), not yet a human-subject instrument. Phase-2 may operationalize (comprehension test / trust
  survey / mock-dispute).
- **Q2 trustee board** → *in-scope adversary*, honest-majority / k-of-n collusion threshold (§3).
- **Q3 MVP closure** → a *selection* (H2 confirmed OR falsified) counts as "mechanism selected"; the
  recorded decision is the deliverable.

## 8. Turnout visibility (decision)
Publish **aggregate turnout + spoiled/invalid counts + reconciliation proofs**; keep **individual
participation private** (public "who voted" enables abstention-coercion). Provide a **private per-voter
"was my ballot accepted" check**.

## 9. Conditions under which paper LOSES (genuine falsification)
The prototype must be able to kill the front-runner. Paper+RLA loses if any hold: RLA is infeasible at
N≈100 with multi-race ballots (audit sample ≈ full hand-count, no efficiency); chain-of-custody is
unauditable without a trusted authority (the Mars constraint bites paper hardest); or physical-observation
leak in close quarters exceeds the secrecy ceiling (raise `physical_observation` past the E2E aggregate and
paper is eliminated too). These are encoded as tunable parameters in `mock_election.py`.

## 10. Per-requirement success metrics
Tamper-detection rate; ballot-secrecy leak (controllable channels) + reported small-cell leak;
double-vote-prevention rate; roll-tamper detection; understandability (deferred-qualitative). A mechanism
is *selected* iff it survives the §7 hard constraints and wins the tiebreak.

## 11. Deferred to phase-2
k-of-n trustee mechanics; full RLA risk-limit math; E2E spec/package/schema pinning; the third (blockchain)
candidate; remote-voting / device-compromise modeling; registry bootstrap-trust; understandability
instrument; small-cell mitigation (result aggregation).
