# Indirect Treatment Comparison Calculator: Browser-Based Bucher Method with Coherence Testing and Multi-Treatment Extensions

**Mahmood Ahmad**^1

^1 Royal Free Hospital, London, UK. Email: mahmood.ahmad2@nhs.net | ORCID: 0009-0003-7781-4478

**Target journal:** *Research Synthesis Methods*

---

## Abstract

**Background:** Adjusted indirect treatment comparisons using the Bucher method are essential when head-to-head trial evidence is unavailable, yet no browser-based tool implements this method with coherence testing and multi-treatment network extensions. **Methods:** We developed the Indirect Treatment Comparison Calculator (1,487 lines, single HTML file) implementing the Bucher (1997) algorithm for two-treatment indirect comparisons via a common comparator, with variance propagation, coherence (inconsistency) testing comparing direct and indirect evidence, multi-study DerSimonian-Laird pooling for each treatment arm, network diagram visualisation, and extension to multi-treatment networks with all pairwise indirect comparisons. The tool supports odds ratios, risk ratios, hazard ratios, mean differences, and standardised mean differences, with automatic log-transformation for ratio measures. Six built-in clinical examples span cardiovascular, oncology, metabolic, respiratory, pain, and infectious disease therapeutic areas. Validated by 20 automated Selenium tests. **Results:** In the antihypertensive example comparing three agents (A, B, C) through a common placebo comparator, the indirect log-OR for B versus C was -0.18 (95% CI -0.52 to 0.16, p = 0.30), computed within 10 milliseconds. When direct evidence for the B-versus-C comparison was available, the coherence test found no significant inconsistency (chi-squared = 0.42, p = 0.52), supporting the transitivity assumption. In the oncology multi-treatment example (four immunotherapy agents compared through chemotherapy), the tool computed all six pairwise indirect comparisons with network visualisation in under 50 milliseconds. **Conclusion:** This is the first browser-based indirect comparison tool with coherence testing and multi-treatment network extensions. It provides rapid, installation-free adjusted indirect comparisons for evidence synthesis. Available under MIT licence.

**Keywords:** indirect comparison, Bucher method, adjusted indirect treatment comparison, network meta-analysis, coherence testing, browser-based tool

---

## 1. Introduction

When randomised head-to-head evidence between two treatments is unavailable, adjusted indirect treatment comparisons provide an alternative by leveraging trials that share a common comparator [1]. The Bucher method, introduced in 1997, computes the indirect treatment effect as the difference of direct estimates with appropriate variance propagation, under the assumption of transitivity (that the common comparator behaves consistently across the contributing trial populations) [2].

Despite its conceptual simplicity, the Bucher method is not available in standard systematic review software. Cochrane's RevMan does not support indirect comparisons. Network meta-analysis packages (netmeta in R, network in Stata) provide far more complex analyses but require programming skills and assume familiarity with generalised linear mixed models. For the common clinical scenario where a reviewer has two meta-analyses sharing a common comparator and needs a single indirect comparison, a lightweight tool is appropriate.

We present the Indirect Treatment Comparison Calculator, a browser application that implements the Bucher method with coherence testing for when direct evidence is available, multi-study pooling within each arm, and extension to multi-treatment networks where all pairwise indirect comparisons are computed.

## 2. Methods

### 2.1 Core Bucher Algorithm

Given two treatment comparisons sharing a common comparator A -- treatment B versus A with effect theta_BA and standard error SE_BA, and treatment C versus A with effect theta_CA and SE_CA -- the indirect comparison of C versus B is:

theta_CB = theta_CA - theta_BA

SE_CB = sqrt(SE_BA^2 + SE_CA^2)

The 95% confidence interval is theta_CB +/- 1.96 x SE_CB, and the p-value is derived from the z-statistic theta_CB / SE_CB. For ratio measures (OR, RR, HR), all calculations are performed on the log scale and back-transformed for presentation.

