# types-maya

[![Typed](https://img.shields.io/pypi/types/types-maya?logo=python&logoColor=white)](https://pypi.org/project/types-maya/)
[![Version](https://img.shields.io/pypi/v/types-maya?logo=pypi&logoColor=white)](https://pypi.org/project/types-maya/)
[![License](https://img.shields.io/github/license/tahv/types-maya)](https://github.com/tahv/types-maya/blob/main/LICENSE)
[![CI Tests](https://img.shields.io/github/actions/workflow/status/tahv/types-maya/tests.yml?logo=github&logoColor=white&label=tests)](https://github.com/tahv/types-maya/actions/workflows/tests.yml)

External type annotations for Autodesk Maya Python API.

The goal is to provide helper for [Pyright](https://github.com/microsoft/pyright)
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
and i mostly focus on Maya Python API 2.0 (`maya.api`).

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

The stubs are written from the
[Maya 2025 Reference](https://help.autodesk.com/view/MAYADEV/2025/ENU/).

## Contributing

Contributions of any kind are welcome.
Please open an issue or a submit pull request.
