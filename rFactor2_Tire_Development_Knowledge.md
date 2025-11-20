# rFactor 2 Tire Development Knowledge Base

## Overview
This knowledge base contains professional tire development methodology, parameter relationships, and technical insights developed through collaboration with racing teams and extensive testing. All information respects NDA boundaries while sharing validated physics principles.

## Core Principles

### TGM vs TBC Relationship
- **TGM files are the master files** - they control actual grip feel and user experience
- **TBC files primarily handle AI behavior and visual appearance**
- Spend 90% of development time on TGM Realtime section, 10% on TBC
- TGM defines how tire deforms, generates grip, heats up, and responds to driver inputs

### Development Philosophy
- **Surgical precision, not sledgehammer approaches** - targeted fixes preserve realistic behavior
- **One parameter at a time** - systematic testing prevents confusion
- **Empirical validation** - real driver feedback and telemetry data over theoretical calculations
- **Respect professional boundaries** - NDA compliance while sharing methodology

## Key Parameter Relationships

### Base Grip Coefficients

#### StaticBaseCoefficient
- **Controls:** Overall grip when tire is not sliding
- **Typical range:** 1.9-3.9 (varies by tire type)
- **Real example:** Changing from 3.64 to 3.39 (-0.25) reduces "front bite" on initial turn-in
- **Use case:** When car has too much grip on turn-in compared to real life

#### SlidingBaseCoefficient
- **Controls:** Grip level when tire is sliding
- **Typical range:** 1.3-2.7 (varies by tire type)
- **Real example:** Changing from 2.63 to 2.45 (-0.18) creates more progressive sliding
- **Use case:** Making sliding more challenging and realistic
- **Important:** Reducing this globally affects ALL slip conditions (braking, cornering, acceleration)

### Diffusive Adhesion (Grip Curve Shape)

#### StaticDiffusiveAdhesion=(0.001, value, sharpness)
- **First value (0.001):** Base parameter, typically unchanged
- **Second value:** Controls grip magnitude at peak (higher = more grip)
  - Typical range: 11,000-21,000
  - Real example: 11,200 → 21,000 increases peak grip significantly
- **Third value:** Controls sharpness of grip falloff (0.75-0.99)
  - 0.75 = Progressive, forgiving
  - 0.90-0.99 = Sharp, snappy, less forgiving
  - Real example: 0.80 → 0.90 creates sharper grip falloff after optimal slip angle

#### SlidingDiffusiveAdhesion=(0.001, value, sharpness)
- **Similar structure to StaticDiffusiveAdhesion**
- **Second value range:** 1,900-6,600
- **Controls:** Sliding grip curve sharpness
- **Real example:** 3,600 → 6,600 changes sliding behavior at higher speeds

### Pressure Sensitivity

#### RubberPressureSensitivityPower=(power, offset, nominal_max, normalize)
- **Power (first value):** Controls curve steepness
  - Typical: -1.17 (gentle) to -40 (very aggressive)
  - Lower (less negative) = flatter pressure response
  - Higher (more negative) = sharper pressure sensitivity
- **Offset (second value):** Shifts optimal pressure point
  - Typical: 4.04e5 (baseline) to 1.13e7 (extreme)
  - Higher values = optimal pressure shifts higher
- **Real example:** (-40, 1.13e7, 5e5, 1) → (-25, 8e6, 5e5, 1)
  - Moves optimal pressure from 1.5 bar to 1.9 bar
  - Fixes drift abuse while preserving normal driving
- **Critical insight:** This parameter specifically targets pressure-related exploits without affecting general sliding behavior

### Temperature Behavior

#### StaticCurve=(temp1, grip1, temp2, grip2, temp3, grip3)
- **Format:** Exactly 3 points (6 values) - Kelvin temperature, grip multiplier
- **Realistic racing range:** 250K-520K (-23°C to 247°C)
- **Typical values:**
  - Cold: 257-273K (-16°C to 0°C) at 0.65-0.75 grip
  - Peak: 366-398K (93°C to 125°C) at 1.0-1.2 grip
  - Overheat: 413-518K (140°C to 245°C) at 0.3-0.7 grip
- **Real example:** (273, 0.6, 378, 1.0, 428, 0.7) → (257, 0.65, 366, 1.2, 518, 0.3)
  - Moves peak to 93°C, creates harsher overheating penalty
- **Never go below ~60% grip** on cold tires or steering instability occurs

### Sliding Behavior Curves

#### SlidingAdhesionCurve=(min_speed, grip_min, peak_speed, grip_peak, max_speed, grip_max)
- **Controls:** Grip at different sliding speeds
- **Real example:** (-7.2, 0.4, -4.2, 1.7, -1.2, 0.2) → (-7.2, 0.35, -4.2, 1.6, -1.2, 0.18)
  - Reduces grip when sliding, makes recovery harder
