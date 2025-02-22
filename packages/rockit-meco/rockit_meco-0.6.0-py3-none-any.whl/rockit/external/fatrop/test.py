from pylab import *
import unittest

from rockit import Ocp, DirectMethod, MultipleShooting, FreeTime, Stage, external_method
import numpy as np
from casadi import kron, DM
import casadi as ca
from rockit.casadi_helpers import AutoBrancher

class FatropTests(unittest.TestCase):
    def test_hello_world(self):

        ocp = Ocp(t0=0, T=10)

        x1 = ocp.state()
        x2 = ocp.state()

        u = ocp.control()


        e = 1 - x1**2

        ocp.set_der(x1, x2)
        ocp.set_der(x2,  e * x2 - x1 + u)

        ocp.add_objective(ocp.sum(x1**2 + x2**2 + u**2))
        ocp.add_objective(ocp.at_tf(x2**2))

        ocp.subject_to(x2 >= -0.25,include_last=False)
        ocp.subject_to(-1 <= (u <= 1 ))

        p = ocp.parameter()

        ocp.set_value(p, 1)
        # Boundary constraints
        ocp.subject_to(ocp.at_t0(x1) == p)
        ocp.subject_to(ocp.at_t0(x2) == 0)

        
        ocp.solver('ipopt', {"expand":True})
        ocp.method(MultipleShooting(N=20, intg = 'expl_euler'))

        sol = ocp.solve()
        _, x1_sampled_ref_p1 = sol.sample(x1, grid='control')
        _, x2_sampled_ref_p1 = sol.sample(x2, grid='control')
        _, u_sampled_ref_p1 = sol.sample(u, grid='control')

        ocp.set_value(p, 0.5)
        sol = ocp.solve()
        
        _, x1_sampled_ref_p05 = sol.sample(x1, grid='control')
        _, x2_sampled_ref_p05 = sol.sample(x2, grid='control')
        _, u_sampled_ref_p05 = sol.sample(u, grid='control')
        
        for ab in AutoBrancher():
            
            ocp = Ocp(t0=0, T=10)

            x1 = ocp.state()
            x2 = ocp.state()

            u = ocp.control()


            e = 1 - x1**2

            ocp.set_der(x1, x2)
            ocp.set_der(x2,  e * x2 - x1 + u)

            ocp.add_objective(ocp.sum(x1**2 + x2**2 + u**2))
            ocp.add_objective(ocp.at_tf(x2**2))

            ocp.subject_to(x2 >= -0.25,include_last=False)
            ocp.subject_to(-1 <= (u <= 1 ))

            p = ocp.parameter()

            ocp.set_value(p, 1)
            # Boundary constraints
            ocp.subject_to(ocp.at_t0(x1) == p)
            ocp.subject_to(ocp.at_t0(x2) == 0)

            
            method = external_method('fatrop',N=20, intg='expl_euler', mode = ab.branch(['fatropy','interface']))
            ocp.method(method)

            sol = ocp.solve()
            _, x1_sampled = sol.sample(x1, grid='control')
            _, x2_sampled = sol.sample(x2, grid='control')
            _, u_sampled = sol.sample(u, grid='control')
            np.testing.assert_allclose(x1_sampled, x1_sampled_ref_p1, atol=1e-6)
            np.testing.assert_allclose(x2_sampled, x2_sampled_ref_p1, atol=1e-6)
            np.testing.assert_allclose(u_sampled, u_sampled_ref_p1, atol=1e-6)
            

            ocp.set_value(p, 0.5)
            sol = ocp.solve()
            
            _, x1_sampled = sol.sample(x1, grid='control')
            _, x2_sampled = sol.sample(x2, grid='control')
            _, u_sampled = sol.sample(u, grid='control')
            np.testing.assert_allclose(x1_sampled, x1_sampled_ref_p05, atol=1e-6)
            np.testing.assert_allclose(x2_sampled, x2_sampled_ref_p05, atol=1e-6)
            np.testing.assert_allclose(u_sampled, u_sampled_ref_p05, atol=1e-6)
            
            _, x1_sampled = ocp.sample(x1, grid='control')
            _, x2_sampled = ocp.sample(x2, grid='control')
            _, u_sampled = ocp.sample(u, grid='control-')

            print([x1_sampled,x2_sampled,u_sampled,p])
            func = ocp.to_function("test", [x1_sampled,x2_sampled,u_sampled,p], [x1_sampled])
            
            x1_sampled = func(ca.DM.zeros(21,1), ca.DM.zeros(21,1), ca.DM.zeros(20,1),1)
            np.testing.assert_allclose(np.array(x1_sampled).squeeze(), x1_sampled_ref_p1, atol=1e-6)
            x1_sampled = func(ca.DM.zeros(21,1), ca.DM.zeros(21,1), ca.DM.zeros(20,1),0.5)
            np.testing.assert_allclose(np.array(x1_sampled).squeeze(), x1_sampled_ref_p05, atol=1e-6)

if __name__ == '__main__':
    unittest.main()

