<!-- audit-trail.md for 2026-09-01-1000-advance-total-tax-and-two-buildings -->

## Batch 1 — total tax (research + edit-local-code)

- Researched Uruguayan rural taxes (contribucion inmobiliaria rural, primaria, patrimonio) and
  Chilean contribuciones (Ley 17.235 art.7, art.7-bis surcharge, H2-2026 exemptions).
- Wrote `D:\land_enterprise_private\total_tax_model.py`. Derived Uruguay's assessed ratio (0.084)
  from the published Durazno benchmark instead of assuming it.
- **First run rejected on inspection** — Chile showed zero income tax for 20 years. Root cause:
  `income_tax_foreign=0.0` on Chile with `holiday_years=3`, so the holiday never expired. Fixed to
  0.30 effective. Answer inverted.
- Second defect: UAE ranked first at USD 0 despite being unable to hold land. Excluded from the
  ranking with the reason printed.
- Sensitivities run: 30-yr horizon, USD 5M holding, USD 80k income. Uruguay wins all (3.8x-5.3x).

## Batch 2 — two buildings (research)

- Uruguay: Ley 18.308 exempts the producer's dwelling; tourist lodging needs Intendencia
  authorisation + MINTUR registration (Decreto 371/2002 art.6 categories). Unit limits are
  DEPARTMENTAL — Colonia allows max 2 units/plot with tourist uses expressly permitted.
- Chile: Art. 55 LGUC for the dwelling; SAG IFC + SEREMI MINVU for tourism equipamiento.
  DL 3.516 subdivision to 0.5 ha exists as a fallback.
- Spain (Andalucia) carried forward as the binding constraint: one dwelling per plot.

## Batch 3 — publish + calibrate

- Memo written; disclaimer relocated under a `## ` heading because ba-beautify's parser drops all
  content before the first one. Converted and VERIFIED (82 paragraphs, 21 tables, 5 content probes).
- Forecast f6 scored MISS (no flip occurred; mechanism falsified). Calibration 0.70 -> 0.58.

## Terminal

Stopped on **authority fork**, not plateau. Two questions are the user's to answer (the coupling
question; earned-vs-passive income) and both gate the next high-value move.
