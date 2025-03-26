import cmath
import math

def calculate_powers(V, I_real, I_imag, Z_real, Z_imag):
    # Convert current and impedance to complex numbers (phasors)
    I = complex(I_real, I_imag)
    Z = complex(Z_real, Z_imag)
    
    # Calculate the angle of the impedance
    phi = cmath.phase(Z)
    
    # Calculate apparent power (S)
    S = V * abs(I)
    
    # Calculate active power (P)
    P = V * abs(I) * cmath.cos(phi)
    
    # Calculate reactive power (Q)
    Q = V * abs(I) * cmath.sin(phi)
    
    # Calculate power factor (fp)
    fp = P / S if S != 0 else 0
    
    # Calculate phasor magnitude and angle
    I_magnitude = abs(I)
    I_angle = math.degrees(cmath.phase(I))
    Z_magnitude = abs(Z)
    Z_angle = math.degrees(cmath.phase(Z))
    
    return P, Q, S, fp, (I_magnitude, I_angle), (Z_magnitude, Z_angle)

# Parameters for different frequencies
parameters = [
    {"frequency": "75,000 Hz", "I_real": -0.532105, "I_imag": 660.888, "V": -0.7385193751783528, "Z_real": -0.000268018, "Z_imag": -0.332885},
]

# Calculate powers for each set of parameters and store results
results = []
for param in parameters:
    P, Q, S, fp, I_phasor, Z_phasor = calculate_powers(param["V"], param["I_real"], param["I_imag"], param["Z_real"], param["Z_imag"])
    results.append({"frequency": param["frequency"], "P": P, "Q": Q, "S": S, "fp": fp, "I_phasor": I_phasor, "Z_phasor": Z_phasor})

# Print the results in a table format
print(f"{'Parámetro':<15}{'100,000 Hz':<25}{'10,000 Hz':<25}{'100 Hz':<25}")
print(f"{'P':<15}{results[0]['P']:<25.2f}{results[1]['P']:<25.2f}{results[2]['P']:<25.2f}")
print(f"{'Q':<15}{results[0]['Q']:<25.2f}{results[1]['Q']:<25.2f}{results[2]['Q']:<25.2f}")
print(f"{'S':<15}{results[0]['S']:<25.2f}{results[1]['S']:<25.2f}{results[2]['S']:<25.2f}")
print(f"{'fp':<15}{results[0]['fp']:<25.2f}{results[1]['fp']:<25.2f}{results[2]['fp']:<25.2f}")
print(f"{'I (phasor)':<15}{results[0]['I_phasor'][0]:.2f} > {results[0]['I_phasor'][1]:.2f}°{'':<10}"
      f"{results[1]['I_phasor'][0]:.2f} < {results[1]['I_phasor'][1]:.2f}°{'':<10}"
      f"{results[2]['I_phasor'][0]:.2f} < {results[2]['I_phasor'][1]:.2f}°")
print(f"{'Z (phasor)':<15}{results[0]['Z_phasor'][0]:.6f} > {results[0]['Z_phasor'][1]:.2f}°{'':<10}"
      f"{results[1]['Z_phasor'][0]:.6f} < {results[1]['Z_phasor'][1]:.2f}°{'':<10}"
      f"{results[2]['Z_phasor'][0]:.6f} < {results[2]['Z_phasor'][1]:.2f}°")