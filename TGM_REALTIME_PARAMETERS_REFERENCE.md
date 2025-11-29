# rFactor2 TGM [Realtime] Parameters - Complete Reference Guide

**Based on:** University thesis "Optimisation of the tyre model in rFactor2 environment for AVEHIL professional simulator" (2018/2019) and practical tire development experience.

## Table of Contents

1. [Introduction](#introduction)
2. [Grip & Friction Parameters](#grip--friction-parameters)
3. [Stiffness & Deformation Parameters](#stiffness--deformation-parameters)
4. [Thermal Parameters](#thermal-parameters)
5. [Wear & Degradation Parameters](#wear--degradation-parameters)
6. [Distribution & Multiplier Parameters](#distribution--multiplier-parameters)
7. [Terrain & Surface Parameters](#terrain--surface-parameters)
8. [Internal Gas Parameters](#internal-gas-parameters)
9. [Tuning Guidelines](#tuning-guidelines)

---

## Introduction

The [Realtime] section of a TGM file contains parameters that act as **scaling factors** and **tuning multipliers** for the tire behavior during gameplay. These parameters work in real-time without requiring recalculation of the lookup table, making them ideal for fine-tuning tire characteristics.

**Key Concepts:**
- Parameters are largely **independent** of each other
- Small changes (±5%) typically show **linear or quadratic** behavior
- Parameters act as **scaling factors** on the base physics calculated in the lookup table
- Changes can be tested immediately without re-running QSA tests

---

## Grip & Friction Parameters

### StaticBaseCoefficient

**Purpose:** Base friction coefficient for static (adhesion) grip conditions. Controls the maximum grip available when the tire is not sliding.

**Format:** `StaticBaseCoefficient=<value>`

**Example from Hybrid Tire:**
```
StaticBaseCoefficient=3.75  // Reduced by ~6% to match target friction coefficient
```

**Thesis Information:**
- One of the most critical parameters for overall tire grip
- Directly affects lateral and longitudinal force generation
- Works in combination with `SlidingBaseCoefficient` to define the friction envelope

**Tuning Guidelines:**
- **Increase** for more grip (higher friction coefficient)
- **Decrease** for less grip (lower friction coefficient)
- Typical range: 2.5 - 4.5
- Changes of ±5-10% are common for fine-tuning
- Higher values = more grip but can lead to overheating if too high

**Real-World Impact:**
- Higher values: Better cornering grip, shorter braking distances, more responsive steering
- Lower values: More sliding, longer braking distances, less responsive steering
- Must be balanced with thermal parameters to avoid overheating

---

### SlidingBaseCoefficient

**Purpose:** Base friction coefficient for sliding conditions. Controls grip when the tire is sliding (beyond the adhesion limit).

**Format:** `SlidingBaseCoefficient=<value>`

**Example from Hybrid Tire:**
```
SlidingBaseCoefficient=2.68  // Reduced by ~5.5% to maintain balance with StaticBaseCoefficient
```

**Thesis Information:**
- Typically 60-75% of `StaticBaseCoefficient` value
- Affects behavior when tire exceeds adhesion limit
- Important for drift behavior and recovery from slides

**Tuning Guidelines:**
- Should be proportional to `StaticBaseCoefficient` (typically 0.65-0.75 ratio)
- **Increase** for more grip during slides (harder to break loose)
- **Decrease** for less grip during slides (easier to break loose, more progressive)
- Typical range: 1.5 - 3.5

**Real-World Impact:**
- Higher values: Tire maintains more grip when sliding, harder to break loose
- Lower values: Tire slides more easily, more progressive breakaway
- Affects how the tire recovers from oversteer/understeer situations

---

### StaticDiffusiveAdhesion

**Purpose:** Controls the diffusive adhesion component of static grip. This parameter affects how grip is distributed across the contact patch based on molecular adhesion mechanisms.

**Format:** `StaticDiffusiveAdhesion=(<min_velocity>, <max_force>, <exponent>)`

**Example from Hybrid Tire:**
```
StaticDiffusiveAdhesion=(0.001, 11200, 0.75)  // Increased for wider tire
```

**Thesis Information:**
- Based on molecular adhesion theory (Van der Waals bonding)
- The second value (max_force) is the maximum adhesion force
- The exponent controls the velocity-dependent behavior
- Higher values increase grip, especially on smooth surfaces

**Tuning Guidelines:**
- First value: Minimum sliding velocity threshold (typically 0.001)
- Second value: Maximum adhesion force (typical range: 8000-15000)
  - **Increase** for more grip on smooth surfaces
  - **Decrease** for less grip
- Third value: Exponent (typically 0.7-0.8)
- For wider tires, increase the second value proportionally

**Real-World Impact:**
- Higher values: Better grip on smooth surfaces, better low-speed grip
- Lower values: Less grip on smooth surfaces, more dependent on surface roughness

---

### SlidingDiffusiveAdhesion

**Purpose:** Controls the diffusive adhesion component during sliding conditions.

**Format:** `SlidingDiffusiveAdhesion=(<min_velocity>, <max_force>, <exponent>)`

**Example from Hybrid Tire:**
```
SlidingDiffusiveAdhesion=(0.001, 1900, 0.75)  // Increased for wider tire
```

**Thesis Information:**
- Similar to `StaticDiffusiveAdhesion` but for sliding conditions
- Typically 15-20% of the static value
- Affects grip maintenance during slides

**Tuning Guidelines:**
- First value: Minimum sliding velocity threshold (typically 0.001)
- Second value: Maximum adhesion force during sliding (typical range: 1500-2500)
  - **Increase** for more grip during slides
  - **Decrease** for less grip during slides
- Third value: Exponent (typically 0.7-0.8)
- Should be proportional to `StaticDiffusiveAdhesion`

**Real-World Impact:**
- Higher values: Tire maintains more grip when sliding
- Lower values: Tire loses grip more quickly when sliding

---

### StaticCurve

**Purpose:** Defines how static friction coefficient varies with carcass temperature. This is a critical parameter for tire warm-up behavior and optimal operating temperature.

**Format:** `StaticCurve=(<temp1_K>, <grip1>, <temp2_K>, <grip2>, <temp3_K>, <grip3>)`

**Example from Hybrid Tire:**
```
StaticCurve=(273, 0.6, 360, 1.0, 420, 0.7)  // Lower peak temp from 378K (105°C) to 360K (87°C) to match target operating temperature range
```

**Thesis Information:**
- Uses cubic spline interpolation between the three points
- Defines a parabolic-like curve of grip vs temperature
- Peak performance occurs in a narrow temperature range (typically 5-10°C wide)
- The middle point defines the optimal operating temperature
- First point: Low temperature (cold tire) grip multiplier
- Second point: Peak temperature and maximum grip multiplier
- Third point: High temperature (overheated) grip multiplier

**Tuning Guidelines:**
- **Temp1 (K):** Cold tire temperature (typically 273K = 0°C)
  - Grip multiplier: Typically 0.5-0.7 (lower grip when cold)
- **Temp2 (K):** Optimal operating temperature (typically 360-380K = 87-107°C)
  - Grip multiplier: Typically 1.0-1.2 (peak performance)
  - **This is the most critical value** - sets optimal tire temperature
- **Temp3 (K):** Overheated temperature (typically 420-450K = 147-177°C)
  - Grip multiplier: Typically 0.6-0.8 (reduced grip when overheated)
- **To match real tire data:** Adjust Temp2 to match the tire's optimal operating temperature range
- **For warm-up training:** Lower the grip multipliers at Temp1 to make cold tires more slippery

**Real-World Impact:**
- Lower Temp2: Tire performs best at lower temperatures (easier to warm up)
- Higher Temp2: Tire performs best at higher temperatures (harder to warm up, more resistant to overheating)
- Lower grip at Temp1: More realistic cold tire behavior, requires proper warm-up
- Higher grip at Temp1: Easier to drive on cold tires (less realistic)

**Example Adjustments:**
- **Cold tire behavior:** `(273, 0.3, 373, 1.0, 673, 0.3)` - Very slippery when cold
- **High temp tire:** `(273, 0.6, 400, 1.2, 450, 0.7)` - Performs best at high temperatures
- **Low temp tire:** `(273, 0.6, 340, 1.0, 400, 0.7)` - Performs best at lower temperatures

---

### SlidingAdhesionCurve

**Purpose:** Defines how sliding friction varies with sliding velocity. Controls grip behavior when tire is sliding.

**Format:** `SlidingAdhesionCurve=(<vel1>, <grip1>, <vel2>, <grip2>, <vel3>, <grip3>)`

**Example from Hybrid Tire:**
```
SlidingAdhesionCurve=(-7.2, 0.4, -4.2, 1.7, -1.2, 0.2)
```

**Thesis Information:**
- Defines grip as a function of sliding velocity
- Negative velocities typically represent higher sliding speeds
- The curve defines how grip changes as sliding speed increases
- Works in combination with `StaticBaseCoefficient` and `SlidingBaseCoefficient`

**Tuning Guidelines:**
- First point: High sliding velocity (negative value, e.g., -7.2)
  - Grip multiplier: Typically 0.3-0.5 (low grip at high sliding speeds)
- Second point: Medium sliding velocity (e.g., -4.2)
  - Grip multiplier: Typically 1.5-2.0 (peak grip during sliding)
- Third point: Low sliding velocity (e.g., -1.2)
  - Grip multiplier: Typically 0.2-0.4 (low grip at low sliding speeds)
- **Increase middle value** for more grip during moderate slides
- **Decrease middle value** for less grip during slides

**Real-World Impact:**
- Higher middle value: Tire maintains more grip during slides, harder to break loose
- Lower middle value: Tire loses grip more quickly when sliding
- Affects how progressive the breakaway is

---

### SlidingMicroDeformationCurve

**Purpose:** Controls grip from micro-deformations (indentation mechanism) as a function of sliding velocity.

**Format:** `SlidingMicroDeformationCurve=(<vel1>, <grip1>, <vel2>, <grip2>, <vel3>, <grip3>)`

**Example from Hybrid Tire:**
```
SlidingMicroDeformationCurve=(-4.2, 0.3, -1.2, 1.8, +1.5, 0.3)
```

**Thesis Information:**
- Based on the indentation mechanism of grip generation
- Rubber asperities compress and relax against road surface
- Energy dissipation from hysteresis creates grip
- Positive velocities can represent different sliding regimes

**Tuning Guidelines:**
- Similar structure to `SlidingAdhesionCurve`
- Middle value (peak) typically 1.5-2.0
- **Increase middle value** for more grip from micro-deformations
- **Decrease middle value** for less grip from micro-deformations
- Affects grip on rough surfaces

**Real-World Impact:**
- Higher values: Better grip on rough surfaces, more grip from tire deformation
- Lower values: Less grip on rough surfaces, more dependent on molecular adhesion

---

### SlidingMacroDeformationCurve

**Purpose:** Controls grip from macro-deformations (large-scale tire deformation) as a function of sliding velocity.

**Format:** `SlidingMacroDeformationCurve=(<vel1>, <grip1>, <vel2>, <grip2>, <vel3>, <grip3>)`

**Example from Hybrid Tire:**
```
SlidingMacroDeformationCurve=(-1.2, 0.2, +1.5, 2, +4.0, 0.4)
```

**Thesis Information:**
- Controls large-scale tire carcass deformation effects
- Works in combination with micro-deformation
- Positive velocities represent different deformation regimes

**Tuning Guidelines:**
- Middle value typically 1.8-2.5
- **Increase middle value** for more grip from carcass deformation
- **Decrease middle value** for less grip from carcass deformation
- Less critical than micro-deformation for most tuning

**Real-World Impact:**
- Higher values: Tire deforms more to maintain grip, better on rough surfaces
- Lower values: Less deformation-based grip, more rigid tire behavior

---

### RubberPressureSensitivityPower

**Purpose:** Controls how grip varies with contact pressure. Higher pressures typically increase grip up to a point, then may decrease.

**Format:** `RubberPressureSensitivityPower=(<exponent>, <coefficient1>, <coefficient2>, <power>)`

**Example from Hybrid Tire:**
```
RubberPressureSensitivityPower=(-35, 9.5e6, 5e5, 1)  // Slightly reduced pressure sensitivity to match target operating pressures
```

**Thesis Information:**
- Defines pressure-grip relationship: `grip = coefficient1 * pressure^power + coefficient2`
- Negative exponent means grip increases with pressure up to a point
- Critical for matching real tire pressure behavior
- Affects how tire responds to load changes

**Tuning Guidelines:**
- First value: Exponent (typically -30 to -40)
  - More negative = more sensitive to pressure changes
- Second value: Primary coefficient (typically 8e6 - 1.2e7)
  - **Increase** for more grip at higher pressures
  - **Decrease** for less grip at higher pressures
- Third value: Offset coefficient (typically 4e5 - 6e5)
- Fourth value: Power (typically 1)
- **To reduce pressure sensitivity:** Decrease second value
- **To increase pressure sensitivity:** Increase second value

**Real-World Impact:**
- Higher sensitivity: Tire grip changes more with pressure variations
- Lower sensitivity: Tire grip is more stable across pressure range
- Must match real tire telemetry data for accurate behavior

---

### StaticRoughnessEffect

**Purpose:** Controls how surface roughness affects static grip. Negative values mean rough surfaces provide more grip.

**Format:** `StaticRoughnessEffect=<value>`

**Example from Hybrid Tire:**
```
StaticRoughnessEffect=-0.2
```

**Thesis Information:**
- Negative values: Rough surfaces provide more grip (realistic)
- Positive values: Smooth surfaces provide more grip (unrealistic)
- Works with diffusive adhesion parameters
- Affects grip on different track surfaces

**Tuning Guidelines:**
- Typical range: -0.3 to -0.1
- **More negative** = rougher surfaces provide significantly more grip
- **Less negative** = less difference between smooth and rough surfaces
- **Zero** = no roughness effect
- **Positive** = smooth surfaces provide more grip (not recommended)

**Real-World Impact:**
- More negative: Better grip on rough surfaces (asphalt), less on smooth (polished concrete)
- Less negative: More uniform grip across different surfaces
- Critical for matching real tire behavior on different track types

---

## Stiffness & Deformation Parameters

### BeltSpringX

**Purpose:** Controls the longitudinal (circumferential) stiffness of the tire belt. Affects how the tire deforms longitudinally under load.

**Format:** `BeltSpringX=(<base>, <pressure_mult>, <temp_mult>, <speed_mult>)`

**Example from Hybrid Tire:**
```
BeltSpringX=(1.5e6, 2.1662, -1866.8077, 1.5448)  // Adjusted for 235mm narrower tire construction
```

**Thesis Information:**
- One of the most critical stiffness parameters
- Total value = base + (pressure_mult * pressure) + (temp_mult * temp) + (speed_mult * speed²)
- Higher values = stiffer tire longitudinally
- Affects braking and acceleration response
- Directly impacts tire transient response

**Tuning Guidelines:**
- **Base value:** Primary stiffness (typical range: 1.0e6 - 2.5e6 N/m)
  - **Increase** for stiffer tire (faster response, less deformation)
  - **Decrease** for softer tire (slower response, more deformation)
- **Pressure multiplier:** How stiffness changes with pressure (typically 1.5-2.5)
- **Temperature multiplier:** How stiffness changes with temperature (typically -1000 to -2000, negative = softer when hot)
- **Speed multiplier:** How stiffness changes with rotational speed (typically 1.0-2.0)
- **For narrower tires:** Reduce base value proportionally
- **For stiffer tire feel:** Increase base value by 10-20%

**Real-World Impact:**
- Higher values: Faster response to load changes, less tire deformation, more direct feel
- Lower values: Slower response, more tire deformation, softer feel
- Critical for matching tire construction characteristics

---

### BeltSpringZ

**Purpose:** Controls the radial (vertical) stiffness of the tire belt. Affects how the tire deforms vertically under load.

**Format:** `BeltSpringZ=(<base>, <pressure_mult>, <temp_mult>, <speed_mult>)`

**Example from Hybrid Tire:**
```
BeltSpringZ=(2.42e6, 2.3551, -1565.643, -0.0148)  // Adjusted for 235mm narrower tire construction
```

**Thesis Information:**
- Controls vertical tire stiffness
- Higher values = stiffer tire vertically
- Affects ride height, load distribution, and contact patch size
- Less critical than BeltSpringX for handling feel

**Tuning Guidelines:**
- **Base value:** Primary stiffness (typical range: 1.5e6 - 3.0e6 N/m)
  - **Increase** for stiffer tire vertically
  - **Decrease** for softer tire vertically
- **Pressure multiplier:** Typically 2.0-2.5
- **Temperature multiplier:** Typically -1500 to -2000
- **Speed multiplier:** Can be negative (typically -0.01 to 0.2)
- **For narrower tires:** Reduce base value proportionally
- **For softer ride:** Decrease base value by 10-15%

**Real-World Impact:**
- Higher values: Less vertical deformation, stiffer ride, smaller contact patch
- Lower values: More vertical deformation, softer ride, larger contact patch
- Affects how tire responds to bumps and curbs

---

### TreadSpringXPerUnitArea

**Purpose:** Controls the longitudinal stiffness of the tread rubber per unit area. Affects how the tread deforms longitudinally.

**Format:** `TreadSpringXPerUnitArea=(<base>, <pressure_mult>, <temp_mult>, <speed_mult>)`

**Example from Hybrid Tire:**
```
TreadSpringXPerUnitArea=(7.5e8, 11.1643, -1.2084e6, -3948.7844)
```

**Thesis Information:**
- One of the most critical parameters for tire response
- Controls tread block stiffness in longitudinal direction
- Higher values = stiffer tread, faster response
- Directly affects braking and acceleration feel
- Per unit area means it scales with contact patch size

**Tuning Guidelines:**
- **Base value:** Primary stiffness (typical range: 6e8 - 1.2e9 N/m²)
  - **Increase** for stiffer tread (faster response, more direct)
  - **Decrease** for softer tread (slower response, more progressive)
- **Pressure multiplier:** Typically 10-15
- **Temperature multiplier:** Typically -1.0e6 to -1.5e6 (negative = softer when hot)
- **Speed multiplier:** Can be negative (typically -3000 to -5000)
- **For more responsive tire:** Increase base value by 10-20%
- **For softer tire:** Decrease base value by 10-20%

**Real-World Impact:**
- Higher values: Faster response to steering/braking inputs, more direct feel, less tire "squish"
- Lower values: Slower response, more progressive feel, more tire deformation
- Critical for matching tire compound characteristics

---

### TreadSpringZPerUnitArea

**Purpose:** Controls the vertical stiffness of the tread rubber per unit area. Affects how the tread deforms vertically.

**Format:** `TreadSpringZPerUnitArea=(<base>, <pressure_mult>, <temp_mult>, <speed_mult>)`

**Example from Hybrid Tire:**
```
TreadSpringZPerUnitArea=(1.141e9, -354.4055, -1.1741e6, -451.2509)
```

**Thesis Information:**
- Controls tread block stiffness in vertical direction
- Higher values = stiffer tread vertically
- Affects contact patch pressure distribution
- Less critical than TreadSpringX for handling feel

**Tuning Guidelines:**
- **Base value:** Primary stiffness (typical range: 8e8 - 1.5e9 N/m²)
  - **Increase** for stiffer tread vertically
  - **Decrease** for softer tread vertically
- **Pressure multiplier:** Can be negative (typically -300 to -400)
- **Temperature multiplier:** Typically -1.0e6 to -1.3e6
- **Speed multiplier:** Typically -400 to -500
- **For stiffer tread:** Increase base value
- **For softer tread:** Decrease base value

**Real-World Impact:**
- Higher values: Less tread deformation, more uniform pressure distribution
- Lower values: More tread deformation, more pressure concentration
- Affects grip on rough surfaces

---

### RingStiffnessMultiplier

**Purpose:** Multiplies the stiffness of the tire ring (carcass) in different directions. Controls overall tire carcass stiffness.

**Format:** `RingStiffnessMultiplier=(<radial>, <lateral>, <longitudinal>, <torsional>, <bending1>, <bending2>)`

**Example from Hybrid Tire:**
```
RingStiffnessMultiplier=(0.90, 1, 1, 1, 1, 1)  // Reduced radial stiffness by 10% for softer feel
```

**Thesis Information:**
- Multiplies the base ring stiffness from the [Node] sections
- Each value affects a different deformation mode
- Values < 1.0 reduce stiffness, values > 1.0 increase stiffness
- First value (radial) is most commonly adjusted

**Tuning Guidelines:**
- **Radial (first value):** Vertical stiffness (typical range: 0.8-1.2)
  - **Decrease** for softer tire (more deformation, better compliance)
  - **Increase** for stiffer tire (less deformation, faster response)
- **Lateral (second value):** Side-to-side stiffness (typically 1.0)
- **Longitudinal (third value):** Fore-aft stiffness (typically 1.0)
- **Torsional (fourth value):** Twist stiffness (typically 1.0)
- **Bending (fifth/sixth values):** Bending stiffness (typically 1.0)
- **For softer tire:** Reduce first value by 5-10%
- **For stiffer tire:** Increase first value by 5-10%

**Real-World Impact:**
- Lower radial value: Softer tire, more compliant, better ride quality, less responsive
- Higher radial value: Stiffer tire, less compliant, harsher ride, more responsive
- Critical for matching tire construction (radial vs bias-ply characteristics)

---

### LoadVsDeflectionMultiplier

**Purpose:** Controls how tire deflection changes with vertical load. Affects the load sensitivity of the tire.

**Format:** `LoadVsDeflectionMultiplier=<value>`

**Example from Hybrid Tire:**
```
LoadVsDeflectionMultiplier=1
```

**Thesis Information:**
- Multiplies the deflection-load relationship
- Value of 1.0 = standard behavior
- Values < 1.0 = less deflection for given load (stiffer)
- Values > 1.0 = more deflection for given load (softer)

**Tuning Guidelines:**
- Typical range: 0.85 - 1.15
- **Decrease** for stiffer tire (less deflection)
- **Increase** for softer tire (more deflection)
- **For load sensitivity tuning:** Adjust in 0.05 increments
- Less commonly adjusted than other stiffness parameters

**Real-World Impact:**
- Lower values: Tire deflects less under load, stiffer feel
- Higher values: Tire deflects more under load, softer feel
- Affects how tire responds to weight transfer

---

## Thermal Parameters

### DampingHeatEnergy

**Purpose:** Controls heat generation from damping/hysteresis effects. Higher values generate more heat from tire deformation.

**Format:** `DampingHeatEnergy=(<adhesion>, <sliding>, <hysteresis>)`

**Example from Hybrid Tire:**
```
DampingHeatEnergy=(0.3, 0.18, 0.45)  // Reduced by ~25% to lower overall heat generation
```

**Thesis Information:**
- First value: Heat from adhesion zone (typically 0.3-0.5)
- Second value: Heat from sliding zone (typically 0.15-0.25)
- Third value: Heat from hysteresis (typically 0.4-0.6)
- Higher values = more heat generation = higher tire temperatures
- Critical for matching real tire temperature profiles

**Tuning Guidelines:**
- **To reduce heat generation:** Decrease all values by 20-30%
- **To increase heat generation:** Increase all values by 20-30%
- **For cooler tires:** Reduce values (e.g., 0.3, 0.18, 0.45)
- **For hotter tires:** Increase values (e.g., 0.5, 0.25, 0.6)
- **To match telemetry:** Adjust based on measured tire temperatures
- All three values should be adjusted proportionally

**Real-World Impact:**
- Lower values: Less heat generation, cooler tires, less thermal degradation
- Higher values: More heat generation, hotter tires, more thermal degradation
- Critical for matching real tire temperature behavior from telemetry

---

### InternalGasHeatTransfer

**Purpose:** Controls heat transfer within the tire (between carcass and internal air). Higher values improve internal heat distribution.

**Format:** `InternalGasHeatTransfer=(<base>, <speed_mult>, <exponent>)`

**Example from Hybrid Tire:**
```
InternalGasHeatTransfer=(6, 5, 0.65)  // Increased to improve internal heat distribution
```

**Thesis Information:**
- Formula: `transfer = base + (speed_mult * speed^exponent)`
- Controls how heat moves from hot spots to cooler areas within the tire
- Higher values = better heat distribution = more uniform temperatures
- Critical for matching real tire temperature distribution (inner vs outer edge)

**Tuning Guidelines:**
- **Base value:** Primary transfer rate (typical range: 4-8)
  - **Increase** for better internal heat distribution
  - **Decrease** for less internal heat distribution
- **Speed multiplier:** How transfer changes with speed (typically 4-6)
- **Exponent:** Typically 0.6-0.7
- **To improve heat distribution:** Increase base value by 20-50%
- **To create hot spots:** Decrease base value

**Real-World Impact:**
- Higher values: More uniform tire temperatures, less hot spots, better heat distribution
- Lower values: More temperature variation across tire, potential hot spots
- Critical for matching real tire inner/outer temperature differences

---

### ExternalGasHeatTransfer

**Purpose:** Controls heat transfer from tire to ambient air (cooling). Higher values increase cooling, especially at speed.

**Format:** `ExternalGasHeatTransfer=(<base>, <speed_mult>, <exponent>)`

**Example from Hybrid Tire:**
```
ExternalGasHeatTransfer=(6.5, 5.0, 0.65)  // Increased base cooling by ~44% to reduce outer edge temps
```

**Thesis Information:**
- Formula: `cooling = base + (speed_mult * speed^exponent)`
- Controls convective cooling to ambient air
- Higher values = more cooling = lower tire temperatures
- Critical for matching real tire cooling behavior on straights
- For open-wheel cars, values are typically higher (more airflow)

**Tuning Guidelines:**
- **Base value:** Primary cooling rate (typical range: 4-8)
  - **Increase** for more cooling (cooler tires)
  - **Decrease** for less cooling (hotter tires)
- **Speed multiplier:** How cooling changes with speed (typically 4-6)
  - Higher values = more cooling at speed (important for straights)
- **Exponent:** Typically 0.6-0.7
  - Higher values = cooling increases more with speed
- **To reduce outer edge temps:** Increase base value by 30-50%
- **To match telemetry:** Adjust based on measured cooling rates on straights

**Real-World Impact:**
- Higher values: More cooling, especially at speed, cooler tires on straights
- Lower values: Less cooling, hotter tires, slower temperature drop on straights
- Critical for matching real tire temperature profiles from telemetry

---

### GroundConductance

**Purpose:** Controls heat transfer from tire to track surface via conduction. Higher values increase heat loss to the track.

**Format:** `GroundConductance=(<base>, <pressure_mult>, <offset>)`

**Example from Hybrid Tire:**
```
GroundConductance=(800, 0.025, 0)  // Increased base conductance by ~26% to cool outer edge
```

**Thesis Information:**
- Formula: `conductance = base + (pressure_mult * contact_pressure)`
- Controls conductive heat transfer to track surface
- Higher values = more heat loss to track = cooler tire surface
- Critical for matching real tire surface temperatures
- The second value multiplies contact pressure (higher pressure = more heat transfer)

**Tuning Guidelines:**
- **Base value:** Primary conductance (typical range: 600-1200)
  - **Increase** for more heat loss to track (cooler surface temps)
  - **Decrease** for less heat loss to track (hotter surface temps)
- **Pressure multiplier:** How conductance changes with pressure (typical range: 0.015-0.030)
  - **Increase** for more pressure-dependent cooling
  - **Decrease** for less pressure-dependent cooling
- **To reduce surface temps:** Increase base value by 20-30%
- **To match telemetry:** Adjust based on measured surface temperatures

**Real-World Impact:**
- Higher values: More heat lost to track, cooler tire surface, better cooling in contact patch
- Lower values: Less heat lost to track, hotter tire surface, less cooling
- Critical for matching real tire surface temperature measurements

---

### ThermalDepthAtSurface

**Purpose:** Defines the thermal depth at the tire surface for temperature calculations.

**Format:** `ThermalDepthAtSurface=<value>`

**Example from Hybrid Tire:**
```
ThermalDepthAtSurface=0.0001
```

**Tuning Guidelines:**
- Typical range: 0.00005 - 0.0002 meters
- Smaller values = thinner thermal layer = faster temperature changes
- Larger values = thicker thermal layer = slower temperature changes
- Rarely adjusted, typically left at default

---

### ThermalDepthBelowSurface

**Purpose:** Defines the thermal depth below the tire surface for internal temperature calculations.

**Format:** `ThermalDepthBelowSurface=<value>`

**Example from Hybrid Tire:**
```
ThermalDepthBelowSurface=0.0004
```

**Tuning Guidelines:**
- Typical range: 0.0002 - 0.0006 meters
- Should be larger than `ThermalDepthAtSurface`
- Rarely adjusted, typically left at default

---

## Distribution & Multiplier Parameters

### LateralDistributionMultiplier

**Purpose:** Controls how forces are distributed laterally across the tire contact patch. Affects heat distribution and grip characteristics.

**Format:** `LateralDistributionMultiplier=<value>`

**Example from Hybrid Tire:**
```
LateralDistributionMultiplier=0.755
```

**Thesis Information:**
- Values < 1.0 distribute forces more evenly across the contact patch
- Values = 1.0 use standard distribution
- Critical for preventing hot spots and rollover issues
- Lower values help distribute heat laterally (prevent outer edge overheating)

**Tuning Guidelines:**
- Typical range: 0.7 - 1.0
- **Decrease** for more even lateral force distribution (prevents hot spots)
- **Increase** for more concentrated force distribution
- **For rollover prevention:** Reduce to 0.75-0.80
- **For hot spot prevention:** Reduce to 0.70-0.75

**Real-World Impact:**
- Lower values: More even heat distribution, less outer edge overheating, better for preventing rollover
- Higher values: More concentrated forces, potential hot spots, can contribute to rollover
- Critical parameter for tire stability

---

### LongitudinalDistributionMultiplier

**Purpose:** Controls how forces are distributed longitudinally across the tire contact patch.

**Format:** `LongitudinalDistributionMultiplier=<value>`

**Example from Hybrid Tire:**
```
LongitudinalDistributionMultiplier=0.535
```

**Tuning Guidelines:**
- Typical range: 0.5 - 1.0
- **Decrease** for more even longitudinal force distribution
- **Increase** for more concentrated force distribution
- Less critical than lateral distribution

**Real-World Impact:**
- Lower values: More even force distribution longitudinally
- Higher values: More concentrated forces

---

### SizeMultiplier

**Purpose:** Adjusts tire size scaling factors. Used to account for differences between modeled tire and actual tire dimensions.

**Format:** `SizeMultiplier=(<width_mult>, <diameter_mult>)`

**Example from Hybrid Tire:**
```
SizeMultiplier=(0.938, 0.992)  // Adjusted for 235mm width vs 250mm baseline
```

**Tuning Guidelines:**
- First value: Width multiplier (typical range: 0.9-1.1)
- Second value: Diameter multiplier (typical range: 0.95-1.05)
- **For narrower tire:** Reduce first value proportionally
- **For wider tire:** Increase first value proportionally
- Used to match actual tire dimensions to model

**Real-World Impact:**
- Adjusts contact patch size and tire geometry scaling
- Critical for matching real tire dimensions

---

### MassInertiaMultiplier

**Purpose:** Multiplies tire mass and inertia properties. Affects tire rotational dynamics.

**Format:** `MassInertiaMultiplier=(<mass>, <inertia_x>, <inertia_y>, <inertia_z>)`

**Example from Hybrid Tire:**
```
MassInertiaMultiplier=(1, 1, 1, 1)
```

**Tuning Guidelines:**
- Typically left at (1, 1, 1, 1)
- Rarely adjusted
- Only change if tire mass/inertia measurements differ significantly from model

---

## Wear & Degradation Parameters

### AbrasionVolumePerUnitEnergy

**Purpose:** Defines how much rubber is abraded (worn away) per unit of energy dissipated. Controls tire wear rate.

**Format:** `AbrasionVolumePerUnitEnergy=(<value1>, <value2>, ..., <value32>)`

**Example from Hybrid Tire:**
```
AbrasionVolumePerUnitEnergy=(3.26E-10,2.76e-10,2.31e-10,2.01e-10,1.74e-10,1.51e-10,1.27e-10,1.06e-10,8.71e-11,6.85e-11,5.43e-11,4.45e-11,3.6e-11,3.14e-11,2.94e-11,2.86e-11,2.91e-11,3.03e-11,3.23e-11,3.51e-11,3.94e-11,4.57e-11,5.23e-11,5.91e-11,6.65e-11,7.85e-11,9.42e-11,1.17e-10,1.51e-10,1.97e-10,2.28e-10,2.57e-10)
```

**Thesis Information:**
- Array of 32 values defining wear rate at different conditions
- Values typically decrease then increase (U-shaped curve)
- Lower values = less wear
- Higher values = more wear
- Rarely adjusted, typically compound-specific

**Tuning Guidelines:**
- Typically left at default values
- Only adjust if specific wear characteristics need to be matched
- Requires extensive testing to validate changes

---

### DegradationPerWearFraction

**Purpose:** Defines how tire performance degrades as wear increases. Controls grip loss with wear.

**Format:** `DegradationPerWearFraction=(<value1>, <value2>, ..., <value32>)`

**Example from Hybrid Tire:**
```
DegradationPerWearFraction=(0.99,1,0.999,0.9976,0.9966,0.9957,0.9949,0.9942,0.9936,0.993,0.9925,0.992,0.9915,0.991,0.9905,0.99,0.9895,0.989,0.9885,0.988,0.9875,0.987,0.9865,0.986,0.9855,0.985,0.9845,0.984,0.9834,0.982,0.96,0.84)
```

**Tuning Guidelines:**
- Array of 32 values (0.0-1.0) defining grip multiplier at different wear levels
- Values start near 1.0 (no wear) and decrease with wear
- Lower values = more grip loss with wear
- Typically left at default values

---

### DegradationCurveParameters

**Purpose:** Parameters for the degradation curve calculation.

**Format:** `DegradationCurveParameters=(<param1>, <param2>)`

**Example from Hybrid Tire:**
```
DegradationCurveParameters=(342.65, 6978.125)
```

**Tuning Guidelines:**
- Rarely adjusted
- Typically left at default values

---

### DegradationPerUnitHistory

**Purpose:** Defines how tire performance degrades based on usage history (thermal cycles, etc.).

**Format:** `DegradationPerUnitHistory=(<value1>, <value2>, ..., <value32>)`

**Example from Hybrid Tire:**
```
DegradationPerUnitHistory=(1,0.98,0.968,0.96,0.956,0.9535,0.9512,0.949,0.9469,0.9449,0.943,0.9411,0.9392,0.9373,0.9354,0.9335,0.9316,0.9297,0.9278,0.9259,0.924,0.9221,0.9202,0.9183,0.9164,0.9144,0.9122,0.9096,0.9064,0.902,0.896,0.89)
```

**Tuning Guidelines:**
- Array of 32 values defining grip multiplier based on usage
- Values decrease with usage (thermal cycles, etc.)
- Typically left at default values

---

## Terrain & Surface Parameters

### TerrainWeightOnContactTemperature

**Purpose:** Controls how much the track surface temperature affects tire contact temperature.

**Format:** `TerrainWeightOnContactTemperature=<value>`

**Example from Hybrid Tire:**
```
TerrainWeightOnContactTemperature=0.05  // 0.1 before
```

**Tuning Guidelines:**
- Typical range: 0.0 - 0.2
- **Increase** for more track temperature influence
- **Decrease** for less track temperature influence
- Lower values = tire temperature less affected by track temperature

**Real-World Impact:**
- Higher values: Tire temperature more affected by hot/cold track
- Lower values: Tire temperature less affected by track temperature

---

### DryTerrainEffect, WetTerrainEffect, etc.

**Purpose:** Defines grip multipliers for different terrain types.

**Format:** `TerrainEffect=(<min_grip>, <max_grip>, <multiplier>)`

**Example from Hybrid Tire:**
```
DryTerrainEffect=(0,1,1)
WetTerrainEffect=(0,1,0.5)
GrassTerrainEffect=(0,1,0.067)
DirtTerrainEffect=(0,1,0.1)
GravelTerrainEffect=(0,1,0.1)
RumbleTerrainEffect=(0,1,1)
SpecialTerrainEffect=(0,1,1)
```

**Tuning Guidelines:**
- Third value is the grip multiplier for that terrain type
- 1.0 = full grip, 0.5 = 50% grip, etc.
- Typically left at default values unless specific terrain behavior needs adjustment

---

### GrooveEffects

**Purpose:** Controls how tire grooves affect grip on wet surfaces.

**Format:** `GrooveEffects=(<value1>, <value2>, <value3>, <value4>)`

**Example from Hybrid Tire:**
```
GrooveEffects=(0.083, 0.083, 0.068, 0.041)
```

**Tuning Guidelines:**
- Typically left at default values
- Only adjust for specific wet weather tire behavior

---

### DampnessEffects

**Purpose:** Controls grip reduction on damp/wet surfaces.

**Format:** `DampnessEffects=(<value1>, <value2>, <value3>, <value4>)`

**Example from Hybrid Tire:**
```
DampnessEffects=(-0.25, -0.4, -0.25, -0.1)
```

**Tuning Guidelines:**
- Negative values = grip reduction
- More negative = more grip loss on wet
- Typically left at default values

---

### TemporaryGripLossForWetness

**Purpose:** Additional grip loss multiplier for wet conditions.

**Format:** `TemporaryGripLossForWetness=<value>`

**Example from Hybrid Tire:**
```
TemporaryGripLossForWetness=0.22
```

**Tuning Guidelines:**
- Typical range: 0.15 - 0.30
- Higher values = more grip loss on wet
- Typically left at default values

---

## Internal Gas Parameters

### InternalGasMolarMass

**Purpose:** Molar mass of the internal gas (typically air or nitrogen).

**Format:** `InternalGasMolarMass=<value>`

**Example from Hybrid Tire:**
```
InternalGasMolarMass=0.028884
```

**Tuning Guidelines:**
- 0.028884 = air
- 0.028 = nitrogen
- Rarely adjusted

---

### InternalGasSpecificHeatAtConstantVolume

**Purpose:** Defines specific heat capacity of internal gas at different temperatures.

**Format:** `InternalGasSpecificHeatAtConstantVolume=(<temp_K>, <specific_heat>)`

**Example from Hybrid Tire:**
```
InternalGasSpecificHeatAtConstantVolume=(250,720.7)
InternalGasSpecificHeatAtConstantVolume=(300,722.9)
InternalGasSpecificHeatAtConstantVolume=(350,726.7)
InternalGasSpecificHeatAtConstantVolume=(400,732.8)
InternalGasSpecificHeatAtConstantVolume=(450,741.2)
InternalGasSpecificHeatAtConstantVolume=(500,752.4)
```

**Tuning Guidelines:**
- Multiple entries define temperature-dependent specific heat
- Typically left at default values (air properties)
- Only adjust if using different gas (e.g., nitrogen)

---

### GaugePressureExtrapolationRange

**Purpose:** Defines the pressure range for extrapolation beyond lookup table limits.

**Format:** `GaugePressureExtrapolationRange=(<min_Pa>, <max_Pa>)`

**Example from Hybrid Tire:**
```
GaugePressureExtrapolationRange=(0,270000)
```

**Tuning Guidelines:**
- Defines valid pressure range (0 to 270000 Pa = 0 to 2.7 bar)
- Adjust if tire operates outside this range
- Typically left at default

---

### CarcassTemperatureExtrapolationRange

**Purpose:** Defines the temperature range for extrapolation beyond lookup table limits.

**Format:** `CarcassTemperatureExtrapolationRange=(<min_K>, <max_K>)`

**Example from Hybrid Tire:**
```
CarcassTemperatureExtrapolationRange=(268.15,423.15)
```

**Tuning Guidelines:**
- Defines valid temperature range (268.15K = -5°C to 423.15K = 150°C)
- Adjust if tire operates outside this range
- Typically left at default

---

### RotationSquaredExtrapolationRange

**Purpose:** Defines the rotational speed range for extrapolation beyond lookup table limits.

**Format:** `RotationSquaredExtrapolationRange=(<min>, <max>)`

**Example from Hybrid Tire:**
```
RotationSquaredExtrapolationRange=(0,47000)
```

**Tuning Guidelines:**
- Defines valid rotational speed range
- Adjust if tire operates outside this range
- Typically left at default

---

## Tuning Guidelines

### General Tuning Philosophy

1. **Start with grip parameters** (`StaticBaseCoefficient`, `SlidingBaseCoefficient`)
2. **Adjust thermal parameters** to match telemetry data
3. **Fine-tune stiffness parameters** for feel and response
4. **Test incrementally** - make small changes (5-10%) and test
5. **Use telemetry data** as reference when available

### Parameter Interaction

- **Grip parameters** affect overall tire performance
- **Thermal parameters** affect tire temperatures and must be balanced with grip
- **Stiffness parameters** affect tire response and feel
- **Distribution parameters** affect heat distribution and stability

### Common Tuning Scenarios

#### Matching Real Tire Telemetry

1. **Temperature matching:**
   - Adjust `DampingHeatEnergy` to match heat generation
   - Adjust `ExternalGasHeatTransfer` to match cooling rates
   - Adjust `GroundConductance` to match surface temperatures
   - Adjust `InternalGasHeatTransfer` to match temperature distribution

2. **Grip matching:**
   - Adjust `StaticBaseCoefficient` and `SlidingBaseCoefficient` to match friction coefficients
   - Adjust `StaticCurve` to match optimal operating temperature
   - Adjust `RubberPressureSensitivityPower` to match pressure behavior

3. **Stability:**
   - Adjust `LateralDistributionMultiplier` to prevent rollover/hot spots
   - Adjust stiffness parameters for desired feel

#### Reducing Rollover Issues

1. **Reduce `LateralDistributionMultiplier`** to 0.75-0.80
2. **Reduce stiffness parameters** by 5-10% if tire feels too stiff
3. **Check `StaticBaseCoefficient`** - may be too high

#### Matching Real Tire Telemetry (Example)

Based on actual tuning work to match real tire telemetry data:

```
StaticBaseCoefficient=3.75          // Reduced by ~6%
SlidingBaseCoefficient=2.68         // Reduced by ~5.5%
StaticCurve=(273, 0.6, 360, 1.0, 420, 0.7)  // Peak at 360K (87°C)
DampingHeatEnergy=(0.3, 0.18, 0.45)  // Reduced by ~25%
InternalGasHeatTransfer=(6, 5, 0.65)  // Increased
ExternalGasHeatTransfer=(6.5, 5.0, 0.65)  // Increased by ~44%
GroundConductance=(800, 0.025, 0)   // Increased by ~26%
RubberPressureSensitivityPower=(-35, 9.5e6, 5e5, 1)  // Reduced
```

### Testing Procedure

1. **Off-line tests** (tTool):
   - Sweep tests for lateral force
   - Longitudinal tests for braking/acceleration
   - Compare with target curves (.tir file if available)

2. **On-line tests** (Simulator):
   - Test at specific track conditions
   - Collect telemetry data (temperatures, pressures, forces)
   - Compare with real tire data
   - Driver feedback on feel and behavior

3. **Iterative refinement:**
   - Make small adjustments (5-10%)
   - Test and compare
   - Refine based on results

### Parameter Priority for Tuning

**High Priority (Most Critical):**
1. `StaticBaseCoefficient` / `SlidingBaseCoefficient` - Overall grip
2. `StaticCurve` - Temperature-grip relationship
3. `DampingHeatEnergy` - Heat generation
4. `ExternalGasHeatTransfer` - Cooling
5. `GroundConductance` - Surface temperature
6. `LateralDistributionMultiplier` - Stability

**Medium Priority:**
1. `BeltSpringX` / `TreadSpringXPerUnitArea` - Response feel
2. `InternalGasHeatTransfer` - Temperature distribution
3. `RubberPressureSensitivityPower` - Pressure behavior
4. `RingStiffnessMultiplier` - Overall stiffness

**Low Priority (Rarely Adjusted):**
1. Wear/degradation parameters
2. Terrain parameters
3. Internal gas parameters
4. Extrapolation ranges

---

## References

- University Thesis: "Optimisation of the tyre model in rFactor2 environment for AVEHIL professional simulator" (2018/2019)
- rFactor2 TGM Tyre Tool Quick Start Guide
- Practical tire development experience with DUN-235-610R17_Hybrid.tgm

---

**Document Version:** 1.0  
**Last Updated:** Based on Hybrid tire development and real tire telemetry matching work

