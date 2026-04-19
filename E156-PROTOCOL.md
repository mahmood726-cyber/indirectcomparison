# E156 Protocol — `IndirectComparison`

This repository is the source code and dashboard backing an E156 micro-paper on the [E156 Student Board](https://mahmood726-cyber.github.io/e156/students.html).

---

## `[71]` Indirect Treatment Comparison Calculator: Browser-Based Bucher Method with Coherence Testing

**Type:** methods  |  ESTIMAND: Indirect log odds ratio (OR)  
**Data:** Six built-in example datasets

### 156-word body

Can a browser tool perform adjusted indirect treatment comparisons using the Bucher method with coherence testing and multi-treatment extensions without any server dependency? The implementation supports user-entered effect estimates and standard errors for treatments sharing a common comparator, with six example datasets spanning cardiovascular, oncology, and metabolic therapeutic areas. The Bucher (1997) algorithm calculates indirect effects as the difference of direct estimates with variance propagation, supplemented by inconsistency tests comparing direct and indirect evidence, and automatic network diagram visualization. For the antihypertensive example comparing three agents via placebo, the indirect OR on the log scale is negative 0.18 with 95% CI negative 0.52 to 0.16 computed within 10 milliseconds. Coherence testing detects no significant inconsistency between direct and indirect evidence across all built-in examples. This provides instant offline indirect comparisons suitable for rapid evidence synthesis during guideline development. The limitation is that the Bucher method assumes transitivity and cannot handle closed loops or complex network geometries.

### Submission metadata

```
Corresponding author: Mahmood Ahmad <mahmood.ahmad2@nhs.net>
ORCID: 0000-0001-9107-3704
Affiliation: Tahir Heart Institute, Rabwah, Pakistan

Links:
  Code:      https://github.com/mahmood726-cyber/IndirectComparison
  Protocol:  https://github.com/mahmood726-cyber/IndirectComparison/blob/main/E156-PROTOCOL.md
  Dashboard: https://mahmood726-cyber.github.io/indirectcomparison/

References (topic pack: network meta-analysis):
  1. Rücker G. 2012. Network meta-analysis, electrical networks and graph theory. Res Synth Methods. 3(4):312-324. doi:10.1002/jrsm.1058
  2. Lu G, Ades AE. 2006. Assessing evidence inconsistency in mixed treatment comparisons. J Am Stat Assoc. 101(474):447-459. doi:10.1198/016214505000001302

Data availability: No patient-level data used. Analysis derived exclusively
  from publicly available aggregate records. All source identifiers are in
  the protocol document linked above.

Ethics: Not required. Study uses only publicly available aggregate data; no
  human participants; no patient-identifiable information; no individual-
  participant data. No institutional review board approval sought or required
  under standard research-ethics guidelines for secondary methodological
  research on published literature.

Funding: None.

Competing interests: MA serves on the editorial board of Synthēsis (the
  target journal); MA had no role in editorial decisions on this
  manuscript, which was handled by an independent editor of the journal.

Author contributions (CRediT):
  [STUDENT REWRITER, first author] — Writing – original draft, Writing –
    review & editing, Validation.
  [SUPERVISING FACULTY, last/senior author] — Supervision, Validation,
    Writing – review & editing.
  Mahmood Ahmad (middle author, NOT first or last) — Conceptualization,
    Methodology, Software, Data curation, Formal analysis, Resources.

AI disclosure: Computational tooling (including AI-assisted coding via
  Claude Code [Anthropic]) was used to develop analysis scripts and assist
  with data extraction. The final manuscript was human-written, reviewed,
  and approved by the author; the submitted text is not AI-generated. All
  quantitative claims were verified against source data; cross-validation
  was performed where applicable. The author retains full responsibility for
  the final content.

Preprint: Not preprinted.

Reporting checklist: PRISMA 2020 (methods-paper variant — reports on review corpus).

Target journal: ◆ Synthēsis (https://www.synthesis-medicine.org/index.php/journal)
  Section: Methods Note — submit the 156-word E156 body verbatim as the main text.
  The journal caps main text at ≤400 words; E156's 156-word, 7-sentence
  contract sits well inside that ceiling. Do NOT pad to 400 — the
  micro-paper length is the point of the format.

Manuscript license: CC-BY-4.0.
Code license: MIT.

SUBMITTED: [ ]
```


---

_Auto-generated from the workbook by `C:/E156/scripts/create_missing_protocols.py`. If something is wrong, edit `rewrite-workbook.txt` and re-run the script — it will overwrite this file via the GitHub API._