import logging
from typing import Dict, List

from atscale.base import enums, private_enums
from atscale.utils import dmv_utils


logger = logging.getLogger(__name__)


def _get_published_features(
    data_model,
    feature_list: List[str] = None,
    folder_list: List[str] = None,
    feature_type: enums.FeatureType = enums.FeatureType.ALL,
) -> Dict:
    """Gets the feature names and metadata for each feature in the published DataModel.

    Args:
        data_model (DataModel): The published AtScale data model to get the features of via dmv
        feature_list (List[str], optional): A list of features to return. Defaults to None to return all.
        folder_list (List[str], optional): A list of folders to filter by. Defaults to None to ignore folder.
        feature_type (enums.FeatureType, optional): The type of features to filter by. Options
            include enums.FeatureType.ALL, enums.FeatureType.CATEGORICAL, or enums.FeatureType.NUMERIC. Defaults to ALL.

    Returns:
        Dict: A dictionary of dictionaries where the feature names are the keys in the outer dictionary
                while the inner keys are the following:
                'atscale_type'(value is a level-type, 'Aggregate', or 'Calculated'),
                'description', 'expression', caption, 'folder', 'data_type', and 'feature_type'(value is Numeric or Categorical).
    """
    level_filter_by = {}
    measure_filter_by = {}
    hier_filter_by = {}
    if feature_list:
        feature_list = [feature_list] if isinstance(feature_list, str) else feature_list
        level_filter_by[private_enums.Level.name] = feature_list
        measure_filter_by[private_enums.Measure.name] = feature_list
    if folder_list:
        folder_list = [folder_list] if isinstance(folder_list, str) else folder_list
        hier_filter_by[private_enums.Hierarchy.folder] = folder_list
        measure_filter_by[private_enums.Measure.folder] = folder_list

    feature_dict = {}

    catalog_licensed = data_model.catalog.repo._atconn._validate_license("FEATURE_DATA_CATALOG_API")

    if feature_type is enums.FeatureType.ALL or feature_type is enums.FeatureType.CATEGORICAL:
        hier_dict = dmv_utils.get_dmv_data(
            model=data_model, fields=[private_enums.Hierarchy.folder], filter_by=hier_filter_by
        )
        level_filter_by[private_enums.Level.hierarchy] = list(hier_dict.keys())
        query_fields = [
            private_enums.Level.type,
            private_enums.Level.description,
            private_enums.Level.hierarchy,
            private_enums.Level.dimension,
            private_enums.Level.caption,
            private_enums.Level.data_type,
        ]
        if catalog_licensed:
            query_fields.append(private_enums.Level.secondary_attribute)
        dimension_dict = dmv_utils.get_dmv_data(
            model=data_model,
            fields=query_fields,
            filter_by=level_filter_by,
        )
        for name, info in dimension_dict.items():
            # if a level was duplicated we might have multiple hierarchies which could mean multiple folders
            folder = []
            if type(info[private_enums.Level.hierarchy.name]) is list:
                for hierarchy_name in info[private_enums.Level.hierarchy.name]:
                    if hier_dict.get(hierarchy_name):
                        folder.append(
                            hier_dict[hierarchy_name][private_enums.Hierarchy.folder.name]
                        )
            else:
                folder.append(
                    hier_dict[info[private_enums.Level.hierarchy.name]][
                        private_enums.Hierarchy.folder.name
                    ]
                )
                info[private_enums.Level.hierarchy.name] = [
                    info[private_enums.Level.hierarchy.name]
                ]

            feature_dict[name] = {
                "caption": info[private_enums.Level.caption.name],
                "atscale_type": info[private_enums.Level.type.name],
                "data_type": info[private_enums.Level.data_type.name],
                "description": info[private_enums.Level.description.name],
                "hierarchy": info[private_enums.Level.hierarchy.name],
                "dimension": info[private_enums.Level.dimension.name],
                "folder": folder,
                "feature_type": "Categorical",
            }
            if catalog_licensed:
                feature_dict[name]["secondary_attribute"] = info[
                    private_enums.Level.secondary_attribute.name
                ]
            else:
                feature_dict[name]["secondary_attribute"] = False
    if feature_type is enums.FeatureType.ALL or feature_type is enums.FeatureType.NUMERIC:
        query_fields = [
            private_enums.Measure.type,
            private_enums.Measure.description,
            private_enums.Measure.folder,
            private_enums.Measure.caption,
            private_enums.Measure.data_type,
        ]
        if catalog_licensed:
            query_fields.append(private_enums.Measure.expression)
        measure_dict = dmv_utils.get_dmv_data(
            model=data_model, fields=query_fields, filter_by=measure_filter_by
        )
        for name, info in measure_dict.items():
            agg_type = info[private_enums.Measure.type.name]
            feature_dict[name] = {
                "caption": info[private_enums.Measure.caption.name],
                "atscale_type": agg_type if agg_type != "Calculated" else "Calculated",
                # "aggregation_type": agg_type,
                "data_type": info[private_enums.Measure.data_type.name],
                "description": info[private_enums.Measure.description.name],
                "folder": [info[private_enums.Measure.folder.name]],
                "feature_type": "Numeric",
            }
            if catalog_licensed:
                feature_dict[name]["expression"] = info[private_enums.Measure.expression.name]
            else:
                feature_dict[name]["expression"] = ""

    return feature_dict
