#
#     This file is part of rockit.
#
#     rockit -- Rapid Optimal Control Kit
#     Copyright (C) 2019 MECO, KU Leuven. All rights reserved.
#
#     Rockit is free software; you can redistribute it and/or
#     modify it under the terms of the GNU Lesser General Public
#     License as published by the Free Software Foundation; either
#     version 3 of the License, or (at your option) any later version.
#
#     Rockit is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#     Lesser General Public License for more details.
#
#     You should have received a copy of the GNU Lesser General Public
#     License along with CasADi; if not, write to the Free Software
#     Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
#

"""
A Hello World Example
===================

Some basic example on solving an Optimal Control Problem with rockit.
"""


# Make available sin, cos, etc
from numpy import *
# Import the project
from rockit import *

import casadi as cs

#%%
# Problem specification
# ---------------------

ocp = Ocp(t0=0, T=2)

u0 = ocp.control()
u1 = ocp.control()

x0 = ocp.state()
x1 = ocp.state()
x2 = ocp.state()
x3 = ocp.state()
x4 = ocp.state()
x5 = ocp.state()

x = cs.vertcat(x0,x1,x2,x3,x4,x5)
u = cs.vertcat(u0,u1)

g = 9.81

ocp.set_der(x0, x1)
ocp.set_der(x1, u0)
ocp.set_der(x2, x3)
ocp.set_der(x3, u1)
ocp.set_der(x4, x5)
ocp.set_der(x5, -((g * sin(x4) + cos(x4)*u0 + 2 * x3 * x5) / x2))


xdes = cs.vertcat( 2.0, 0.0, 2.0, 0.0, 0.0, 0.0 )
udes = cs.vertcat(0.0, 0.0 )
umax = cs.vertcat(2.0, 2.0 )
umin = cs.vertcat(-2.0, -2.0 )




q = cs.vertcat(1,2,2,1,1,4)
r = cs.vertcat(0.05,0.05)

quad = lambda w, b : cs.dot(w,b**2)

ocp.add_objective(ocp.integral(quad(q,x-xdes)))
ocp.add_objective(ocp.integral(quad(r,u-udes)))


p = cs.vertcat(0.2,1.25,0.3)

x_pos = x0+sin(x4)*x2

ocp.subject_to(cos(x4)*x2-p[0]*x_pos**2-p[1]<= 0)
ocp.subject_to(-p[2]<= (x5 <= p[2]))

ocp.subject_to(umin <= (u <= umax))


x0 = cs.vertcat(-2.0, 0.0, 2.0, 0.0, 0.0, 0.0 )
u0 = cs.vertcat(0.0, 0.0 )

ocp.subject_to(ocp.at_t0(x) == x0)

#%%
# Solving the problem
# -------------------

# Pick an NLP solver backend
#  (CasADi `nlpsol` plugin):
ocp.solver('ipopt')

# Pick a solution method
grampc_options = {}
grampc_options["LineSearchType"] = "explicit2"
grampc_options["ConvergenceCheck"] = "off"
grampc_options["ConvergenceGradientRelTol"] = 1.00e-06
grampc_options["MaxGradIter"] = 2
grampc_options["MaxMultIter"] = 1
grampc_options["TerminalCost"] = "off"
grampc_options["ConstraintsAbsTol"] = [1e-4,1e-3,1e-3]

method = external_method('grampc',N=19,verbose=True,grampc_options=grampc_options)
#method = MultipleShooting(N=20)
ocp.method(method)
#ocp.method(MultipleShooting(N=50))

# Solve
try:
    sol = ocp.solve()
except Exception as e:
    print(str(e))
    sol = ocp.non_converged_solution

#%%
# Post-processing
# ---------------

from pylab import *

# Sample a state/control or expression thereof on a grid
tsa, x1a = sol.sample(x1, grid='control')
tsa, x2a = sol.sample(x2, grid='control')

figure(figsize=(10, 4))
subplot(1, 2, 1)
plot(tsa, x1a, 'o--')
xlabel("Times [s]", fontsize=14)
grid(True)
title('State x1')

subplot(1, 2, 2)
plot(tsa, x2a, 'o--')
legend(['grid_control'])
xlabel("Times [s]", fontsize=14)
title('State x2')
grid(True)

# sphinx_gallery_thumbnail_number = 2

# Refine the grid for a more detailed plot
tsol, usol = sol.sample(u, grid='control')

figure()
step(tsol,usol,where='post')
title("Control signal")
xlabel("Times [s]")
grid(True)

show(block=True)