"""
Tests for Indirect Treatment Comparison (Bucher Method) HTML tool.
Uses Selenium to test the browser-based application.

20 tests covering:
- Bucher method core algorithm
- SE from CI conversion
- DerSimonian-Laird pooling
- Normal CDF / quantile functions
- Example loading
- Multi-comparison
- Coherence test
- Export functionality
- UI interactions (tabs, dark mode)
- Edge cases
"""

import sys
import io
import os
import json
import math
import time
import unittest

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


def get_driver():
    """Create Chrome driver in headless mode."""
    opts = Options()
    opts.add_argument('--headless=new')
    opts.add_argument('--no-sandbox')
    opts.add_argument('--disable-dev-shm-usage')
    opts.add_argument('--window-size=1280,900')
    opts.set_capability('goog:loggingPrefs', {'browser': 'ALL'})
    return webdriver.Chrome(options=opts)


FILE_URL = 'file:///' + os.path.abspath(
    os.path.join(os.path.dirname(__file__), 'indirect-comparison.html')
).replace('\\', '/')


class TestIndirectComparison(unittest.TestCase):
    """Test suite for ITC Bucher method tool."""

    @classmethod
    def setUpClass(cls):
        cls.driver = get_driver()
        cls.driver.get(FILE_URL)
        time.sleep(1)  # let DOM settle

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def js(self, script):
        """Execute JavaScript and return result."""
        return self.driver.execute_script('return ' + script)

    def reload(self):
        """Reload page."""
        self.driver.get(FILE_URL)
        time.sleep(0.5)

    # ================================================================
    # Test 1: Bucher method - basic computation
    # ================================================================
    def test_01_bucher_basic(self):
        """Bucher: theta_BC = theta_AC - theta_AB, SE = sqrt(SE_AB^2 + SE_AC^2)"""
        r = self.js("ITC._bucherMethod(0.3, 0.1, 0.5, 0.15)")
        # theta_BC = 0.5 - 0.3 = 0.2
        self.assertAlmostEqual(r['effect'], 0.2, places=10)
        # SE = sqrt(0.01 + 0.0225) = sqrt(0.0325) = 0.18028...
        expected_se = math.sqrt(0.01 + 0.0225)
        self.assertAlmostEqual(r['se'], expected_se, places=6)
        # z = 0.2 / 0.18028... = 1.1094...
        self.assertAlmostEqual(r['z'], 0.2 / expected_se, places=4)

    # ================================================================
    # Test 2: Bucher method - symmetric around zero
    # ================================================================
    def test_02_bucher_symmetric(self):
        """When AB == AC, indirect estimate should be 0."""
        r = self.js("ITC._bucherMethod(0.5, 0.1, 0.5, 0.1)")
        self.assertAlmostEqual(r['effect'], 0.0, places=10)
        self.assertAlmostEqual(r['p'], 1.0, places=2)

    # ================================================================
    # Test 3: Bucher method - negative effects
    # ================================================================
    def test_03_bucher_negative(self):
        """Negative effects handled correctly."""
        r = self.js("ITC._bucherMethod(-0.261, 0.05, -0.386, 0.08)")
        # theta_BC = -0.386 - (-0.261) = -0.125
        self.assertAlmostEqual(r['effect'], -0.125, places=6)
        expected_se = math.sqrt(0.05**2 + 0.08**2)
        self.assertAlmostEqual(r['se'], expected_se, places=6)

    # ================================================================
    # Test 4: CI computation
    # ================================================================
    def test_04_ci_bounds(self):
        """95% CI = effect +/- 1.96 * SE."""
        r = self.js("ITC._bucherMethod(0.0, 0.1, 0.4, 0.1)")
        # effect = 0.4, SE = sqrt(0.02) = 0.14142...
        se = math.sqrt(0.02)
        self.assertAlmostEqual(r['ciLow'], 0.4 - 1.959964 * se, places=3)
        self.assertAlmostEqual(r['ciHigh'], 0.4 + 1.959964 * se, places=3)

    # ================================================================
    # Test 5: p-value for significant result
    # ================================================================
    def test_05_pvalue_significant(self):
        """Large effect / small SE should give p < 0.05."""
        r = self.js("ITC._bucherMethod(0.0, 0.05, 0.5, 0.05)")
        # effect = 0.5, SE = sqrt(0.005) = 0.0707, z = 7.07 -> p ~ 0
        self.assertLess(r['p'], 0.001)

    # ================================================================
    # Test 6: p-value for non-significant result
    # ================================================================
    def test_06_pvalue_nonsignificant(self):
        """Small effect / large SE should give p > 0.05."""
        r = self.js("ITC._bucherMethod(0.0, 0.5, 0.05, 0.5)")
        # effect = 0.05, SE = sqrt(0.5) = 0.707, z = 0.07 -> p ~ 0.94
        self.assertGreater(r['p'], 0.05)

    # ================================================================
    # Test 7: Normal CDF at known values
    # ================================================================
    def test_07_normalCDF(self):
        """normalCDF at 0 = 0.5, at 1.96 ~ 0.975."""
        cdf0 = self.js("ITC._normalCDF(0)")
        self.assertAlmostEqual(cdf0, 0.5, places=6)
        cdf196 = self.js("ITC._normalCDF(1.96)")
        self.assertAlmostEqual(cdf196, 0.975, places=3)
        # Symmetry
        cdf_neg = self.js("ITC._normalCDF(-1.96)")
        self.assertAlmostEqual(cdf_neg, 0.025, places=3)

    # ================================================================
    # Test 8: SE from CI
    # ================================================================
    def test_08_se_from_ci(self):
        """SE = (upper - lower) / (2 * 1.96)."""
        se = self.js("ITC._seFromCI(0.1, 0.5)")
        expected = (0.5 - 0.1) / (2 * 1.959964)
        self.assertAlmostEqual(se, expected, places=6)

    # ================================================================
    # Test 9: DL pooling - single study
    # ================================================================
    def test_09_dl_single_study(self):
        """Pooling a single study returns it unchanged."""
        r = self.js("ITC._poolDL([{effect: 0.3, se: 0.1}])")
        self.assertAlmostEqual(r['effect'], 0.3, places=10)
        self.assertAlmostEqual(r['se'], 0.1, places=10)
        self.assertEqual(r['k'], 1)
        self.assertAlmostEqual(r['tau2'], 0.0, places=10)

    # ================================================================
    # Test 10: DL pooling - two homogeneous studies
    # ================================================================
    def test_10_dl_homogeneous(self):
        """Two identical studies: tau2 should be 0, pooled = same effect."""
        r = self.js("ITC._poolDL([{effect: 0.5, se: 0.1}, {effect: 0.5, se: 0.1}])")
        self.assertAlmostEqual(r['effect'], 0.5, places=6)
        self.assertAlmostEqual(r['tau2'], 0.0, places=6)
        # SE should be smaller than individual
        self.assertLess(r['se'], 0.1)
        self.assertEqual(r['k'], 2)

    # ================================================================
    # Test 11: DL pooling - heterogeneous studies
    # ================================================================
    def test_11_dl_heterogeneous(self):
        """Three studies with spread: tau2 > 0, I2 > 0."""
        r = self.js("ITC._poolDL([{effect: 0.1, se: 0.05}, {effect: 0.5, se: 0.05}, {effect: 0.9, se: 0.05}])")
        self.assertGreater(r['tau2'], 0)
        self.assertGreater(r['I2'], 0)
        # Pooled effect should be near 0.5 (mean)
        self.assertAlmostEqual(r['effect'], 0.5, places=2)

    # ================================================================
    # Test 12: Coherence test - consistent estimates
    # ================================================================
    def test_12_coherence_consistent(self):
        """When direct == indirect, p should be high (no inconsistency)."""
        r = self.js("ITC._coherenceTest(0.2, 0.1, 0.2, 0.15)")
        self.assertAlmostEqual(r['diff'], 0.0, places=10)
        self.assertAlmostEqual(r['p'], 1.0, places=2)

    # ================================================================
    # Test 13: Coherence test - inconsistent estimates
    # ================================================================
    def test_13_coherence_inconsistent(self):
        """Large difference between direct and indirect: p should be small."""
        r = self.js("ITC._coherenceTest(1.0, 0.05, 0.0, 0.05)")
        # diff = 1.0, SE = sqrt(0.005) = 0.0707, z = 14.1 -> p ~ 0
        self.assertLess(r['p'], 0.001)

    # ================================================================
    # Test 14: Load antiplatelet example and compute
    # ================================================================
    def test_14_example_antiplatelet(self):
        """Load antiplatelet example and verify computation."""
        self.reload()
        self.driver.execute_script("ITC.loadExample('antiplatelet')")
        time.sleep(0.3)

        # Verify fields populated
        ab = self.driver.find_element(By.ID, 'abEffect').get_attribute('value')
        self.assertEqual(ab, '-0.261')

        # Compute
        self.driver.execute_script("ITC.compute()")
        time.sleep(0.5)

        # Check results tab is active
        panel = self.driver.find_element(By.ID, 'panel-results')
        self.assertEqual(panel.get_attribute('aria-hidden'), 'false')

        # Check result content has the indirect estimate
        content = panel.text
        self.assertIn('Indirect Estimate', content)

    # ================================================================
    # Test 15: Load antidepressants example
    # ================================================================
    def test_15_example_antidepressants(self):
        """Load antidepressants example - SMD effect type."""
        self.reload()
        self.driver.execute_script("ITC.loadExample('antidepressants')")
        time.sleep(0.3)

        et = self.driver.find_element(By.ID, 'effectType').get_attribute('value')
        self.assertEqual(et, 'SMD')

        ab = float(self.driver.find_element(By.ID, 'abEffect').get_attribute('value'))
        ac = float(self.driver.find_element(By.ID, 'acEffect').get_attribute('value'))
        # SNRI vs SSRI indirect = 0.35 - 0.31 = 0.04
        self.assertAlmostEqual(ac - ab, 0.04, places=6)

    # ================================================================
    # Test 16: Tab switching via ARIA
    # ================================================================
    def test_16_tab_switching(self):
        """Tab buttons properly set aria-selected and panel visibility."""
        self.reload()
        # Click Results tab
        self.driver.execute_script("document.getElementById('tab-results').click()")
        time.sleep(0.3)

        tab = self.driver.find_element(By.ID, 'tab-results')
        self.assertEqual(tab.get_attribute('aria-selected'), 'true')

        panel = self.driver.find_element(By.ID, 'panel-results')
        self.assertEqual(panel.get_attribute('aria-hidden'), 'false')

        # Input panel should be hidden
        input_panel = self.driver.find_element(By.ID, 'panel-input')
        self.assertEqual(input_panel.get_attribute('aria-hidden'), 'true')

    # ================================================================
    # Test 17: Dark mode toggle
    # ================================================================
    def test_17_dark_mode(self):
        """Dark mode toggle adds class to body."""
        self.reload()
        body_classes = self.driver.find_element(By.TAG_NAME, 'body').get_attribute('class') or ''
        was_dark = 'dark-mode' in body_classes

        self.driver.execute_script("document.getElementById('darkToggle').click()")
        time.sleep(0.3)

        body_classes_after = self.driver.find_element(By.TAG_NAME, 'body').get_attribute('class') or ''
        if was_dark:
            self.assertNotIn('dark-mode', body_classes_after)
        else:
            self.assertIn('dark-mode', body_classes_after)

    # ================================================================
    # Test 18: Multi-comparison with 4 treatments
    # ================================================================
    def test_18_multi_comparison(self):
        """Multi-comparison produces correct number of pairwise comparisons."""
        self.reload()
        # Switch to multi tab first so panel is visible
        self.driver.execute_script("document.getElementById('tab-multi').click()")
        time.sleep(0.3)
        self.driver.execute_script("ITC.loadMultiExample()")
        time.sleep(0.3)
        self.driver.execute_script("ITC.computeMulti()")
        time.sleep(0.5)

        # 4 treatments -> C(4,2) = 6 pairwise comparisons
        content = self.js("document.getElementById('multiResults').innerHTML")
        self.assertIn('League Table', content)
        # Verify 6 rows in last pairwise table
        rows = self.js(
            "document.querySelectorAll('#multiResults .data-table')[2].querySelectorAll('tbody tr').length"
        )
        self.assertEqual(rows, 6)

    # ================================================================
    # Test 19: csvSafe handles special characters
    # ================================================================
    def test_19_csv_safe(self):
        """csvSafe escapes commas, quotes, and formula injections."""
        # Comma
        r1 = self.js("ITC._csvSafe('hello, world')")
        self.assertEqual(r1, '"hello, world"')

        # Quote
        r2 = self.js("ITC._csvSafe('say \"hi\"')")
        self.assertEqual(r2, '"say ""hi"""')

        # Formula injection
        r3 = self.js("ITC._csvSafe('=SUM(A1)')")
        self.assertEqual(r3, "'=SUM(A1)")

        # Normal value
        r4 = self.js("ITC._csvSafe('normal')")
        self.assertEqual(r4, 'normal')

        # Null
        r5 = self.js("ITC._csvSafe(null)")
        self.assertEqual(r5, '')

    # ================================================================
    # Test 20: escapeHtml prevents XSS
    # ================================================================
    def test_20_escapeHtml(self):
        """escapeHtml escapes <, >, &, quotes."""
        r = self.js("ITC._escapeHtml('<script>alert(1)</script>')")
        self.assertNotIn('<script>', r)
        self.assertIn('&lt;', r)

        r2 = self.js("ITC._escapeHtml('a & b')")
        self.assertIn('&amp;', r2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
