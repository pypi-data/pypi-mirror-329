""" xyz
Parser of the .xyz file format. 
"""
import os
from dataclasses import dataclass
from typing import Iterator


class ParseError(Exception):
    """ Error in parsing an xyz file. """


@dataclass
class AtomLineXYZ:
    symbol: str
    x: float
    y: float
    z: float
    extra: list[float]

    def __str__(self) -> str:
        fmt = '-13.8f'
        str_xyz = f"{self.symbol:<3}"
        for coord in [self.x, self.y, self.z] + self.extra:
            str_xyz += f"{coord:{fmt}}"
        return str_xyz


@dataclass
class MoleculeXYZ:
    """

    Test str on water::
        >>> water = MoleculeXYZ(
        ...     natoms=3,
        ...     comment='water',
        ...     atoms=[
        ...         AtomLineXYZ(symbol='H', x=0.0, y=-1.0, z=0.0, extra=[]),
        ...         AtomLineXYZ(symbol='O', x=0.0, y=0.0, z=1.0, extra=[]),
        ...         AtomLineXYZ(symbol='H', x=0.0, y=1.0, z=0.0, extra=[]),
        ...     ])
        >>> print(water)
        3
        water
        H     0.00000000  -1.00000000   0.00000000
        O     0.00000000   0.00000000   1.00000000
        H     0.00000000   1.00000000   0.00000000
    """
    natoms: int
    comment: str
    atoms: list[AtomLineXYZ]

    def __str__(self) -> str:
        str_xyz = f"{self.natoms}\n"
        str_xyz += f"{self.comment}\n"
        for atomline in self.atoms:
            str_xyz += f"{str(atomline)}\n"
        str_xyz = str_xyz[:-1]  # trim trailin new line

        return str_xyz

    @classmethod
    def from_Geometry(cls, geometry, comment: str = "Comment"):
        natoms = len(geometry.atoms)
        atoms = list()
        for atom in geometry.atoms:
            atoms.append(AtomLineXYZ(
                symbol=atom.name,
                x = atom.xyz[0],
                y = atom.xyz[1],
                z = atom.xyz[2],
                extra = [],
            ))
        return cls(natoms=natoms, comment=comment, atoms=atoms)


def parse_molecule(xyz_file: Iterator[str], natoms_line: str) -> MoleculeXYZ:
    try:
        natoms = int(natoms_line)
    except ValueError:
        raise ParseError(f"Expected number of atoms. Got {natoms_line}") from None

    comment = next(xyz_file).strip()
    atoms = list()
    for _ in range(natoms):
        try:
            line = next(xyz_file)
        except StopIteration:
            raise ParseError(f"Expected to find {natoms} atoms. Found only {len(atoms)}")
        atom_line = line.split()
        if len(atom_line) >= 4:
            atom = AtomLineXYZ(
                symbol=atom_line[0],
                x = float(atom_line[1]),
                y = float(atom_line[2]),
                z = float(atom_line[3]),
                extra = [float(coord) for coord in atom_line[4:]],
            )
            atoms += [atom]
        else:
            raise RuntimeError(
                "An incorrect xyz line; at least the atom symbol and"
                " three coordinates are required. Instead got this:\n"
                f"{line}"
            )

    entry_lengths = set(len(atom.extra) for atom in atoms)
    if len(entry_lengths) != 1:
        raise ParseError("Varying input length.")

    return MoleculeXYZ(natoms=natoms, comment=comment, atoms=atoms)


def parse(xyz_file: Iterator[str]) -> list[MoleculeXYZ]:
    """ Use this function to parse an xyz file.
    See the example below for a sample use.

    Water::
        >>> xyz_file=iter('''3
        ... water
        ... H 0.0 -1.0 0.0
        ... O 0.0  0.0 1.0
        ... H 0.0  1.0 0.0'''.split('\\n'))
        >>> parsed_xyz = parse(xyz_file)
        >>> water = parsed_xyz[0]
        >>> water.natoms
        3
        >>> water.comment
        'water'
        >>> atoms = water.atoms
        >>> atoms[0]
        AtomLineXYZ(symbol='H', x=0.0, y=-1.0, z=0.0, extra=[])
        >>> atoms[1].symbol
        'O'
        >>> atoms[2].y
        1.0
    """
    molecules = list()
    while True:
        try:
            natoms_line = next(xyz_file)
        except StopIteration:
            break
        molecules += [parse_molecule(xyz_file, natoms_line)]
    return molecules


def read_xyz_file(xyz_path: str) -> list[MoleculeXYZ]:
    xyz_path = os.path.expanduser(xyz_path)
    with open(xyz_path) as xyz_file:
        xyz_structures = parse(xyz_file)
    return xyz_structures
