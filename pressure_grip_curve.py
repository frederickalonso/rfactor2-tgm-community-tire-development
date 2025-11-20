import numpy as np
import matplotlib.pyplot as plt

# D_260-650-R18x10_C98D_SOFT_2025_STABLE2.tgm Parameters
pressure_points = [100000, 150000, 200000, 220000, 230000]  # Pa
pressure_bars = [p/100000 for p in pressure_points]  # Convert to bars

# RubberPressureSensitivityPower=(-40, 1.13e7, 5e5, 1)
power = -40
offset = 1.13e7
nominal_max = 5e5
normalize = 1

# Create pressure range for smooth curve
pressure_range = np.linspace(80000, 250000, 100)  # 0.8 to 2.5 bar
pressure_bars_range = pressure_range / 100000

# Calculate grip based on pressure sensitivity formula
# This is a simplified interpretation of the rFactor 2 pressure sensitivity
def calculate_grip(pressure, power, offset, nominal_max):
    # Normalized pressure relative to nominal
    norm_pressure = pressure / nominal_max
    
    # Calculate grip multiplier (simplified version)
    # The actual rF2 formula is more complex, but this gives the general shape
    grip_factor = 1.0 + (power / 100) * np.log(norm_pressure + offset/nominal_max)
    
    # Normalize to make peak around 1.5 bar (150000 Pa)
    peak_pressure = 150000
    peak_norm = peak_pressure / nominal_max
    peak_factor = 1.0 + (power / 100) * np.log(peak_norm + offset/nominal_max)
    
    # Normalize so peak = 1.0
    normalized_grip = grip_factor / peak_factor
    
    # Ensure grip doesn't go negative and apply realistic bounds
    normalized_grip = np.clip(normalized_grip, 0.1, 1.2)
    
    return normalized_grip

# Calculate grip for the range
grip_values = calculate_grip(pressure_range, power, offset, nominal_max)

# Create the plot
plt.figure(figsize=(12, 8))
plt.plot(pressure_bars_range, grip_values, 'b-', linewidth=3, label='Current Tire (Peak ~1.5 bar)')

# Mark the defined pressure points
defined_grip = calculate_grip(np.array(pressure_points), power, offset, nominal_max)
plt.scatter(pressure_bars, defined_grip, color='red', s=100, zorder=5, label='Defined Test Points')

# Add target optimal point
plt.axvline(x=1.9, color='green', linestyle='--', linewidth=2, label='Target Optimal (1.9 bar)')
plt.axvline(x=1.5, color='orange', linestyle='--', linewidth=2, label='Current Optimal (~1.5 bar)')

# Formatting
plt.xlabel('Tire Pressure (bar)', fontsize=14)
plt.ylabel('Relative Grip Level', fontsize=14)
plt.title('Grip vs Pressure Curve\nD_260-650-R18x10_C98D_SOFT_2025_STABLE2.tgm', fontsize=16)
plt.grid(True, alpha=0.3)
plt.legend(fontsize=12)

# Add annotations
plt.annotate('Current Peak\n(~1.5 bar)', xy=(1.5, max(grip_values)), xytext=(1.3, 1.1),
            arrowprops=dict(arrowstyle='->', color='orange'), fontsize=10, ha='center')
            
plt.annotate('Target Peak\n(1.9 bar)', xy=(1.9, 0.85), xytext=(2.1, 1.0),
            arrowprops=dict(arrowstyle='->', color='green'), fontsize=10, ha='center')

# Add parameter info
param_text = f"RubberPressureSensitivityPower=({power}, {offset:.1e}, {nominal_max:.0e}, {normalize})"
plt.figtext(0.02, 0.02, param_text, fontsize=10, style='italic')

plt.tight_layout()
plt.savefig('tire_pressure_grip_curve.png', dpi=300, bbox_inches='tight')
plt.show()

print("Grip vs Pressure Analysis:")
print("=" * 40)
print(f"Current optimal pressure: ~1.5 bar")
print(f"Target optimal pressure: 1.9 bar")
print(f"Current parameters: Power={power}, Offset={offset:.1e}")
print("=" * 40)
print("Pressure Points:")
for i, (bar, grip) in enumerate(zip(pressure_bars, defined_grip)):
    print(f"  {bar:.1f} bar: {grip:.2f} relative grip") 