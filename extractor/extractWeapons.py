# py "E:\Squad SDK\SquadEditor\Squad\Content\Python\squadwiki\extractWeapons.py"
# ----- Imports -----
import unreal
import os
import json


# ----- Settings -----
# Install Path of the SDK
installDirectory = "E:\\Squad SDK\\"

# Directory to export to
exportDirectory = "E:\\Squad SDK\\"

# Dict that contains directory and folders. Modders can add a new dict under vanilla with a directory and one set of sub-folders to look through.
# Note that the file structure needs to be the same as vanilla. If you're having issues, reach out on GitHub or Discord.
# "GrenadeLaunchers", "RocketLaunchers", "Shotguns", "SubmachineGuns"
weaponsDirectoryObject = {
    "vanilla": {
        "weaponDirectory": f"{installDirectory}SquadEditor\\Squad\\Content\\Blueprints\\Items\\",
        "factionsDirectory": f"{installDirectory}SquadEditor\\Squad\\Content\\Settings\\FactionSetups\\",
        "folders": ["MachineGuns", "Pistols", "Rifles"],
        "factionBlacklist": ["Templates", "TestFactionSetups", "UI", "Tutorials", "Units"]
    },
}


# ----- Exception Classes -----
class InvalidWeaponFolder(OSError):
    def __init__(self, folder):
        raise OSError(f"Invalid Weapon Folder Listed: {folder}")


class InvalidAttribute(AttributeError):
    def __init__(self, weapon):
        raise AttributeError(f"Invalid Weapon: {weapon}")


class InvalidDirectoryKeySetup(KeyError):
    def __init__(self, type, key):
        raise KeyError(f"Key {key} is missing in {type} in the weaponsDirectoryObject")

def searchFolderForFactions(baseFolder, directoryType):
    # Blacklist for folders/files to not check CASE SENSITIVE
    blacklist = weaponsDirectoryObject[directoryType]["factionBlacklist"]
    weapons = {}
    '''
        "name": {
            "factions": []
        }
    '''
    for item in os.listdir(baseFolder):
        # If the item is blacklisted, skip
        if not any(x == item for x in blacklist):
            # If it's a folder, we need to search it so recursively search
            if os.path.isdir(baseFolder + item):
                returnWeapons = searchFolderForFactions(baseFolder + item + "\\", directoryType)

                # Merge returned weapon and current weapons
                for attr, value in returnWeapons.items():
                    if attr not in weapons:
                        weapons[attr] = value
                    else:
                        for faction in value["factions"]:
                            if faction not in  weapons[attr]["factions"]:
                                weapons[attr]["factions"].append(faction)

            # If it's a file, we need to extract the data from it
            elif os.path.isfile(baseFolder + item):
                # Adjust path to load object based on where the file is located. Base game, expansions, and mods all are in different locations, so we need to cut and add accordingly.'
                newBaseFolder = ""
                if "content" in weaponsDirectory or "Content" in weaponsDirectory:
                    pathToCutSearch = f"{installDirectory}SquadEditor\\Squad\\Content\\"
                    newBaseFolder = "/Game/" + baseFolder[len(pathToCutSearch):]

                elif "expansions" in weaponsDirectory or "Expansions" in weaponsDirectory:
                    pathToCutSearch = f"{installDirectory}SquadEditor\\Squad\\Plugins\\Expansions\\"
                    newBaseFolder = "/" + baseFolder[len(pathToCutSearch):]

                elif "mods" in weaponsDirectory or "Mods" in weaponsDirectory:
                    pathToCutSearch = f"{installDirectory}SquadEditor\\Squad\\Plugins\\Mods\\"
                    newBaseFolder = "/" + baseFolder[len(pathToCutSearch):]

                # Remove .uasset from asset name
                itemName = item.split(".")[0]

                unrealFaction = unreal.load_object(None, f"{newBaseFolder}{itemName}.{itemName}")
                # Create a shorthand less descriptive version

                # Check to see if the item is a faction setup, if it is then we can get the info we need from it
                if unrealFaction.get_class().get_name() == "BP_SQFactionSetup_C":
                    factionID = unrealFaction.faction_id

                    # Loop through every role in the roles array
                    for roleSetting in unrealFaction.roles:
                        role = roleSetting.setting

                        # Loop through the inventory slots
                        for inventorySlot in role.inventory:
                            slotWeapons = inventorySlot.weapon_items
                            # Loop through the weapons in the slot
                            for slotWeapon in slotWeapons:
                                weaponInSlotName = str(slotWeapon.equipable_item.get_name())

                                # If the weapon slot is in the array then append to the factions list otherwise just add the dict in
                                if weaponInSlotName in weapons:
                                    # If the faction is not present yet, then add it
                                    if str(factionID) not in weapons[weaponInSlotName]["factions"]:
                                        weapons[weaponInSlotName]["factions"].append(str(factionID))
                                else:
                                    weapons[weaponInSlotName] = {
                                        "factions": [str(factionID)]
                                    }


    return weapons

