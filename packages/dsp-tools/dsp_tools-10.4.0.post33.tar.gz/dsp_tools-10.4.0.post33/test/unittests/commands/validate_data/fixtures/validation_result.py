from functools import lru_cache

import pytest
from rdflib import RDF
from rdflib import RDFS
from rdflib import SH
from rdflib import Graph
from rdflib import Literal

from dsp_tools.commands.validate_data.models.validation import DetailBaseInfo
from dsp_tools.commands.validate_data.models.validation import ValidationResult
from dsp_tools.commands.validate_data.models.validation import ValidationResultBaseInfo
from dsp_tools.commands.validate_data.models.validation import ViolationType
from test.unittests.commands.validate_data.constants import DASH
from test.unittests.commands.validate_data.constants import DATA
from test.unittests.commands.validate_data.constants import IN_BUILT_ONTO
from test.unittests.commands.validate_data.constants import KNORA_API
from test.unittests.commands.validate_data.constants import ONTO
from test.unittests.commands.validate_data.constants import PREFIXES


@lru_cache(maxsize=None)
@pytest.fixture
def onto_graph() -> Graph:
    g = Graph()
    g.parse("testdata/validate-data/onto.ttl")
    g.parse("testdata/validate-data/knora-api-subset.ttl")
    return g


@pytest.fixture
def report_target_resource_wrong_type(onto_graph: Graph) -> tuple[Graph, Graph]:
    validation_str = f"""{PREFIXES}
    [ 
        a sh:ValidationResult ;
        sh:detail _:detail_bn ;
        sh:focusNode <http://data/region_isRegionOf_resource_not_a_representation> ;
        sh:resultMessage "Value does not have shape api-shapes:isRegionOf_NodeShape" ;
        sh:resultPath <http://api.knora.org/ontology/knora-api/v2#isRegionOf> ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:NodeConstraintComponent ;
        sh:sourceShape <http://api.knora.org/ontology/knora-api/shapes/v2#isRegionOf_PropertyShape> ;
        sh:value <http://data/value_isRegionOf> 
    ] .
    
    _:detail_bn a sh:ValidationResult ;
        sh:focusNode <http://data/value_isRegionOf> ;
        sh:resultMessage "http://api.knora.org/ontology/knora-api/v2#Representation" ;
        sh:resultPath <http://api.knora.org/ontology/knora-api/shapes/v2#linkValueHasTargetID> ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:ClassConstraintComponent ;
        sh:sourceShape _:source_shape ;
        sh:value <http://data/target_res_without_representation_1> .
    """
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
    <http://data/region_isRegionOf_resource_not_a_representation> 
        a knora-api:Region ;
        rdfs:label "Region"^^xsd:string ;
        knora-api:hasColor <http://data/value_hasColor> ;
        knora-api:hasGeometry <http://data/value_hasGeometry> ;
        knora-api:isRegionOf <http://data/value_isRegionOf> .
    
    <http://data/value_isRegionOf> a knora-api:LinkValue ;
        api-shapes:linkValueHasTargetID <http://data/target_res_without_representation_1> .
    
    <http://data/target_res_without_representation_1> a in-built:TestNormalResource ;
        rdfs:label "Resource without Representation"^^xsd:string .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    return validation_g, onto_data_g


@pytest.fixture
def report_not_resource(onto_graph: Graph) -> tuple[Graph, Graph]:
    validation_str = f"""{PREFIXES}
    _:bn_id_simpletext a sh:ValidationResult ;
        sh:focusNode <http://data/value_id_simpletext> ;
        sh:resultMessage "TextValue without formatting" ;
        sh:resultPath knora-api:valueAsString ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
        sh:sourceShape api-shapes:SimpleTextValue_PropShape .
    """
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
    <http://data/id_simpletext> a onto:ClassWithEverything ;
        rdfs:label "Simpletext"^^xsd:string ;
        onto:testTextarea <http://data/value_id_simpletext> .
    <http://data/value_id_simpletext> a knora-api:TextValue ;
        knora-api:textValueAsXml "Text"^^xsd:string .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    return validation_g, onto_data_g


