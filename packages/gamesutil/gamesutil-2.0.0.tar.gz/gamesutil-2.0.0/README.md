# Gamesutil

> [!NOTE]
> Installation is supported only for the following: 
> - Windows
> - Linux

> [!NOTE]
> Development requires a fully configured [Dotfiles](https://github.com/florez-carlos/dotfiles) dev environment <br>

## Table of Contents

* [Installation](#installation)
  * [pip](#pip)
  * [manifest](#manifest) 
* [Usage](#usage)
  * [collect](#collect)
  * [inject](#inject) 
* [Old](#old)
* [Development](#development)

## Installation
### Pip
```bash
python3 -m pip install gamesutil
```
### Manifest
Create the Save-Manifest.json <br ><br >
> [!NOTE]
> Any instances of {STEAM_ID} are automatically replaced by the program with your Steam ID <br >
> If multiple Steam Ids are present in the Steam installation, the program will prompt the user for clarification <br >

The Manifest should contain: <br >
- coldLocation: The folder where the cold saves are stored
- saves:
  - save:
    - coldName: The folder name that will be stored in the cold save location
    - hotLocation: The location of the hot save
```json
{
  "coldLocation":"F:\\misc\\src\\gamesutil\\saves",
  "saves": [
    {
      "coldName":"My Game Save",
      "hotLocation": "%USERPROFILE%\\AppData\\Local\\Game Company\\The Game"
    },
    {
      "coldName":"My Other Game Save",
      "hotLocation": "C:\\Program Files (x86)\\Steam\\userdata\\{STEAM_ID}\\976730"
    }
  ]
}
```
In the above sample:

- cold location: F:\\misc\\src\\gamesutil\\saves\\My Game Save <br >

- hot location: "%USERPROFILE%\\AppData\\Local\\Game Company\\The Game" <br >
- hot location: "C:\\Program Files (x86)\\Steam\\userdata\\{STEAM_ID}\\976730" <br >

> [!NOTE]
> Hot location: should point to the directory where the game saves <br >
> Cold location: your backup
> {STEAM_ID} is replaced by the program with the actual Steam Id, if multiple exist in your system it will prompt the user for clarification

## Usage

### Collect

-sm The location of the Save Manifest<br >

```bash
gamesutil collect -sm C:\PATH\TO\SAVE-MANIFEST.JSON
```
This will copy all hot saves listed in the manifest into the cold save location

### Inject

-sm The location of the Save Manifest<br >

```bash
gamesutil inject -sm C:\PATH\TO\SAVE-MANIFEST.JSON
```

This will copy all the cold saves listed in the manifest into the hot save location

## Old

An "old" folder will be created inside the cold location, this folder maintains <br>
a copy from the previous collection and its useful in the event the most recent game save is corrupted

## Development

> [!NOTE]
> Development requires a fully configured [Dotfiles](https://github.com/florez-carlos/dotfiles) dev environment <br>

```bash
source init.sh
```

