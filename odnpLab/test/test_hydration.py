import sys
sys.path.append('.../odnplab')

import unittest
import numpy as np
import odnpLab
from odnpLab.hydration import HydrationCalculator, HydrationParameter


class TestHydration(unittest.TestCase):
    def setUp(self):
        self.T1p = np.array([2.020153734009,
        2.276836030132750,
        2.3708172489377400,
        2.4428968088189100,
        2.5709096032675700])
        self.T1_powers = np.array([0.000589495934876689,
        0.024242327290569100,
        0.054429505156431400,
        0.0862844940360515,
        0.11617812912435900])
        self.Ep = np.array([0.57794113752189,
        -0.4688718613022250,
        -0.5464528159680670,
        -1.0725090541762200,
        -1.4141203961920700,
        -1.695789643686440,
        -1.771840068080760,
        -1.8420812985152700,
        -1.97571340381877,
        -2.091405209753480,
        -2.1860546327712800,
        -2.280712535872610,
        -2.4709892163826400,
        -2.5184316153191200,
        -2.556110148443770,
        -2.576413132701720,
        -2.675593912859120,
        -2.8153300703866400,
        -2.897475156648710,
        -3.0042154567120800,
        -3.087886507216510])
        self.E_powers = np.array([0.0006454923080882520,
        0.004277023425898170,
        0.004719543572446050,
        0.00909714298712173,
        0.01344187403986090,
        0.01896059941058610,
        0.02101937603827090,
        0.022335737104727900,
        0.026029715703921800,
        0.02917012237740640,
        0.0338523245243911,
        0.03820738749745440,
        0.04733370907740660,
        0.05269608016472140,
        0.053790874615060400,
        0.05697639350179900,
        0.06435487925718170,
        0.07909179437004270,
        0.08958910066880800,
        0.1051813598911370,
        0.11617812912435900])

        hp = HydrationParameter()
        hp.field = 348.5
        hp.spin_C = 125
        hp.T100 = 2.0
        hp.T10 = 1.5
        self.hp = hp
        self.hc = HydrationCalculator(T1=self.T1p, T1_power=self.T1_powers,
                                 E=self.Ep, E_power=self.E_powers,
                                 hp=hp)
    
    def _run_tethered_2ord(self):
        self.hc.hp.smax_model = 'tethered'
        self.hc.hp.t1_interp_method = 'second_order'
        self.hc.run()
        
    def _run_tethered_linear(self):
        self.hc.hp.smax_model = 'tethered'
        self.hc.hp.t1_interp_method = 'linear'
        self.hc.run()
    
    def _run_free_2ord(self):
        self.hc.hp.smax_model = 'free'
        self.hc.hp.t1_interp_method = 'second_order'
        self.hc.run()
        
    def _run_free_linear(self):
        self.hc.hp.smax_model = 'free'
        self.hc.hp.t1_interp_method = 'linear'
        self.hc.run()
        
    def test_interpT1_linear_tethered(self):
        self._run_tethered_linear()
        self.assertAlmostEqual(self.hc.results.interpolated_T1[0], 2.0959, places=4)
        self.assertAlmostEqual(self.hc.results.interpolated_T1[len(self.hc.results.interpolated_T1)-1], 2.5802, places=4)

    def test_interpT1_2ord_tethered(self):
        self._run_tethered_2ord()
        self.assertAlmostEqual(self.hc.results.interpolated_T1[0], 2.0517, places=4)
        self.assertAlmostEqual(self.hc.results.interpolated_T1[len(self.hc.results.interpolated_T1)-1], 2.5383, places=4)
        
    def test_interpT1_linear_free(self):
        self._run_free_linear()
        self.assertAlmostEqual(self.hc.results.interpolated_T1[0], 2.0959, places=4)
        self.assertAlmostEqual(self.hc.results.interpolated_T1[len(self.hc.results.interpolated_T1)-1], 2.5802, places=4)

    def test_interpT1_2ord_free(self):
        self._run_free_2ord()
        self.assertAlmostEqual(self.hc.results.interpolated_T1[0], 2.0517, places=4)
        self.assertAlmostEqual(self.hc.results.interpolated_T1[len(self.hc.results.interpolated_T1)-1], 2.5383, places=4)
    
    #tethered
    def test_2ord_krho(self):
        self._run_2ord_tethered()
        self.assertAlmostEqual(self.hc.results.k_rho, 1333.33, places=2)
    
    def test_2ord_ksigma(self):
        self._run_2ord_tethered()
        self.assertAlmostEqual(self.hc.results.k_sigma, 20.18, places=2)
        self.assertAlmostEqual(self.hc.results.k_sigma_array[0], 2.50, places=2)
        self.assertAlmostEqual(self.hc.results.k_sigma_array[len(self.hc.results.k_sigma_array)-1], 19.57, places=2)
    
    def test_2ord_xi(self):
        self._run_2ord_tethered()
        self.assertAlmostEqual(self.hc.results.coupling_factor, 0.0151, places=4)
    
    def test_2ord_klow(self):
        self._run_2ord_tethered()
        self.assertAlmostEqual(self.hc.results.k_low, 2175.14, places=2)

    def test_2ord_tcorr(self):
        self._run_2ord_tethered()
        self.assertAlmostEqual(self.hc.results.tcorr, 667.63, places=2)

    def test_2ord_Dlocal(self):
        self._run_2ord_tethered()
        self.assertAlmostEqual(self.hc.results.d_local, 2.19e-10, places=12)
        
    def test_linear_krho(self):
        self._run_tethered_linear()
        self.assertAlmostEqual(self.hc.results.k_rho, 1333.33, places=2)
    
    def test_linear_ksigma(self):
        self._run_tethered_linear()
        self.assertAlmostEqual(self.hc.results.k_sigma, 20.48, places=2)
        self.assertAlmostEqual(self.hc.results.k_sigma_array[0], 2.45, places=2)
        self.assertAlmostEqual(self.hc.results.k_sigma_array[len(self.hc.results.k_sigma_array)-1], 19.26, places=2)
    
    def test_linear_xi(self):
        self._run_tethered_linear()
        self.assertAlmostEqual(self.hc.results.coupling_factor, 0.0154, places=4)

    def test_linear_klow(self):
        self._run_tethered_linear()
        self.assertAlmostEqual(self.hc.results.k_low, 2174.44, places=2)

    def test_linear_tcorr(self):
        self._run_tethered_linear()
        self.assertAlmostEqual(self.hc.results.tcorr, 661.67, places=2)

    def test_linear_Dlocal(self):
        self._run_tethered_linear()
        self.assertAlmostEqual(self.hc.results.d_local, 2.21e-10, places=12)
        
    # free
    def test_2ord_krho(self):
        self._run_free_2ord()
        self.assertAlmostEqual(self.hc.results.k_rho, 1333.33, places=2)
    
    def test_2ord_ksigma(self):
        self._run_free_2ord()
        self.assertAlmostEqual(self.hc.results.k_sigma, 57.74, places=2)
        self.assertAlmostEqual(self.hc.results.k_sigma_array[0], 2.50, places=2)
        self.assertAlmostEqual(self.hc.results.k_sigma_array[len(self.hc.results.k_sigma_array)-1], 19.57, places=2)
    
    def test_2ord_xi(self):
        self._run_free_2ord()
        self.assertAlmostEqual(self.hc.results.coupling_factor, 0.0433, places=4)

    def test_2ord_klow(self):
        self._run_free_2ord()
        self.assertAlmostEqual(self.hc.results.k_low, 2087.51, places=2)

    def test_2ord_tcorr(self):
        self._run_free_2ord()
        self.assertAlmostEqual(self.hc.results.tcorr, 340.24, places=2)

    def test_2ord_Dlocal(self):
        self._run_free_2ord()
        self.assertAlmostEqual(self.hc.results.d_local, 4.30e-10, places=12)
        
    def test_linear_krho(self):
        self._run_free_linear()
        self.assertAlmostEqual(self.hc.results.k_rho, 1333.33, places=2)
    
    def test_linear_ksigma(self):
        self._run_free_linear()
        self.assertAlmostEqual(self.hc.results.k_sigma, 58.59, places=2)
        self.assertAlmostEqual(self.hc.results.k_sigma_array[0], 2.45, places=2)
        self.assertAlmostEqual(self.hc.results.k_sigma_array[len(self.hc.results.k_sigma_array)-1], 19.26, places=2)
    
    def test_linear_xi(self):
        self._run_free_linear()
        self.assertAlmostEqual(self.hc.results.coupling_factor, 0.0439, places=4)

    def test_linear_klow(self):
        self._run_free_linear()
        self.assertAlmostEqual(self.hc.results.k_low, 2085.51, places=2)

    def test_linear_tcorr(self):
        self._run_free_linear()
        self.assertAlmostEqual(self.hc.results.tcorr, 336.81, places=2)

    def test_linear_Dlocal(self):
        self._run_free_linear()
        self.assertAlmostEqual(self.hc.results.d_local, 4.34e-10, places=12)

if __name__ == '__main__':
    unittest.main()