@pytest.fixture
def report_min_card(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
        sh:focusNode <http://data/id_card_one> ;
        sh:resultMessage "1" ;
        sh:resultPath onto:testBoolean ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
        sh:sourceShape [ ] ] .
    """
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
    <http://data/id_card_one> a onto:ClassInheritedCardinalityOverwriting ;
        rdfs:label "Bool Card 1"^^xsd:string .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=SH.MinCountConstraintComponent,
        resource_iri=DATA.id_card_one,
        res_class_type=ONTO.ClassInheritedCardinalityOverwriting,
        result_path=ONTO.testBoolean,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def file_value_cardinality_to_ignore(onto_graph: Graph) -> tuple[Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
[   a sh:ValidationResult ;
    sh:focusNode <http://data/id_wrong_file_type> ;
    sh:resultMessage "Property knora-api:hasMovingImageFileValue is not among those permitted for any of the types" ;
    sh:resultPath <http://api.knora.org/ontology/knora-api/v2#hasMovingImageFileValue> ;
    sh:resultSeverity sh:Violation ;
    sh:sourceConstraintComponent <http://datashapes.org/dash#ClosedByTypesConstraintComponent> ;
    sh:sourceShape <http://0.0.0.0:3333/ontology/9999/onto/v2#TestStillImageRepresentation> ;
    sh:value <http://data/fileValueBn> ] .
    """
    data_str = f"""{PREFIXES}
    <http://data/id_wrong_file_type> a onto:TestStillImageRepresentation ;
        rdfs:label "TestStillImageRepresentation File mp4"^^xsd:string ;
        knora-api:hasMovingImageFileValue <http://data/fileValueBn> .
    """
    graphs = Graph()
    graphs.parse(data=validation_str, format="ttl")
    graphs.parse(data=data_str, format="ttl")
    graphs += onto_graph
    val_bn = next(graphs.subjects(RDF.type, SH.ValidationResult))
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=DASH.ClosedByTypesConstraintComponent,
        resource_iri=DATA.id_wrong_file_type,
        res_class_type=ONTO.TestStillImageRepresentation,
        result_path=KNORA_API.hasMovingImageFileValue,
    )
    return graphs, base_info


