#Load relevant libraries
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# Construct auxiliary Jacobian matrix for 4 variables
  # endogenous: (1) Y, (2) C, (3) I
  # exogenous: (4) G0
# where non-zero elements in regular Jacobian are set to 1 and zero elements are
# unchanged
M_mat = np.array([[0, 1, 1, 1],
         [1, 0, 0, 0],
         [0, 1, 0, 0],
         [0, 0, 0, 0]])

# Create adjacency matrix from transpose of auxiliary Jacobian and add column names
A_mat = M_mat.transpose()

# Create the graph from the adjacency matrix
G = nx.DiGraph(A_mat)

# Define node labels
nodelabs = {0: "Y", 1: "C", 2: "I", 3: "$G_0$"}

# Plot the directed graph
pos = nx.spring_layout(G, seed=42)  
nx.draw(G, pos, with_labels=True, labels=nodelabs, node_size=500, node_color='lightblue', font_size=10)
edge_labels = {(u, v): '' for u, v in G.edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='black')
plt.title("Figure 5: Directed graph of Samuelson model", fontsize=12)
plt.axis('off')
plt.show()