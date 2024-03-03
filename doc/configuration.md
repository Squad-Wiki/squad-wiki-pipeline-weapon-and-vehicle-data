# Configuring the Pipeline

Each part of the pipeline can be configured individually. Currently only the weapons extractor is implmented so only that can be configured.

## Configuring the Weapons Extractor

Within `extractWeapons.py` is a section of code called settings.

```python
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
```
### Directories

The `installDirectory` must point towards the location of the squad base folder (the folder before `SquadEditor`).

The `exportDirectory` must point towards where you want the extracted data to export to.

### Directory Object

The `weaponsDirectoryObject` can be used for mods or to only extract specific folders. Mods **must** follow the same vanilla sub-folder layout to guarantee function.

The `weaponsDirectory` should point towards the folder that the weapons are located in. The extractor will look for the folders located in `folders` within this folder.

The `factionsDirectory` should point towards the folder where the factions data objects are located. The extractor will recursively search all folders within this main folder. The extractor **will** cause issues if there are other file types that are located within these folders. To avoid this, add specific files to the `factionBlacklist`.