@pytest.fixture
def file_value_for_resource_without_representation(onto_graph: Graph) -> tuple[Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
[ a sh:ValidationResult ;
    sh:focusNode <http://data/id_resource_without_representation> ;
    sh:resultMessage "Property knora-api:hasMovingImageFileValue is not among those permitted for any of the types" ;
    sh:resultPath <http://api.knora.org/ontology/knora-api/v2#hasMovingImageFileValue> ;
    sh:resultSeverity sh:Violation ;
    sh:sourceConstraintComponent <http://datashapes.org/dash#ClosedByTypesConstraintComponent> ;
    sh:sourceShape <http://0.0.0.0:3333/ontology/9999/onto/v2#ClassWithEverything> ;
    sh:value <http://data/fileBn> ] .
    """
    data_str = f"""{PREFIXES}
    <http://data/id_resource_without_representation> a <http://0.0.0.0:3333/ontology/9999/onto/v2#ClassWithEverything> ;
        rdfs:label "Resource Without Representation"^^xsd:string ;
        knora-api:hasMovingImageFileValue <http://data/fileBn> .
    """
    graphs = Graph()
    graphs.parse(data=validation_str, format="ttl")
    graphs.parse(data=data_str, format="ttl")
    graphs += onto_graph
    val_bn = next(graphs.subjects(RDF.type, SH.ValidationResult))
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=DASH.ClosedByTypesConstraintComponent,
        resource_iri=DATA.id_resource_without_representation,
        res_class_type=ONTO.ClassWithEverything,
        result_path=KNORA_API.hasMovingImageFileValue,
    )
    return graphs, base_info


@pytest.fixture
def extracted_file_value_for_resource_without_representation() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.FILEVALUE_PROHIBITED,
        res_iri=DATA.id_resource_without_representation,
        res_class=ONTO.ClassWithEverything,
        property=ONTO.hasMovingImageFileValue,
    )


@pytest.fixture
def extracted_min_card() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.MIN_CARD,
        res_iri=DATA.id_card_one,
        res_class=ONTO.ClassInheritedCardinalityOverwriting,
        property=ONTO.testBoolean,
        expected=Literal("1"),
    )


@pytest.fixture
def report_value_type_simpletext(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
        sh:detail _:bn_id_simpletext ;
        sh:focusNode <http://data/id_simpletext> ;
        sh:resultMessage "Value does not have shape <http://api.knora.org/ontology/knora-api/shapes/v2#SimpleTextValue_ClassShape>" ;
        sh:resultPath onto:testTextarea ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:NodeConstraintComponent ;
        sh:sourceShape onto:testTextarea_PropShape ;
        sh:value <http://data/value_id_simpletext> ] .

    _:bn_id_simpletext a sh:ValidationResult ;
        sh:focusNode <http://data/value_id_simpletext> ;
        sh:resultMessage "TextValue without formatting" ;
        sh:resultPath knora-api:valueAsString ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
        sh:sourceShape api-shapes:SimpleTextValue_PropShape .
    """  # noqa: E501 (Line too long)
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
    <http://data/id_simpletext> a onto:ClassWithEverything ;
        rdfs:label "Simpletext"^^xsd:string ;
        onto:testTextarea <http://data/value_id_simpletext> .

    <http://data/value_id_simpletext> a knora-api:TextValue ;
        knora-api:textValueAsXml "Text"^^xsd:string .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    detail_bn = next(validation_g.objects(val_bn, SH.detail))
    detail = DetailBaseInfo(
        detail_bn=detail_bn,
        source_constraint_component=SH.MinCountConstraintComponent,
    )
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        result_path=ONTO.testTextarea,
        source_constraint_component=SH.NodeConstraintComponent,
        resource_iri=DATA.id_simpletext,
        res_class_type=ONTO.ClassWithEverything,
        detail=detail,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def extracted_value_type_simpletext() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.VALUE_TYPE,
        res_iri=DATA.id_simpletext,
        res_class=ONTO.ClassWithEverything,
        property=ONTO.testTextarea,
        expected=Literal("TextValue without formatting"),
        input_type=KNORA_API.TextValue,
    )


@pytest.fixture
def report_min_inclusive(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ 
        a sh:ValidationResult ;
        sh:detail _:detail_bn ;
        sh:focusNode <http://data/video_segment_negative_bounds> ;
        sh:resultMessage "Value does not have shape api-shapes:IntervalValue_ClassShape" ;
        sh:resultPath <http://api.knora.org/ontology/knora-api/v2#hasSegmentBounds> ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:NodeConstraintComponent ;
        sh:sourceShape <http://api.knora.org/ontology/knora-api/shapes/v2#hasSegmentBounds_PropertyShape> ;
        sh:value <http://data/value_iri> 
    ] .
            
    _:detail_bn a sh:ValidationResult ;
    sh:focusNode <http://data/value_iri> ;
    sh:resultMessage "The interval start must be a non-negative integer or decimal." ;
    sh:resultPath <http://api.knora.org/ontology/knora-api/v2#intervalValueHasStart> ;
    sh:resultSeverity sh:Violation ;
    sh:sourceConstraintComponent sh:MinInclusiveConstraintComponent ;
    sh:sourceShape <http://api.knora.org/ontology/knora-api/shapes/v2#intervalValueHasStart_PropShape> ;
    sh:value -2.0 .
    """
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}

    <http://data/video_segment_negative_bounds> a knora-api:VideoSegment ;
        rdfs:label "Video Segment"^^xsd:string ;
        knora-api:hasSegmentBounds <http://data/value_iri> .
    
    <http://data/value_iri> a knora-api:IntervalValue ;
        knora-api:intervalValueHasEnd -1.0 ;
        knora-api:intervalValueHasStart -2.0 .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    detail_bn = next(validation_g.objects(val_bn, SH.detail))
    detail = DetailBaseInfo(
        detail_bn=detail_bn,
        source_constraint_component=SH.MinInclusiveConstraintComponent,
    )
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        result_path=KNORA_API.hasSegmentBounds,
        source_constraint_component=SH.NodeConstraintComponent,
        resource_iri=DATA.video_segment_negative_bounds,
        res_class_type=KNORA_API.VideoSegment,
        detail=detail,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def extracted_min_inclusive() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.GENERIC,
        res_iri=DATA.video_segment_negative_bounds,
        res_class=KNORA_API.VideoSegment,
        property=KNORA_API.hasSegmentBounds,
        message=Literal("The interval start must be a non-negative integer or decimal."),
        input_value=Literal("-2.0"),
    )


@pytest.fixture
def report_value_type(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
        sh:detail _:bn_id_uri ;
        sh:focusNode <http://data/id_uri> ;
        sh:resultMessage "Value does not have shape <http://api.knora.org/ontology/knora-api/shapes/v2#UriValue_ClassShape>" ;
        sh:resultPath onto:testUriValue ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:NodeConstraintComponent ;
        sh:sourceShape onto:testUriValue_PropShape ;
        sh:value <http://data/value_id_uri> ] .
    
    _:bn_id_uri a sh:ValidationResult ;
        sh:focusNode <http://data/value_id_uri> ;
        sh:resultMessage "UriValue" ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:ClassConstraintComponent ;
        sh:sourceShape api-shapes:UriValue_ClassShape ;
        sh:value <http://data/value_id_uri> .
    """  # noqa: E501 (Line too long)
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
    <http://data/id_uri> a onto:ClassWithEverything ;
        rdfs:label "Uri"^^xsd:string ;
        onto:testUriValue <http://data/value_id_uri> .

    <http://data/value_id_uri> a knora-api:TextValue ;
        knora-api:valueAsString "https://dasch.swiss"^^xsd:string .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    detail_bn = next(validation_g.objects(predicate=SH.detail))
    detail_component = next(validation_g.objects(detail_bn, SH.sourceConstraintComponent))
    detail = DetailBaseInfo(
        detail_bn=detail_bn,
        source_constraint_component=detail_component,
    )
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=SH.NodeConstraintComponent,
        resource_iri=DATA.id_uri,
        res_class_type=ONTO.ClassWithEverything,
        result_path=ONTO.testUriValue,
        detail=detail,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def extracted_value_type() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.VALUE_TYPE,
        res_iri=DATA.id_uri,
        res_class=ONTO.ClassWithEverything,
        property=ONTO.testUriValue,
        expected=Literal("UriValue"),
        input_type=KNORA_API.TextValue,
    )


