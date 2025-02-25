from typing import List, Any
from dataclasses import dataclass

@dataclass
class Checksum:
    algorithm: str
    checksumValue: str

    @staticmethod
    def from_dict(obj: Any) -> 'Checksum':
        _algorithm = str(obj.get("algorithm"))
        _checksumValue = str(obj.get("checksumValue"))
        return Checksum(_algorithm, _checksumValue)

@dataclass
class CreationInfo:
    comment: str
    created: str
    creators: List[str]
    licenseListVersion: str

    @staticmethod
    def from_dict(obj: Any) -> 'CreationInfo':
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, but got {type(obj).__name__}: {obj}")

        _comment = str(obj.get("comment", ""))
        _created = str(obj.get("created", ""))
        _creators = [str(y) for y in obj.get("creators", [])]
        _licenseListVersion = str(obj.get("licenseListVersion", ""))

        return CreationInfo(_comment, _created, _creators, _licenseListVersion)

@dataclass
class File:
    SPDXID: str
    checksums: List[Checksum]
    copyrightText: str
    fileName: str
    fileTypes: List[str]
    licenseConcluded: str
    licenseInfoInFiles: List[str]

    @staticmethod
    def from_dict(obj: Any) -> 'File':
        _SPDXID = str(obj.get("SPDXID"))
        _checksums = [Checksum.from_dict(y) for y in obj.get("checksums")]
        _copyrightText = str(obj.get("copyrightText"))
        _fileName = str(obj.get("fileName"))
        _fileTypes = [str(y) for y in obj.get("fileTypes",[])]
        _licenseConcluded = str(obj.get("licenseConcluded"))
        _licenseInfoInFiles = [str(y) for y in obj.get("licenseInfoInFiles",[])]
        return File(_SPDXID, _checksums, _copyrightText, _fileName, _fileTypes, _licenseConcluded, _licenseInfoInFiles)

@dataclass
class ExternalDocumentRef:
    checksum: Checksum
    externalDocumentId: str
    spdxDocument: str

    @staticmethod
    def from_dict(obj: Any) -> 'ExternalDocumentRef':
        _checksum = Checksum.from_dict(obj.get("checksum"))
        _externalDocumentId = str(obj.get("externalDocumentId"))
        _spdxDocument = str(obj.get("spdxDocument"))
        return ExternalDocumentRef(_checksum, _externalDocumentId, _spdxDocument)

@dataclass
class Package:
    SPDXID: str
    copyrightText: str
    downloadLocation: str
    licenseConcluded: str
    licenseDeclared: str
    licenseInfoFromFiles: List[str]
    name: str
    supplier: str
    versionInfo: str

    @staticmethod
    def from_dict(obj: Any) -> 'Package':
        if not isinstance(obj, dict):
            raise TypeError(f"Expected dict, but got {type(obj).__name__}: {obj}")

        _SPDXID = str(obj.get("SPDXID", ""))
        _copyrightText = str(obj.get("copyrightText", ""))
        _downloadLocation = str(obj.get("downloadLocation", ""))
        _licenseConcluded = str(obj.get("licenseConcluded", ""))
        _licenseDeclared = str(obj.get("licenseDeclared", ""))
        _licenseInfoFromFiles = [str(y) for y in obj.get("licenseInfoFromFiles", [])]
        _name = str(obj.get("name", ""))
        _supplier = str(obj.get("supplier", ""))
        _versionInfo = str(obj.get("versionInfo", ""))

        return Package(
            _SPDXID, _copyrightText, _downloadLocation, _licenseConcluded,
            _licenseDeclared, _licenseInfoFromFiles, _name, _supplier, _versionInfo
        )

@dataclass
class Relationship:
    relatedSpdxElement: str
    relationshipType: str
    spdxElementId: str
    comment: str

    @staticmethod
    def from_dict(obj: Any) -> 'Relationship':
        _relatedSpdxElement = str(obj.get("relatedSpdxElement"))
        _relationshipType = str(obj.get("relationshipType"))
        _spdxElementId = str(obj.get("spdxElementId"))
        _comment = str(obj.get("comment"))
        return Relationship(_relatedSpdxElement, _relationshipType, _spdxElementId, _comment)

@dataclass
class SystemRoot:
    SPDXID: str
    creationInfo: CreationInfo
    dataLicense: str
    documentNamespace: str
    externalDocumentRefs: List[ExternalDocumentRef]
    name: str
    packages: List[Package]
    relationships: List[Relationship]
    spdxVersion: str

    @staticmethod
    def from_dict(obj: Any) -> 'SystemRoot':
        _SPDXID = str(obj.get("SPDXID"))
        _creationInfo = CreationInfo.from_dict(obj.get("creationInfo"))
        _dataLicense = str(obj.get("dataLicense"))
        _documentNamespace = str(obj.get("documentNamespace"))
        _externalDocumentRefs = [ExternalDocumentRef.from_dict(y) for y in obj.get("externalDocumentRefs")]
        _name = str(obj.get("name"))
        _packages = [Package.from_dict(y) for y in obj.get("packages")]
        _relationships = [Relationship.from_dict(y) for y in obj.get("relationships")]
        _spdxVersion = str(obj.get("spdxVersion"))
        return SystemRoot(_SPDXID, _creationInfo, _dataLicense, _documentNamespace, _externalDocumentRefs, _name, _packages, _relationships, _spdxVersion)

@dataclass
class Document:
    documentNamespace: str
    filename: str
    sha1: str

    @staticmethod
    def from_dict(obj: Any) -> 'Document':
        _documentNamespace = str(obj.get("documentNamespace"))
        _filename = str(obj.get("filename"))
        _sha1 = str(obj.get("sha1"))
        return Document(_documentNamespace, _filename, _sha1)

@dataclass
class IndexRoot:
    documents: List[Document]

    @staticmethod
    def from_dict(obj: Any) -> 'IndexRoot':
        _documents = [Document.from_dict(y) for y in obj.get("documents")]
        return IndexRoot(_documents)