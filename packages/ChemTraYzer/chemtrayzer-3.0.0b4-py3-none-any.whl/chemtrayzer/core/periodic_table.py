'''
Periodic table of elements.

.. data:: PERIODIC_TABLE

    Mapping containing all elements of the periodic table. Elements are
    retreivable by element symbol or atomic number, simply import this table,
    e.g. via ``from periodic_table import PERIODIC_TABLE as PTOE``, and obtain
    the element ``PTOE['He']`` or ``PTOE[2]``

'''
from dataclasses import dataclass
from types import MappingProxyType
from typing import Union
from collections.abc import Mapping


@dataclass
class Element:
    '''
    represents chemical element

    :param symbol: atomic symbol
    :param atomic_nr: atomic number of element
    :param mass: atomic mass in amu
    :param covalent_radius: covalent radius in (Pekka Pyykkö and Michiko
        Atsumi. Molecular Double-Bond Covalent Radii for Elements Li-E112.
        Chemistry - A European Journal, 15(46):12770–12779, nov 2009.
        URL: http://doi.wiley.com/10.1002/chem.200901472,
        doi:10.1002/chem.200901472.)
    '''

    symbol: str
    atomic_nr: int
    mass: float
    covalent_radius: float

    def __str__(self) -> str:
        return self.symbol

    def __eq__(self, other) -> bool:
        if isinstance(other, Element):
            return self.atomic_nr == other.atomic_nr

    def __lt__(self, other) -> bool:
        if isinstance(other, Element):
            return self.atomic_nr < other.atomic_nr

    def __repr__(self) -> str:
        return self.symbol

    def __hash__(self) -> int:
        '''
        Equal for same elements, so that Element objects can be used as keys
        '''
        return hash((self.symbol, self.mass))

    def __format__(self, __format_spec: str) -> str:
        if __format_spec == 's':
            return self.symbol
        elif __format_spec == 'd':
            return self.atomic_nr
        else:
            raise TypeError('unsupported format string passed to Element.'
                            '__format__')

# added underscore so that these are not imported with from constants import *
_SYMBOLS = {1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C', 7: 'N', 8: 'O',
            9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al', 14: 'Si', 15: 'P',
            16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K', 20: 'Ca', 21: 'Sc', 22: 'Ti',
            23: 'V', 24: 'Cr', 25: 'Mn', 26: 'Fe', 27: 'Co', 28: 'Ni',
            29: 'Cu', 30: 'Zn', 31: 'Ga', 32: 'Ge', 33: 'As', 34: 'Se',
            35: 'Br', 36: 'Kr', 37: 'Rb', 38: 'Sr', 39: 'Y', 40: 'Zr',
            41: 'Nb', 42: 'Mo', 43: 'Tc', 44: 'Ru', 45: 'Rh', 46: 'Pd',
            47: 'Ag', 48: 'Cd', 49: 'In', 50: 'Sn', 51: 'Sb', 52: 'Te',
            53: 'I', 54: 'Xe', 55: 'Cs', 56: 'Ba', 57: 'La', 58: 'Ce',
            59: 'Pr', 60: 'Nd', 61: 'Pm', 62: 'Sm', 63: 'Eu', 64: 'Gd',
            65: 'Tb', 66: 'Dy', 67: 'Ho', 68: 'Er', 69: 'Tm', 70: 'Yb',
            71: 'Lu', 72: 'Hf', 73: 'Ta', 74: 'W', 75: 'Re', 76: 'Os',
            77: 'Ir', 78: 'Pt', 79: 'Au', 80: 'Hg', 81: 'Tl', 82: 'Pb',
            83: 'Bi', 84: 'Po', 85: 'At', 86: 'Rn', 87: 'Fr', 88: 'Ra',
            89: 'Ac', 90: 'Th', 91: 'Pa', 92: 'U', 93: 'Np', 94: 'Pu',
            95: 'Am', 96: 'Cm', 97: 'Bk', 98: 'Cf', 99: 'Es', 100: 'Fm',
            101: 'Md', 102: 'No', 103: 'Lr', 104: 'Rf', 105: 'Db',
            106: 'Sg', 107: 'Bh', 108: 'Hs', 109: 'Mt', 110: 'Ds',
            111: 'Rg', 112: 'Cn', 113: 'Nh', 114: 'Fl', 115: 'Mc',
            116: 'Lv', 117: 'Ts', 118: 'Og'}

