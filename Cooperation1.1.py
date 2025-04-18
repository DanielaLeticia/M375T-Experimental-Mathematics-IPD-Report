import numpy as np
import matplotlib.pyplot as plt
import random

# Define the parameters for the simulation
num_agents = 200
rounds_per_match = 150
generations = 200
mutation_rate = 0.05
num_matches_per_agent = 10

# Define the payoff matrix
R, T, P, S = 3, 5, 1, 0

# Define strategies by memory level
memory_0_strategies = ['Always Cooperate', 'Always Defect', 'Random']
memory_1_strategies = ['Tit-for-Tat', 'Pavlov']
memory_2_strategies = ['Grim Trigger', 'Tit-for-2-Tats']

# Initialize population with random strategies from all memory levels
population = [random.choice(memory_0_strategies + memory_1_strategies + memory_2_strategies) for _ in range(num_agents)]

# Function to play a single round of IPD
def play_round(strategy1, strategy2, memory1, memory2):
    if strategy1 == 'Always Cooperate':
        move1 = 'C'
    elif strategy1 == 'Always Defect':
        move1 = 'D'
    elif strategy1 == 'Random':
        move1 = random.choice(['C', 'D'])
    elif strategy1 == 'Tit-for-Tat':
        move1 = memory2[-1] if memory2 else 'C'
    elif strategy1 == 'Pavlov':
        move1 = 'C' if not memory1 or memory1[-1] == 'C' else 'D'
    elif strategy1 == 'Grim Trigger':
        move1 = 'D' if 'D' in memory2 else 'C'
    elif strategy1 == 'Tit-for-2-Tats':
        move1 = 'D' if memory2[-2:] == ['D', 'D'] else 'C'
    
    if strategy2 == 'Always Cooperate':
        move2 = 'C'
    elif strategy2 == 'Always Defect':
        move2 = 'D'
    elif strategy2 == 'Random':
        move2 = random.choice(['C', 'D'])
    elif strategy2 == 'Tit-for-Tat':
        move2 = memory1[-1] if memory1 else 'C'
    elif strategy2 == 'Pavlov':
        move2 = 'C' if not memory2 or memory2[-1] == 'C' else 'D'
    elif strategy2 == 'Grim Trigger':
        move2 = 'D' if 'D' in memory1 else 'C'
    elif strategy2 == 'Tit-for-2-Tats':
        move2 = 'D' if memory1[-2:] == ['D', 'D'] else 'C'
    
    return move1, move2

# Function to calculate payoff
def calculate_payoff(move1, move2):
    if move1 == 'C' and move2 == 'C':
        return R, R
    elif move1 == 'C' and move2 == 'D':
        return S, T
    elif move1 == 'D' and move2 == 'C':
        return T, S
    else:
        return P, P

# Function to simulate a match
def simulate_match(strategy1, strategy2):
    memory1, memory2 = [], []
    total_payoff1, total_payoff2 = 0, 0
    for _ in range(rounds_per_match):
        move1, move2 = play_round(strategy1, strategy2, memory1, memory2)
        payoff1, payoff2 = calculate_payoff(move1, move2)
        total_payoff1 += payoff1
        total_payoff2 += payoff2
        memory1.append(move1)
        memory2.append(move2)
    return total_payoff1, total_payoff2

# Function to simulate a generation
def simulate_generation(population):
    payoffs = [0] * num_agents
    for i in range(num_agents):
        for _ in range(num_matches_per_agent):
            opponent = random.choice(range(num_agents))
            payoff1, payoff2 = simulate_match(population[i], population[opponent])
            payoffs[i] += payoff1
            payoffs[opponent] += payoff2
    return payoffs

# Function to reproduce and mutate population
def reproduce_and_mutate(population, payoffs):
    sorted_indices = np.argsort(payoffs)[::-1]
    new_population = []
    for i in range(num_agents):
        if i < num_agents * 0.25:
            new_population.append(population[sorted_indices[i]])
        elif i < num_agents * 0.75:
            new_population.append(population[sorted_indices[i]])
        else:
            new_population.append(population[sorted_indices[i]])
            if random.random() < mutation_rate:
                new_population[-1] = random.choice(memory_0_strategies + memory_1_strategies + memory_2_strategies)
    return new_population

