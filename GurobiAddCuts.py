# A KNAPSACK PROBLEM
# Solve the following IP:
#  maximize
#        16 * x1 + 22 * x2 + 12 * x3 + 8 * x4 + 11 * x5 + 19 * x6
#  subject to
#        5 * x1 + 7 * x2 + 4 * x3 + 3 * x4 + 4 * x5 + 6 * x6 <= 14
#        xj binary, j=1,2,...,5,6

import gurobipy as gp
from gurobipy import GRB

# Create a new model
m = gp.Model()

# Create variables: where vtype: B=binary , I=integer , C=continuos
x1 = m.addVar(vtype='C', name="x1")
x2 = m.addVar(vtype='C', name="x2")
x3 = m.addVar(vtype='C', name="x3")
x4 = m.addVar(vtype='C', name="x4")
x5 = m.addVar(vtype='C', name="x5")
x6 = m.addVar(vtype='C', name="x6")

# Set objective function
m.setObjective(16 * x1 + 22 * x2 + 12 * x3 + 8 * x4 + 11 * x5 + 19 * x6, gp.GRB.MAXIMIZE)

# Add constraints
m.addConstr(5 * x1 + 7 * x2 + 4 * x3 + 3 * x4 + 4 * x5 + 6 * x6 <= 14)
m.addConstr(x1 >= 0)
m.addConstr(x1 <= 1)
m.addConstr(x2 >= 0)
m.addConstr(x2 <= 1)
m.addConstr(x3 >= 0)
m.addConstr(x3 <= 1)
m.addConstr(x4 >= 0)
m.addConstr(x4 <= 1)
m.addConstr(x5 >= 0)
m.addConstr(x5 <= 1)
m.addConstr(x6 >= 0)
m.addConstr(x6 <= 1)
#m.addConstr(x1 + x2 + x6 <= 2)
#m.addConstr(x1 + x2 + x3 <= 2)
#m.addConstr(x1 + x2 + x3 + x6 <= 2)

# Add cuts
#def myaddCuts(m,where):
#    if where == GRB.Callback.MIPNODE:
#        m.cbCut(x1 + x2 + x6 <= 1)


def myaddCuts(m,where):
#    if where == GRB.Callback.MIPNODE:
#       status = m.cbGet(GRB.Callback.MIPNODE_STATUS)
#        if status == GRB.OPTIMAL:
#            print(m.cbGetNodeRel(m._vars))


    if where == GRB.Callback.MIPNODE:
        if m.cbGet(GRB.Callback.MIPNODE_STATUS) == GRB.OPTIMAL:
            rel = m.cbGetNodeRel(x1,x2,x3,x4,x5,x6)
            if rel[x1] + rel[x2] + rel[x3] + rel[x4] + rel[x5] + rel[x6] > 1.1:
                m.cbCut(x1 + x2 + x6 <= 2)
                if where == GRB.Callback.MIPSOL:
                    m._vars = m.getVars()
                    m.optimize(myaddCuts)
                    print(f"Current objective value: {m.cbGetSolution(m._vars)}")

# Solve it!
m._vars = m.getVars()
m.Params.PreCrush = 1
m.optimize(myaddCuts)

# Print!
print(f"Optimal objective value: {m.objVal}")
print(f"Solution values: x1={x1.X}, x2={x2.X}, x3={x3.X},x4={x4.X}, x5={x5.X}, x6={x6.X},")