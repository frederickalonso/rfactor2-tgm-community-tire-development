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

**Typical Values:**
- **Minimum:** 2.5 (low grip, slippery tire)
- **Typical:** 3.5 - 4.0 (standard racing tire)
- **Maximum:** 4.5 (very high grip, may overheat)

**Example:**
```
StaticBaseCoefficient=3.75
```

**Thesis Information:**
- One of the most critical parameters for overall tire grip
- Directly affects lateral and longitudinal force generation
- Works in combination with `SlidingBaseCoefficient` to define the friction envelope

**Tuning Guidelines:**
- **Range:** 2.5 - 4.5
- **Typical adjustments:** ±5-10% for fine-tuning
- **Increase:** More grip, better cornering, shorter braking distances, more responsive steering
  - **Effect:** Higher friction coefficient, tire grips better but may overheat if too high
- **Decrease:** Less grip, more sliding, longer braking distances, less responsive steering
  - **Effect:** Lower friction coefficient, more progressive breakaway, less prone to overheating
- Must be balanced with thermal parameters to avoid overheating

---

### SlidingBaseCoefficient

**Purpose:** Base friction coefficient for sliding conditions. Controls grip when the tire is sliding (beyond the adhesion limit).

**Format:** `SlidingBaseCoefficient=<value>`

**Typical Values:**
- **Minimum:** 1.5 (low sliding grip, easy to break loose)
- **Typical:** 2.3 - 2.8 (standard racing tire, ~65-70% of StaticBaseCoefficient)
- **Maximum:** 3.5 (high sliding grip, hard to break loose)

**Example:**
```
SlidingBaseCoefficient=2.68
```

**Thesis Information:**
- Typically 60-75% of `StaticBaseCoefficient` value
- Affects behavior when tire exceeds adhesion limit
- Important for drift behavior and recovery from slides

**Tuning Guidelines:**
- **Range:** 1.5 - 3.5
- **Ratio to StaticBaseCoefficient:** Typically 0.65-0.75 (should be proportional)
- **Increase:** More grip during slides, harder to break loose, tire maintains grip when sliding
  - **Effect:** More progressive breakaway, better recovery from slides
- **Decrease:** Less grip during slides, easier to break loose, more progressive slide
  - **Effect:** Tire slides more easily, more predictable breakaway behavior
- Affects how the tire recovers from oversteer/understeer situations

---

### StaticDiffusiveAdhesion

**Purpose:** Controls the diffusive adhesion component of static grip. This parameter affects how grip is distributed across the contact patch based on molecular adhesion mechanisms.

**Format:** `StaticDiffusiveAdhesion=(<min_velocity>, <max_force>, <exponent>)`

**Typical Values:**
- **First value (min_velocity):** 0.001 (fixed, rarely changed)
- **Second value (max_force):**
  - **Minimum:** 8000 (low grip on smooth surfaces)
  - **Typical:** 10000 - 12000 (standard racing tire)
  - **Maximum:** 15000 (high grip on smooth surfaces)
- **Third value (exponent):** 0.7 - 0.8 (typically 0.75)

**Example:**
```
StaticDiffusiveAdhesion=(0.001, 11200, 0.75)
```

**Thesis Information:**
- Based on molecular adhesion theory (Van der Waals bonding)
- The second value (max_force) is the maximum adhesion force
- The exponent controls the velocity-dependent behavior
- Higher values increase grip, especially on smooth surfaces

**Tuning Guidelines:**
- **First value:** Minimum sliding velocity threshold (typically 0.001, rarely adjusted)
- **Second value (max_force):**
  - **Range:** 8000 - 15000
  - **Increase:** More grip on smooth surfaces, better low-speed grip, better molecular adhesion
  - **Decrease:** Less grip on smooth surfaces, more dependent on surface roughness
  - **For wider tires:** Increase proportionally to tire width
- **Third value (exponent):**
  - **Range:** 0.7 - 0.8
  - **Increase:** More velocity-dependent behavior
  - **Decrease:** Less velocity-dependent behavior

**Real-World Impact:**
- Higher max_force: Better grip on smooth surfaces, better low-speed grip
- Lower max_force: Less grip on smooth surfaces, more dependent on surface roughness

---

### SlidingDiffusiveAdhesion

**Purpose:** Controls the diffusive adhesion component during sliding conditions.

**Format:** `SlidingDiffusiveAdhesion=(<min_velocity>, <max_force>, <exponent>)`

**Typical Values:**
- **First value (min_velocity):** 0.001 (fixed, rarely changed)
- **Second value (max_force):**
  - **Minimum:** 1500 (low grip during slides)
  - **Typical:** 1700 - 2000 (standard racing tire, ~15-20% of StaticDiffusiveAdhesion)
  - **Maximum:** 2500 (high grip during slides)
- **Third value (exponent):** 0.7 - 0.8 (typically 0.75)

**Example:**
```
SlidingDiffusiveAdhesion=(0.001, 1900, 0.75)
```