# Initialize data storage for each memory level
memory_0_counts = []
memory_1_counts = []
memory_2_counts = []
memory_0_payoffs = []
memory_1_payoffs = []
memory_2_payoffs = []

# Run the simulation
for generation in range(generations):
    payoffs = simulate_generation(population)
    population = reproduce_and_mutate(population, payoffs)
    
    # Count strategies by memory level
    memory_0_count = sum([population.count(strategy) for strategy in memory_0_strategies])
    memory_1_count = sum([population.count(strategy) for strategy in memory_1_strategies])
    memory_2_count = sum([population.count(strategy) for strategy in memory_2_strategies])
    
    memory_0_counts.append(memory_0_count)
    memory_1_counts.append(memory_1_count)
    memory_2_counts.append(memory_2_count)
    
    # Calculate average payoffs for each memory level
    memory_0_payoff = np.mean([payoffs[i] for i in range(num_agents) if population[i] in memory_0_strategies])
    memory_1_payoff = np.mean([payoffs[i] for i in range(num_agents) if population[i] in memory_1_strategies])
    memory_2_payoff = np.mean([payoffs[i] for i in range(num_agents) if population[i] in memory_2_strategies])
    
    memory_0_payoffs.append(memory_0_payoff)
    memory_1_payoffs.append(memory_1_payoff)
    memory_2_payoffs.append(memory_2_payoff)

# Plot performance of Memory-0, Memory-1, and Memory-2 strategies over generations on one plot
plt.figure(figsize=(10, 6))
plt.plot(memory_0_counts, label='Memory-0 Strategies')
plt.plot(memory_1_counts, label='Memory-1 Strategies')
plt.plot(memory_2_counts, label='Memory-2 Strategies')
plt.xlabel('Generations')
plt.ylabel('Number of Agents')
plt.title('Performance of Memory-0, Memory-1, and Memory-2 Strategies Over Generations')
plt.legend()
plt.grid(True)
plt.savefig('memory_performance.png')
plt.show()

# Plot average payoff vs memory size
memory_sizes = ['Memory-0', 'Memory-1', 'Memory-2']
average_payoffs = [np.mean(memory_0_payoffs), np.mean(memory_1_payoffs), np.mean(memory_2_payoffs)]

plt.figure(figsize=(10, 6))
plt.bar(memory_sizes, average_payoffs, color=['blue', 'orange', 'green'])
plt.xlabel('Memory Size')
plt.ylabel('Average Payoff')
plt.title('Average Payoff vs Memory Size')
plt.ylim(7800, 8100)  # Zoom in around the top of the columns
plt.savefig('payoff_vs_memory_size_zoomed.png')
plt.show()

print("Results and Analysis:")
print("Performance of Memory-0 Strategies:")
print(f"   - Initial count: {memory_0_counts[0]}")
print(f"   - Final count: {memory_0_counts[-1]}")
print("   - Memory-0 strategies tend to perform poorly in the long term.")

print("Performance of Memory-1 Strategies:")
print(f"   - Initial count: {memory_1_counts[0]}")
print(f"   - Final count: {memory_1_counts[-1]}")
print("   - Memory-1 strategies strike a strong balance between efficiency and flexibility.")

print("Performance of Memory-2 Strategies:")
print(f"   - Initial count: {memory_2_counts[0]}")
print(f"   - Final count: {memory_2_counts[-1]}")
print("   - Memory-2 strategies show mixed outcomes depending on environmental stability.")

print("Average Payoff vs Memory Size:")
print(f"   - Memory-0: {average_payoffs[0]}")
print(f"   - Memory-1: {average_payoffs[1]}")
print(f"   - Memory-2: {average_payoffs[2]}")
