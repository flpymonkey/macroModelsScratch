# https://macrosimulation.org/how_to_use


################################### Python Basics ###########################



# Load relevant libraries
import numpy as np 

### Simulate Samuelson 1939

# Set the number of periods for which you want to simulate
Q = 100

# Set the number of parameterisations that will be considered
S = 2

# Set the period in which a shock or shift in 'an' will occur
s = 15

# Set fixed parameter values
c1 = 0.8
beta = 0.6

# Construct (S x Q) matrices in which values for different periods will be stored; initialize at 1
C = np.ones((S, Q))
I = np.ones((S, Q))

# Construct matrices for exogenous variables or parameters that will change 
# over time to capture different scenarios, initialise at 5
G0 = np.ones((S, Q))*5 

# Set parameter values for different scenarios
G0[1, s:Q] = 6  # scenario: permanent increase in government spending from I0=5 to I0=6 from period s=15 onwards

# Solve this system recursively based on the initialization
for i in range(S):
    for t in range(1, Q):
        C[i, t] = c1 * (C[i, t - 1] + I[i, t - 1] + G0[i, t - 1])
        I[i, t] = beta * (c1 * (C[i, t - 1] + I[i, t - 1] + G0[i, t - 1]) - 
                          C[i, t - 1])

# Calculate output
Y = C + G0 + I

# Display the solutions at time Q
print(Y[:, Q - 1])

# Verify solutions for Y
print((G0[:,Q - 1])/(1-c1))


import matplotlib.pyplot as plt

# Bar chart of different equilibrium solutions of Samuelson (1939) model
scenario_labels = ["Baseline", "Increase in G0"]
plt.bar(scenario_labels, Y[:, Q - 1])
plt.xlabel("Scenario")
plt.ylabel("Y")
plt.title("Figure 1: Output")
plt.show()

# Time series chart of output dynamics in Samuelson (1939) model
plt.plot(range(1, Q), Y[0, 0:Q - 1], color='black', linewidth=2, linestyle='-')
plt.xlabel("Time")
plt.ylabel("Y")
plt.title("Figure 2: Output", fontsize=10)
plt.show()

# Time series chart of output dynamics for different scenarios in Samuelson 
#(1939) model
plt.plot(range(1, Q), Y[0, 0:Q - 1], color='black', linewidth=1, linestyle='-')
plt.plot(range(1, Q), Y[1, 0:Q - 1], color='black', linewidth=1, linestyle='--')
plt.xlabel("Time")
plt.ylabel("Y")
plt.title("Figure 3: Output under different scenarios", fontsize=10)
plt.legend(["Baseline", "Increase in G0"], loc='lower right')
plt.show()

# Time series chart of Samuelson (1939) model with separate axes for consumption 
# and investment
fig, ax1 = plt.subplots()
ax1.plot(range(1, Q), C[0, 0:Q - 1], color='black', linewidth=2, linestyle='-', 
         label='C')
ax1.set_xlabel("Time")
ax1.set_ylabel("C", color='black')
ax1.tick_params(axis='y', labelcolor='black')
ax2 = ax1.twinx()
ax2.plot(range(1, Q), I[0, 0:Q - 1], color='black', linewidth=2, linestyle='--',
         label='I')
ax2.set_ylabel("I", color='black')
ax2.tick_params(axis='y', labelcolor='black')
plt.title("Figure 4: Consumption and Investment", fontsize=10)
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax2.legend(lines + lines2, labels + labels2, loc='right')
plt.show()




# If we want to simulate this in continuous time, we must approx the continue differential equation,
# Using a small differential equation: https://macrosimulation.org/how_to_simulate#sec-sim-continuous
# This is Euler Forward method.