- **Important:** Reducing all sliding curves by 0.1 ≈ reducing SlidingBaseCoefficient by 0.15
  - But individual curves allow targeted fixes vs global changes

#### SlidingMicroDeformationCurve & SlidingMacroDeformationCurve
- **Fine-tune sliding behavior** at different scales
- **Reducing values by 0.05-0.1** creates more progressive sliding
- **Use for:** Balancing challenge vs drivability

### Tire Structure Parameters

#### BeltSpringX & BeltSpringZ
- **BeltSpringX:** Lateral (sidewall) stiffness
- **BeltSpringZ:** Vertical (radial) stiffness
- **Format:** (base, per_unit_pressure, per_unit_temperature, per_unit_rotation_squared)
- **For narrower tires:** Reduce base value by 5-10%
  - Example: 1.95e6 → 1.85e6 for 235mm vs 260mm tire
- **For wider tires:** Increase base value proportionally

#### TreadSpringXPerUnitArea & TreadSpringZPerUnitArea
- **Per unit area** - typically unchanged when scaling tire width
- **Controls:** Tread rubber compliance
- **Format:** (base, per_unit_pressure, per_unit_temperature, per_unit_rotation_squared)

### Contact Patch Distribution

#### LateralDistributionMultiplier
- **Controls:** How lateral forces spread across contact patch
- **Typical range:** 0.75-0.90
- **For narrower tires:** Increase to compensate for smaller contact patch
  - Example: 0.801 → 0.855 for 235mm vs 260mm tire
- **Higher values:** Better lateral force distribution

#### LongitudinalDistributionMultiplier
- **Controls:** How longitudinal forces spread across contact patch
- **Typical range:** 0.4-0.6
- **For narrower tires:** Slight increase (0.5 → 0.535)
- **Lower values:** More forward slip under braking (less aggressive ABS)

### Tire Wear & Degradation

#### AbrasionVolumePerUnitEnergy
- **32 values** defining wear rate at different conditions
- **To double tire life:** Halve all values
  - Example: 3.26e-10 → 1.63e-10
- **No tTool regeneration needed** - Realtime section parameter

#### DegradationCurveParameters=(activation_temp_K, heat_history_step_Ks)
- **First value:** Temperature where thermal degradation starts (typically 342-349K)
- **Second value:** Rate of thermal degradation (lower = slower degradation)
  - Typical: 3,700-6,978
  - Lower values = longer tire life when hot
- **Real example:** (342.65, 6978.125) → (349.15, 3700)
  - Higher activation temp + slower rate = much longer tire life

#### DegradationPerUnitHistory
- **32 values** defining grip loss from accumulated heat damage
- **To slow degradation:** Make values closer to 1.0
  - Example: 0.98 → 0.99 (slower grip loss)
- **No tTool regeneration needed**

## Tire Scaling Methodology

### Converting Tire Width (Example: 260mm → 235mm)

#### Dimensional Changes:
1. **SizeMultiplier:** (1.040, 0.992) → (0.938, 0.992)
   - First value: new_width / baseline_width (235/250 = 0.94)
   - Second value: Typically unchanged

2. **Mass Properties:**
   - TotalMass: Scale proportionally (9.85 → 8.8 kg)
   - TotalInertiaStandard: Scale all values proportionally
   - RingMass: Scale proportionally
   - RingInertiaStandard: Scale all values proportionally

3. **Load Test Forces:**
   - LateralTestForce: Reduce by ~10% for smaller contact patch
   - LongitudinalTestForce: Reduce by ~10%

#### Physics Adjustments:
1. **Distribution Multipliers:**
   - LateralDistributionMultiplier: Increase to compensate (0.801 → 0.855)
   - LongitudinalDistributionMultiplier: Slight increase (0.5 → 0.535)

2. **Spring Rates:**
   - BeltSpringX: Reduce base by 5% (1.95e6 → 1.85e6)
   - BeltSpringZ: Reduce base by 5% (2.55e6 → 2.42e6)
   - TreadSpringPerUnitArea: Keep unchanged (per unit area)

3. **Grip Coefficients:**
   - StaticBaseCoefficient: Keep unchanged (maintain performance)
   - SlidingBaseCoefficient: Keep unchanged
   - All sliding curves: Keep unchanged

4. **TreadDepth:**
   - Typically unchanged (0.0022-0.0024) - represents rubber thickness, not width-dependent

## Common Issues & Solutions

### Problem: Drift Abuse / Wide Grip Window
**Symptoms:** Drivers gain time by sliding at high slip angles, unrealistic "drift mode" behavior

