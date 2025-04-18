# growth strategies visualization
# This code visualizes the growth of the number of pure strategies in a game as a function of memory length.

import matplotlib.pyplot as plt
import numpy as np

# Memory length from 0 to 10
memory_lengths = np.arange(0, 11)

# Number of pure strategies: 2^(2^n) where n is memory length
pure_strategies = 2 ** (2 ** memory_lengths)

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(memory_lengths, pure_strategies, marker='o', linestyle='-', color='teal')
plt.yscale('log')
plt.xticks(memory_lengths)
plt.title("Growth of Pure Strategy Space with Memory Length", fontsize=14)
plt.xlabel("Memory Length (n)", fontsize=12)
plt.ylabel("Number of Pure Strategies (log scale)", fontsize=12)
plt.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()
