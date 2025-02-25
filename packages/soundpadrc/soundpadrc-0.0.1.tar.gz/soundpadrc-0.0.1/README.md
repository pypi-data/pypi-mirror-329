![PyPI - Version](https://img.shields.io/pypi/v/soundpadrc)

# soundpadrc

Python library for controlling [Soundpad](https://www.leppsoft.com/soundpad/en/) via the [Soundpad Remote Control API](https://www.leppsoft.com/soundpad/en/rc/).

## Installation

To install soundpadrc from PyPI:

```bash
pip install soundpadrc
```

To install release candidate versions:

```bash
pip install --pre --upgrade -i https://test.pypi.org/simple/ soundpadrc
```

## Example Usage

```python
from soundpadrc import Soundpad

sp = Soundpad()

print(sp.categories())

print(sp.query_sounds("hobbit"))
```

## References

- https://github.com/Ilya-Kokhanovsky/soundpad.py
- https://www.leppsoft.com/soundpad/files/rc/SoundpadRemoteControl.java
- https://www.leppsoft.com/soundpad/en/rc/

## Python packaging

https://packaging.python.org/en/latest/tutorials/packaging-projects/  
https://github.com/pypa/sampleproject  
https://python-semantic-release.readthedocs.io/en/latest/  
https://python-semantic-release.readthedocs.io/en/latest/automatic-releases/github-actions.html  
https://packaging.python.org/en/latest/guides/publishing-package-distribution-releases-using-github-actions-ci-cd-workflows/
