Comments with "" are pulled directly from SDK. Some values are currently unknown what they do.

```yaml
"BP_C6": { # Blueprint Name

        # General Info
        "displayName": "C6",            # Display name found in HUD
        "rawName": "BP_C6.BP_C6_C",     # Raw blueprint name
        "folder": "MachineGuns",        # Folder where blueprint is loaded
        "factions": [                   # Factions that the weapon is used by
            "CAF"
        ],


        # Inventory Info
        "inventoryInfo": {
            "description": "description",                           # Item desciption found in game
            "inventoryTexture": "inventory_category_machinegun",    # Inventory texture
            "ammoPerRearm": 11,                                     # Ammo point cost from FOB for 1 mag/item
            "showItemCount": false,                                 # Show item count in inventory
            "showMagCount": true                                    # Show mag counts on hud
        },



        # Weapon Config Info
        "weaponInfo": {
            # Mag info
            "maxMags": 8,               # Max # of mags
            "roundsPerMag": 75,         # Rounds per mag
            "roundInChamber": false,    # Allow a round to stay loaded in chamber
            "allowSingleLoad": false,   # Allow item to be loaded bullet by bullet

            # Firemode info
            "firemodes": [              # Firemodes. -1 -> automatic | 0 -> burst | 1 -> semi-auto
                -1
            ],
            "timeBetweenShots": 0.085,              # Min time betwen two shots (burst/auto)
            "timeBetweenSingleShots": 0.125,=       # Min time between two shots (semi-auto)
            "avgFireRate": true,                    # Unknown
            "resetBurstOnTriggerRelease": false,    # Unknown

            # Reload Info
            "reloadCancelGracePeriod": 0.0,         # "Finish reload grace peroid for cancelling reload close to finishing the reload process"
            "tacticalReloadDuration": 9.5,          # Time it takes to reload weapon without an empty mag
            "dryReloadDuration": 11.2,              # Time it takes to reload weapon with an empty mag
            "tacticalReloadBipodDuration": 8.0,     # Time it takes to reload weapon without an empty mag with a bipod
            "dryReloadBipodDuration": 8.75,         # Time it takes to reload weapon with an empty mag with a bipod

            # ADS Info
            "ADSPostTransitionRation": 0.4,         # "ADS Post Process transtion point == ZoomedFOV / (CurrentFOV - FOVSetting - 90)
            "allowZoom": true,                      # If ADS is allowed on the weapon
            "ADSMoveSpeedMultiplier": 0.6,          # How much ADS slows a player

            # Projectile info
            "projectileClass": "BP_Projectile_7_62mm_C",            # Projectile blueprint
            "tracerProjectileClass": "BP_Projectile_Red_762mm_C",   # Tracer blueprint (MAY BE NULL)
            "roundsBetweenTracer": 4,                               # Rounds between tracer

            # Damage and velocity damage
            "muzzleVelocity": 85300,                    # Starting/muzzle velocity for projectiles
            "damageFallOffMinDamage": 35.0,             # Min damage from fall off
            "damageFallOffMinDamageDistance": 80000.0,  # Distance the min damage occurs
            "damageFallOffMaxDamage": 86.0,             # Max damage from fall off
            "damageFallOffMaxDamageDistance": 38000.0,  # Distance the max damage occurs until
            "armorPenetrationDepthMM": 7,               # Armor pen depth (mm)
            "traceDistanceAfterPen": 10.0,                # Trace distance after penetrating to determine if damage will occur

            "MOA": 3,                   # How accurate the weapon is (In minutes of angle aka 1/60th of a degree)
            "emptyMagReload": false,    # If a mag must be empty to reload
            "equipDuration": 1.63,      # How long it takes to equip
            "unequipDuration": 1.316    # How long it takes to dequip
        },


        # Physical info
        "physicalInfo": {
            "skeletalMesh": "C6",                  # Mesh of weapon
            "attachments": [                       # Attachments (blueprint names, there are no pretty names afaik)
                "BP_Attachment_PAQ_NoSwitch_C"
            ]
        },

        # ICO Info
        "staticInfo": {
            "sway": {
                "dynamic": {
                    "lowStaminaSwayFactor": 3.5,        # "Amount of additive sway to apply when low on stamina"
                    "fullStaminaSwayFactor": 0.0,       # "Amount of additive sway to apply when full on stamina"
                    "holdingBreathSwayFactor": 0.66,    # "Sway factor applied to stance's minimum sway range"
                    "addMoveSway": 0.0004,              # "Amount of additve sway to add when moving"
                    "minMoveSwayFactor": 0.0,           # "Minimum amount of additve sway possible when moving"
                    "maxMoveSwayFactor": 22.0           # "Maximum amount of additve sway possible when moving"
                },
                "stance": {
                    "proneADSSwayMin": 1.5,             # Min sway range when aiming down sights while prone
                    "proneSwayMin": 3.0,                # Min sway range while prone
                    "crouchADSSwayMin": 6.0,            # Min sway range when aiming down sights while crouching
                    "crouchSwayMin": 8.0,               # Min sway range while crouching
                    "standingADSSwayMin": 9.0,          # Min sway range when aiming down sights while standing
                    "standingSwayMin": 12.0,            # Min sway range while standing
                    "bipodADSSwayMin": 0.0,             # Min sway range when aiming down sights while using a bipod
                    "bipodSwayMin": 0.0                 # Min sway range when while using a bipod
                },
                "maxSway": 10.0                         # Max sway
            },
            "swayAlignment": { # Unsure how sway alignment is different than sway but the numbers are different so here they are!
                "dynamic": {
                    "lowStaminaSwayFactor": 3.5,        # "Amount of additive sway to apply when low on stamina"
                    "fullStaminaSwayFactor": 0.0,       # "Amount of additive sway to apply when full on stamina"
                    "holdingBreathSwayFactor": 0.66,    # "Sway factor applied to stance's minimum sway range"
                    "addMoveSway": 0.0004,              # "Amount of additve sway to add when moving"
                    "minMoveSwayFactor": 0.0,           # "Minimum amount of additve sway possible when moving"
                    "maxMoveSwayFactor": 22.0           # "Maximum amount of additve sway possible when moving"
                },
                "stance": {
                    "proneADSSwayMin": 1.5,             # Min sway range when aiming down sights while prone
                    "proneSwayMin": 1.5,                # Min sway range while prone
                    "crouchADSSwayMin": 2.7,            # Min sway range when aiming down sights while crouching
                    "crouchSwayMin": 2.7,               # Min sway range while crouching
                    "standingADSSwayMin": 3.5,          # Min sway range when aiming down sights while standing
                    "standingSwayMin": 5.0,             # Min sway range while standing
                    "bipodADSSwayMin": 0.6,             # Min sway range when aiming down sights while using a bipod
                    "bipodSwayMin": 0.7                 # Min sway range when while using a bipod
                },
                "maxSway": -1.0                         # Max sway
            },

            # Sway
            "spring": {
                "weaponSpringSide": -1,             # "Should the item follow or counter player rotation"
                "weaponSpringStiffness": 0.75,      # "How oscillating should the spring be" 
                "weaponSpringDamping": 0.4,         # "Decay speed of spring oscillation"
                "weaponSpringMass": 0.05            # "Amplitude and resistance to change of the spring oscillation"
            },
            "recoil": {
                "camera": {
                    "recoilCameraOffsetFactor": 0.35,           # "How much the camera goes up as the sight is offsetting from the center"
                    "recoilCameraOffsetInterpSpeed": 5.0,       # "How fast the camera goes up as the sight is offsetting from the center"
                    "recoilLofCameraOffsetLimit": 20.0,         # "How far the sight can go away from the center of the screen (on any axis)"
                    "recoilLofAttackInterpSpeed": 45.0,         # "How fast the sight is reaching the new point defined by the past shot (don't change it except for specific cases)"
                    "recoilCanReleaseInterpSpeed": 30.0,        # "Speed of timer allowing the sight to go back to the center"
                    "recoilLofReleaseInterpSpeed": 10.0,        # "How fast the sight goes back to the cetner of the screen when it's allowed to"
                    "recoilAdsCameraShotInterpSpeed": 200.0     # "Speed of camera bone rotation update when firing while ads. Set to zero for disabiling it"
                },
                "dynamic": {
                    "recoilAlignmentMultiplierMax": 2.0             # "Maxium additve multiplier for recoil misalignment (Stance + Movement + Stamina)
                    "movement": {
                        "moveRecoilFactorRelease": 1.0,             # "Reset shot recoil multiplier (Increases the szie of deltatime, reducing the time to get to minumum after movement)"
                        "addMoveRecoil": 1.0,                       # "Amount of additive recoil to add when moving"
                        "maxMoveRecoilFactor": 2.0,                 # "Maximum amount of additive recoil possible when moving"
                        "minMoveRecoilFactor": 0.07,                # "Minumum amount of additve recoil possible when moving"
                        "recoilAlignmentMovementAddative": 0.3,     # "Additve recoil misalignment from moving when firing"
                        "recoilAlignmentMovementExponent": 1.0      # "Allows you to ease in the addtional recoil misalignment from firing while moving"
                    },
                    "stamina": {                                    
                        "lowStaminaRecoilFactor": 0.2,              # "Amount of additve recoil to apply when low on stamina"
                        "fullStaminaRecoilFactor": 0.0,             # "Amount of additve recoil to apply when full on stamina"
                        "recoilAlignmentStaminaAddative": 0.1,      # "Additve recoil misalignment from firing with low stamina"
                        "recoilAlignmentStaminaExponent": 0.5       # "Allows you to ease in the addtional recoil misalignment from firing while tired"
                    },
                    "shoulder": {
                        "recoilAlignmentShoulderMax": {             # "Maximum misalgnment per-shot, rotating around the shoulder bone"
                            "x": 3.0,
                            "y": 2.0
                        },
                        "recoilAlignmentShoulderAngleLimits": {     # "Maximum overall misalginent, to prevent misalignment adding up too far from rapid fire"
                            "x": 5.0,
                            "y": 4.0
                        }
                    },
                    "grip": {
                        "recoilAlignmentGripMax": {                 # "Maximum misalgnment per-shot, rotating around the grip bone"
                            "x": 5.0,
                            "y": 4.0
                        },
                        "recoilAlignmentGripAngleLimits": {         # "Maximum overall misalginent, to prevent misalignment adding up too far from rapid fire"
                            "x": 11.0,
                            "y": 7.0
                        }
                    },
                }
            }
        }
    },
```