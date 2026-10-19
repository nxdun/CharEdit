# CharEdit Slider Mechanics - Agent Knowledge Base
# SOURCE: Direct visual verification (Screenshots: 095326, 100057, 101634)

## CRITICAL ANATOMICAL LIMITS
WARNING: Do not blindly trust semantic slider names or target aesthetics ("petite", "lean", "fairy") with absolute values near 0 or 100. The engine's baseline (50) is neutral. Values deviating too far from ~35-60 cause catastrophic anatomical collapse.

### 1. Torso & Shoulders (The A-Frame Collapse)
- `txt_shoulderWidth`, `txt_chestWidth`, `txt_waistWidth`
- **OBSERVATION**: Setting shoulder/chest width below 30 results in an impossibly narrow clavicle and ribcage, causing the arms to merge directly into the neck (A-Frame deformity).
- **RULE**: ALWAYS keep `txt_shoulderWidth` and `txt_chestWidth` between 35-50 for a functional human skeleton.
- **RULE**: `txt_waistWidth` should rarely drop below 20.

### 2. Waist, Pelvis & Limbs (The "Barrel & Twig" Deformity)
- `txt_waistWidth`, `txt_waistThickness`, `txt_pelvisWidth`, `txt_thighs`, `txt_calves`, `txt_waistHeight`
- **OBSERVATION**: Setting the waist values too high relative to the pelvis creates a rigid "barrel" or "tube" torso. Setting thighs/calves too low creates a massive thigh gap. 
- **OBSERVATION (Waist Height)**: `txt_waistHeight` > 45 pulls the natural waistline up directly under the breasts, creating an impossibly short, blocky upper torso and weirdly long pelvis.
- **RULE**: To create a natural curve, waist (`~25-30`) must be narrower than pelvis (`~40-45`).
- **RULE**: Thigh thickness must scale with pelvis width. Keep `txt_waistHeight` ~35-40 for a natural torso length.

### 3. Craniofacial Structure (The Lightbulb Deformity)
- `txt_jawWidth`, `txt_chinSize`, `txt_jawHeight`, `txt_headWidth`
- **OBSERVATION**: Values below 30 create a dangerously sharp, pinched lower third, resulting in an alien/lightbulb head shape.
- **RULE**: For a natural oval/heart face, keep `txt_jawWidth` ~35-45, `txt_chinSize` ~30-40, and `txt_headWidth` ~35-45.

### 4. Eyes & Expressions (The Squinting Alien)
- `txt_eyeSpacing`, `txt_eyeAngleZ`, `txt_eyeWidth`, `txt_eyeHeight`
- **OBSERVATION**: `txt_eyeSpacing` > 45 spaces the eyes too far apart. Low `txt_eyeHeight` (< 60 for stylized characters) creates tiny, squinting slits that look unnatural.
- **RULE**: Realistic eye spacing is tight (~30-35). For Disney/stylized characters, `txt_eyeWidth` and `txt_eyeHeight` must be exceptionally high (65-75) to avoid the "alien squint."

### 5. Bust Placement (Splayed Breasts)
- `txt_bustHeight`, `txt_bustSpacing`, `txt_bustDirection`
- **OBSERVATION**: `txt_bustSpacing` > 40 causes the breasts to splay violently outward toward the armpits.
- **RULE**: Keep `txt_bustSpacing` tightly centered (~30-35) and angled forward (`txt_bustDirection` ~55) for natural cleavage and support.

## SCALING RELATIONS
- **Head to Body**: `txt_headSize` must scale inversely with `txt_ovrlHeight`.
- **Neck to Shoulders**: `txt_neckWidth` must match `txt_shoulderWidth` ratio.
