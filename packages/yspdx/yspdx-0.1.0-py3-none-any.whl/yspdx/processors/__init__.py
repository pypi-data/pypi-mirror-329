"""SPDX processors package"""
from .full_processor import FullProcessor
from .binary_processor import BinaryProcessor
from .minimal_processor import MinimalProcessor

__all__ = ['FullProcessor', 'BinaryProcessor', 'MinimalProcessor']