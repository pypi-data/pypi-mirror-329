from atlaz.sources.interface import validate_layers
from atlaz.sources.utility import get_name_from_entity, get_name_from_relationship_entity
from atlaz.sources.interface import gather_source_scores_entities
from atlaz.sources.schema import Textsource
from atlaz.sources.validators import validate_source_against_text

def build_with_validators(entity: dict, text: str):
    source_start = entity.TextSource.StartOfSource
    source_end = entity.TextSource.EndOfSource
    _, _, final_source = validate_layers(source_start, source_end, 'nomatter', text)
    entity.TextSource = final_source
    return entity

def validate_sources(generated_graph_extension: dict, text: str, type_relationship_id = 3):
    """
    Validate the sources in the generated graph extension.
    """
    entities = generated_graph_extension['NewEntities']
    relationships = generated_graph_extension["NewRelationships"]
    list_of_obj = []
    for object in entities:
        list_of_obj.append((object, get_name_from_entity))
    for object in relationships:
        if get_name_from_relationship_entity(object) == "Is A Type Of":
            continue
        list_of_obj.append((object, get_name_from_relationship_entity))
    errors_entities, complexity_entities = gather_source_scores_entities(list_of_obj, text, type_relationship_id=type_relationship_id)
    return errors_entities

def repair_sources(generated_graph_extension: dict, text: str, type_relationship_id = 3):
    """
    Repair the sources in the generated graph extension.
    """
    updated_entities = []
    for entity in generated_graph_extension.Entities:
        attr = getattr(entity, 'TextSource', None)
        if attr:
            entity.TextSource = Textsource(
                StartOfSource=entity.TextSource.StartOfSource,
                EndOfSource=entity.TextSource.EndOfSource,
                Source=entity.TextSource.Source
            )
            updated_entities.append(entity)
    generated_graph_extension.Entities = [build_with_validators(obj, text) for obj in generated_graph_extension.Entities if obj.TextSource]
    generated_graph_extension.Relationships = [build_with_validators(obj, text) for obj in generated_graph_extension.Relationships if obj.TextSource]
    return generated_graph_extension

def gather_valid_subset(result: dict, text: str) -> dict:
    """
    Re-validate each item in `result` independently
    and return a dict with only the valid ones.
    """
    valid_portion = {}
    for key, value in result.items():
        src = value["TextSource"]
        source_start = src["StartOfSource"]
        source_end = src["EndOfSource"]
        error_msg, complexity_level = validate_source_against_text(
            source_start, source_end, key, text
        )
        if not error_msg:

            valid_portion[key] = value
    return valid_portion