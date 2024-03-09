import numpy as np

# Set the number of scenarios (including baseline)
S = 6

# Create arrays to store equilibrium solutions from different parameterizations
Y_star = np.empty(S)  # Income/output
C_star = np.empty(S)  # Consumption
I_star = np.empty(S)  # Investment
r_star = np.empty(S)  # Real interest rate
N_star = np.empty(S)  # Employment
U_star = np.empty(S)  # Unemployment rate
P_star = np.empty(S)  # Price level
w_star = np.empty(S)  # Real wage
W_star = np.empty(S)  # Nominal wage

# Set exogenous variables that will be shifted
i0 = np.zeros(S)  # Autonomous investment (animal spirits)
M0 = np.zeros(S)  # Money supply
G0 = np.zeros(S)  # Government spending
P0 = np.zeros(S)  # Expected price level
A = np.empty(S)  # Exogenous productivity

# Construct different scenarios
# baseline
A[:] = 2
i0[:] = 2
M0[:] = 5
G0[:] = 1
P0[:] = 1

# scenario 2: fall in animal spirits
i0[1] = 1.5

# scenario 3: increase in productivity
A[2] = 3

# scenario 4: increase in expected price level
P0[3] = 1.5

# scenario 5: monetary expansion
M0[4] = 6

# scenario 6: fiscal expansion
G0[5] = 2

# Set constant parameter values
c0 = 2  # Autonomous consumption
c1 = 0.6  # Sensitivity of consumption with respect to income (marginal propensity to consume)
i1 = 0.1  # Sensitivity of investment with respect to the interest rate
m1 = 0.2  # Sensitivity of money demand with respect to income
m2 = 0.4  # Sensitivity of money demand with respect to interest rate
Nf = 5  # Full employment/labor force
K = 4  # Exogenous capital stock
a = 0.3  # Capital elasticity of output
b = 0.4  # Household preference for leisure
T0 = 1  # Tax revenues
m0 = 6  # Liquidity preference

# Initialize endogenous variables at some arbitrary positive value
Y = C = I = r = P = w = N = W = 1

# Solve this system numerically through 1000 iterations based on the initialization
for i in range(S):
    for iterations in range(1000):
        # Model equations

        # Goods market equilibrium
        Y = C + I + G0[i]

        # Consumption demand
        C = c0 + c1 * (Y - T0)

        # Investment demand
        I = i0[i] - i1 * r

        # Money market, solved for interest rate
        r = (m0 - (M0[i] / P)) / m2 + m1 * Y / m2

        # Unemployment rate
        U = 1 - N / Nf

        # Real wage
        w = A[i] * (1 - a) * (K ** a) * (N ** (-a))

        # Nominal wage
        W = (P0[i] * b * C) / (1 - (N / Nf))

        # Price level
        P = W / w

        # Employment
        N = (Y / (A[i] * (K ** a))) ** (1 / (1 - a))

    # Save results for different parameterizations in the arrays
    Y_star[i] = Y
    C_star[i] = C
    I_star[i] = I