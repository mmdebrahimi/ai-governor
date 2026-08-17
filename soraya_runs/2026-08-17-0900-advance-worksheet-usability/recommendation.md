# Recommendation — 2026-08-17-0900-advance-worksheet-usability

## What is now possible that was not

Before this run there was no way to get your answers back INTO the instrument. The worksheet posed
18 questions and the code could derive from answered decisions, but the step between them was
unspecified — every real session would have ended with answers on paper and an improvised
transcription. That gap is closed.

## Two ways to answer, pick either

**Conversationally.** Say the answers the way you did for E01. I encode them. Nothing changes for
you, and the encoding is now mechanical rather than improvised.

**Offline, in a file.** Generate a blank answers file, fill it in at your own pace:

    python scripts/land_enterprise_inventory.py --answers-template --out <a private path>/answers.toml

Then, whenever you want to see what it derives:

    python scripts/land_enterprise_inventory.py --answers <a private path>/answers.toml

It works partially filled. Three answered decisions give you three verdicts and an honest count of
what is still missing — you do not have to finish before you see anything.

## The privacy decision is now half-made for you

You still have to choose WHERE the file lives, but the code no longer trusts anyone to remember.
`load_answers` refuses to read an answers file from inside this repository and exits 2. It checks
by LOCATION, not by `.gitignore`, because an ignore rule is one `git add -f` away from protecting
nothing.

So the remaining decision is narrow: name a folder outside the repo. Any private location does.

## One thing the live run showed you

I marked E01 as "more than one decision" in a synthetic test, and the instrument refused to give it
any verdict at all — it told me to split it and re-run. That is deliberate. "Whether a jurisdiction
is politically stable" and "whether it is personally safe for family to operate there" are both
real questions and they can have different answers. Expect that refusal on E02 and E15 too; they
are pre-flagged as suspected compound.

## Still parked on you

| | |
|---|---|
| the answers themselves | 1–2 hrs, the only thing that moves the bar |
| where the private file lives | one folder path outside the repo |
| the `--supersede-goal` command | narrows the bar from "recurring" decisions to entry decisions; run from the project root |
| the shared `ba-beautify` parser fix | affects your Bombardier documents too; wider blast radius, your call |
