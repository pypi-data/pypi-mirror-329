from rockit import *

from numpy import sin, cos
from casadi import vertcat

import sys
sys.exit(0)

ocp = Ocp(T=2.0)

mcart=0.5
m=1
L=2
g=9.81

pos = ocp.state()
theta = ocp.state()
dpos = ocp.state()
dtheta = ocp.state()

F = ocp.control()

ocp.set_der(pos,dpos)
ocp.set_der(theta,dtheta)
ocp.set_der(dpos, (-m*L*sin(theta)*dtheta*dtheta + m*g*cos(theta)*sin(theta)+F)/(mcart + m - m*cos(theta)*cos(theta)))
ocp.set_der(dtheta,(-m*L*cos(theta)*sin(theta)*dtheta*dtheta + F*cos(theta)+(mcart+m)*g*sin(theta))/(L*(mcart + m - m*cos(theta)*cos(theta))))

nx = 4
x = vertcat(pos,theta,dpos,dtheta)

# Parameters
x_current = ocp.parameter(nx)
x_final = ocp.parameter(nx)

# Objectives
ocp.add_objective(ocp.sum(F**2 + 100*pos**2))

# Boundary constraints
ocp.subject_to(ocp.at_t0(x)==x_current)
ocp.subject_to(ocp.at_tf(x)==x_final)

# Path constraints
ocp.subject_to(-2 <= (F <= 2 ))
# In ocp, you typically do not want to enforce state constraints at the initial time
ocp.subject_to(-2 <= (pos <= 2), include_first=False)

# Solver
options = {}
options["qpsol"] = "qrqp"
ocp.solver('sqpmethod',options)

ocp.set_value(x_current, [0.5,0,0,0])
ocp.set_value(x_final, [0,0,0,0])

method = external_method('fatrop',N=50, intg='expl_euler', mode = 'interface')
#method = MultipleShooting(N=50,M=1,intg='rk')
ocp.method(method)

sol = ocp.solve()


print(sol.sample(x,grid='control')[1])

ocp.save("impact")

ocp.export("cart_pendulum",qp_error_on_fail=False)
