> Update
```bash
...do changes...
git commit -m "Version 1.0.1"
git tag v1.0.1
git push origin v1.0.1
```

> Make sure hatch & twine are installed
```bash
pip install hatch
pip install twine
```

> Build
```bash
hatch build
```

This creates:
```bash
dist/
│── spida_api-1.0.1.tar.gz
│── spida_api-1.0.1-py3-none-any.whl
```
