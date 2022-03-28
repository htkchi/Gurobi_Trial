# Solve the following MIP:
#  maximize
#        x +   5y + 2 z
#  subject to
#        x + 2 y + 3 z <= 4
#        x +   y       >= 1/2
#        x, y, z binary

import gurobipy as gp
from gurobipy import GRB

# Create a new model
m = gp.Model()

# Create variables
x = m.addVar(vtype='B', name="x")
y = m.addVar(vtype='B', name="y")
z = m.addVar(vtype='B', name="z")

# Set objective function
m.setObjective(x + 5*y + 2 * z, gp.GRB.MAXIMIZE)

# Add constraints
m.addConstr(x + 2 * y + 3 * z <= 4)
m.addConstr(x + y + x >= 1/2)
#m.addConstr(x + y <= 1)

# Presolved Problem
m.write('gurobi.rew')
r = m.relax()
r.write('gurobi.relax-nopre.rew')
p = m.presolve()
r = p.relax()
r.write('gurobi.relax-pre.rew')
m.reset()
m.Params.Aggregate = 0
p = m.presolve()
r = p.relax()
r.write('gurobi.relax-agg0.rew')
m.printStats()
p.printStats()
r.printStats()

# Note that the MIPNODE callback will be called once for each cut pass during the root node solve.
# cbCut(): https://www.gurobi.com/documentation/9.0/refman/py_model_cbcut.html
# Model.cbGet(): https://www.gurobi.com/documentation/9.0/refman/py_model_cbget.html
def myaddcut(m,where):
#    if where == GRB.Callback.MIPNODE:
#       if GRB.CB_MIPNODE_STATUS == GRB.Status.OPTIMAL:
#            m.setParam(GRB.Param.PRECRUSH, 1)
#            m.cbAddCuts(x + y <= 1)
#            print(f"Added cut: {AddCut}")

    if where == GRB.Callback.MIPNODE:
        status = m.cbGet(GRB.Callback.MIPNODE_STATUS)
        if status == GRB.OPTIMAL:
            rel = m.cbGetNodeRel(x,y,z)
            if rel[x] + rel[y] > 1.1:
                m.cbCut(x + y <= 1)

#m._vars = m.getVars()

# Solve it!
#m.optimize()
m.optimize(myaddcut)

print(f"Optimal objective value: {m.objVal}")
print(f"Solution values: x={x.X}, y={y.X}, z={z.X}")

#GRB.Callback.addCut(x+y,GRB.LESS_EQUAL,2)