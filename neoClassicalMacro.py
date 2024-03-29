import numpy as np

# Set the number of scenarios (including baseline)
S = 6

# Create arrays to store equilibrium solutions from different parameterizations
Y_star = np.empty(S)  # Income/output
w_star = np.empty(S)  # Real wage
C_star = np.empty(S)  # Consumption
I_star = np.empty(S)  # Investment
r_star = np.empty(S)  # Real interest rate
rn_star = np.empty(S)  # Nominal interest rate
N_star = np.empty(S)  # Employment
P_star = np.empty(S)  # Price level

# Create and parameterize exogenous variables/parameters that will be shifted
M0 = np.zeros(S)  # Money supply
G0 = np.zeros(S)  # Government expenditures
A = np.zeros(S)   # Productivity
Yf = np.zeros(S)  # Expected future income
leisure = np.zeros(S)  # Household preference for leisure (b1)

# Baseline parameterisation
M0[:] = 5
G0[:] = 1
A[:] = 2
Yf[:] = 1
leisure[:] = 0.4

# Set parameter values for different scenarios
M0[1] = 6   # Scenario 2: monetary expansion
G0[2] = 2   # Scenario 3: fiscal expansion
A[3] = 2.5  # Scenario 4: productivity boost
Yf[4] = 0.2  # Scenario 5: lower expected future income
leisure[5] = 0.8  # Scenario 6: increased preference for leisure

# Set constant parameter values
a = 0.3  # Capital elasticity of output
discount_rate = 0.9  # Discount rate
money_pref = 0.6  # Household preference for money
K = 5  # Exogenous capital stock
pe = 0.02  # Expected rate of inflation
Gf = 1  # Future government spending

# Initialize endogenous variables at arbitrary positive values
w = C = I = Y = r = N = P = 1 

def iterate_economy(i, A, a, K, N, I, leisure, discount_rate, money_pref, G0, Yf, Gf, r):
        '''
        i: Simulation index
        A: Productivity shifter
        a: Capital elasticity of output
        K: Exogenous capital stock
        N: Labour supply
        I: Investment
        leisure: Household preference for leisure
        discount_rate: ??????????????
        money_pref: Household preference for money ????????????
        G0: Government expenditures
        Yf: Expected future income
        Gf: Future government spending
        r: Real interest rate ?
        '''
        # (1) Cobb-Douglas production function
        Y = A[i] * (K**a) * N**(1-a)

        # (2) Labour demand
        w = A[i] * (1-a) * (K**a) * N**(-a)

        # (3) Labour supply
        N = 1 - (leisure[i]) / w

        # (4) Consumption demand
        C = (1 / (1 + discount_rate + money_pref)) * (Y - G0[i] + (Yf[i] - Gf) / (1 + r) - leisure[i] * (discount_rate + money_pref) * np.log(leisure[i] / w))

        # (5) Investment demand, solved for r
        r = (I**(a-1)) * a * A[i] * N**(1-a)

        # (6) Goods market equilibrium condition, solved for I
        I = Y - C - G0[i]

        # (7) Nominal interest rate
        rn = r + pe

        # (8) Price level
        P = (M0[i] * rn) / ((1 + rn) * money_pref * C)

        return Y, w, N, C, r, I, rn, P

# Solve this system numerically through 1000 iterations based on the initialization
for i in range(S):
    for iterations in range(1000):
        Y, w, N, C, r, I, rn, P = iterate_economy(i, A, a, K, N, I, leisure, discount_rate, money_pref, G0, Yf, Gf, r)

    # Save results for different parameterizations in the arrays
    Y_star[i] = Y
    w_star[i] = w
    C_star[i] = C
    I_star[i] = I
    r_star[i] = r
    N_star[i] = N
    P_star[i] = P
    rn_star[i] = rn

    # Print some results after the 1000 simulation
    print(Y)

# Plot results (here for output only)
# See code examples in R for plotting other results: https://macrosimulation.org/a_neoclassical_macro_model
import matplotlib.pyplot as plt

scenario_names = ["1: Baseline", "2: Increase in M0", "3: Increase in G0", 
                  "4: Increase in A", "5: Decrease in Yf", "6: Increase in b1"]

# Output
plt.bar(scenario_names , Y_star)
plt.ylabel('Y')
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
plt.tight_layout()  # Ensure the labels fit within the plot area
plt.show()

plt.bar(scenario_names , N_star)
plt.ylabel('N')
plt.xticks(rotation=45, ha="right")  # Rotate x-axis labels for better readability
plt.tight_layout()  # Ensure the labels fit within the plot area
plt.show()


import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Construct the auxiliary Jacobian matrix
M_mat = np.array([
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0],
    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 0, 0]
])

# Create adjacency matrix from transpose of auxiliary Jacobian and add column names
A_mat = M_mat.transpose()

# Create the graph from the adjacency matrix
G = nx.DiGraph(A_mat)

# Define node labels
nodelabs = {
    0: "Y",
    1: "w",
    2: "N",
    3: "C",
    4: "I",
    5: "r",
    6: "P",
    7: r"$r_n$",
    8: r"$M_0$",
    9: r"$G_0$",
    10: "A",
    11: r"$Y^f$",
    12: r"$M_d$"
}

# Plot the directed graph
pos = nx.spring_layout(G, seed=42)  
nx.draw(G, pos, with_labels=True, labels=nodelabs, node_size=300, node_color='lightblue', 
        font_size=10)
edge_labels = {(u, v): '' for u, v in G.edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')
plt.axis('off')
plt.show()