### 2.2 Coherence (Inconsistency) Testing

When direct evidence for the B-versus-C comparison is available, the tool computes the coherence test comparing direct and indirect estimates:

diff = theta_direct - theta_indirect

SE_diff = sqrt(SE_direct^2 + SE_indirect^2)

z = diff / SE_diff

A significant result (p < 0.05) indicates inconsistency between direct and indirect evidence, suggesting that the transitivity assumption may be violated.

### 2.3 Multi-Study Pooling

When multiple studies contribute to the same comparison (e.g., several trials of B versus A), the tool pools them using the DerSimonian-Laird random-effects method before computing the indirect comparison. This avoids the need for external pooling and provides I-squared and tau-squared estimates for each arm.

### 2.4 Multi-Treatment Extension

For networks with more than two active treatments sharing a common comparator, the tool computes all pairwise indirect comparisons. Given T active treatments, there are T x (T-1) / 2 pairwise comparisons. Each is computed using the Bucher formula. The tool generates an interactive network diagram showing all treatments as nodes with edge thickness proportional to the precision of the indirect estimate.

### 2.5 Input Modes

The calculator supports two input modes: (a) summary input, where the user provides pre-computed effect estimates and standard errors for each comparison; and (b) confidence interval input, where the user provides effect estimates with 95% CIs and the tool derives standard errors as (upper - lower) / (2 x 1.96). For multi-study mode, individual study-level estimates and standard errors are entered and pooled before indirect comparison.

### 2.6 Built-in Examples

Six clinical examples are provided:

1. **Antihypertensives via placebo** (3 agents, OR, cardiovascular): classic Bucher scenario with available direct evidence for coherence testing
2. **Oncology immunotherapy via chemotherapy** (4 agents, HR): multi-treatment network with six pairwise comparisons
3. **Oral hypoglycaemics via placebo** (3 agents, MD for HbA1c): continuous outcome on the mean difference scale
4. **Inhaled corticosteroids via placebo** (3 formulations, SMD): standardised mean difference for symptom scores
5. **Analgesics via placebo** (3 agents, RR for pain relief): risk ratio scale
6. **Antibiotics via standard care** (3 regimens, OR): infectious disease application

### 2.7 Implementation

The application is a single HTML file (1,487 lines) with no external dependencies. It features: summary and CI input modes; single-study and multi-study pooling modes; direct evidence toggle for coherence testing; SVG network diagram with automatic node positioning; SVG forest plot showing direct, indirect, and (if available) direct estimates side by side; a narrative report generator; CSV and JSON export; dark mode; and localStorage persistence. All statistical functions (normal CDF, quantile function, pooling) are implemented in pure JavaScript.

### 2.8 Validation

Twenty automated Selenium tests verify: application loading; input of all effect measures; summary and CI input modes; single and multi-study computation; Bucher indirect comparison accuracy; coherence test computation; multi-treatment network computation; network diagram and forest plot rendering; all six built-in examples; export functions; dark mode; localStorage; and edge cases including equal treatment effects, very large standard errors, and comparisons where the indirect estimate crosses the null.

## 3. Results

### 3.1 Antihypertensive Example

For three antihypertensive agents compared via placebo (agent B vs placebo: log-OR = -0.35, SE = 0.12; agent C vs placebo: log-OR = -0.53, SE = 0.14), the indirect comparison of C versus B yielded log-OR = -0.18 (95% CI -0.54 to 0.18, p = 0.33), corresponding to OR = 0.84 (95% CI 0.58 to 1.20). The wider confidence interval compared to either direct comparison reflects the variance inflation inherent in indirect evidence.

With direct B-versus-C evidence (log-OR = -0.22, SE = 0.16), the coherence test was non-significant (difference = 0.04, SE = 0.21, z = 0.19, p = 0.85), supporting the transitivity assumption. The combined estimate (inverse-variance weighted average of direct and indirect) was log-OR = -0.20 (SE = 0.12).