**Thesis Information:**
- Similar to `StaticDiffusiveAdhesion` but for sliding conditions
- Typically 15-20% of the static value
- Affects grip maintenance during slides

**Tuning Guidelines:**
- **First value:** Minimum sliding velocity threshold (typically 0.001, rarely adjusted)
- **Second value (max_force):**
  - **Range:** 1500 - 2500
  - **Increase:** More grip during slides, tire maintains grip better when sliding
  - **Decrease:** Less grip during slides, tire loses grip more quickly when sliding
  - **Should be proportional:** Typically 15-20% of `StaticDiffusiveAdhesion` value
- **Third value (exponent):**
  - **Range:** 0.7 - 0.8
  - Same as `StaticDiffusiveAdhesion` for consistency

**Real-World Impact:**
- Higher max_force: Tire maintains more grip when sliding, better recovery from slides
- Lower max_force: Tire loses grip more quickly when sliding, more progressive breakaway

---

### StaticCurve

**Purpose:** Defines how static friction coefficient varies with carcass temperature. This is a critical parameter for tire warm-up behavior and optimal operating temperature.

**Format:** `StaticCurve=(<temp1_K>, <grip1>, <temp2_K>, <grip2>, <temp3_K>, <grip3>)`

**Typical Values:**
- **Temp1 (cold tire):** 273K (0°C) - fixed
  - **Grip1 range:** 0.3 - 0.7
  - **Typical:** 0.5 - 0.6 (lower grip when cold)
- **Temp2 (optimal temp):** 340K - 400K (67°C - 127°C)
  - **Typical:** 360K - 380K (87°C - 107°C)
  - **Grip2 range:** 1.0 - 1.2
  - **Typical:** 1.0 (peak performance)
- **Temp3 (overheated):** 420K - 450K (147°C - 177°C)
  - **Grip3 range:** 0.6 - 0.8
  - **Typical:** 0.7 (reduced grip when overheated)

