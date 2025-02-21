from rockit import *
      
mode = "nominal"

ocp = Ocp(T=1.0)

x      = ocp.state()
v      = ocp.state()

F       = ocp.control()

ocp.set_der(x, v)
ocp.set_der(v, F)

ocp.add_objective(ocp.sum(v**2))
ocp.add_objective(5*ocp.at_tf(v)**2)

ocp.subject_to(ocp.at_t0(x)==0.0)
ocp.subject_to(ocp.at_t0(v)==0.0)

constraints = []


constr_type = "nonlinear"
if constr_type=="simple":
    constraints.append((lambda e: F <= 15+e,True,{})) # simple
    constraints.append((lambda e: v <= 7+e,True,dict(include_first=False,include_last=False)))  # include_first=True induces failure
    constraints.append((lambda e: ocp.at_tf(x) + e>=5.0,False,{})) # boundary constraint on state
elif constr_type=="linear":
    constraints.append((lambda e: F <= 15+e,True,{})) # simple
    constraints.append((lambda e: v+0.01*x <= 7+e,True,dict(include_first=True,include_last=False)))  # include_first=True induces failure
    constraints.append((lambda e: ocp.at_tf(x+0.01*v) + e>=5.0,False,{})) # boundary constraint on state
elif constr_type=="nonlinear":
    constraints.append((lambda e: F <= 15+e,True,{})) # simple
    constraints.append((lambda e: v+0.01*x**2 <= 7+e,True,dict(include_first=False,include_last=False)))  # include_first=True induces failure
    constraints.append((lambda e: ocp.at_tf(x+0.01*v**2) + e>=5.0,False,{}))



if mode=="nominal":
    for c,_,kwargs in constraints:
        ocp.subject_to(c(0),**kwargs)
elif mode=="perturbed":
    k = 0
    for i,(c,_,kwargs) in enumerate(constraints):
        ocp.subject_to(c(0.1 if i==k else 0),**kwargs)
elif mode=="soft":
    k = 0
    power = 1 # 1-norm or 2-norm?
    for i,(c,signal,kwargs) in enumerate(constraints):
        if i!=k:
            ocp.subject_to(c(0),**kwargs)
    else:
        slack = ocp.variable(grid='control' if signal else '')
        ocp.subject_to(slack>=0)
        ocp.subject_to(c(slack),**kwargs)
        penalty = 0.3*slack**power
        print("signal",signal, penalty)
        ocp.add_objective(ocp.sum(penalty) if signal else penalty)

ocp.method(MultipleShooting(N=4,intg='rk'))

ocp.solver('ipopt',{"ipopt.tol":1e-10})

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

#raise Exception("")

for method in [external_method('acados',N=4,qp_solver='PARTIAL_CONDENSING_HPIPM',nlp_solver_max_iter=2000,hessian_approx='EXACT',regularize_method = 'CONVEXIFY',integrator_type='ERK',nlp_solver_type='SQP',qp_solver_cond_N=4)]:

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
