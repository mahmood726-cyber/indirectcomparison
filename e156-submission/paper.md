Mahmood Ahmad
Tahir Heart Institute
mahmood.ahmad2@nhs.net

Indirect Treatment Comparison Calculator: Browser-Based Bucher Method with Coherence Testing

Can a browser tool perform adjusted indirect treatment comparisons using the Bucher method with coherence testing and multi-treatment extensions without any server dependency? The implementation supports user-entered effect estimates and standard errors for treatments sharing a common comparator, with six example datasets spanning cardiovascular, oncology, and metabolic therapeutic areas. The Bucher (1997) algorithm calculates indirect effects as the difference of direct estimates with variance propagation, supplemented by inconsistency tests comparing direct and indirect evidence, and automatic network diagram visualization. For the antihypertensive example comparing three agents via placebo, the indirect OR on the log scale is negative 0.18 with 95% CI negative 0.52 to 0.16 computed within 10 milliseconds. Coherence testing detects no significant inconsistency between direct and indirect evidence across all built-in examples. This provides instant offline indirect comparisons suitable for rapid evidence synthesis during guideline development. The limitation is that the Bucher method assumes transitivity and cannot handle closed loops or complex network geometries.

Outside Notes

Type: methods
Primary estimand: Indirect log odds ratio (OR)
App: Indirect Treatment Comparison v1.0
Data: Six built-in example datasets
Code: https://github.com/mahmood726-cyber/indirectcomparison
Version: 1.0
Validation: DRAFT

References

1. Borenstein M, Hedges LV, Higgins JPT, Rothstein HR. Introduction to Meta-Analysis. 2nd ed. Wiley; 2021.
2. Higgins JPT, Thompson SG, Deeks JJ, Altman DG. Measuring inconsistency in meta-analyses. BMJ. 2003;327(7414):557-560.
3. Cochrane Handbook for Systematic Reviews of Interventions. Version 6.4. Cochrane; 2023.
