from pathlib import Path

from rdflib import RDF
from rdflib import XSD
from rdflib import BNode
from rdflib import Graph
from rdflib import Literal
from rdflib import URIRef

from dsp_tools.commands.xmlupload.make_rdf_graph.constants import ARCHIVE_FILE_VALUE
from dsp_tools.commands.xmlupload.make_rdf_graph.constants import AUDIO_FILE_VALUE
from dsp_tools.commands.xmlupload.make_rdf_graph.constants import DOCUMENT_FILE_VALUE
from dsp_tools.commands.xmlupload.make_rdf_graph.constants import IIIF_URI_VALUE
from dsp_tools.commands.xmlupload.make_rdf_graph.constants import KNORA_API
from dsp_tools.commands.xmlupload.make_rdf_graph.constants import MOVING_IMAGE_FILE_VALUE
from dsp_tools.commands.xmlupload.make_rdf_graph.constants import STILL_IMAGE_FILE_VALUE
from dsp_tools.commands.xmlupload.make_rdf_graph.constants import TEXT_FILE_VALUE
from dsp_tools.commands.xmlupload.models.deserialise.xmlresource import BitstreamInfo
from dsp_tools.commands.xmlupload.models.rdf_models import AbstractFileValue
from dsp_tools.commands.xmlupload.models.rdf_models import FileValueMetadata
from dsp_tools.commands.xmlupload.models.rdf_models import RDFPropTypeInfo
from dsp_tools.models.exceptions import BaseError


def make_iiif_uri_value_graph(iiif_uri: AbstractFileValue, res_node: BNode | URIRef) -> Graph:
    """
    Creates a graph with the IIIF-URI Link

    Args:
        iiif_uri: Information about the IIIF URI
        res_node: Node of the resource

    Returns:
        Graph with the IIIF-URI Value
    """
    return _make_abstract_file_value_graph(
        iiif_uri, IIIF_URI_VALUE, res_node, KNORA_API.stillImageFileValueHasExternalUrl
    )


def make_file_value_graph(bitstream_info: BitstreamInfo, res_node: BNode | URIRef) -> Graph:
    """
    Creates a graph with the File Value information.

    Args:
        bitstream_info: Information about the previously uploaded file
        res_node: Node of the resource

    Returns:
        Graph with the File Value
    """
    file_type = get_file_type_info(bitstream_info.local_file)
    internal_filename = bitstream_info.internal_file_name
    bitstream_permissions = None
    if bitstream_info.permissions:
        bitstream_permissions = str(bitstream_info.permissions)
    metadata = FileValueMetadata(bitstream_permissions)
    file_value = AbstractFileValue(internal_filename, metadata)
    return _make_abstract_file_value_graph(file_value, file_type, res_node)


def get_file_type_info(local_file: str) -> RDFPropTypeInfo:
    """
    Takes path of a file and returns the correct file value type.

    Args:
        local_file: filepath

    Returns:
        File type info to construct the graph

    Raises:
        BaseError: in case the extension is unknown
    """
    file_ending = Path(local_file).suffix[1:].lower()
    match file_ending:
        case "zip" | "tar" | "gz" | "z" | "tgz" | "gzip" | "7z":
            return ARCHIVE_FILE_VALUE
        case "mp3" | "wav":
            return AUDIO_FILE_VALUE
        case "pdf" | "doc" | "docx" | "xls" | "xlsx" | "ppt" | "pptx":
            return DOCUMENT_FILE_VALUE
        case "mp4":
            return MOVING_IMAGE_FILE_VALUE
        # jpx is the extension of the files returned by dsp-ingest
        case "jpg" | "jpeg" | "jp2" | "png" | "tif" | "tiff" | "jpx":
            return STILL_IMAGE_FILE_VALUE
        case "odd" | "rng" | "txt" | "xml" | "xsd" | "xsl" | "csv" | "json":
            return TEXT_FILE_VALUE
        case _:
            raise BaseError(f"Unknown file ending '{file_ending}' for file '{local_file}'")


def _make_abstract_file_value_graph(
    file_value: AbstractFileValue,
    type_info: RDFPropTypeInfo,
    res_node: BNode | URIRef,
    has_file_name_prop: URIRef = KNORA_API.fileValueHasFilename,
) -> Graph:
    file_bn = BNode()
    g = _add_metadata(file_bn, file_value.metadata)
    g.add((res_node, type_info.knora_prop, file_bn))
    g.add((file_bn, RDF.type, type_info.knora_type))
    g.add((file_bn, has_file_name_prop, Literal(file_value.value, datatype=XSD.string)))
    return g


def _add_metadata(file_bn: BNode, metadata: FileValueMetadata) -> Graph:
    g = Graph()
    if metadata.permissions:
        g.add((file_bn, KNORA_API.hasPermissions, Literal(metadata.permissions, datatype=XSD.string)))
    return g
