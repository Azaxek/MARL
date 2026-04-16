import numpy as np
import matplotlib.pyplot as plt
import os

def simulate_marl(epochs=10000, num_creators=100):
    # Initial random strategies (drama index between 0 and 1)
    strategies = np.random.uniform(0, 1, num_creators)
    
    # Store history for plotting
    history_d_mean = []
    
    # Environment coefficients
    # C(d) = 1000 + 4000d  (Beefing gives more clicks)
    # W(d) = 10 - 8d     (Collab gives more watch time)
    # S(d) = 100 + 500d   (Beefing gives more shares)
    
    # Initial Algorithm Weights (High watch time preference early on)
    alpha = 0.5  # clicks
    beta = 2.0   # watch time
    gamma = 0.5  # shares
    delta = 5.0  # sponsor penalty
    
    learning_rate = 0.05
    
    for epoch in range(epochs):
        # Algorithm shifts priorities automatically midway
        if epoch == epochs // 2:
            alpha = 2.5 # Shifts to favor clicks and shares (viral)
            beta = 0.2
            gamma = 2.0
        
        # Creators optimize via localized gradient ascent
        # U(d) = alpha * log(1 + 1000 + 4000d) + beta * (10 - 8d) + gamma * (100 + 500d) - delta * d^2
        # dU/dd = (4000 * alpha) / (1001 + 4000d) - 8 * beta + 500 * gamma - 2 * delta * d
        
        for i in range(num_creators):
            d = strategies[i]
            grad = (4000 * alpha) / (1001 + 4000 * d) - 8 * beta + 500 * gamma - 2 * delta * d
            strategies[i] += learning_rate * grad
            
            # Clip between 0 and 1 (continuous strategy space bounded)
            strategies[i] = np.clip(strategies[i], 0.0, 1.0)
            
        history_d_mean.append(np.mean(strategies))
        
    # Plotting
    plt.figure(figsize=(8, 4))
    plt.plot(range(epochs), history_d_mean, label='Average Creator Drama Index ($d$)', color='darkred', linewidth=2)
    
    plt.axvline(x=epochs//2, color='gray', linestyle='--', label='Algorithm Shift (Favors Virality)')
    plt.title('MARL Simulation of Creator Strategies Over Time')
    plt.xlabel('Epochs')
    plt.ylabel('Average Drama Index $d \in [0,1]$')
    plt.ylim(-0.05, 1.05)
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
        
    plt.savefig('graphs/simulation_results.png', dpi=300)
    print("Simulation complete. Graph saved to graphs/simulation_results.png")

if __name__ == '__main__':
    simulate_marl()
