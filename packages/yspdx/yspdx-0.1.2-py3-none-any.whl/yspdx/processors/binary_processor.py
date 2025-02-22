"""Functions from processIndexbinaries.py"""
import os
import json
import sys
from typing import List
from typing import Any
from ..models import (
    IndexRoot, SystemRoot, Document, ExternalDocumentRef,
    File, Package, Relationship
)

# Global variables for compatibility with original functions
g_indexroot = None
g_sysroot = None
g_root_pkg = None

class BinaryProcessor:
    def __init__(self, input_folder: str, indexroot: IndexRoot = None, sysroot: SystemRoot = None):
        self.input_folder = input_folder
        self.indexroot = indexroot
        self.sysroot = sysroot
        self.root_pkg = None
        if sysroot and sysroot.packages:
            self.root_pkg = sysroot.packages[0]
        
        # Initialize globals for compatibility with original functions
        global g_indexroot, g_sysroot, g_root_pkg
        g_indexroot = self.indexroot
        g_sysroot = self.sysroot
        g_root_pkg = self.root_pkg

    def process(self) -> List[str]:
        # Redirect stdout to capture print output
        from io import StringIO
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        
        try:
            process_system_root_spdx_files(self.input_folder)
            output = mystdout.getvalue().splitlines()
            return output
        finally:
            sys.stdout = old_stdout

def process_system_root_spdx_files(input_folder: str) -> None:
    global g_indexroot, g_sysroot, g_root_pkg
    recipe_count = 0
    dirs = os.listdir(input_folder)
    
    # Load index.json
    for file in dirs:
        if file == "index.json": 
            recipe_count = recipe_count + 1
            file_path = os.path.join(input_folder, file)
            with open(file_path, "r", encoding="utf-8") as f:
                myjsonstring = json.load(f)
                g_indexroot = IndexRoot.from_dict(myjsonstring)
    
    # Load system_extra.json
    for file in dirs:
        if file.startswith("system_extra") and file.endswith(".json"):
            recipe_count = recipe_count + 1
            file_path = os.path.join(input_folder, file)
            with open(file_path, "r", encoding="utf-8") as f:
                myjsonstring = json.load(f)
                g_sysroot = SystemRoot.from_dict(myjsonstring)

    g_root_pkg = g_sysroot.packages[0]
    sys_rels = g_sysroot.relationships
    indexroot_documents = g_indexroot.documents
    sys_ext_doc_refs = g_sysroot.externalDocumentRefs
    print(f"Machine: {g_root_pkg.name} v{g_root_pkg.versionInfo}")

    root_rel_types = sorted(set([rel.relationshipType for rel in sys_rels]))

    for root_rel_type in root_rel_types:
        if root_rel_type not in ["DESCRIBES", "AMENDS", "OTHER"]:
            print(f"{root_rel_type}:")
            rel_count = 0
            rel_count2 = 0
            for sys_rel in sys_rels:
                if sys_rel.relationshipType == root_rel_type:
                    if "DocumentRef-runtime" not in sys_rel.relatedSpdxElement:
                        rel_count = rel_count + 1
                        doc_ref = sys_rel.relatedSpdxElement.split(":SPDXRef-Package")[0]
                        file_name = find_and_get_filename(doc_ref, sys_ext_doc_refs, indexroot_documents)
                        print(f"   {rel_count}.  ------")
                        process_pkg_spdx_files(input_folder, file_name, indexroot_documents)
                    
                    if "DocumentRef-runtime" in sys_rel.relatedSpdxElement:
                        rel_count2 = rel_count2 + 1
                        doc_ref_runtime = sys_rel.relatedSpdxElement.split(":SPDXRef-DOCUMENT")[0]
                        file_name = find_and_get_filename(doc_ref_runtime, sys_ext_doc_refs, indexroot_documents)
                        print(f"   {rel_count2}. {file_name} | {sys_rel.comment}")
                        process_runtime_spdx_files(input_folder, file_name, indexroot_documents)