@pytest.fixture
def report_regex(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
        sh:detail _:bn_geoname_not_number ;
        sh:focusNode <http://data/geoname_not_number> ;
        sh:resultMessage "Value does not have shape <http://api.knora.org/ontology/knora-api/shapes/v2#GeonameValue_ClassShape>" ;
        sh:resultPath onto:testGeoname ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:NodeConstraintComponent ;
        sh:sourceShape onto:testGeoname_PropShape ;
        sh:value <http://data/value_geoname_not_number> ] .

    _:bn_geoname_not_number a sh:ValidationResult ;
        sh:focusNode <http://data/value_geoname_not_number> ;
        sh:resultMessage "The value must be a valid geoname code" ;
        sh:resultPath knora-api:geonameValueAsGeonameCode ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:PatternConstraintComponent ;
        sh:sourceShape api-shapes:geonameValueAsGeonameCode_Shape ;
        sh:value "this-is-not-a-valid-code" .
    """  # noqa: E501 (Line too long)
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
    <http://data/geoname_not_number> a onto:ClassWithEverything ;
        rdfs:label "Geoname is not a number"^^xsd:string ;
        onto:testGeoname <http://data/value_geoname_not_number> .

    <http://data/value_geoname_not_number> a knora-api:GeonameValue ;
        knora-api:geonameValueAsGeonameCode "this-is-not-a-valid-code"^^xsd:string .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    detail_bn = next(validation_g.objects(val_bn, SH.detail))
    detail_component = next(validation_g.objects(detail_bn, SH.sourceConstraintComponent))
    detail = DetailBaseInfo(
        detail_bn=detail_bn,
        source_constraint_component=detail_component,
    )
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=SH.NodeConstraintComponent,
        resource_iri=DATA.geoname_not_number,
        res_class_type=ONTO.ClassWithEverything,
        result_path=ONTO.testGeoname,
        detail=detail,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def extracted_regex() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.PATTERN,
        res_iri=DATA.geoname_not_number,
        res_class=ONTO.ClassWithEverything,
        property=ONTO.testGeoname,
        expected=Literal("The value must be a valid geoname code"),
        input_value=Literal("this-is-not-a-valid-code"),
    )


@pytest.fixture
def report_link_target_non_existent(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
        sh:detail _:bn_link_target_non_existent ;
        sh:focusNode <http://data/link_target_non_existent> ;
        sh:resultMessage "Value does not have shape <http://0.0.0.0:3333/ontology/9999/onto/v2#testHasLinkTo_NodeShape>" ;
        sh:resultPath onto:testHasLinkTo ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:NodeConstraintComponent ;
        sh:sourceShape onto:testHasLinkTo_PropShape ;
        sh:value <http://data/value_link_target_non_existent> ] .
    
    _:bn_link_target_non_existent a sh:ValidationResult ;
        sh:focusNode <http://data/value_link_target_non_existent> ;
        sh:resultMessage <http://api.knora.org/ontology/knora-api/v2#Resource> ;
        sh:resultPath api-shapes:linkValueHasTargetID ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:ClassConstraintComponent ;
        sh:sourceShape [ ] ;
        sh:value <http://data/other> .
    """  # noqa: E501 (Line too long)
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
    <http://data/link_target_non_existent> a onto:ClassWithEverything ;
        rdfs:label "Target does not exist"^^xsd:string ;
        onto:testHasLinkTo <http://data/value_link_target_non_existent> .
    
    <http://data/value_link_target_non_existent> a knora-api:LinkValue ;
    api-shapes:linkValueHasTargetID <http://data/other> .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    detail_bn = next(validation_g.objects(val_bn, SH.detail))
    detail_component = next(validation_g.objects(detail_bn, SH.sourceConstraintComponent))
    detail = DetailBaseInfo(
        detail_bn=detail_bn,
        source_constraint_component=detail_component,
    )
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=SH.NodeConstraintComponent,
        resource_iri=DATA.link_target_non_existent,
        res_class_type=ONTO.ClassWithEverything,
        result_path=ONTO.testHasLinkTo,
        detail=detail,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def extracted_link_target_non_existent() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.LINK_TARGET,
        res_iri=DATA.link_target_non_existent,
        res_class=ONTO.ClassWithEverything,
        property=ONTO.testHasLinkTo,
        expected=KNORA_API.Resource,
        input_value=DATA.other,
    )


