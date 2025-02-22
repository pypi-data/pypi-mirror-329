# Sphinx Minecraft

Add different Minecraft-oriented components to Sphinx.

## Installation

```bash
pip install sphinx-minecraft
```

Add the extension to your Sphinx `conf.py`:

```python
extensions = [
    'sphinx_minecraft'
]
```

## Available components

### Tree views

These components are based on [sphinx-treeview](https://github.com/Altearn/Sphinx-Tree-View).

#### Minecraft directory tree
**Usage:**
```rst
:::{treeview}
- {mcdir}`folder` folder
  - {mcdir}`mcfunction` function.mcfunction
  - {mcdir}`mcmeta` pack.mcmeta
  - {mcdir}`nbt` structure.nbt
- {mcdir}`folder` folder2
  - {mcdir}`file` file.txt
  - {mcdir}`audio` sound.ogg
  - {mcdir}`image` texture.png
  - {mcdir}`json` advancement.json
  - {mcdir}`yml` config.yml
:::
```
**Result:**

![Minecraft directory tree](https://raw.githubusercontent.com/Gunivers/Sphinx-Minecraft/main/imgs/mcdir.png)

#### NBT tree
**Usage:**
```rst
:::{treeview}
- {nbt}`compound` A compound tag
  - {nbt}`bool` A boolean tag
  - {nbt}`byte` A byte tag
  - {nbt}`short` A short tag
  - {nbt}`int` An integer tag
  - {nbt}`long` A long tag
  - {nbt}`float` A float tag
  - {nbt}`double` A double tag
  - {nbt}`string` A string tag
  - {nbt}`list` A list tag
  - {nbt}`number` A number tag
  - {nbt}`any` A tag to represent any type
- {nbt}`compound` A compound tag
  - {nbt}`long-array` A long array tag
  - {nbt}`byte-array` A byte array tag
  - {nbt}`int-array` An integer array tag
:::
```
**Result:**

![Minecraft NBT tree](https://raw.githubusercontent.com/Gunivers/Sphinx-Minecraft/main/imgs/nbt.png)

# License

This project is licensed under the MPL-2.0 License. See the [LICENSE](LICENSE) file for details.
File and folder icons came from [pictogrammers](https://pictogrammers.com/library/mdi/) and are under [Apache-2.0 License](https://pictogrammers.com/docs/general/license/).
Other icons of the Minecraft directory tree view are from [Material Icon Theme](https://github.com/material-extensions/vscode-material-icon-theme) and are under [MIT License](https://github.com/material-extensions/vscode-material-icon-theme/blob/main/LICENSE).