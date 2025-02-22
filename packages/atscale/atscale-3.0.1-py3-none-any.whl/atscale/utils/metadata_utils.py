from typing import List, Dict

from atscale.utils import dmv_utils
from atscale.base import enums, private_enums


def _get_dimensions(data_model, filter_by: Dict[private_enums.Dimension, List[str]] = None) -> Dict:
    """Gets a dictionary of dictionaries with the dimension names and metadata.

    Args:
        data_model (DataModel): The DataModel object to search through
        filter_by (Dict[private_enums.Dimension fields, str], optional): A dict with keys of fields and values of a list of that field's value
                to exclusively include in the return. Defaults to None for no filtering.

    Returns:
        Dict: A dictionary of dictionaries where the dimension names are the keys in the outer dictionary
              while the inner keys are the following: 'description', 'type'(value is Time
              or Standard).
    """
    dimension_dict = dmv_utils.get_dmv_data(
        model=data_model,
        fields=[
            private_enums.Dimension.description,
            private_enums.Dimension.type,
        ],
        filter_by=filter_by,
    )
    dimensions = {}
    for name, info in dimension_dict.items():
        dimensions[name] = {
            "description": info[private_enums.Dimension.description.name],
            "type": info[private_enums.Dimension.type.name],
        }
    return dimensions


def _get_hierarchies(
    data_model,
    filter_by: Dict[private_enums.Hierarchy, List[str]] = None,
) -> Dict:
    """Gets a dictionary of dictionaries with the hierarchies names and metadata.
    Secondary attributes are treated as their own hierarchies.

    Args:
        data_model (DataModel): The DataModel object to search through
        filter_by (Dict[private_enums.Hierarchy fields, str], optional): A dict with keys of fields and values of a list of that field's value
                to exclusively include in the return. Defaults to None for no filtering.

    Returns:
        Dict: A dictionary of dictionaries where the hierarchy names are the keys in the outer dictionary
              while the inner keys are the following: 'dimension', 'description', 'caption', 'folder', 'type'(value is Time
              or Standard), 'secondary_attribute'.
    """
    hierarchy_dict = dmv_utils.get_dmv_data(
        model=data_model,
        fields=[
            private_enums.Hierarchy.dimension,
            private_enums.Hierarchy.description,
            private_enums.Hierarchy.folder,
            private_enums.Hierarchy.caption,
            private_enums.Hierarchy.type,
            private_enums.Hierarchy.secondary_attribute,
        ],
        filter_by=filter_by,
    )
    hierarchies = {}
    for name, info in hierarchy_dict.items():
        hierarchies[name] = {
            "dimension": info[private_enums.Hierarchy.dimension.name],
            "description": info[private_enums.Hierarchy.description.name],
            "caption": info[private_enums.Hierarchy.caption.name],
            "folder": info[private_enums.Hierarchy.folder.name],
            "type": info[private_enums.Hierarchy.type.name],
            "secondary_attribute": info[private_enums.Hierarchy.secondary_attribute.name],
        }
    return hierarchies


def _get_hierarchy_levels(
    data_model,
    hierarchy_name: str,
) -> List[str]:
    """Gets a list of the levels of a given hierarchy

    Args:
        data_model (DataModel): The DataModel object the given hierarchy exists within.
        hierarchy_name (str): The name of the hierarchy

    Returns:
        List[str]: A list containing the hierarchy's levels
    """

    levels_from_hierarchy = dmv_utils.get_dmv_data(
        model=data_model,
        fields=[private_enums.Level.name],
        id_field=private_enums.Level.hierarchy,
        filter_by={private_enums.Level.hierarchy: [hierarchy_name]},
    )

    hierarchy = levels_from_hierarchy.get(hierarchy_name)
    if hierarchy:
        levels = hierarchy.get(private_enums.Level.name.name, [])
        if type(levels) is list:
            return levels
        else:
            return [levels]
    else:
        return []


def _get_all_numeric_feature_names(
    data_model,
    folder: str = None,
) -> List[str]:
    """Returns a list of all numeric features (ie Aggregate and Calculated Measures) in a given data model.

    Args:
        data_model (DataModel): The DataModel object to be queried.
        folder (str, optional): The name of a folder in the data model containing measures to exclusively list.
            Defaults to None to not filter by folder.

    Returns:
        List[str]: A list of the query names of numeric features in the data model and, if given, in the folder.
    """
    folders = [folder] if folder else None
    return list(
        data_model.get_features(folder_list=folders, feature_type=enums.FeatureType.NUMERIC).keys()
    )


def _get_all_categorical_feature_names(
    data_model,
    folder: str = None,
) -> List[str]:
    """Returns a list of all categorical features (ie Hierarchy levels and secondary_attributes) in a given DataModel.

    Args:
        data_model (DataModel): The DataModel object to be queried.
        folder (str, optional): The name of a folder in the DataModel containing features to exclusively list.
            Defaults to None to not filter by folder.

    Returns:
        List[str]: A list of the query names of categorical features in the DataModel and, if given, in the folder.
    """
    folders = [folder] if folder else None
    return list(
        data_model.get_features(
            folder_list=folders, feature_type=enums.FeatureType.CATEGORICAL
        ).keys()
    )


def _get_folders(
    data_model,
) -> List[str]:
    """Returns a list of the available folders in a given DataModel.

    Args:
        data_model (DataModel): The DataModel object to be queried.

    Returns:
        List[str]: A list of the available folders
    """

    measure_dict = dmv_utils.get_dmv_data(model=data_model, fields=[private_enums.Measure.folder])

    hierarchy_dict = dmv_utils.get_dmv_data(
        model=data_model, fields=[private_enums.Hierarchy.folder]
    )

    folders = sorted(
        set(
            [measure_dict[key]["folder"] for key in measure_dict.keys()]
            + [hierarchy_dict[key]["folder"] for key in hierarchy_dict.keys()]
        )
    )
    if "" in folders:
        folders.remove("")
    return folders