@pytest.fixture
def report_link_target_wrong_class(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
        sh:detail _:bn_link_target_wrong_class ;
        sh:focusNode <http://data/link_target_wrong_class> ;
        sh:resultMessage "Value does not have shape <http://0.0.0.0:3333/ontology/9999/onto/v2#testHasLinkToCardOneResource_NodeShape>" ;
        sh:resultPath onto:testHasLinkToCardOneResource ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:NodeConstraintComponent ;
        sh:sourceShape onto:testHasLinkToCardOneResource_PropShape ;
        sh:value <http://data/value_link_target_wrong_class> ] .
        
    _:bn_link_target_wrong_class a sh:ValidationResult ;
        sh:focusNode <http://data/value_link_target_wrong_class> ;
        sh:resultMessage <http://0.0.0.0:3333/ontology/9999/onto/v2#CardOneResource> ;
        sh:resultPath api-shapes:linkValueHasTargetID ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:ClassConstraintComponent ;
        sh:sourceShape [ ] ;
        sh:value <http://data/id_9_target> .
    """  # noqa: E501 (Line too long)
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
    <http://data/link_target_wrong_class> a onto:ClassWithEverything ;
        rdfs:label "Target not the right class"^^xsd:string ;
        onto:testHasLinkToCardOneResource <http://data/value_link_target_wrong_class> .
    
    <http://data/id_9_target> a onto:ClassWithEverything ;
        rdfs:label "Link Prop"^^xsd:string .

    <http://data/value_link_target_wrong_class> a knora-api:LinkValue ;
        api-shapes:linkValueHasTargetID <http://data/id_9_target> .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    detail_bn = next(validation_g.objects(val_bn, SH.detail))
    detail_component = next(validation_g.objects(detail_bn, SH.sourceConstraintComponent))
    detail = DetailBaseInfo(
        detail_bn=detail_bn,
        source_constraint_component=detail_component,
    )
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=SH.NodeConstraintComponent,
        resource_iri=DATA.link_target_wrong_class,
        res_class_type=ONTO.ClassWithEverything,
        result_path=ONTO.testHasLinkToCardOneResource,
        detail=detail,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def extracted_link_target_wrong_class() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.LINK_TARGET,
        res_iri=DATA.link_target_wrong_class,
        res_class=ONTO.ClassWithEverything,
        property=ONTO.testHasLinkToCardOneResource,
        expected=ONTO.CardOneResource,
        input_value=DATA.id_9_target,
        input_type=ONTO.ClassWithEverything,
    )


@pytest.fixture
def report_closed_constraint(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
        sh:focusNode <http://data/id_closed_constraint> ;
        sh:resultMessage "Property onto:testIntegerSimpleText is not among those permitted for any of the types" ;
        sh:resultPath onto:testIntegerSimpleText ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent dash:ClosedByTypesConstraintComponent ;
        sh:sourceShape onto:CardOneResource ;
        sh:value <http://data/value_id_closed_constraint> ] .
    """
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
    <http://data/id_closed_constraint> a onto:CardOneResource ;
        rdfs:label "Int card does not exist"^^xsd:string ;
        onto:testIntegerSimpleText <http://data/value_id_closed_constraint> .
    <http://data/value_id_closed_constraint> a knora-api:IntValue ;
        knora-api:intValueAsInt 1 .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=DASH.ClosedByTypesConstraintComponent,
        resource_iri=DATA.id_closed_constraint,
        res_class_type=ONTO.CardOneResource,
        result_path=ONTO.testIntegerSimpleText,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def extracted_closed_constraint() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.NON_EXISTING_CARD,
        res_iri=DATA.id_closed_constraint,
        res_class=ONTO.CardOneResource,
        property=ONTO.testIntegerSimpleText,
    )