**Solution - Targeted Fix:**
- **Adjust RubberPressureSensitivityPower:** (-40, 1.13e7, 5e5, 1) → (-25, 8e6, 5e5, 1)
  - This specifically targets pressure-related exploits
  - Does NOT affect normal braking, cornering, or acceleration
  - Surgical precision vs global grip reduction

**Alternative (Less Effective):**
- Reducing SlidingBaseCoefficient affects ALL slip conditions
- May require rebalancing entire car setup
- Doesn't solve pressure-specific exploits

### Problem: Too Much Front Bite on Turn-In
**Symptoms:** Car feels too pointy, unrealistic initial grip

**Solution:**
- **Reduce StaticBaseCoefficient:** 3.64 → 3.39 (-0.25)
- **Reduce StaticDiffusiveAdhesion second value:** 21,000 → 18,000
- **Result:** Less initial bite, more progressive grip buildup

### Problem: Tires Overheat Too Fast
**Symptoms:** Tires reach critical temperatures quickly from slip or aggressive driving

**Solution:**
- **Reduce heating in TBC:** Lower first value by 20-30%
- **Increase heat transfer:** ExternalGasHeatTransfer=(4.5,4.5,0.65) → (8,4,0.6)
- **Adjust StaticCurve:** Move peak temperature higher (378K → 390K)
- **Reduce lateral heat generation:** TemporaryBristleDamper first value: 0.95 → 0.75

### Problem: Tires Wear Too Fast
**Symptoms:** Tire life only 15 laps instead of 30+

**Solution:**
- **Halve AbrasionVolumePerUnitEnergy:** All 32 values reduced by 50%
- **Adjust DegradationCurveParameters:** (342.65, 6978.125) → (349.15, 3700)
  - Higher activation temp + slower degradation rate
- **Slow DegradationPerUnitHistory:** Values closer to 1.0

### Problem: Cold Tire Steering Instability
**Symptoms:** Steering wants to snap left/right when tires are cold

**Solution:**
- **Increase StaticCurve cold grip:** (273, 0.4, ...) → (273, 0.65, ...)
- **Never go below ~60% grip** on cold tires
- **Minimum safe cold grip:** 0.60-0.65

### Problem: ABS Feels Too Harsh
**Symptoms:** ABS intervention too aggressive, unrealistic braking feel

**Solution:**
- **Reduce LongitudinalDistributionMultiplier:** 0.5 → 0.35-0.40
- **Balance StaticBaseCoefficient vs SlidingBaseCoefficient:** Wider gap = harsher ABS
- **Smooth SlidingAdhesionCurve:** Less aggressive dropoff

## Professional Development Workflow

### Systematic Testing Process:
1. **Data Collection:** Gather all available technical data about real tire
2. **Initial Implementation:** Create basic TBC/TGM files with conservative estimates
3. **Baseline Testing:** Run extensive in-sim testing to establish baseline behavior
4. **Iterative Refinement:** Adjust parameters based on testing feedback, **one variable at a time**
5. **Validation:** Compare to real-world data; adjust until correlation is acceptable
6. **Multi-Compound Development:** Once base compound validated, create variants (soft/hard)
7. **Documentation:** Record all parameter choices and justifications

### Testing Methodology:
- **One parameter at a time** - prevents confusion about what caused changes
- **Document each change** - parameter, old value, new value, expected effect
- **Validate with telemetry** - MoTeC analysis confirms behavior
- **Professional driver feedback** - real racing experience validation
- **Systematic iteration** - methodical approach beats random tweaking

## Parameter Reference Quick Guide

### Most Critical Parameters (Realtime Section):
1. **StaticBaseCoefficient** - Overall grip level
2. **SlidingBaseCoefficient** - Sliding grip level
3. **RubberPressureSensitivityPower** - Pressure vs grip relationship
4. **StaticCurve** - Temperature vs grip relationship
5. **StaticDiffusiveAdhesion** - Grip curve sharpness
6. **SlidingAdhesionCurve** - Sliding behavior at different speeds

### Scaling Parameters (When Changing Tire Size):
1. **SizeMultiplier** - Width and diameter scaling
2. **Mass properties** - TotalMass, RingMass, Inertia values
3. **Load test forces** - LateralTestForce, LongitudinalTestForce
4. **Distribution multipliers** - LateralDistributionMultiplier, LongitudinalDistributionMultiplier
5. **Belt spring rates** - BeltSpringX, BeltSpringZ base values

### Wear & Degradation (No tTool Regeneration Needed):
1. **AbrasionVolumePerUnitEnergy** - Physical wear rate
2. **DegradationCurveParameters** - Thermal degradation activation
3. **DegradationPerUnitHistory** - Heat damage accumulation