_ATOMIC_NRS = {'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7,
               'O': 8, 'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13,
               'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19,
               'Ca': 20, 'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25,
               'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30, 'Ga': 31,
               'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36, 'Rb': 37,
               'Sr': 38, 'Y': 39, 'Zr': 40, 'Nb': 41, 'Mo': 42, 'Tc': 43,
               'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49,
               'Sn': 50, 'Sb': 51, 'Te': 52, 'I': 53, 'Xe': 54, 'Cs': 55,
               'Ba': 56, 'La': 57, 'Ce': 58, 'Pr': 59, 'Nd': 60, 'Pm': 61,
               'Sm': 62, 'Eu': 63, 'Gd': 64, 'Tb': 65, 'Dy': 66, 'Ho': 67,
               'Er': 68, 'Tm': 69, 'Yb': 70, 'Lu': 71, 'Hf': 72, 'Ta': 73,
               'W': 74, 'Re': 75, 'Os': 76, 'Ir': 77, 'Pt': 78, 'Au': 79,
               'Hg': 80, 'Tl': 81, 'Pb': 82, 'Bi': 83, 'Po': 84, 'At': 85,
               'Rn': 86, 'Fr': 87, 'Ra': 88, 'Ac': 89, 'Th': 90, 'Pa': 91,
               'U': 92, 'Np': 93, 'Pu': 94, 'Am': 95, 'Cm': 96, 'Bk': 97,
               'Cf': 98, 'Es': 99, 'Fm': 100, 'Md': 101, 'No': 102,
               'Lr': 103, 'Rf': 104, 'Db': 105, 'Sg': 106, 'Bh': 107,
               'Hs': 108, 'Mt': 109, 'Ds': 110, 'Rg': 111, 'Cn': 112,
               'Nh': 113, 'Fl': 114, 'Mc': 115, 'Lv': 116, 'Ts': 117,
               'Og': 118}

_ELEMENT_WEIGHTS = {'H': 1.00794, 'He': 4.002602, 'Li': 6.941, 'Be': 9.012182,
                    'B': 10.811, 'C': 12.0107, 'N': 14.0067, 'O': 15.9994,
                    'F': 18.9984032, 'Ne': 20.1797, 'Na': 22.98976928,
                    'Mg': 24.305, 'Al': 26.9815386, 'Si': 28.0855,
                    'P': 30.973762, 'S': 32.065, 'Cl': 35.453, 'Ar': 39.948,
                    'K': 39.0983, 'Ca': 40.078, 'Sc': 44.955912, 'Ti': 47.867,
                    'V': 50.9415, 'Cr': 51.9961, 'Mn': 54.938045, 'Fe': 55.845,
                    'Co': 58.933195, 'Ni': 58.6934, 'Cu': 63.546, 'Zn': 65.409,
                    'Ga': 69.723, 'Ge': 72.64, 'As': 74.9216, 'Se': 78.96,
                    'Br': 79.904, 'Kr': 83.798, 'Rb': 85.4678, 'Sr': 87.62,
                    'Y': 88.90585, 'Zr': 91.224, 'Nb': 92.90638, 'Mo': 95.94,
                    'Tc': 98.9063, 'Ru': 101.07, 'Rh': 102.9055, 'Pd': 106.42,
                    'Ag': 107.8682, 'Cd': 112.411, 'In': 114.818, 'Sn': 118.71,
                    'Sb': 121.760, 'Te': 127.6, 'I': 126.90447, 'Xe': 131.293,
                    'Cs': 132.9054519, 'Ba': 137.327, 'La': 138.90547,
                    'Ce': 140.116, 'Pr': 140.90465, 'Nd': 144.242,
                    'Pm': 146.9151, 'Sm': 150.36, 'Eu': 151.964, 'Gd': 157.25,
                    'Tb': 158.92535, 'Dy': 162.5, 'Ho': 164.93032,
                    'Er': 167.259, 'Tm': 168.93421, 'Yb': 173.04,
                    'Lu': 174.967, 'Hf': 178.49, 'Ta': 180.9479, 'W': 183.84,
                    'Re': 186.207, 'Os': 190.23, 'Ir': 192.217, 'Pt': 195.084,
                    'Au': 196.966569, 'Hg': 200.59, 'Tl': 204.3833,
                    'Pb': 207.2, 'Bi': 208.9804, 'Po': 208.9824,
                    'At': 209.9871, 'Rn': 222.0176, 'Fr': 223.0197,
                    'Ra': 226.0254, 'Ac': 227.0278, 'Th': 232.03806,
                    'Pa': 231.03588, 'U': 238.02891, 'Np': 237.0482,
                    'Pu': 244.0642, 'Am': 243.0614, 'Cm': 247.0703,
                    'Bk': 247.0703, 'Cf': 251.0796, 'Es': 252.0829,
                    'Fm': 257.0951, 'Md': 258.0951, 'No': 259.1009,
                    'Lr': 262, 'Rf': 267, 'Db': 268, 'Sg': 271, 'Bh': 270,
                    'Hs': 269, 'Mt': 278, 'Ds': 281, 'Rg': 281, 'Cn': 285,
                    'Nh': 284, 'Fl': 289, 'Mc': 289, 'Lv': 292, 'Ts': 294,
                    'Og': 294}