@pytest.fixture
def report_max_card(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
        sh:focusNode <http://data/id_max_card> ;
        sh:resultMessage "1" ;
        sh:resultPath onto:testHasLinkToCardOneResource ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:MaxCountConstraintComponent ;
        sh:sourceShape [ ] ] .
    """
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
    <http://data/id_max_card> a onto:ClassMixedCard ;
        rdfs:label "Decimal Card 0-1"^^xsd:string ;
        onto:testHasLinkToCardOneResource <http://data/value_1> , <http://data/value_2> .

    <http://data/value_1> a knora-api:LinkValue ;
        api-shapes:linkValueHasTargetID <http://data/id_card_one> .
    <http://data/value_2> a knora-api:LinkValue ;
        api-shapes:linkValueHasTargetID <http://data/id_closed_constraint> .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=SH.MaxCountConstraintComponent,
        resource_iri=DATA.id_max_card,
        res_class_type=ONTO.ClassMixedCard,
        result_path=ONTO.testHasLinkToCardOneResource,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def extracted_max_card() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.MAX_CARD,
        res_iri=DATA.id_max_card,
        res_class=ONTO.ClassMixedCard,
        property=ONTO.testDecimalSimpleText,
        expected=Literal("0-1"),
    )


@pytest.fixture
def report_empty_label(onto_graph: Graph) -> tuple[Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
        sh:focusNode <http://data/empty_label> ;
        sh:resultMessage "The label must be a non-empty string" ;
        sh:resultPath rdfs:label ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:PatternConstraintComponent ;
        sh:sourceShape api-shapes:rdfsLabel_Shape ;
        sh:value " " ] .
    """
    data_str = f"""{PREFIXES}
        <http://data/empty_label> a onto:ClassWithEverything ;
            rdfs:label " "^^xsd:string .
    """
    graphs = Graph()
    graphs.parse(data=validation_str, format="ttl")
    graphs.parse(data=data_str, format="ttl")
    graphs += onto_graph
    val_bn = next(graphs.subjects(RDF.type, SH.ValidationResult))
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=SH.PatternConstraintComponent,
        resource_iri=DATA.empty_label,
        res_class_type=ONTO.ClassWithEverything,
        result_path=RDFS.label,
    )
    return graphs, base_info


@pytest.fixture
def extracted_empty_label() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.PATTERN,
        res_iri=DATA.empty_label,
        res_class=ONTO.ClassWithEverything,
        property=RDFS.label,
        expected=Literal("The label must be a non-empty string"),
        input_value=Literal(" "),
    )


@pytest.fixture
def report_unique_value_literal(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
        sh:focusNode <http://data/identical_values_valueHas> ;
        sh:resultMessage "A resource may not have the same property and value more than one time." ;
        sh:resultPath onto:testGeoname ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraint _:1 ;
        sh:sourceConstraintComponent sh:SPARQLConstraintComponent ;
        sh:sourceShape onto:ClassWithEverything_Unique ;
        sh:value "00111111" ] .
    """
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
        <http://data/identical_values_valueHas> a onto:ClassWithEverything .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=SH.SPARQLConstraintComponent,
        resource_iri=DATA.identical_values_valueHas,
        res_class_type=ONTO.ClassWithEverything,
        result_path=ONTO.testGeoname,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def extracted_unique_value_literal() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.UNIQUE_VALUE,
        res_iri=DATA.identical_values_valueHas,
        res_class=ONTO.ClassWithEverything,
        property=ONTO.testGeoname,
        input_value=Literal("00111111"),
    )


@pytest.fixture
def report_unique_value_iri(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
        sh:focusNode <http://data/identical_values_LinkValue> ;
        sh:resultMessage "A resource may not have the same property and value more than one time." ;
        sh:resultPath onto:testHasLinkTo ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraint _:1 ;
        sh:sourceConstraintComponent sh:SPARQLConstraintComponent ;
        sh:sourceShape onto:ClassWithEverything_Unique ;
        sh:value <http://data/link_valueTarget_id> ] .
    """
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
        <http://data/identical_values_LinkValue> a onto:ClassWithEverything .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=SH.SPARQLConstraintComponent,
        resource_iri=DATA.identical_values_LinkValue,
        res_class_type=ONTO.ClassWithEverything,
        result_path=ONTO.testHasLinkTo,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def extracted_unique_value_iri() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.UNIQUE_VALUE,
        res_iri=DATA.identical_values_LinkValue,
        res_class=ONTO.ClassWithEverything,
        property=ONTO.testHasLinkTo,
        input_value=DATA.link_valueTarget_id,
    )