**Example:**
```
StaticCurve=(273, 0.6, 360, 1.0, 420, 0.7)
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
- **Temp1 (K):** Cold tire temperature (typically 273K = 0°C, fixed)
  - **Grip1:**
    - **Range:** 0.3 - 0.7
    - **Increase:** More grip when cold, easier to drive on cold tires (less realistic)
    - **Decrease:** Less grip when cold, more realistic cold tire behavior, requires proper warm-up
- **Temp2 (K):** Optimal operating temperature (**most critical value**)
  - **Range:** 340K - 400K (67°C - 127°C)
  - **Typical:** 360K - 380K (87°C - 107°C)
  - **Grip2:**
    - **Range:** 1.0 - 1.2
    - **Increase:** Higher peak grip, but may overheat more easily
    - **Decrease:** Lower peak grip, but more stable
  - **Increase Temp2:** Tire performs best at higher temperatures (harder to warm up, more resistant to overheating)
  - **Decrease Temp2:** Tire performs best at lower temperatures (easier to warm up, less resistant to overheating)
- **Temp3 (K):** Overheated temperature
  - **Range:** 420K - 450K (147°C - 177°C)
  - **Grip3:**
    - **Range:** 0.6 - 0.8
    - **Increase:** More grip retention when overheated
    - **Decrease:** Less grip retention when overheated

**Real-World Impact:**
- Lower Temp2: Tire performs best at lower temperatures (easier to warm up)
- Higher Temp2: Tire performs best at higher temperatures (harder to warm up, more resistant to overheating)
- Lower Grip1: More realistic cold tire behavior, requires proper warm-up
- Higher Grip1: Easier to drive on cold tires (less realistic)

**Example Configurations:**
- **Cold tire behavior:** `(273, 0.3, 373, 1.0, 673, 0.3)` - Very slippery when cold
- **High temp tire:** `(273, 0.6, 400, 1.2, 450, 0.7)` - Performs best at high temperatures
- **Low temp tire:** `(273, 0.6, 340, 1.0, 400, 0.7)` - Performs best at lower temperatures

---

### SlidingAdhesionCurve

**Purpose:** Defines how sliding friction varies with sliding velocity. Controls grip behavior when tire is sliding.

**Format:** `SlidingAdhesionCurve=(<vel1>, <grip1>, <vel2>, <grip2>, <vel3>, <grip3>)`

**Example:**
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

**Example:**
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

**Example:**
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

**Typical Values:**
- **First value (exponent):**
  - **Range:** -40 to -30
  - **Typical:** -35 to -38
- **Second value (coefficient1):**
  - **Range:** 8e6 - 1.2e7
  - **Typical:** 9e6 - 1.1e7
- **Third value (coefficient2):**
  - **Range:** 4e5 - 6e5
  - **Typical:** 5e5
- **Fourth value (power):** 1 (fixed)

**Example:**
```
RubberPressureSensitivityPower=(-35, 9.5e6, 5e5, 1)
```

**Thesis Information:**
- Defines pressure-grip relationship: `grip = coefficient1 * pressure^power + coefficient2`
- Negative exponent means grip increases with pressure up to a point
- Critical for matching real tire pressure behavior
- Affects how tire responds to load changes

**Tuning Guidelines:**
- **First value (exponent):**
  - **Range:** -40 to -30
  - **Increase (less negative):** Less sensitive to pressure changes
  - **Decrease (more negative):** More sensitive to pressure changes
- **Second value (coefficient1):**
  - **Range:** 8e6 - 1.2e7
  - **Increase:** More grip at higher pressures, higher pressure sensitivity
  - **Decrease:** Less grip at higher pressures, lower pressure sensitivity
- **Third value (coefficient2):**
  - **Range:** 4e5 - 6e5
  - **Typical:** 5e5 (rarely adjusted)
- **Fourth value (power):** 1 (fixed, rarely changed)
- **To reduce pressure sensitivity:** Decrease second value or increase first value (less negative)
- **To increase pressure sensitivity:** Increase second value or decrease first value (more negative)

**Real-World Impact:**
- Higher sensitivity: Tire grip changes more with pressure variations, more responsive to load changes
- Lower sensitivity: Tire grip is more stable across pressure range, less responsive to load changes
- Must match real tire telemetry data for accurate behavior

---

### StaticRoughnessEffect

**Purpose:** Controls how surface roughness affects static grip. Negative values mean rough surfaces provide more grip.

**Format:** `StaticRoughnessEffect=<value>`

**Typical Values:**
- **Range:** -0.3 to -0.1
- **Typical:** -0.15 to -0.25
- **Minimum:** -0.3 (strong roughness effect)
- **Maximum:** -0.1 (weak roughness effect)

**Example:**
```
StaticRoughnessEffect=-0.2
```

**Thesis Information:**
- Negative values: Rough surfaces provide more grip (realistic)
- Positive values: Smooth surfaces provide more grip (unrealistic)
- Works with diffusive adhesion parameters
- Affects grip on different track surfaces

**Tuning Guidelines:**
- **Range:** -0.3 to -0.1
- **Increase (less negative):** Less difference between smooth and rough surfaces, more uniform grip
- **Decrease (more negative):** Rougher surfaces provide significantly more grip, better grip on asphalt
- **Zero:** No roughness effect (not realistic)
- **Positive:** Smooth surfaces provide more grip (not recommended, unrealistic)

**Real-World Impact:**
- More negative: Better grip on rough surfaces (asphalt), less on smooth (polished concrete)
- Less negative: More uniform grip across different surfaces
- Critical for matching real tire behavior on different track types

---

## Stiffness & Deformation Parameters

### BeltSpringX

**Purpose:** Controls the longitudinal (circumferential) stiffness of the tire belt. Affects how the tire deforms longitudinally under load.

**Format:** `BeltSpringX=(<base>, <pressure_mult>, <temp_mult>, <speed_mult>)`

**Typical Values:**
- **Base value:**
  - **Range:** 1.0e6 - 2.5e6 N/m
  - **Typical:** 1.5e6 - 2.0e6 N/m
- **Pressure multiplier:**
  - **Range:** 1.5 - 2.5
  - **Typical:** 2.0 - 2.2
- **Temperature multiplier:**
  - **Range:** -2000 to -1000 (negative = softer when hot)
  - **Typical:** -1500 to -1800
- **Speed multiplier:**
  - **Range:** 1.0 - 2.0
  - **Typical:** 1.5 - 1.8

**Example:**
```
BeltSpringX=(1.5e6, 2.1662, -1866.8077, 1.5448)
```

**Thesis Information:**
- One of the most critical stiffness parameters
- Total value = base + (pressure_mult * pressure) + (temp_mult * temp) + (speed_mult * speed²)
- Higher values = stiffer tire longitudinally
- Affects braking and acceleration response
- Directly impacts tire transient response

**Tuning Guidelines:**
- **Base value:**
  - **Range:** 1.0e6 - 2.5e6 N/m
  - **Increase:** Stiffer tire longitudinally, faster response to load changes, less tire deformation, more direct feel
  - **Decrease:** Softer tire longitudinally, slower response, more tire deformation, softer feel
  - **For narrower tires:** Reduce proportionally to tire width
  - **For stiffer tire feel:** Increase by 10-20%
- **Pressure multiplier:**
  - **Range:** 1.5 - 2.5
  - **Increase:** Stiffness increases more with pressure
  - **Decrease:** Stiffness increases less with pressure
- **Temperature multiplier:**
  - **Range:** -2000 to -1000 (negative = softer when hot)
  - **Increase (less negative):** Less temperature sensitivity
  - **Decrease (more negative):** More temperature sensitivity, tire gets softer more when hot
- **Speed multiplier:**
  - **Range:** 1.0 - 2.0
  - **Increase:** Stiffness increases more with rotational speed
  - **Decrease:** Stiffness increases less with rotational speed

**Real-World Impact:**
- Higher base: Faster response to load changes, less tire deformation, more direct feel, better braking/acceleration response
- Lower base: Slower response, more tire deformation, softer feel, more progressive response
- Critical for matching tire construction characteristics

---

### BeltSpringZ

**Purpose:** Controls the radial (vertical) stiffness of the tire belt. Affects how the tire deforms vertically under load.

**Format:** `BeltSpringZ=(<base>, <pressure_mult>, <temp_mult>, <speed_mult>)`

**Typical Values:**
- **Base value:**
  - **Range:** 1.5e6 - 3.0e6 N/m
  - **Typical:** 2.0e6 - 2.5e6 N/m
- **Pressure multiplier:**
  - **Range:** 2.0 - 2.5
  - **Typical:** 2.2 - 2.4
- **Temperature multiplier:**
  - **Range:** -2000 to -1500 (negative = softer when hot)
  - **Typical:** -1500 to -1800
- **Speed multiplier:**
  - **Range:** -0.01 to 0.2 (can be negative)
  - **Typical:** -0.01 to 0.1

**Example:**
```
BeltSpringZ=(2.42e6, 2.3551, -1565.643, -0.0148)
```

**Thesis Information:**
- Controls vertical tire stiffness
- Higher values = stiffer tire vertically
- Affects ride height, load distribution, and contact patch size
- Less critical than BeltSpringX for handling feel

**Tuning Guidelines:**
- **Base value:**
  - **Range:** 1.5e6 - 3.0e6 N/m
  - **Increase:** Stiffer tire vertically, less vertical deformation, stiffer ride, smaller contact patch
  - **Decrease:** Softer tire vertically, more vertical deformation, softer ride, larger contact patch
  - **For narrower tires:** Reduce proportionally to tire width
  - **For softer ride:** Decrease by 10-15%
- **Pressure multiplier:**
  - **Range:** 2.0 - 2.5
  - **Increase:** Vertical stiffness increases more with pressure
  - **Decrease:** Vertical stiffness increases less with pressure
- **Temperature multiplier:**
  - **Range:** -2000 to -1500
  - **Increase (less negative):** Less temperature sensitivity
  - **Decrease (more negative):** More temperature sensitivity
- **Speed multiplier:**
  - **Range:** -0.01 to 0.2
  - **Increase:** Stiffness increases more with speed (or decreases less if negative)
  - **Decrease:** Stiffness increases less with speed

**Real-World Impact:**
- Higher base: Less vertical deformation, stiffer ride, smaller contact patch, better response to bumps
- Lower base: More vertical deformation, softer ride, larger contact patch, more compliant over bumps and curbs
- Affects how tire responds to bumps and curbs

---

### TreadSpringXPerUnitArea

**Purpose:** Controls the longitudinal stiffness of the tread rubber per unit area. Affects how the tread deforms longitudinally.

**Format:** `TreadSpringXPerUnitArea=(<base>, <pressure_mult>, <temp_mult>, <speed_mult>)`

**Typical Values:**
- **Base value:**
  - **Range:** 6e8 - 1.2e9 N/m²
  - **Typical:** 7e8 - 1.0e9 N/m²
- **Pressure multiplier:**
  - **Range:** 10 - 15
  - **Typical:** 11 - 13
- **Temperature multiplier:**
  - **Range:** -1.5e6 to -1.0e6 (negative = softer when hot)
  - **Typical:** -1.1e6 to -1.3e6
- **Speed multiplier:**
  - **Range:** -5000 to -3000 (negative)
  - **Typical:** -3500 to -4500

**Example:**
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
- **Base value:**
  - **Range:** 6e8 - 1.2e9 N/m²
  - **Increase:** Stiffer tread longitudinally, faster response to steering/braking inputs, more direct feel, less tire "squish"
  - **Decrease:** Softer tread longitudinally, slower response, more progressive feel, more tire deformation
  - **For more responsive tire:** Increase by 10-20%
  - **For softer tire:** Decrease by 10-20%
- **Pressure multiplier:**
  - **Range:** 10 - 15
  - **Increase:** Tread stiffness increases more with pressure
  - **Decrease:** Tread stiffness increases less with pressure
- **Temperature multiplier:**
  - **Range:** -1.5e6 to -1.0e6
  - **Increase (less negative):** Less temperature sensitivity
  - **Decrease (more negative):** More temperature sensitivity, tread gets softer more when hot
- **Speed multiplier:**
  - **Range:** -5000 to -3000
  - **Increase (less negative):** Stiffness decreases less with speed
  - **Decrease (more negative):** Stiffness decreases more with speed

**Real-World Impact:**
- Higher base: Faster response to steering/braking inputs, more direct feel, less tire "squish", better transient response
- Lower base: Slower response, more progressive feel, more tire deformation, softer compound feel
- Critical for matching tire compound characteristics

---

### TreadSpringZPerUnitArea

**Purpose:** Controls the vertical stiffness of the tread rubber per unit area. Affects how the tread deforms vertically.

**Format:** `TreadSpringZPerUnitArea=(<base>, <pressure_mult>, <temp_mult>, <speed_mult>)`

**Typical Values:**
- **Base value:**
  - **Range:** 8e8 - 1.5e9 N/m²
  - **Typical:** 1.0e9 - 1.2e9 N/m²
- **Pressure multiplier:**
  - **Range:** -400 to -300 (negative)
  - **Typical:** -350 to -380
- **Temperature multiplier:**
  - **Range:** -1.3e6 to -1.0e6 (negative = softer when hot)
  - **Typical:** -1.1e6 to -1.2e6
- **Speed multiplier:**
  - **Range:** -500 to -400 (negative)
  - **Typical:** -450 to -480

**Example:**
```
TreadSpringZPerUnitArea=(1.141e9, -354.4055, -1.1741e6, -451.2509)
```

**Thesis Information:**
- Controls tread block stiffness in the vertical direction
- Higher values = stiffer tread vertically
- Affects contact patch pressure distribution
- Less critical than TreadSpringX for handling feel

**Tuning Guidelines:**
- **Base value:**
  - **Range:** 8e8 - 1.5e9 N/m²
  - **Increase:** Stiffer tread vertically, less tread deformation, more uniform pressure distribution
  - **Decrease:** Softer tread vertically, more tread deformation, more pressure concentration
- **Pressure multiplier:**
  - **Range:** -400 to -300 (negative)
  - **Increase (less negative):** Stiffness decreases less with pressure
  - **Decrease (more negative):** Stiffness decreases more with pressure
- **Temperature multiplier:**
  - **Range:** -1.3e6 to -1.0e6
  - **Increase (less negative):** Less temperature sensitivity
  - **Decrease (more negative):** More temperature sensitivity
- **Speed multiplier:**
  - **Range:** -500 to -400
  - **Increase (less negative):** Stiffness decreases less with speed
  - **Decrease (more negative):** Stiffness decreases more with speed

**Real-World Impact:**
- Higher base: Less tread deformation, more uniform pressure distribution, better grip on smooth surfaces
- Lower base: More tread deformation, more pressure concentration, better grip on rough surfaces
- Affects grip on rough surfaces

---

### RingStiffnessMultiplier

**Purpose:** Multiplies the stiffness of the tire ring (carcass) in different directions. Controls overall tire carcass stiffness.

**Format:** `RingStiffnessMultiplier=(<radial>, <lateral>, <longitudinal>, <torsional>, <bending1>, <bending2>)`

**Typical Values:**
- **Radial (first value):**
  - **Range:** 0.8 - 1.2
  - **Typical:** 0.9 - 1.0
- **Lateral (second value):** 1.0 (typically fixed)
- **Longitudinal (third value):** 1.0 (typically fixed)
- **Torsional (fourth value):** 1.0 (typically fixed)
- **Bending (fifth/sixth values):** 1.0 (typically fixed)

**Example:**
```
RingStiffnessMultiplier=(0.90, 1, 1, 1, 1, 1)
```

**Thesis Information:**
- Multiplies the base ring stiffness from the [Node] sections
- Each value affects a different deformation mode
- Values < 1.0 reduce stiffness, values > 1.0 increase stiffness
- First value (radial) is most commonly adjusted

**Tuning Guidelines:**
- **Radial (first value):**
  - **Range:** 0.8 - 1.2
  - **Decrease:** Softer tire, more deformation, better compliance, better ride quality, less responsive
  - **Increase:** Stiffer tire, less deformation, faster response, harsher ride, more responsive
  - **For softer tire:** Reduce by 5-10%
  - **For stiffer tire:** Increase by 5-10%
- **Lateral (second value):** Side-to-side stiffness (typically 1.0, rarely adjusted)
- **Longitudinal (third value):** Fore-aft stiffness (typically 1.0, rarely adjusted)
- **Torsional (fourth value):** Twist stiffness (typically 1.0, rarely adjusted)
- **Bending (fifth/sixth values):** Bending stiffness (typically 1.0, rarely adjusted)

**Real-World Impact:**
- Lower radial value: Softer tire, more compliant, better ride quality, less responsive
- Higher radial value: Stiffer tire, less compliant, harsher ride, more responsive
- Critical for matching tire construction (radial vs bias-ply characteristics)

---

### LoadVsDeflectionMultiplier

**Purpose:** Controls how tire deflection changes with vertical load. Affects the load sensitivity of the tire.

**Format:** `LoadVsDeflectionMultiplier=<value>`

**Typical Values:**
- **Range:** 0.85 - 1.15
- **Typical:** 1.0 (standard behavior)
- **Minimum:** 0.85 (stiffer, less deflection)
- **Maximum:** 1.15 (softer, more deflection)

**Example:**
```
LoadVsDeflectionMultiplier=1
```

**Thesis Information:**
- Multiplies the deflection-load relationship
- Value of 1.0 = standard behavior
- Values < 1.0 = less deflection for given load (stiffer)
- Values > 1.0 = more deflection for given load (softer)

**Tuning Guidelines:**
- **Range:** 0.85 - 1.15
- **Decrease:** Stiffer tire, less deflection for given load, tire deflects less under load, stiffer feel
- **Increase:** Softer tire, more deflection for given load, tire deflects more under load, softer feel
- **For load sensitivity tuning:** Adjust in 0.05 increments
- Less commonly adjusted than other stiffness parameters

**Real-World Impact:**
- Lower values: Tire deflects less under load, stiffer feel, less load sensitivity
- Higher values: Tire deflects more under load, softer feel, more load sensitivity
- Affects how tire responds to weight transfer

---

## Thermal Parameters

### DampingHeatEnergy

**Purpose:** Controls heat generation from damping/hysteresis effects. Higher values generate more heat from tire deformation.

**Format:** `DampingHeatEnergy=(<adhesion>, <sliding>, <hysteresis>)`

**Typical Values:**
- **First value (adhesion):**
  - **Range:** 0.3 - 0.5
  - **Typical:** 0.35 - 0.45
- **Second value (sliding):**
  - **Range:** 0.15 - 0.25
  - **Typical:** 0.18 - 0.22
- **Third value (hysteresis):**
  - **Range:** 0.4 - 0.6
  - **Typical:** 0.45 - 0.55

**Example:**
```
DampingHeatEnergy=(0.3, 0.18, 0.45)
```

**Thesis Information:**
- First value: Heat from adhesion zone (typically 0.3-0.5)
- Second value: Heat from sliding zone (typically 0.15-0.25)
- Third value: Heat from hysteresis (typically 0.4-0.6)
- Higher values = more heat generation = higher tire temperatures
- Critical for matching real tire temperature profiles

**Tuning Guidelines:**
- **First value (adhesion):**
  - **Range:** 0.3 - 0.5
  - **Increase:** More heat from adhesion zone, higher tire temperatures
  - **Decrease:** Less heat from adhesion zone, lower tire temperatures
- **Second value (sliding):**
  - **Range:** 0.15 - 0.25
  - **Increase:** More heat from sliding zone, higher tire temperatures during slides
  - **Decrease:** Less heat from sliding zone, lower tire temperatures during slides
- **Third value (hysteresis):**
  - **Range:** 0.4 - 0.6
  - **Increase:** More heat from hysteresis, higher tire temperatures
  - **Decrease:** Less heat from hysteresis, lower tire temperatures
- **To reduce heat generation:** Decrease all values by 20-30%
- **To increase heat generation:** Increase all values by 20-30%
- **All three values should be adjusted proportionally**
- **To match telemetry:** Adjust based on measured tire temperatures

**Real-World Impact:**
- Lower values: Less heat generation, cooler tires, less thermal degradation, slower warm-up
- Higher values: More heat generation, hotter tires, more thermal degradation, faster warm-up
- Critical for matching real tire temperature behavior from telemetry

---

### InternalGasHeatTransfer

**Purpose:** Controls heat transfer within the tire (between carcass and internal air). Higher values improve internal heat distribution.

**Format:** `InternalGasHeatTransfer=(<base>, <speed_mult>, <exponent>)`

**Typical Values:**
- **Base value:**
  - **Range:** 4 - 8
  - **Typical:** 5 - 7
- **Speed multiplier:**
  - **Range:** 4 - 6
  - **Typical:** 5
- **Exponent:**
  - **Range:** 0.6 - 0.7
  - **Typical:** 0.65

**Example:**
```
InternalGasHeatTransfer=(6, 5, 0.65)
```

**Thesis Information:**
- Formula: `transfer = base + (speed_mult * speed^exponent)`
- Controls how heat moves from hot spots to cooler areas within the tire
- Higher values = better heat distribution = more uniform temperatures
- Critical for matching real tire temperature distribution (inner vs outer edge)

**Tuning Guidelines:**
- **Base value:**
  - **Range:** 4 - 8
  - **Increase:** Better internal heat distribution, more uniform tire temperatures, less hot spots
  - **Decrease:** Less internal heat distribution, more temperature variation across tire, potential hot spots
  - **To improve heat distribution:** Increase by 20-50%
- **Speed multiplier:**
  - **Range:** 4 - 6
  - **Increase:** Heat transfer increases more with speed
  - **Decrease:** Heat transfer increases less with speed
- **Exponent:**
  - **Range:** 0.6 - 0.7
  - **Increase:** More speed-dependent behavior
  - **Decrease:** Less speed-dependent behavior

**Real-World Impact:**
- Higher base: More uniform tire temperatures, less hot spots, better heat distribution, matches inner/outer temp differences
- Lower base: More temperature variation across tire, potential hot spots, less uniform distribution
- Critical for matching real tire inner/outer temperature differences from telemetry

---

### ExternalGasHeatTransfer

**Purpose:** Controls heat transfer from tire to ambient air (cooling). Higher values increase cooling, especially at speed.

**Format:** `ExternalGasHeatTransfer=(<base>, <speed_mult>, <exponent>)`

**Typical Values:**
- **Base value:**
  - **Range:** 4 - 8
  - **Typical:** 5 - 7
  - **Open-wheel cars:** 6 - 8 (more airflow)
- **Speed multiplier:**
  - **Range:** 4 - 6
  - **Typical:** 5
- **Exponent:**
  - **Range:** 0.6 - 0.7
  - **Typical:** 0.65

**Example:**
```
ExternalGasHeatTransfer=(6.5, 5.0, 0.65)
```

**Thesis Information:**
- Formula: `cooling = base + (speed_mult * speed^exponent)`
- Controls convective cooling to ambient air
- Higher values = more cooling = lower tire temperatures
- Critical for matching real tire cooling behavior on straights
- For open-wheel cars, values are typically higher (more airflow)

**Tuning Guidelines:**
- **Base value:**
  - **Range:** 4 - 8
  - **Increase:** More cooling, cooler tires, especially at speed, cooler tires on straights, faster temperature drop
  - **Decrease:** Less cooling, hotter tires, slower temperature drop on straights
  - **To reduce outer edge temps:** Increase by 30-50%
- **Speed multiplier:**
  - **Range:** 4 - 6
  - **Increase:** More cooling at speed (important for straights), cooling increases more with speed
  - **Decrease:** Less cooling at speed, cooling increases less with speed
- **Exponent:**
  - **Range:** 0.6 - 0.7
  - **Increase:** Cooling increases more with speed
  - **Decrease:** Cooling increases less with speed

**Real-World Impact:**
- Higher base: More cooling, especially at speed, cooler tires on straights, faster temperature drop, better matches telemetry
- Lower base: Less cooling, hotter tires, slower temperature drop on straights
- Critical for matching real tire temperature profiles from telemetry

---

### GroundConductance

**Purpose:** Controls heat transfer from tire to track surface via conduction. Higher values increase heat loss to the track.

**Format:** `GroundConductance=(<base>, <pressure_mult>, <offset>)`

**Typical Values:**
- **Base value:**
  - **Range:** 600 - 1200
  - **Typical:** 700 - 900
- **Pressure multiplier:**
  - **Range:** 0.015 - 0.030
  - **Typical:** 0.020 - 0.025
- **Offset:** 0 (typically fixed)

**Example:**
```
GroundConductance=(800, 0.025, 0)
```

**Thesis Information:**
- Formula: `conductance = base + (pressure_mult * contact_pressure)`
- Controls conductive heat transfer to track surface
- Higher values = more heat loss to track = cooler tire surface
- Critical for matching real tire surface temperatures
- The second value multiplies contact pressure (higher pressure = more heat transfer)

**Tuning Guidelines:**
- **Base value:**
  - **Range:** 600 - 1200
  - **Increase:** More heat loss to track, cooler tire surface, better cooling in contact patch
  - **Decrease:** Less heat loss to track, hotter tire surface, less cooling
  - **To reduce surface temps:** Increase by 20-30%
- **Pressure multiplier:**
  - **Range:** 0.015 - 0.030
  - **Increase:** More pressure-dependent cooling, higher pressure = more heat transfer
  - **Decrease:** Less pressure-dependent cooling, less variation with pressure
- **Offset:** Typically 0 (rarely adjusted)

**Real-World Impact:**
- Higher base: More heat lost to track, cooler tire surface, better cooling in contact patch, matches surface temp measurements
- Lower base: Less heat lost to track, hotter tire surface, less cooling
- Critical for matching real tire surface temperature measurements from telemetry

---

### ThermalDepthAtSurface

**Purpose:** Defines the thermal depth at the tire surface for temperature calculations.

**Format:** `ThermalDepthAtSurface=<value>`

**Example:**
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

**Example:**
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

**Typical Values:**
- **Range:** 0.7 - 1.0
- **Typical:** 0.75 - 0.85
- **Minimum:** 0.7 (very even distribution)
- **Maximum:** 1.0 (standard distribution)

**Example:**
```
LateralDistributionMultiplier=0.755
```

**Thesis Information:**
- Values < 1.0 distribute forces more evenly across the contact patch
- Values = 1.0 use standard distribution
- Critical for preventing hot spots and rollover issues
- Lower values help distribute heat laterally (prevent outer edge overheating)

**Tuning Guidelines:**
- **Range:** 0.7 - 1.0
- **Decrease:** More even lateral force distribution, prevents hot spots, more even heat distribution, less outer edge overheating, better for preventing rollover
- **Increase:** More concentrated force distribution, potential hot spots, can contribute to rollover
- **For rollover prevention:** Reduce to 0.75-0.80
- **For hot spot prevention:** Reduce to 0.70-0.75

**Real-World Impact:**
- Lower values: More even heat distribution, less outer edge overheating, better for preventing rollover, more stable tire
- Higher values: More concentrated forces, potential hot spots, can contribute to rollover, less stable tire
- Critical parameter for tire stability

---

### LongitudinalDistributionMultiplier

**Purpose:** Controls how forces are distributed longitudinally across the tire contact patch.

**Format:** `LongitudinalDistributionMultiplier=<value>`

**Example:**
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

**Example:**
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

**Example:**
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

**Example:**
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

**Example:**
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

**Example:**
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

**Example:**
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

**Typical Values:**
- **Range:** 0.0 - 0.2
- **Typical:** 0.05 - 0.1

**Example:**
```
TerrainWeightOnContactTemperature=0.05
```

**Tuning Guidelines:**
- **Range:** 0.0 - 0.2
- **Increase:** More track temperature influence, tire temperature is more affected by the hot/cold track
- **Decrease:** Less track temperature influence, tire temperature is less affected by track temperature

**Real-World Impact:**
- Higher values: Tire temperature is more affected by a hot/cold track
- Lower values: Tire temperature is less affected by track temperature

---

### DryTerrainEffect, WetTerrainEffect, etc.

**Purpose:** Defines grip multipliers for different terrain types.

**Format:** `TerrainEffect=(<min_grip>, <max_grip>, <multiplier>)`

**Example:**
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

**Example:**
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

**Example:**
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

**Example:**
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

**Example:**
```
InternalGasMolarMass=0.028884
```

**Tuning Guidelines:**
- 0.028884 = air
- 0.028 = nitrogen
- Rarely adjusted

---

### InternalGasSpecificHeatAtConstantVolume

**Purpose:** Defines the specific heat capacity of internal gas at different temperatures.

**Format:** `InternalGasSpecificHeatAtConstantVolume=(<temp_K>, <specific_heat>)`

**Example:**
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
- Only adjust if using a different gas (e.g., nitrogen)

---

### GaugePressureExtrapolationRange

**Purpose:** Defines the pressure range for extrapolation beyond lookup table limits.

**Format:** `GaugePressureExtrapolationRange=(<min_Pa>, <max_Pa>)`

**Example:**
```
GaugePressureExtrapolationRange=(0,270000)
```

**Tuning Guidelines:**
- Defines valid pressure range (0 to 270000 Pa = 0 to 2.7 bar)
- Adjust if the tire operates outside this range
- Typically left at the default

---

### CarcassTemperatureExtrapolationRange

**Purpose:** Defines the temperature range for extrapolation beyond lookup table limits.

**Format:** `CarcassTemperatureExtrapolationRange=(<min_K>, <max_K>)`

**Example:**
```
CarcassTemperatureExtrapolationRange=(268.15,423.15)
```

**Tuning Guidelines:**
- Defines valid temperature range (268.15K = -5°C to 423.15K = 150°C)
- Adjust if the tire operates outside this range
- Typically left at the default

---

### RotationSquaredExtrapolationRange

**Purpose:** Defines the rotational speed range for extrapolation beyond lookup table limits.

**Format:** `RotationSquaredExtrapolationRange=(<min>, <max>)`

**Example:**
```
RotationSquaredExtrapolationRange=(0,47000)
```

**Tuning Guidelines:**
- Defines valid rotational speed range
- Adjust if tire operates outside this range
- Typically left at the default

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
   - Adjust `InternalGasHeatTransfer` to match the temperature distribution

2. **Grip matching:**
   - Adjust `StaticBaseCoefficient` and `SlidingBaseCoefficient` to match friction coefficients
   - Adjust `StaticCurve` to match optimal operating temperature
   - Adjust `RubberPressureSensitivityPower` to match pressure behavior

3. **Stability:**
   - Adjust `LateralDistributionMultiplier` to prevent rollover/hot spots
   - Adjust stiffness parameters for desired feel

#### Reducing Rollover Issues

1. **Reduce `LateralDistributionMultiplier`** to 0.75-0.80
2. **Reduce stiffness parameters** by 5-10% if the tire feels too stiff
3. **Check `StaticBaseCoefficient`** - may be too high

#### Matching Real Tire Telemetry (Example)

Example parameter set for matching real tire telemetry data:

```
StaticBaseCoefficient=3.75
SlidingBaseCoefficient=2.68
StaticCurve=(273, 0.6, 360, 1.0, 420, 0.7)  // Peak at 360K (87°C)
DampingHeatEnergy=(0.3, 0.18, 0.45)
InternalGasHeatTransfer=(6, 5, 0.65)
ExternalGasHeatTransfer=(6.5, 5.0, 0.65)
GroundConductance=(800, 0.025, 0)
RubberPressureSensitivityPower=(-35, 9.5e6, 5e5, 1)
```

**Note:** These values represent a typical configuration. Adjust based on your specific tire telemetry data and requirements.

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

---

**Document Version:** 1.0  
**Last Updated:** Based on real tire telemetry matching work

