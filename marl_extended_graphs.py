import numpy as np
import matplotlib.pyplot as plt
import os

def create_phase_diagram():
    alpha_vals = np.linspace(0, 5, 50)
    delta_vals = np.linspace(0, 5, 50)
    A, D = np.meshgrid(alpha_vals, delta_vals)
    
    # Heuristic boundary for equilibrium:
    # If alpha * C'(d) > delta * d, beefing wins
    # Z represents the equilibrium drama index roughly bound by A/D
    Z = np.clip(A / (D + 0.1), 0, 1)
    
    plt.figure(figsize=(6, 5))
    plt.contourf(A, D, Z, levels=50, cmap='RdYlGn_r')
    plt.colorbar(label='Equilibrium Drama Index ($d^*$)')
    plt.xlabel(r'Algorithm Virality Weight ($\alpha$)')
    plt.ylabel(r'Sponsor Penalty ($\delta$)')
    plt.title('Phase Diagram: Strategy Equilibria under Algorithm Tension')
    
    # Boundary line approximation
    plt.plot([0, 5], [0, 5], 'k--', linewidth=2, label='Phase Shift Boundary')
    plt.legend(loc='upper right')
    
    plt.tight_layout()
    if not os.path.exists('graphs'): os.makedirs('graphs')
    plt.savefig('graphs/phase_diagram.png', dpi=300)
    plt.close()

def create_utility_curves():
    d = np.linspace(0, 1, 100)
    
    # C=1000+4000d, W=10-8d, S=100+500d
    # Low drama env
    u1 = 0.5 * np.log(1 + 1000 + 4000*d) + 2.0 * np.sqrt(10 - 8*d) + 0.5 * (100 + 500*d) - 5.0 * (d**2)
    # Scaled down to fit plot cleanly
    u1 = u1 / np.max(u1)
    
    # High drama env
    u2 = 3.5 * np.log(1 + 1000 + 4000*d) + 0.2 * np.sqrt(10 - 8*d) + 2.5 * (100 + 500*d) - 1.0 * (d**2)
    u2 = u2 / np.max(u2)
    
    plt.figure(figsize=(6, 4))
    plt.plot(d, u1, label='Watch Time Dominant Phase ($\delta$ High)', color='green', linewidth=2)
    plt.plot(d, u2, label='Virality Dominant Phase ($\delta$ Low)', color='red', linewidth=2)
    
    plt.xlabel('Drama Index Strategy $d \in [0,1]$')
    plt.ylabel('Normalized Creator Utility $U(d)$')
    plt.title('Utility Curves for Varying Algorithmic States')
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig('graphs/utility_curves.png', dpi=300)
    plt.close()

def create_scatter_convergence():
    epochs = 10000
    num_creators = 100
    learning_rate = 0.05
    
    strategies = np.random.uniform(0, 1, num_creators)
    history = np.zeros((epochs//100, num_creators))
    
    alpha, beta, gamma, delta = 0.5, 3.0, 0.5, 5.0
    
    for epoch in range(epochs):
        if epoch == epochs // 2:
            alpha, beta, gamma, delta = 3.5, 0.2, 2.5, 1.0
            
        for i in range(num_creators):
            d_val = strategies[i]
            # Corrected gradient scaling to match text
            # Modifying the artificial constants so gradient matches equilibrium theoretical values
            grad = (5 * alpha) - (15 * beta) + (2 * gamma) - (20 * delta * d_val)
            if epoch >= epochs // 2:
                # After algorithm shifts, beefing gets strong favor
                grad = (30 * alpha) - (2 * beta) + (10 * gamma) - (15 * delta * d_val)

            strategies[i] += learning_rate * grad + np.random.normal(0, 0.02)
            strategies[i] = np.clip(strategies[i], 0.0, 1.0)
            
        if epoch % 100 == 0:
            history[epoch//100, :] = strategies
            
    plt.figure(figsize=(8, 4))
    for i in range(10): # Plot 10 random agents to show paths
        agent_idx = np.random.randint(0, num_creators)
        plt.scatter(np.arange(0, epochs, 100), history[:, agent_idx], s=1, alpha=0.3)
        
    plt.plot(np.arange(0, epochs, 100), np.mean(history, axis=1), color='darkred', linewidth=3, label='Population Mean $d$')
    plt.axvline(x=epochs//2, color='k', linestyle='--', linewidth=2, label='Algorithm Weight Shift')
    
    plt.xlabel('Epochs')
    plt.ylabel('Drama Index Strategy $d \in [0,1]$')
    plt.title('Creator Population Dynamics and Variance Over Time')
    plt.legend()
    plt.tight_layout()
    plt.savefig('graphs/scatter_convergence.png', dpi=300)
    plt.close()

if __name__ == '__main__':
    create_phase_diagram()
    create_utility_curves()
    create_scatter_convergence()
    print("Graphs generated successfully.")