_ELEMENT_COVALENT_RADII = {'H': 0.32, 'He': 0.46, 'Li': 1.33, 'Be': 1.02,
                           'B': 0.85, 'C': 0.75, 'N': 0.71, 'O': 0.63,
                           'F': 0.64, 'Ne': 0.67, 'Na': 1.55, 'Mg': 1.39,
                           'Al': 1.26, 'Si': 1.16, 'P': 1.11, 'S': 1.03,
                           'Cl': 0.99, 'Ar': 0.96, 'K': 1.96, 'Ca': 1.71,
                           'Sc': 1.48, 'Ti': 1.36, 'V': 1.34, 'Cr': 1.22,
                           'Mn': 1.19, 'Fe': 1.16, 'Co': 1.11, 'Ni': 1.1,
                           'Cu': 1.12, 'Zn': 1.18, 'Ga': 1.24, 'Ge': 1.21,
                           'As': 1.21, 'Se': 1.16, 'Br': 1.14, 'Kr': 1.17,
                           'Rb': 2.1, 'Sr': 1.85, 'Y': 1.63, 'Zr': 1.54,
                           'Nb': 1.47, 'Mo': 1.38, 'Tc': 1.28, 'Ru': 1.25,
                           'Rh': 1.25, 'Pd': 1.2, 'Ag': 1.28, 'Cd': 1.36,
                           'In': 1.42, 'Sn': 1.4, 'Sb': 1.4, 'Te': 1.36,
                           'I': 1.33, 'Xe': 1.31, 'Cs': 2.32, 'Ba': 1.96,
                           'La': 1.8, 'Ce': 1.63, 'Pr': 1.76, 'Nd': 1.74,
                           'Pm': 1.73, 'Sm': 1.72, 'Eu': 1.68, 'Gd': 1.69,
                           'Tb': 1.68, 'Dy': 1.67, 'Ho': 1.66, 'Er': 1.65,
                           'Tm': 1.64, 'Yb': 1.7, 'Lu': 1.62, 'Hf': 1.52,
                           'Ta': 1.46, 'W': 1.37, 'Re': 1.31, 'Os': 1.29,
                           'Ir': 1.22, 'Pt': 1.23, 'Au': 1.24, 'Hg': 1.33,
                           'Tl': 1.44, 'Pb': 1.44, 'Bi': 1.51, 'Po': 1.45,
                           'At': 1.47, 'Rn': 1.42, 'Fr': 2.23, 'Ra': 2.01,
                           'Ac': 1.86, 'Th': 1.75, 'Pa': 1.69, 'U': 1.7,
                           'Np': 1.71, 'Pu': 1.72, 'Am': 1.66, 'Cm': 1.66,
                           'Bk': 1.68, 'Cf': 1.68, 'Es': 1.65, 'Fm': 1.67,
                           'Md': 1.73, 'No': 1.76, 'Lr': 1.61, 'Rf': 1.57,
                           'Db': 1.49, 'Sg': 1.43, 'Bh': 1.41, 'Hs': 1.34,
                           'Mt': 1.29, 'Ds': 1.28, 'Rg': 1.21, 'Cn': 1.22,
                           'Nh': 1.36, 'Fl': 1.43, 'Mc': 1.62, 'Lv': 1.75,
                           'Ts': 1.65, 'Og': 1.57}


# put all elements in a table searchable by atomic number and symbol
_PERIODIC_TABLE:dict[Union[int,str,Element], Element] = {
    sym : Element(sym,
                  _ATOMIC_NRS[sym],
                  _ELEMENT_WEIGHTS[sym],
                  _ELEMENT_COVALENT_RADII[sym])
    for sym in _ATOMIC_NRS}

_PERIODIC_TABLE.update({
    nr : _PERIODIC_TABLE[_SYMBOLS[nr]]
    for nr in _SYMBOLS})

_PERIODIC_TABLE.update({
    _PERIODIC_TABLE[_SYMBOLS[nr]] : _PERIODIC_TABLE[_SYMBOLS[nr]]
    for nr in _SYMBOLS})

_PERIODIC_TABLE.update({
    sym.upper() : _PERIODIC_TABLE[sym]
    for sym in _ATOMIC_NRS})

_PERIODIC_TABLE.update({
    sym.lower() : _PERIODIC_TABLE[sym]
    for sym in _ATOMIC_NRS})


# use MappingProxyType to make the public table immutable
PERIODIC_TABLE: Mapping[str|int|Element, Element] = MappingProxyType(
                                                            _PERIODIC_TABLE)