## Professional Insights

### Key Lessons Learned:
1. **Theoretical equivalencies don't always match real-world behavior**
   - Mathematical relationships (e.g., sliding curves ≈ base coefficient) may be equivalent but don't solve specific problems
   - Empirical testing beats theoretical calculations

2. **Targeted fixes vs global changes**
   - Pressure-related exploits need pressure-specific fixes
   - Global grip reduction creates new problems while solving old ones

3. **Professional validation is essential**
   - Real racing teams provide honest, respectful feedback
   - Driver experience validation catches physics issues data alone misses

4. **Respect professional boundaries**
   - NDA compliance maintains industry relationships
   - Share methodology, not proprietary data
   - Public data + physics principles = realistic tires

### Development Philosophy:
- **Surgical precision** over sledgehammer approaches
- **Systematic iteration** over random tweaking
- **Empirical validation** over theoretical assumptions
- **Professional collaboration** while respecting boundaries
- **Community engagement** with structured feedback

## Technical Notes

### tTool Regeneration Requirements:
- **Realtime section changes:** NO regeneration needed
- **QuasiStaticAnalysis changes:** Regeneration required
- **Node geometry changes:** Regeneration required
- **Physical construction changes:** Regeneration required

### DT (Delta Time) in tTool:
- **Lower DT (0.32):** More stable, slower calculation
- **Higher DT (0.70):** Faster but can cause numerical instability
- **Rule of thumb:** Higher node count = lower DT required
- **75+ nodes:** Use DT 0.32-0.45 for stability
- **61 nodes:** Can handle DT 0.45-0.50
- **49 nodes:** Can handle DT 0.50-0.60

### Node Count Guidelines:
- **Minimum:** 31 nodes
- **Recommended:** 41-49 nodes (good balance)
- **High detail:** 61 nodes (more accurate, slower)
- **Maximum practical:** 75 nodes (very slow, diminishing returns)

## Parameter Value Ranges Reference

### Base Coefficients:
- **StaticBaseCoefficient:** 1.9-3.9 (varies by tire type)
- **SlidingBaseCoefficient:** 1.3-2.7 (varies by tire type)

### Diffusive Adhesion:
- **StaticDiffusiveAdhesion second value:** 11,000-21,000
- **StaticDiffusiveAdhesion third value:** 0.75-0.99
- **SlidingDiffusiveAdhesion second value:** 1,900-6,600
- **SlidingDiffusiveAdhesion third value:** 0.75-0.99

### Pressure Sensitivity:
- **Power:** -1.17 (gentle) to -40 (aggressive)
- **Offset:** 4.04e5 (baseline) to 1.13e7 (extreme)

### Temperature Curves:
- **Cold grip:** 0.60-0.75 (never below 0.60)
- **Peak temperature:** 366-398K (93-125°C)
- **Overheat grip:** 0.30-0.70

### Distribution Multipliers:
- **LateralDistributionMultiplier:** 0.75-0.90
- **LongitudinalDistributionMultiplier:** 0.35-0.60

### Spring Rates:
- **BeltSpringX base:** 0.8e6-2.05e6
- **BeltSpringZ base:** 1.2e6-2.7e6
- **TreadSpringXPerUnitArea base:** 2e8-9.2e8
- **TreadSpringZPerUnitArea base:** 1.0e9-1.14e9

## Best Practices

1. **Always test one parameter at a time**
2. **Document all changes** with old/new values and reasoning
3. **Validate with telemetry** (MoTeC analysis)
4. **Get professional driver feedback** when possible
5. **Respect NDA boundaries** while sharing methodology
6. **Use systematic iteration** - methodical approach
7. **Compare to real-world data** when available
8. **Maintain parameter consistency** across related values
9. **Scale proportionally** when changing tire dimensions
10. **Preserve proven physics** when adapting to new applications

## Community Development Guidelines

### Contribution Framework:
- **Test Drivers:** Structured feedback using evaluation templates
- **Data Analysts:** MoTeC interpretation and validation
- **Parameter Developers:** Research and implement changes
- **Professional Validators:** Real racing experience validation

### Feedback Requirements:
- **Structured format:** Straight brake, trail brake, cornering, traction, overall
- **Real experience context:** Racing background for validation
- **Specific conditions:** Track, temperature, pressure, setup
- **Comparative analysis:** vs default tires, vs real experience

### Development Ethics:
- **NDA compliance:** All professional agreements respected
- **Public domain focus:** Use only publicly available information
- **Methodology sharing:** Share HOW to develop, not proprietary WHAT
- **Community benefit:** Knowledge should benefit entire sim racing community
- **Professional respect:** Racing teams' competitive advantages protected

---