# ----- Code -----


weaponsJSON = {}

print("Squad Wiki Pipeline: Weapons and Vehicles")

for attr, value in weaponsDirectoryObject.items():

    # --- Loading Files ---
    # Try saving the directories, if there is an issue then raise an exception
    try:
        weaponsDirectory = value["weaponDirectory"]
    except KeyError:
        raise InvalidDirectoryKeySetup(attr, "weaponDirectory")

    try:
        factionsDirectory = value["factionsDirectory"]
    except KeyError:
        raise InvalidDirectoryKeySetup(attr, "factionsDirectory")

    try:
        listOfWeaponFolders = value["folders"]
    except KeyError:
        raise InvalidDirectoryKeySetup(attr, "folders")
    
    try:
        test = value["factionBlacklist"]
    except KeyError:
        raise InvalidDirectoryKeySetup(attr, "factionBlacklist")

    # --- Get Faction Info ---
    print(f"Searching through {attr} factions...")

    weaponFactions = searchFolderForFactions(factionsDirectory, attr)

    # --- Get Weapon Info ---
    print(f"Searching through {attr} weapons...")

    for weaponFolder in listOfWeaponFolders:
        print(f"Searching in {weaponFolder}...", flush=True)

        # Verify weapon folder is valid
        pathToSearch = weaponsDirectory + weaponFolder
        if not os.path.isdir(pathToSearch):
            raise InvalidWeaponFolder(weaponFolder)

        # Loop through each file/dir in the folder
        for weapon in os.listdir(weaponsDirectory + weaponFolder):

            # -- Setup --
            weaponName = weapon.split(".")[0]
            # Only look at files, not child directories
            if not os.path.isfile(pathToSearch + "\\" + weapon):
                continue

            # Skip any generic weapons. These are not setup as real weapons and have invalid values
            if "Generic" in weaponName:
                continue

            # Create new path for unreal reference
            if "content" in weaponsDirectory or "Content" in weaponsDirectory:
                pathToCut = f"{installDirectory}SquadEditor\\Squad\\Content\\"
                newPath = "/Game/" + pathToSearch[len(pathToCut):]

            elif "expansions" in weaponsDirectory or "Expansions" in weaponsDirectory:
                pathToCut = f"{installDirectory}SquadEditor\\Squad\\Plugins\\Expansions\\"
                newPath = "/" + pathToSearch[len(pathToCut):]

            elif "mods" in weaponsDirectory or "Mods" in weaponsDirectory:
                pathToCut = f"{installDirectory}SquadEditor\\Squad\\Plugins\\Mods\\"
                newPath = "/" + pathToSearch[len(pathToCut):]



            # Get unreal version of the file
            unrealWeapon = unreal.load_object(None, f"{newPath}/{weaponName}.{weaponName}_C")
            unrealWeaponDefault = unreal.get_default_object(unrealWeapon)
            # Create a shorthand less descriptive version
            uWD = unrealWeaponDefault


            # -- Tracers --

            # Check to see if the tracer projectile class is present, if it is grab the name of it, otherwise leave as None
            tracerProjectileClass = uWD.weapon_config.tracer_projectile_class
            if tracerProjectileClass is not None:
                tracerProjectileClass = uWD.weapon_config.tracer_projectile_class.get_name()

            # -- Curves --

            # Damage Curve
            damageFallOffTimeRange = uWD.weapon_config.damage_falloff_curve.get_time_range()  # Get max and min of time (distance) range
            damageFOTFarDistance = damageFallOffTimeRange[1]
            damageFOTCloseDistance = damageFallOffTimeRange[0]
            damageFOMaxDamage = uWD.weapon_config.damage_falloff_curve.get_float_value(damageFOTCloseDistance)
            damageFOMinDamage = uWD.weapon_config.damage_falloff_curve.get_float_value(damageFOTFarDistance)


            # -- Faction --
            # Get faction info for the weapon
            factions = []

            if weaponName + "_C" in weaponFactions:
                factions = weaponFactions[weaponName + "_C"]["factions"]

            # -- Attachments --

            attachments = uWD.attachment_classes

            attachmentNames = []

            for attachment in attachments:
                if attachment is not None:
                    attachmentName = attachment.get_name()
                    attachmentNames.append(attachmentName)

            # -- ICO Static Info

            staticInfoClass = unreal.get_default_object(uWD.item_static_info_class)

            staticInfo = {
                "sway": {
                    "dynamic": {
                        "lowStaminaSwayFactor": round(staticInfoClass.sway_data.dynamic_group.stamina.low_stamina_sway_factor, 5),
                        "fullStaminaSwayFactor": round(staticInfoClass.sway_data.dynamic_group.stamina.full_stamina_sway_factor, 5),
                        "holdingBreathSwayFactor": round(staticInfoClass.sway_data.dynamic_group.breath.holding_breath_sway_factor, 5),
                        "addMoveSway": round(staticInfoClass.sway_data.dynamic_group.movement.add_move_sway, 5),
                        "minMoveSwayFactor": round(staticInfoClass.sway_data.dynamic_group.movement.min_move_sway_factor, 5),
                        "maxMoveSwayFactor": round(staticInfoClass.sway_data.dynamic_group.movement.max_move_sway_factor, 5),
                    },
                    "stance": {
                        "proneADSSwayMin": round(staticInfoClass.sway_data.stance_group.prone.ads_sway_min, 5),
                        "proneSwayMin": round(staticInfoClass.sway_data.stance_group.prone.sway_min, 5),
                        "crouchADSSwayMin": round(staticInfoClass.sway_data.stance_group.crouch.ads_sway_min, 5),
                        "crouchSwayMin": round(staticInfoClass.sway_data.stance_group.crouch.sway_min, 5),
                        "standingADSSwayMin": round(staticInfoClass.sway_data.stance_group.standing.ads_sway_min, 5),
                        "standingSwayMin": round(staticInfoClass.sway_data.stance_group.standing.sway_min, 5),
                        "bipodADSSwayMin": round(staticInfoClass.sway_data.stance_group.bipod.ads_sway_min, 5),
                        "bipodSwayMin": round(staticInfoClass.sway_data.stance_group.bipod.sway_min, 5),
                    },
                    "maxSway": round(staticInfoClass.sway_data.limits.final_sway_clamp, 5),
                },
                "swayAlignment": {
                    "dynamic": {
                        "lowStaminaSwayFactor": round(staticInfoClass.sway_alignment_data.dynamic_group.stamina.low_stamina_sway_factor, 5),
                        "fullStaminaSwayFactor": round(staticInfoClass.sway_alignment_data.dynamic_group.stamina.full_stamina_sway_factor, 5),
                        "holdingBreathSwayFactor": round(staticInfoClass.sway_alignment_data.dynamic_group.breath.holding_breath_sway_factor, 5),
                        "addMoveSway": round(staticInfoClass.sway_alignment_data.dynamic_group.movement.add_move_sway, 5),
                        "minMoveSwayFactor": round(staticInfoClass.sway_alignment_data.dynamic_group.movement.min_move_sway_factor, 5),
                        "maxMoveSwayFactor": round(staticInfoClass.sway_alignment_data.dynamic_group.movement.max_move_sway_factor, 5),
                    },
                    "stance": {
                        "proneADSSwayMin": round(staticInfoClass.sway_alignment_data.stance_group.prone.ads_sway_min, 5),
                        "proneSwayMin": round(staticInfoClass.sway_alignment_data.stance_group.prone.sway_min, 5),
                        "crouchADSSwayMin": round(staticInfoClass.sway_alignment_data.stance_group.crouch.ads_sway_min, 5),
                        "crouchSwayMin": round(staticInfoClass.sway_alignment_data.stance_group.crouch.sway_min, 5),
                        "standingADSSwayMin": round(staticInfoClass.sway_alignment_data.stance_group.standing.ads_sway_min, 5),
                        "standingSwayMin": round(staticInfoClass.sway_alignment_data.stance_group.standing.sway_min, 5),
                        "bipodADSSwayMin": round(staticInfoClass.sway_alignment_data.stance_group.bipod.ads_sway_min, 5),
                        "bipodSwayMin": round(staticInfoClass.sway_alignment_data.stance_group.bipod.sway_min, 5),
                    },
                    "maxSway": round(staticInfoClass.sway_alignment_data.limits.final_sway_clamp, 5),
                },
                "spring": {
                    "weaponSpringSide": round(staticInfoClass.weapon_spring_side, 5),
                    "weaponSpringStiffness": round(staticInfoClass.weapon_spring_stiffness, 5),
                    "weaponSpringDamping": round(staticInfoClass.weapon_spring_critical_damping_factor, 5),
                    "weaponSpringMass": round(staticInfoClass.weapon_spring_mass, 5)
                },
                "recoil": {
                    "camera": {
                        "recoilCameraOffsetFactor": round(staticInfoClass.recoil_camera_offset_factor, 5),
                        "recoilCameraOffsetInterpSpeed": round(staticInfoClass.recoil_camera_offset_interp_speed, 5),
                        "recoilLofCameraOffsetLimit": round(staticInfoClass.recoil_lof_camera_offset_limit, 5),
                        "recoilLofAttackInterpSpeed": round(staticInfoClass.recoil_lof_attack_interp_speed, 5),
                        "recoilCanReleaseInterpSpeed": round(staticInfoClass.recoil_can_release_interp_speed, 5),
                        "recoilLofReleaseInterpSpeed": round(staticInfoClass.recoil_lof_release_interp_speed, 5),
                        "recoilAdsCameraShotInterpSpeed": round(staticInfoClass.recoil_ads_camera_shot_interp_speed, 5)
                    },
                    "dynamic": {
                        "movement": {
                            "moveRecoilFactorRelease": round(staticInfoClass.move_recoil_factor_release, 5),
                            "addMoveRecoil": round(staticInfoClass.add_move_recoil, 5),
                            "maxMoveRecoilFactor": round(staticInfoClass.max_move_recoil_factor, 5),
                            "minMoveRecoilFactor": round(staticInfoClass.min_move_recoil_factor, 5),
                            "recoilAlignmentMovementAddative": round(staticInfoClass.recoil_alignment_movement_addative, 5),
                            "recoilAlignmentMovementExponent": round(staticInfoClass.recoil_alignment_movement_exponent, 5)
                        },
                        "stamina": {
                            "lowStaminaRecoilFactor": round(staticInfoClass.low_stamina_recoil_factor, 5),
                            "fullStaminaRecoilFactor": round(staticInfoClass.full_stamina_recoil_factor, 5),
                            "recoilAlignmentStaminaAddative": round(staticInfoClass.recoil_alignment_stamina_addative, 5),
                            "recoilAlignmentStaminaExponent": round(staticInfoClass.recoil_alignment_stamina_exponent, 5)
                        },
                        "shoulder": {
                            "recoilAlignmentShoulderMax": {
                                "x": round(staticInfoClass.recoil_alignment_shoulder_max.x, 5),
                                "y" : round(staticInfoClass.recoil_alignment_shoulder_max.y, 5)
                            },
                            "recoilAlignmentShoulderAngleLimits": {
                                "x": round(staticInfoClass.recoil_alignment_shoulder_angle_limits.x, 5),
                                "y" : round(staticInfoClass.recoil_alignment_shoulder_angle_limits.y, 5)
                            }
                        },
                        "grip": {
                            "recoilAlignmentGripMax": {
                                "x": round(staticInfoClass.recoil_alignment_grip_max.x, 5),
                                "y" : round(staticInfoClass.recoil_alignment_grip_max.y, 5)
                            },
                            "recoilAlignmentGripAngleLimits": {
                                "x": round(staticInfoClass.recoil_alignment_grip_angle_limits.x, 5),
                                "y" : round(staticInfoClass.recoil_alignment_grip_angle_limits.y, 5)
                            }
                        },
                        "recoilAlignmentMultiplierMax": round(staticInfoClass.recoil_alignment_multiplier_max, 5),
                    }
                }
            }

            # Need to add: ICO
            # -- Dict Creation --
            try:
                weaponInfo = {
                    "displayName": str(uWD.display_name),
                    "rawName": f"{weaponName}.{weaponName}_C",
                    "folder": weaponFolder,
                    "factions": factions,

                    # Inventory Info
                    "inventoryInfo": {
                        "description": str(uWD.item_description),
                        "HUDTexture": str(uWD.hud_selected_texture.get_name()),
                        "inventoryTexture": str(uWD.hud_texture.get_name()),
                        "ammoPerRearm": round(uWD.ammo_per_rearm_item, 5),
                        "showItemCount": bool(uWD.show_item_count_in_inventory),
                        "showMagCount": bool(uWD.show_mag_count_in_inventory),
                    },

                    # Weapon info
                    "weaponInfo": {
                        # Mag info
                        "maxMags": round(uWD.weapon_config.max_mags, 5),
                        "roundsPerMag": round(uWD.weapon_config.rounds_per_mag, 5),
                        "roundInChamber": bool(uWD.weapon_config.allow_round_in_chamber),
                        "allowSingleLoad": bool(uWD.weapon_config.allow_single_load),

                        # Shooting
                        "firemodes": list(uWD.weapon_config.firemodes),
                        "timeBetweenShots": round(uWD.weapon_config.time_between_shots, 5),  # Burst, auto fire
                        "timeBetweenSingleShots": round(uWD.weapon_config.time_between_single_shots, 5),  # Semi-Auto
                        "avgFireRate": bool(uWD.weapon_config.average_fire_rate),
                        "resetBurstOnTriggerRelease": bool(uWD.weapon_config.reset_burst_on_trigger_release),

                        # Reloading
                        "reloadCancelGracePeriod": round(uWD.weapon_config.finish_reload_grace_period, 5),  # "Finish reload grace period for cancelling reload close to finishing the reload process"
                        "tacticalReloadDuration": round(uWD.weapon_config.tactical_reload_duration, 5),
                        "dryReloadDuration": round(uWD.weapon_config.dry_reload_duration, 5),
                        "tacticalReloadBipodDuration": round(uWD.weapon_config.tactical_reload_bipod_duration, 5),
                        "dryReloadBipodDuration": round(uWD.weapon_config.reload_dry_bipod_duration, 5),

                        # ADS
                        "ADSPostTransitionRation": round(uWD.weapon_config.ads_post_transition_ratio, 5),
                        "allowZoom": bool(uWD.weapon_config.allow_zoom),  # Allow ADS
                        "ADSMoveSpeedMultiplier": round(uWD.ads_move_speed_multiplier, 5),

                        # Projectile
                        "projectileClass": str(uWD.weapon_config.projectile_class.get_name()),
                        "tracerProjectileClass": tracerProjectileClass,
                        "roundsBetweenTracer": round(uWD.weapon_config.rounds_between_tracer, 5),
                        "muzzleVelocity": round(uWD.weapon_config.muzzle_velocity, 5),

                        # Damage
                        "damageFallOffMinDamage": damageFOMinDamage,
                        "damageFallOffMinDamageDistance": damageFOTFarDistance,
                        "damageFallOffMaxDamage": damageFOMaxDamage,
                        "damageFallOffMaxDamageDistance": damageFOTCloseDistance,
                        "armorPenetrationDepthMM": round(uWD.weapon_config.armor_penetration_depth_millimeters, 5),
                        "traceDistanceAfterPen": round(uWD.weapon_config.trace_distance_after_penetration_meters, 5),

                        # Accuracy
                        "MOA": round(uWD.weapon_config.moa),

                        "emptyMagReload": bool(uWD.weapon_config.empty_mag_to_reload),

                        # Equipping
                        "equipDuration": round(uWD.equip_duration, 5),
                        "unequipDuration": round(uWD.unequip_duration, 5),
                    },

                    # Focus info

                    # Physical info of the gun
                    "physicalInfo": {
                        "skeletalMesh": str(uWD.mesh1p.skeletal_mesh.get_name()),
                        "attachments": attachmentNames,
                    },

                    "staticInfo": staticInfo

                }

                '''"focusInfo": {
                                    "focusDistanceHipfire": round(uWD.dof_focus_distance_hipfire),
                                    "focusDistanceADS": round(uWD.dof_focus_distance_ads),
                                    "apertureHipfire": round(uWD.dof_aperture_hipfire),
                                    "apertureADS": round(uWD.dof_aperture_ads),
                                    "aimTimeMultiplier": round(uWD.aim_time_multiplier),
                                    "transitionCurve": "TOBEADDED",
                                    "recoilRampUpSpeed": round(uWD.dof_recoil_ramp_up_speed),
                                    "recoilDecaySpeed": round(uWD.dof_recoild_decay_speed),
                                    "recoilRandomMin": round(uWD.dof_recoil_random_min),
                                    "recoilRandomMax": round(uWD.dof_recoil_random_max)
                                },'''
            except AttributeError:
                raise InvalidAttribute(weaponName)

            weaponsJSON[weaponName] = weaponInfo