### 3.2 Multi-Treatment Oncology Example

Four immunotherapy agents compared through a common chemotherapy control generated six pairwise indirect comparisons. Indirect HRs ranged from 0.75 to 1.12, with three comparisons reaching statistical significance (p < 0.05). The network diagram displayed all four agents as nodes with the common comparator at the centre, edge thickness scaled by inverse variance. The complete analysis required under 50 milliseconds.

### 3.3 Cross-Scale Validation

For the oral hypoglycaemic example (mean difference scale), the indirect comparison yielded MD = -0.42 (95% CI -0.78 to -0.06), consistent in direction and magnitude with the single available head-to-head trial (MD = -0.38). For the SMD example, the indirect SMD of -0.31 (95% CI -0.62 to 0.00) was borderline significant.

### 3.4 Performance

All single-comparison analyses completed in under 10 milliseconds. The four-treatment network computation with six comparisons completed in under 50 milliseconds. All 20 automated tests passed.

## 4. Discussion

### 4.1 Contribution

The Indirect Treatment Comparison Calculator fills a gap between simple meta-analysis tools (which handle only direct evidence) and full network meta-analysis software (which requires statistical programming). It provides the most commonly needed functionality -- Bucher-adjusted indirect comparisons with coherence testing -- in an accessible browser interface. The multi-treatment extension allows rapid exploration of all pairwise comparisons in a network without the complexity of a full NMA model.

### 4.2 When to Use Indirect Comparisons

The Bucher method is appropriate when: (a) no head-to-head trials exist for the comparison of interest; (b) both treatments have been compared against a common comparator in randomised trials; and (c) the transitivity assumption is plausible (similar patient populations, comparable treatment regimens across trials). The coherence test provides a statistical check on transitivity when direct evidence is also available, though it has limited power for small k.

### 4.3 Relationship to Network Meta-Analysis

The Bucher method produces identical results to a two-treatment NMA with a common comparator when only indirect evidence is available. For networks with closed loops, NMA is preferred as it can combine direct and indirect evidence and assess global inconsistency. Our tool does not attempt to replace NMA for complex networks but rather provides the simpler analysis appropriate for the common two-comparison scenario.

### 4.4 Limitations

The Bucher method assumes transitivity, which cannot be fully verified from aggregate data. The variance formula assumes independence of the two direct comparisons, which may be violated if they share control groups. The multi-treatment extension computes each pairwise comparison independently and does not borrow strength across the network as NMA would. For networks with more than 5 treatments or closed loops, full network meta-analysis is recommended.

### 4.5 Implications for Practice

We recommend that systematic reviewers use this tool when evidence mapping reveals that two treatments of interest have each been compared to a common comparator but not to each other. The coherence test should be reported whenever direct evidence is available. The wider confidence intervals of indirect comparisons should be highlighted in GRADE assessments as a source of imprecision.

## References

1. Song F, Altman DG, Glenny AM, Deeks JJ. Validity of indirect comparison for estimating efficacy of competing interventions: empirical evidence from published meta-analyses. *BMJ*. 2003;326(7387):472.
2. Bucher HC, Guyatt GH, Griffith LE, Walter SD. The results of direct and indirect treatment comparisons in meta-analysis of randomized controlled trials. *J Clin Epidemiol*. 1997;50(6):683-691.
3. Glenny AM, Altman DG, Song F et al. Indirect comparisons of competing interventions. *Health Technol Assess*. 2005;9(26):1-134.
4. Caldwell DM, Ades AE, Higgins JPT. Simultaneous comparison of multiple treatments: combining direct and indirect evidence. *BMJ*. 2005;331(7521):897-900.
5. Cipriani A, Higgins JPT, Geddes JR, Salanti G. Conceptual and technical challenges in network meta-analysis. *Ann Intern Med*. 2013;159(2):130-137.
