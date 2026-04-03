## REVIEW CLEAN
## Code Review Audit: IndirectComparison (indirect-comparison.html)
### Date: 2026-04-03
### Summary: 1 P0 FIXED, 1 P1, 4 P2

---

#### P0 -- Critical

- **P0-1** [FIXED] [Accessibility]: Missing skip-nav link. Keyboard-only users had no way to bypass the header and tab bar to reach content.
  - Fix: Added `.sr-only` CSS class and skip-nav `<a>` element targeting `#panel-input` with focus/blur visibility toggle.

#### P1 -- Important

- **P1-1** [Security]: `escapeHtml()` uses `div.textContent`/`div.innerHTML` approach (line 485-488) which escapes `< > &` but NOT `"` or `'`. However, in this codebase, `escapeHtml` is only used in element content contexts (not attribute values), so this is safe in practice. If future code uses it in attributes, it would need to be upgraded to also escape quotes.

#### P2 -- Minor / Enhancement

- **P2-1** [Statistics]: Bucher method formula (line 603-611) is correct: `theta_BC = theta_AC - theta_AB`, `SE_BC = sqrt(SE_AB^2 + SE_AC^2)`. This matches the canonical reference (Bucher et al., J Clin Epidemiol, 1997).

- **P2-2** [Statistics]: DerSimonian-Laird pooling (lines 569-594) is correct. The tau2 = max(0, (Q-(k-1))/C) formula and I2 = max(0, (Q-(k-1))/Q)*100 are standard.

- **P2-3** [Security]: CSV injection guard (line 498) correctly prepends `'` to cells starting with `=+@\t\r`, and correctly excludes `-` (which would corrupt negative medical values). This follows the correct pattern.

- **P2-4** [Accessibility]: Tab bar has proper ARIA: `role="tablist"`, `role="tab"`, `aria-selected`, `aria-controls`, keyboard arrow navigation (lines 623-637). SVG charts have `role="img"` with `aria-label`. Dark mode toggle has `aria-label`.

#### Checklist

- [x] `</html>` closing tag present
- [x] Div balance: 63/63 (excluding JS)
- [x] No literal `</script>` inside script blocks
- [x] Skip-nav link present (FIXED: P0-1)
- [x] Blob URLs revoked after use (line 1158)
- [x] Tab navigation with ARIA (roles, aria-selected, keyboard arrows)
- [x] Bucher method: theta_BC = theta_AC - theta_AB -- correct
- [x] SE_BC = sqrt(SE_AB^2 + SE_AC^2) -- correct
- [x] Coherence test: diff/sqrt(SE_direct^2 + SE_indirect^2) -- correct
- [x] normalCDF: Abramowitz & Stegun (Hart approximation) -- correct
- [x] normalQuantile: Beasley-Springer-Moro algorithm -- correct
- [x] Multi-comparison: all pairwise combinations via nested loops -- correct
- [x] League table negation for symmetric entries (line 1409-1420) -- correct
- [x] CSV injection guard excludes `-` for negative numbers -- correct