# Write file
with open(f"{installDirectory}weaponInfo.json", "w") as f:
    json.dump(weaponsJSON, f, indent=4)

print(f"File exported at {installDirectory}weaponInfo.json")

'''['recoil_alignment_new_shoulder_alignment', 'recoil_alignment_shoulder_target_offset', 'recoil_alignment_shoulder_current_offset', 'recoil_alignment_new_grip_alignment', 'recoil_alignment_grip_target_offset',
 'recoil_alignment_grip_current_offset', 'recoil_alignment_mult', 'recoil_magnitude', 'is_holding_breath', 'holding_breath_sway_factor', 'bul
 let_count_incrementer', 'hold_breath_ease_timeline', 'recoil_grip_alignment_timeline', 'recoil_shoulder_alignment_timeline', '__doc__', 'recoil_alignment_target_offset_setup', 'recoil_alignment_multiplier_setup', 'get_owner_soldier
 ', 'blueprint_is_animation_system_valid', '_wrapper_meta_data', 'weapon_config', 'current_state', 'cached_pip_scope', 'ads_move_s
 peed_multiplier', 'aiming_down_sights', 'fire_input', 'pending_fire', 'max_time_to_loop_sounds_after_last_fire', 'modified_tactical_reload_duration', 'modified_dry_reload_duration', 'current_fire_mode', 'magazines', '
 attachment_classes', 'attachments', 'ads_post_process_settings', 'dynamic_first_person_mesh_materials', 'fov_shader_name', 'focus_zoom_alpha',
                                                                                                                                             'simulated_ads_alpha', 'use_stop_adspp_drawing', 'stop_adspp_drawing',
 'holding_zoom_easing', 'holding_zoom_easing_alpha', 'fixed_zoom_fov', 'current_fov', 'zoomed_fov', 'focus_zoom_time', 'focus_additional_zoom', 'time_since_last_zoom_toggle', 'last_zoom_progress_at_toggle',
 'adjust_ads_sight_item_anim_pos', 'cached_adjust_ads_sight_item_anim_pos', 'new_adj
 ust_ads_sight_item_anim_pos', 'adjust_ads_sight_item_anim_pos_alpha', 'is_modifying_zeroing', 'adjustable_sight_item_pos', 'suppression_info_class_override', 'calculated_ads_time', 'cached_last_zeroing_time', '
 cached_last_zeroing_play_time', 'cached_last_zeroing_position', 'cached_is_bipod_deployed', 'cached_aim_prone_bobbing', 'finished_ads_transition', 'la
 st_new_zoom', 'fire_sway_selector', 'pre_fire_sway_selector', 'update_bipod', 'update_aim_prone_bobbing', 'toggle_firemode', 'stop_modify_zeroing', 'start_reload', 'start_modify_zeroing', 'set_zoom', 'play_impact_effect', '
 play_firing_sound', 'magazine_has_ammo', 'is_zoomed', 'is_reloading', 'is_pulling_trigger', 'is_pending_fire', 'is_fully_zoomed', 'is_aim
 ing_down_sights', 'get_zoom_progress', 'get_weapon_static_info', 'get_moa_adjusted_aim_direction_from_rotator', 'get_moa_adjusted_aim_direction', 'get_current_moa', 'get_aim_location', 'get_aim_direction', 'can_toggle_firemode', '
 blueprint_on_zoom', 'blueprint_on_toggle_firemode', 'blueprint_on_reloaded', 'blueprint_on_reload', 'blueprint_on_pre_reload', 'bl
 ueprint_on_fire', 'item_static_info_class', 'debug_item_static_info_class', 'on_pawn_owner_changed_event', 'display_name', 'item_description', 'rearm_types_allowed', 'use_owner_as_master_pose', 'ammo_per_rearm_item', '
 unequipped_net_update_rate', 'action_state', 'sprint_blendspace', 'walk_forward_anim', 'idle_anim', 'use_anim', 'stand_anim', 'equip_anim', 'u
 nequip_anim', 'alt_use_anim', 'custom1_anim', 'custom2_anim', 'custom3_anim', 'pre_use_anim', 'post_use_anim', 'pre_alt_use_anim', 'post_alt_use_anim', 'hud_selected_texture', 'hud_texture', 'item_count_icon_texture', '
 show_item_count_in_inventory', 'show_mag_count_in_inventory', 'show_ammo_data_in_hud', 'change_dormancy_on_equip_state', 'item_count', 'max_i
 tem_count', 'cannot_rearm', 'equip_duration', 'unequip_duration', 'rearm_counter_multiplier', 'mesh1p', 'mesh3p', 'pawn_owner', 'cached_weapon1p_anim_instance', 'cached_weapon3p_anim_instance', 'cached_soldier1p_anim_instance', '
 cached_soldier3p_anim_instance', 'cached_equip_duration', 'cached_unequip_duration', 'equip_state', 'cached_move_bobbing', 'cached_
 sprint_bobbing', 'cached_has_movement', 'cached_is_pulling_trigger', 'cached_is_leaning_right', 'cached_is_leaning_left', 'cached_delta_time', 'update_sprint_bobbing', 'update_move_inputs', 'update_move_bobbing', 'update_lean_right
 ', 'update_lean_left', 'update_first_person_visibility', 'shovel_hit_deployable', 'set_raising_animation', 'set_lowering_animatio
 n', 'server_consume_item', 'reinitialize_equip', 'reinitialize_anim_instances', 'rearm', 'play_unequip_animation', 'play_sound_attached_to_weapon', 'play_equip_animation', 'pickup', 'is_first_person_view_target', 'is_equipped', '
 is_being_used', 'is_ammo_full', 'initialize_ammo_values', 'hide', 'has_ammo', 'get_rearm_max_item_count', 'get_rearm_item_count', '
 get_owner_pawn', 'get_mesh', 'get_item_static_info', 'get_fire_direction', 'get_controller', 'end_use', 'end_alt_use', 'drop', 'create_persisting_ammo_count', 'can_use', 'can_shovel', 'can_rearm_from_type', 'can_rearm', '
 can_alt_use', 'calculate_rearm_ammo_cost', 'calculate_missing_rearm_items', 'calculate_missing_ammo_cost', 'calculate_max_ammo_cost', 'bp_e
 nd_use', 'bp_end_alt_use', 'bp_begin_use', 'bp_begin_alt_use', 'blueprint_update_first_person_visibility', 'blueprint_on_unequipped', 'blueprint_on_unequip', 'blueprint_on_equipped', 'blueprint_on_equip', 'blueprint_draw_hud', '
 begin_use', 'begin_alt_use', 'only_relevant_to_owner', 'always_relevant', 'hidden', 'net_use_owner_relevancy', 'auto_destroy_when_fi
 nished', 'can_be_damaged', 'find_camera_component_when_view_target', 'generate_overlap_events_during_level_streaming', 'enable_auto_lod_generation', 'replicates', 'initial_life_span', 'life_span', 'custom_time_dilation', '
 net_dormancy', 'spawn_collision_handling_method', 'net_cull_distance_squared', 'net_update_frequency', 'min_net_update_frequency', 'net_pr
 iority', 'instigator', 'root_component', 'pivot_offset', 'sprite_scale', 'tags', 'on_take_any_damage', 'on_take_point_damage', 'on_take_radial_damage', 'on_actor_begin_overlap', 'on_actor_touch', 'on_actor_end_overlap', '
 on_actor_un_touch', 'on_begin_cursor_over', 'on_end_cursor_over', 'on_clicked', 'on_released', 'on_input_touch_begin', 'on_input_touch_end'
    , 'on_input_touch_enter', 'on_input_touch_leave', 'on_actor_hit', 'on_destroyed', 'on_end_play', 'was_recently_rendered', 'tear_off', 'set_tick_group', 'set_tickable_when_paused', 'set_replicates', 'set_replicate_movement',
 'set_owner', 'set_net_dormancy', 'set_life_span', 'set_is_temporarily_hidden_in_editor', 'set_folder_path', 'set_actor_tick_interval', '
 set_actor_tick_enabled', 'set_tick_enabled', 'set_actor_scale3d', 'set_actor_relative_scale3d', 'set_actor_label', 'set_actor_hidden_in_game', 'set_actor_hidden', 'set_actor_enable_collision', 'remove_tick_prerequisite_component
 ', 'remove_tick_prerequisite_actor', 'receive_tick', 'receive_radial_damage', 'receive_point_damage', 'receive_hit', 'receive_end_pl
 ay', 'receive_destroyed', 'receive_begin_play', 'receive_any_damage', 'receive_actor_on_released', 'receive_actor_on_input_touch_leave', 'receive_actor_on_input_touch_enter', 'receive_actor_on_input_touch_end', '
 receive_actor_on_input_touch_begin', 'receive_actor_on_clicked', 'receive_actor_end_overlap', 'receive_actor_untouch', 'receive_actor_end_cursor_ove
 r', 'receive_actor_begin_overlap', 'receive_actor_touch', 'receive_actor_begin_cursor_over', 'prestream_textures', 'make_noise', 'make_mid_for_material', 'teleport', 'set_actor_transform', 'set_actor_rotation', '
 set_actor_relative_transform', 'set_actor_relative_rotation', 'set_actor_relative_location', 'set_actor_location_and_rotation', 'set_actor_location'
    , 'on_reset', 'on_end_view_target', 'on_become_view_target', 'get_components_by_class', 'get_actor_rotation', 'get_actor_location', 'detach_from_actor', 'destroy_component', 'destroy_actor', 'attach_to_component',
 'attach_to_actor', 'add_actor_world_transform_keep_scale', 'add_actor_world_transform', 'add_actor_world_rotation', 'add_actor_world_offset', 'add
 _actor_local_transform', 'add_actor_local_rotation', 'add_actor_local_offset', 'is_temporarily_hidden_in_editor', 'is_selectable', 'is_overlapping_actor', 'is_hidden_ed_at_startup', 'is_hidden_ed', 'is_editable', 'is_child_actor
 ', 'is_actor_tick_enabled', 'is_actor_being_destroyed', 'has_authority', 'get_vertical_distance_to', 'get_velocity', 'get_actor_tran
 sform', 'get_tickable_when_paused', 'get_squared_horizontal_distance_to', 'get_squared_distance_to', 'get_remote_role', 'get_parent_component', 'get_parent_actor', 'get_owner', 'get_overlapping_components', 'get_touching_components
 ', 'get_overlapping_actors', 'get_touching_actors', 'get_local_role', 'get_life_span', 'get_instigator_controller', 'get_instigat
 or ', 'get_horizontal_dot_product_to', 'get_horizontal_distance_to', 'get_game_time_since_creation', 'get_folder_path', 'get_dot_product_to', 'get_distance_to', 'get_components_by_tag', 'get_components_by_interface', '
 get_component_by_class', 'get_attach_parent_socket_name', 'get_attach_parent_actor', 'get_attached_actors', 'get_all_child_actors', 'get_actor_
 up_vector', 'get_actor_time_dilation', 'get_actor_tick_interval', 'get_actor_scale3d', 'get_actor_right_vector', 'get_actor_relative_scale3d', 'get_actor_label', 'get_actor_forward_vector', 'get_actor_eyes_view_point', '
 get_actor_enable_collision', 'get_actor_bounds', 'force_net_update', 'flush_net_dormancy', 'enable_input', 'disable_input', 'add_tick_prereq
 uisite_component', 'add_tick_prerequisite_actor', 'set_tick_prerequisite', 'actor_has_tag', 'has_tag', '__hash__', '__str__', '__init__', '__new__', '_post_init', 'cast', 'get_default_object', 'static_class', 'get_class', '
 get_outer', 'get_typed_outer', 'get_outermost', 'get_name', 'get_fname', 'get_full_name', 'get_path_name', 'get_world', 'modify', 'rename
 ', 'get_editor_property', 'set_editor_property', 'set_editor_properties', 'call_method', '__repr__', '__getattribute__', '__setattr__', '__delattr__', '__lt__', '__le__', '__eq__', '__ne__', '__gt__', '__ge__', '__reduce_ex__', '
 __reduce__', '__subclasshook__', '__init_subclass__', '__format__', '__sizeof__', '__dir__', '__class__']'''

'''['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '_post_init', '_wrapper_meta_data', 'call_met
hod', 'cast', 'get_class', 'get_default_object', 'get_editor_property', 'get_float_value', 'get_fname', 'get_full_name', 'get_name', 'get_outer', 'get_outermost', 'get_path_name', 'get_time_range', 'get_typed_outer', 'get_value_range', 'get_world', 'modify', 'rename', 'set_editor_properties', 'set_editor_property', 'static_class']'''
