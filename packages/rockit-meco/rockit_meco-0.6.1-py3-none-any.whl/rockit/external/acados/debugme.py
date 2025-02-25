from rockit import *
import numpy as np

ocp = Ocp(T=1.0)

x      = ocp.state()
v      = ocp.state()

F       = ocp.control()

ocp.set_der(x, v)
ocp.set_der(v, F)

ocp.add_objective(ocp.sum(v**2))
ocp.add_objective(5*ocp.at_tf(v)**2)

ocp.subject_to(ocp.at_t0(x)==0)
ocp.subject_to(ocp.at_t0(v)==3.03030303)

ocp.subject_to(ocp.at_tf(x)==5.0)
ocp.subject_to(F<=15.0)
ocp.subject_to(v<=7.0,include_first=False,include_last=False)

ocp.method(MultipleShooting(N=4,intg='rk'))

ocp.solver('ipopt',{"ipopt.tol":1e-10})


#ocp.set_initial(x, [-1.46569578e-13,  7.77175578e-01 , 2.27513837e+00 , 4.02513837e+00, 5.00000000e+00])
#ocp.set_initial(v, [1.23370231, 4.98370231, 7.   ,      7.     ,    0.79889307])
#ocp.set_initial(F, [ 1.50000000e+01 , 8.06519075e+00 ,-2.23072479e-10, -2.48044277e+01])

sol = ocp.solve()

signals = [("x",x),("v",v),("F",F)]
values = []#("mayer",mayer)]#[("slack",slack)]

ref = {}
for k, expr in signals:
  ref[k] = sol.sample(expr,grid='control')[1]
for k, expr in values:
  ref[k] = sol.value(expr)

[ref_t,_] = sol.sample(signals[0][1],grid='control')

print(ref)


for method in [external_method('acados',N=4,qp_solver='PARTIAL_CONDENSING_HPIPM',nlp_solver_max_iter=2000,hessian_approx='EXACT',regularize_method = 'CONVEXIFY',integrator_type='ERK',nlp_solver_type='SQP',qp_solver_cond_N=4,tol=1e-8)]:

  ocp.method(method)
  sol = ocp.solve()

  sold = {}
  for k, expr in signals:
    sold[k] = sol.sample(expr,grid='control')[1]
  for k, expr in values:
    sold[k] = sol.value(expr)

  [sol_t,_] = sol.sample(signals[0][1],grid='control')

  tolerance = 1e-5

  for k, expr in signals:
    print(k+"ref",ref[k])
    print(k+"sol",sold[k])
  for k, expr in values:
    print(k+"ref",ref[k])
    print(k+"sol",sold[k])
  print("ref_t",ref_t)
  print("sol_t",sol_t)

  for k, expr in signals:
    np.testing.assert_allclose(sold[k], ref[k], atol=tolerance)
  for k, expr in values:
    np.testing.assert_allclose(sold[k], ref[k], atol=tolerance)
  np.testing.assert_allclose(sol_t, ref_t, atol=tolerance)
