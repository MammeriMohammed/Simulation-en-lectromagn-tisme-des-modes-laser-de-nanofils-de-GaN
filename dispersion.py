import numpy as np
import matplotlib.pyplot as plt

# Assuming modes function is defined and provided in the modes_ module
from modes_ import modes

# Definitions of the functions
def beta(b, l, a, nc, ng):
    ON = np.sqrt(nc**2 - ng**2)
    V = 2 * np.pi * a / l * ON
    u = V * np.sqrt(b)
    k0 = 2 * np.pi / l
    beta1 = k0 * nc
    beta = np.sqrt(beta1**2 - (u / a)**2)
    return beta

def neff(b, l, a, nc, ng):
    k0 = 2 * np.pi / l
    temp = beta(b, l, a, nc, ng)
    n = temp / k0
    return n

# Parameters
a = 1  # Normalized to 1
nc = 2.5
ng = 1
N = 100
nb = 5
c = 1  # Normalized to 1

# Calculate V parameter
V = np.linspace(1e-8, 6, N + 1)

# Get modes and cuts from the modes function
all_modes, cuts = modes(V, nc, ng, nb, False)

# Calculate corresponding wavelengths
lambdas = [2 * np.pi * a / v for v in V]
k0_values = [2 * np.pi / l for l in lambdas]
omega_values = k0_values  # Since c = 1, omega = k0

# Calculate effective indices and propagation constants for each mode
effective_indices = {}
propagation_constants = {}

for key, b_values in all_modes.items():
    print(f"Processing mode {key}")
    effective_indices[key] = []
    propagation_constants[key] = []
    for b, l in zip(b_values, lambdas):
        if b is None or l is None:
            print(f"Warning: b or l is None (b={b}, l={l}) for mode {key}")
            continue
        try:
            n_eff = neff(b, l, a, nc, ng)
            k0 = 2 * np.pi / l
            k = k0 * n_eff
            effective_indices[key].append(n_eff)
            propagation_constants[key].append(k)
        except Exception as e:
            print(f"Error calculating neff for mode {key} with b={b} and l={l}: {e}")

# Calculate the light cone line (k = omega since c = 1)
light_cone_k = omega_values

# Print the propagation constants for each mode
for mode, constants in propagation_constants.items():
    print(f"Propagation constants for mode {mode}:")
    for omega, k in zip(omega_values, constants):
        print(f"omega: {omega:.3e}, k: {k:.6e}")

# Plot the propagation constants for each mode and the light cone
plt.figure(figsize=(14, 10))
for mode, k_values in propagation_constants.items():
    plt.plot(k_values, omega_values[:len(k_values)], label=f'Mode {mode}')
plt.plot(light_cone_k, omega_values, 'k--', label='Light Cone (k = ω)')

plt.xlabel('Propagation Constant k')
plt.ylabel('ω (normalized)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.title('ω vs. Propagation Constant k for Different Modes')
plt.grid(True)
plt.show()
