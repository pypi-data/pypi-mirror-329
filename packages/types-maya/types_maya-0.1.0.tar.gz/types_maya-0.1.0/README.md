# types-maya

External type annotations for Autodesk Maya Python API.

The main goal is to provide helper for [Pyright](https://github.com/microsoft/pyright)
language server to offer better autocompletion.

## Installation

Install with [pip](https://pip.pypa.io/en/stable/topics/vcs-support/#git)
or [uv pip](https://docs.astral.sh/uv/pip/packages/#installing-a-package).

```bash
pip install types-maya
```

<!--
Install from vcs with [pip](https://pip.pypa.io/en/stable/topics/vcs-support/#git)
or [uv pip](https://docs.astral.sh/uv/pip/packages/#installing-a-package).

```bash
pip install git+https://github.com/tahv/types-maya@main
```
-->

## Available stubs

The stubs are maintained manually.
This means they will likely remains incomplete for some time.

I update the stubs based on the needs of my projects
and i mostly focus on Maya Python API 2.0 (`maya.api` modules).

| Import name               | Status               |
|---------------------------|----------------------|
| `maya.api.OpenMaya`       | 🟠 Incomplete (~20%) |
| `maya.api.OpenMayaAnim`   | 🔴 Not Covered       |
| `maya.api.OpenMayaRender` | 🔴 Not Covered       |
| `maya.api.OpenMayaUI`     | 🔴 Not Covered       |
| `maya.cmds`               | 🔴 Not Covered       |
| `maya.mel`                | 🟢 Complete          |
| `maya.standalone`         | 🟢 Complete          |
| `maya.OpenMaya`           | 🔴 Not Covered       |
| `maya.OpenMayaAnim`       | 🔴 Not Covered       |
| `maya.OpenMayaFX`         | 🔴 Not Covered       |
| `maya.OpenMayaMPx`        | 🔴 Not Covered       |
| `maya.OpenMayaRender`     | 🔴 Not Covered       |
| `maya.OpenMayaUI`         | 🔴 Not Covered       |

## Contributing

Contributions of any kind are welcome.
Please open an issue or a send pull request.
