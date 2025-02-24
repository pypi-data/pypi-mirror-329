# xyz_parser
A python parser for the fileformat (.xyz) used for storing computational
chemistry data.

# Install
```bash
pip install xyz_parser
```

# Use
```python
import xyz_parser

with open('molecules.xyz') as molecules_file:
    molecule = xyz_parser.parse(molecules_file)

for molecule in molecules:
    print(f'{molecule.natoms=}')
    print(f'{molecule.comment=}')
    for atom in molecule.atoms:
        print(f'{atom.symbol=}', end='')
        print(f' {atom.x=}', end='')
        print(f' {atom.y=}', end='')
        print(f' {atom.z=}', end='')
        print(f' {atom.extra=}')
```
