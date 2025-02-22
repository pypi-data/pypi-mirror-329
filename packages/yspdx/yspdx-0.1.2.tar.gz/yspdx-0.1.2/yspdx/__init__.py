"""SPDX file processor package"""
from .processor import SPDXProcessor
from .models import (
    Checksum, CreationInfo, File, ExternalDocumentRef,
    Package, Relationship, SystemRoot, Document, IndexRoot
)

__version__ = "0.1.2"
__author__ = "Dinesh Ravi"