@pytest.fixture
def report_coexist_with(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
        sh:focusNode <http://data/missing_seqnum> ;
        sh:resultMessage "The property seqnum must be used together with isPartOf" ;
        sh:resultPath <http://api.knora.org/ontology/knora-api/v2#seqnum> ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent <http://datashapes.org/dash#CoExistsWithConstraintComponent> ;
        sh:sourceShape <http://api.knora.org/ontology/knora-api/shapes/v2#seqnum_PropShape> ] .
    """
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
    <http://data/missing_seqnum> a in-built:TestStillImageRepresentationWithSeqnum ;
        rdfs:label "Image with sequence"^^xsd:string ;
        knora-api:hasStillImageFileValue <http://data/file_value> ;
        knora-api:isPartOf <http://data/is_part_of_value> .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=DASH.CoExistsWithConstraintComponent,
        resource_iri=DATA.missing_seqnum,
        res_class_type=IN_BUILT_ONTO.TestStillImageRepresentationWithSeqnum,
        result_path=KNORA_API.seqnum,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def extracted_coexist_with() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.SEQNUM_IS_PART_OF,
        res_iri=DATA.missing_seqnum,
        res_class=IN_BUILT_ONTO.TestStillImageRepresentationWithSeqnum,
        message=Literal("Coexist message from knora-api turtle"),
    )


@pytest.fixture
def report_unknown_list_node(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ 
    a sh:ValidationResult ;
sh:detail _:bn_list_node_non_existent ;
sh:focusNode <http://data/list_node_non_existent> ;
sh:resultMessage "Value does not have shape <http://api.knora.org/ontology/knora-api/shapes/v2#firstList_NodeShape>" ;
sh:resultPath onto:testListProp ;
sh:resultSeverity sh:Violation ;
sh:sourceConstraintComponent sh:NodeConstraintComponent ;
sh:sourceShape onto:testListProp_PropShape ;
sh:value <http://data/value_list_node_non_existent> ] .
    
    _:bn_list_node_non_existent a sh:ValidationResult ;
    sh:focusNode <http://data/value_list_node_non_existent> ;
    sh:resultMessage "A valid node from the list 'firstList' must be used with this property." ;
    sh:resultPath api-shapes:listNodeAsString ;
    sh:resultSeverity sh:Violation ;
    sh:sourceConstraintComponent sh:InConstraintComponent ;
    sh:sourceShape [ ] ;
    sh:value "firstList / other" .
    """
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
    <http://data/list_node_non_existent> a onto:ClassWithEverything .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    detail_bn = next(validation_g.objects(val_bn, SH.detail))
    detail = DetailBaseInfo(
        detail_bn=detail_bn,
        source_constraint_component=SH.InConstraintComponent,
    )
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=SH.NodeConstraintComponent,
        resource_iri=DATA.list_node_non_existent,
        res_class_type=ONTO.ClassWithEverything,
        result_path=ONTO.testListProp,
        detail=detail,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def extracted_unknown_list_node() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.GENERIC,
        res_iri=DATA.list_node_non_existent,
        res_class=ONTO.ClassWithEverything,
        property=ONTO.testListProp,
        message=Literal("A valid node from the list 'firstList' must be used with this property."),
        input_value=Literal("firstList / other"),
    )


