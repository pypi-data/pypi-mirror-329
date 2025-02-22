"""
The core package contains very basic classes and functions that are used
throughout the project. It is carefully managed to avoid incompatible changes.
Code in the core package should not depend on any other package in the project
and dependencies to external packages should be kept to a minimum or wrapped.
"""

__all__ = ['chemid', 'constants', 'database', 'graph', 'kinetics', 'lot', 'md',
           'mechanism', 'periodic_table', 'thermo']