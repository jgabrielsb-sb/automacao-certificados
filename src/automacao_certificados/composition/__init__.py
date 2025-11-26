"""
Composition Root for Automação Certificados.

This module is responsible for creating and wiring together all dependencies
in the application following hexagonal architecture principles.

The composition root is the single place where object creation happens,
keeping the rest of the application clean and testable.
"""

from .container import Container

__all__ = ['Container']