@pytest.fixture
def report_unknown_list_name(onto_graph: Graph) -> tuple[Graph, Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
[
    a sh:ValidationResult ;
    sh:detail _:bn_list_name_non_existent ;
    sh:focusNode <http://data/list_name_non_existent> ;
    sh:resultMessage "Value does not have shape <http://rdfh.ch/lists/9999/b7p3ucDWQ5CZuKpVo-im7Q>" ;
    sh:resultPath <http://0.0.0.0:3333/ontology/9999/onto/v2#testListProp> ;
    sh:resultSeverity sh:Violation ;
    sh:sourceConstraintComponent sh:NodeConstraintComponent ;
    sh:sourceShape <http://0.0.0.0:3333/ontology/9999/onto/v2#testListProp_PropShape> ;
    sh:value <http://data/value_list_name_non_existent> ] .

_:bn_list_name_non_existent a sh:ValidationResult ;
    sh:focusNode <http://data/value_list_name_non_existent> ;
    sh:resultMessage "A valid node from the list 'firstList' must be used with this property." ;
    sh:resultPath <http://api.knora.org/ontology/knora-api/shapes/v2#listNodeAsString> ;
    sh:resultSeverity sh:Violation ;
    sh:sourceConstraintComponent sh:InConstraintComponent ;
    sh:sourceShape _:bn_source ;
    sh:value "other / n1" .
    """
    validation_g = Graph()
    validation_g.parse(data=validation_str, format="ttl")
    data_str = f"""{PREFIXES}
    <http://data/list_name_non_existent> a onto:ClassWithEverything .
    """
    onto_data_g = Graph()
    onto_data_g += onto_graph
    onto_data_g.parse(data=data_str, format="ttl")
    val_bn = next(validation_g.subjects(RDF.type, SH.ValidationResult))
    detail_bn = next(validation_g.objects(val_bn, SH.detail))
    detail = DetailBaseInfo(
        detail_bn=detail_bn,
        source_constraint_component=SH.InConstraintComponent,
    )
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=SH.NodeConstraintComponent,
        resource_iri=DATA.list_name_non_existent,
        res_class_type=ONTO.ClassWithEverything,
        result_path=ONTO.testListProp,
        detail=detail,
    )
    return validation_g, onto_data_g, base_info


@pytest.fixture
def extracted_unknown_list_name() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.GENERIC,
        res_iri=DATA.list_name_non_existent,
        res_class=ONTO.ClassWithEverything,
        property=ONTO.testListProp,
        message=Literal("A valid node from the list 'firstList' must be used with this property."),
        input_value=Literal("other / n1"),
    )


@pytest.fixture
def report_missing_file_value(onto_graph: Graph) -> tuple[Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
            sh:focusNode <http://data/id_video_missing> ;
            sh:resultMessage "A MovingImageRepresentation requires a file with the extension 'mp4'." ;
            sh:resultPath <http://api.knora.org/ontology/knora-api/v2#hasMovingImageFileValue> ;
            sh:resultSeverity sh:Violation ;
            sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
            sh:sourceShape <http://api.knora.org/ontology/knora-api/shapes/v2#hasMovingImageFileValue_PropShape> 
    ] .
    """
    data_str = f"""{PREFIXES}
    <http://data/id_video_missing> a <http://0.0.0.0:3333/ontology/9999/onto/v2#TestMovingImageRepresentation> ;
        rdfs:label "TestMovingImageRepresentation"^^xsd:string .
    """
    graphs = Graph()
    graphs.parse(data=validation_str, format="ttl")
    graphs.parse(data=data_str, format="ttl")
    graphs += onto_graph
    val_bn = next(graphs.subjects(RDF.type, SH.ValidationResult))
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=SH.MinCountConstraintComponent,
        resource_iri=DATA.id_video_missing,
        res_class_type=ONTO.TestMovingImageRepresentation,
        result_path=KNORA_API.hasMovingImageFileValue,
    )
    return graphs, base_info


@pytest.fixture
def extracted_missing_file_value() -> ValidationResult:
    return ValidationResult(
        violation_type=ViolationType.FILE_VALUE,
        res_iri=DATA.id_video_missing,
        res_class=ONTO.TestMovingImageRepresentation,
        property=KNORA_API.hasMovingImageFileValue,
        expected=Literal("A MovingImageRepresentation requires a file with the extension 'mp4'."),
    )


@pytest.fixture
def result_unknown_component(onto_graph: Graph) -> tuple[Graph, ValidationResultBaseInfo]:
    validation_str = f"""{PREFIXES}
    [ a sh:ValidationResult ;
        sh:focusNode <http://data/empty_label> ;
        sh:resultMessage "The label must be a non-empty string" ;
        sh:resultPath rdfs:label ;
        sh:resultSeverity sh:Violation ;
        sh:sourceConstraintComponent sh:UniqueLangConstraintComponent ;
        sh:sourceShape api-shapes:rdfsLabel_Shape ;
        sh:value " " ] .
    """
    data_str = f"""{PREFIXES}
        <http://data/empty_label> a onto:ClassWithEverything ;
            rdfs:label " "^^xsd:string .
    """
    graphs = Graph()
    graphs.parse(data=validation_str, format="ttl")
    graphs.parse(data=data_str, format="ttl")
    graphs += onto_graph
    val_bn = next(graphs.subjects(RDF.type, SH.ValidationResult))
    base_info = ValidationResultBaseInfo(
        result_bn=val_bn,
        source_constraint_component=SH.PatternConstraintComponent,
        resource_iri=DATA.empty_label,
        res_class_type=ONTO.ClassWithEverything,
        result_path=RDFS.label,
    )
    return graphs, base_info