def process_runtime_spdx_files(input_folder: str, input_file: str, indexroot_documents: List[Document]) -> None:
    file_path = os.path.join(input_folder, input_file)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        relationships = data.get("relationships", [])
        externalDocumentRefs = [ExternalDocumentRef.from_dict(ref) for ref in data.get("externalDocumentRefs", [])]
        relationship_types = set([rel["relationshipType"] for rel in relationships])
        
        for relationship_type in relationship_types:
            if relationship_type not in ["DESCRIBES", "AMENDS"]:
                print(f"    {relationship_type}:")
                rel_count = 0
                for relationship in relationships:
                    if relationship["relationshipType"] == relationship_type:
                        rel_count = rel_count + 1
                        doc_ref_runtime = relationship["spdxElementId"].split(":")[0]
                        file_name = find_and_get_filename(doc_ref_runtime, externalDocumentRefs, indexroot_documents)
                        process_pkg_spdx_files(input_folder, file_name, indexroot_documents)

def getfilename_from_index(spdxDocument_link: str, indexroot_documents: List[Document]) -> str:
    for doc in indexroot_documents:
        if doc.documentNamespace == spdxDocument_link:
            return doc.filename
    return ""

def find_and_get_filename(dec_ref: str, sys_ext_doc_refs: List[ExternalDocumentRef], indexroot_documents: List[Document]) -> str:
    for ref in sys_ext_doc_refs:
        if ref.externalDocumentId == dec_ref:
            return getfilename_from_index(ref.spdxDocument, indexroot_documents)
    return ""

def process_recipe_spdx_files(input_folder: str, input_file: str, indexroot_documents: List[Document]) -> None:
    file_path = os.path.join(input_folder, input_file)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        pkg = data.get("packages", [{}])[0]
        supplier = pkg.get("supplier", "Unknown")
        description = pkg.get("description", "Unknown")
        summary = pkg.get("summary", "Unknown")
        downloadLocation = pkg.get("downloadLocation", "Unknown")
        homepage = pkg.get("homepage", "Unknown")
        
        if supplier != "Unknown":
            print(f"                 supplier         : {supplier}")
        if description != "Unknown":
            print(f"                 description      : {description}")
        if summary != "Unknown":
            print(f"                 summary          : {summary}")
        if downloadLocation != "Unknown":
            print(f"                 downloadLocation : {downloadLocation}")
        if homepage != "Unknown":
            print(f"                 homepage         : {homepage}")

def process_recipe_minimal_spdx_info(input_folder: str, input_file: str, indexroot_documents: List[Document]) -> str:
    file_path = os.path.join(input_folder, input_file)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        pkg = data.get("packages", [{}])[0]
        package_name = pkg.get("name", "Unknown")
        versionInfo = pkg.get("versionInfo", "Unknown")
        downloadLocation = pkg.get("downloadLocation", "Unknown")
        return f"{package_name} : {versionInfo} : {downloadLocation}"

def process_pkg_spdx_files(input_folder: str, input_file: str, indexroot_documents: List[Document]) -> None:
    if not any(input_file.startswith(x) for x in ["runtime-", "recipe-", "index", "system"]) and input_file.endswith(".json"):
        file_path = os.path.join(input_folder, input_file)
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            pkg = data.get("packages", [{}])[0]
            package_name = pkg.get("name", "Unknown")
            versionInfo = pkg.get("versionInfo", "Unknown")
            
            relationships = data.get("relationships", [])
            files = [File.from_dict(f) for f in data.get("files", [])]
            externalDocumentRefs = [ExternalDocumentRef.from_dict(ref) for ref in data.get("externalDocumentRefs", [])]
            relationship_types = sorted(set([rel["relationshipType"] for rel in relationships]))
            
            print(f"        {package_name}:{versionInfo}")
            
            for relationship_type in relationship_types:
                if relationship_type not in ["DESCRIBES", "AMENDS"]:
                    print(f"            {relationship_type}:")
                    rel_count = 0
                    for relationship in relationships:
                        if relationship["relationshipType"] == relationship_type:
                            rel_count = rel_count + 1
                            relatedSpdxElement = relationship["relatedSpdxElement"]
                            if relationship_type == "GENERATED_FROM":
                                doc_ref_recipe = relatedSpdxElement.split(":")[0]
                                recipe_file_name = find_and_get_filename(doc_ref_recipe, externalDocumentRefs, indexroot_documents)
                                process_recipe_spdx_files(input_folder, recipe_file_name, indexroot_documents)
                            else:
                                actual_file = find_actual_file(relatedSpdxElement, files)
                                print(f"                 {rel_count}. {actual_file}")
            print('        ------')

def find_actual_file(relatedSpdxElement: str, files: List[File]) -> str:
    for file in files:
        if file.SPDXID == relatedSpdxElement:
            return f"{file.fileName} of type {file.fileTypes[0]}"
    return "Unknown file"