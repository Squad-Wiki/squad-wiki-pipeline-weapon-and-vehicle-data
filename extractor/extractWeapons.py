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

# Dict that contains directory and folders. Modders can add a new dict under vanilla with a directory and one set of sub-folders to look through
weaponsDirectoryObject = {
    "vanilla": {
        "weaponDirectory": f"{installDirectory}SquadEditor\\Squad\\Content\\Blueprints\\Items\\",
        "factionsDirectory": f"{installDirectory}SquadEditor\\Squad\\Content\\Settings\\FactionSetups\\",
        "folders": ["MachineGuns", "Pistols", "Rifles"]
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


# ----- Code -----


weaponsJSON = {}

print("Squad Wiki Pipeline: Weapons and Vehicles")

for attr, value in weaponsDirectoryObject.items():

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

    print(f"Searching through {attr} factions...")

    searchFolderForFactions(factionsDirectory)

    print(f"Searching through {attr} weapons...")

    for weaponFolder in listOfWeaponFolders:
        print(f"Searching in {weaponFolder}...", flush=True)

        # Verify weapon folder is valid
        pathToSearch = weaponsDirectory + weaponFolder
        if not os.path.isdir(pathToSearch):
            raise InvalidWeaponFolder(weaponFolder)

        # Loop through each file/dir in the folder
        for weapon in os.listdir(weaponsDirectory + weaponFolder):

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

            # print(uWD.weapon_config.damage_falloff_curve.get_time_range())

            # Check to see if the tracer projectile class is present, if it is grab the name of it, otherwise leave as None
            tracerProjectileClass = uWD.weapon_config.tracer_projectile_class
            if tracerProjectileClass is not None:
                tracerProjectileClass = uWD.weapon_config.tracer_projectile_class.get_name()

            # Curves

            # Damage Curve
            damageFallOffTimeRange = uWD.weapon_config.damage_falloff_curve.get_time_range()  # Get max and min of time (distance) range
            damageFOTFarDistance = damageFallOffTimeRange[1]
            damageFOTCloseDistance = damageFallOffTimeRange[0]
            damageFOMaxDamage = uWD.weapon_config.damage_falloff_curve.get_float_value(damageFOTCloseDistance)
            damageFOMinDamage = uWD.weapon_config.damage_falloff_curve.get_float_value(damageFOTFarDistance)

            # Need to add: ICO
            try:
                weaponInfo = {
                    "displayName": str(uWD.display_name),
                    "rawName": f"{weaponName}.{weaponName}_C",
                    "folder": weaponFolder,

                    # Inventory Info
                    "inventoryInfo": {
                        "description": str(uWD.item_description),
                        "HUDTexture": str(uWD.hud_selected_texture.get_name()),
                        "inventoryTexture": str(uWD.hud_texture.get_name()),
                        "ammoPerRearm": int(uWD.ammo_per_rearm_item),
                        "showItemCount": bool(uWD.show_item_count_in_inventory),
                        "showMagCount": bool(uWD.show_mag_count_in_inventory),
                    },

                    # Weapon info
                    "weaponInfo": {
                        # Mag info
                        "maxMags": int(uWD.weapon_config.max_mags),
                        "roundsPerMag": int(uWD.weapon_config.rounds_per_mag),
                        "roundInChamber": bool(uWD.weapon_config.allow_round_in_chamber),
                        "allowSingleLoad": bool(uWD.weapon_config.allow_single_load),

                        # Shooting
                        "firemodes": list(uWD.weapon_config.firemodes),
                        "timeBetweenShots": int(uWD.weapon_config.time_between_shots),  # Burst, auto fire
                        "timeBetweenSingleShots": int(uWD.weapon_config.time_between_single_shots),  # Semi-Auto
                        "avgFireRate": bool(uWD.weapon_config.average_fire_rate),
                        "resetBurstOnTriggerRelease": bool(uWD.weapon_config.reset_burst_on_trigger_release),

                        # Reloading
                        "reloadCancelGracePeriod": int(uWD.weapon_config.finish_reload_grace_period),  # "Finish reload grace period for cancelling reload close to finishing the reload process"
                        "tacticalReloadDuration": int(uWD.weapon_config.tactical_reload_duration),
                        "dryReloadDuration": int(uWD.weapon_config.dry_reload_duration),
                        "tacticalReloadBipodDuration": int(uWD.weapon_config.tactical_reload_bipod_duration),
                        "dryReloadBipodDuration": int(uWD.weapon_config.reload_dry_bipod_duration),

                        # ADS
                        "ADSPostTransitionRation": int(uWD.weapon_config.ads_post_transition_ratio),
                        "allowZoom": bool(uWD.weapon_config.allow_zoom),  # Allow ADS
                        "ADSMoveSpeedMultiplier": int(uWD.ads_move_speed_multiplier),

                        # Projectile
                        "projectileClass": str(uWD.weapon_config.projectile_class.get_name()),
                        "tracerProjectileClass": tracerProjectileClass,
                        "roundsBetweenTracer": int(uWD.weapon_config.rounds_between_tracer),
                        "muzzleVelocity": int(uWD.weapon_config.muzzle_velocity),

                        # Damage
                        "damageFallOffMinDamage": damageFOMinDamage,
                        "damageFallOffMinDamageDistance": damageFOTFarDistance,
                        "damageFallOffMaxDamage": damageFOMaxDamage,
                        "damageFallOffMaxDamageDistance": damageFOTCloseDistance,
                        "armorPenetrationDepthMM": int(uWD.weapon_config.armor_penetration_depth_millimeters),
                        "traceDistanceAfterPen": int(uWD.weapon_config.trace_distance_after_penetration_meters),

                        # Accuracy
                        "MOA": int(uWD.weapon_config.moa),

                        "emptyMagReload": bool(uWD.weapon_config.empty_mag_to_reload),

                        # Equipping
                        "equipDuration": int(uWD.equip_duration),
                        "unequipDuration": int(uWD.unequip_duration),
                    },

                    # Focus info

                    # Physical info of the gun
                    "physicalInfo": {
                        "skeletalMesh": str(uWD.mesh1p.skeletal_mesh.get_name()),
                        "attachments": "TOBEADDED",
                    },

                }

                '''"focusInfo": {
                                    "focusDistanceHipfire": int(uWD.dof_focus_distance_hipfire),
                                    "focusDistanceADS": int(uWD.dof_focus_distance_ads),
                                    "apertureHipfire": int(uWD.dof_aperture_hipfire),
                                    "apertureADS": int(uWD.dof_aperture_ads),
                                    "aimTimeMultiplier": int(uWD.aim_time_multiplier),
                                    "transitionCurve": "TOBEADDED",
                                    "recoilRampUpSpeed": int(uWD.dof_recoil_ramp_up_speed),
                                    "recoilDecaySpeed": int(uWD.dof_recoild_decay_speed),
                                    "recoilRandomMin": int(uWD.dof_recoil_random_min),
                                    "recoilRandomMax": int(uWD.dof_recoil_random_max)
                                },'''
            except AttributeError:
                raise InvalidAttribute(weaponName)

            weaponsJSON[weaponName] = weaponInfo

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
