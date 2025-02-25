import os
import json
import tarfile
import zstandard as zstd
from typing import List, Optional
from .models import (
    IndexRoot, SystemRoot, Document, ExternalDocumentRef,
    File, Package, Relationship
)
from .processors.full_processor import FullProcessor
from .processors.binary_processor import BinaryProcessor
from .processors.minimal_processor import MinimalProcessor

class SPDXProcessor:
    def __init__(self, archive_path: str = "system_extra.spdx.tar.zst"):
        self.archive_path = archive_path
        self.input_folder = "system_extra.spdx"
        self.indexroot: Optional[IndexRoot] = None
        self.sysroot: Optional[SystemRoot] = None
        self.root_pkg: Optional[Package] = None
        
    def extract_archive(self):
        """Extract the SPDX archive if it hasn't been extracted yet"""
        if not os.path.exists(self.input_folder):
            if not os.path.exists(self.archive_path):
                raise FileNotFoundError(f"Archive file not found: {self.archive_path}")
            
            os.makedirs(self.input_folder, exist_ok=True)
            with open(self.archive_path, 'rb') as fh:
                dctx = zstd.ZstdDecompressor()
                with dctx.stream_reader(fh) as reader:
                    with tarfile.open(fileobj=reader, mode='r|*') as tar:
                        tar.extractall(path=self.input_folder)

    def load_data(self):
        """Load SPDX data from extracted files"""
        if not os.path.exists(self.input_folder):
            self.extract_archive()
            
        dirs = os.listdir(self.input_folder)
        
        # Load index.json
        if "index.json" in dirs:
            with open(os.path.join(self.input_folder, "index.json"), "r", encoding="utf-8") as f:
                self.indexroot = IndexRoot.from_dict(json.load(f))
        
        # Load system_extra.json
        for file in dirs:
            if file.startswith("system_extra") and file.endswith(".json"):
                with open(os.path.join(self.input_folder, file), "r", encoding="utf-8") as f:
                    self.sysroot = SystemRoot.from_dict(json.load(f))
                break
        
        if self.sysroot and self.sysroot.packages:
            self.root_pkg = self.sysroot.packages[0]

    def process_full(self) -> List[str]:
        """Process data using full processor (from processIndex.py)"""
        self.load_data()
        processor = FullProcessor(self.input_folder, self.indexroot, self.sysroot)
        return processor.process()

    def process_binaries(self) -> List[str]:
        """Process data using binary processor (from processIndexbinaries.py)"""
        self.load_data()
        processor = BinaryProcessor(self.input_folder, self.indexroot, self.sysroot)
        return processor.process()

    def process_minimal(self) -> List[str]:
        """Process data using minimal processor (from processminimalIndex.py)"""
        self.load_data()
        processor = MinimalProcessor(self.input_folder, self.indexroot, self.sysroot)
        return processor.process()

    def getfilename_from_index(self, spdxDocument_link: str) -> Optional[str]:
        """Get filename from document namespace in index"""
        if not self.indexroot:
            return None
        for doc in self.indexroot.documents:
            if doc.documentNamespace == spdxDocument_link:
                return doc.filename
        return None

    def find_and_get_filename(self, dec_ref: str) -> Optional[str]:
        """Find filename from external document reference"""
        if not (self.sysroot and self.indexroot):
            return None
        for ref in self.sysroot.externalDocumentRefs:
            if ref.externalDocumentId == dec_ref:
                return self.getfilename_from_index(ref.spdxDocument)
        return None