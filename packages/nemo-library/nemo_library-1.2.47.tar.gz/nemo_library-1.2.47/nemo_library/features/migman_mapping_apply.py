import json
import logging
import pandas as pd
from nemo_library.utils.config import Config
from nemo_library.features.fileingestion import ReUploadDataFrame
from nemo_library.features.focus import focusCoupleAttributes
from nemo_library.features.projects import (
    LoadReport,
    createImportedColumns,
    createOrUpdateReport,
    getImportedColumns,
)
from nemo_library.utils.migmanutils import (
    getMappingRelations,
)
from nemo_library.utils.utils import (
    get_display_name,
    get_import_name,
    get_internal_name,
)

__all__ = ["MigManApplyMapping"]


def MigManApplyMapping(config: Config) -> None:

    # get configuration
    mappingrelationsdf = getMappingRelations(config=config)

    # extract list of affected projects from that dictionary
    projects = mappingrelationsdf["project"].unique().tolist()

    for project in projects:
        mappingrelationsdf_filtered = mappingrelationsdf[
            mappingrelationsdf["project"] == project
        ]
        _process_project(
            config=config,
            project=project,
            mappingrelationsdf=mappingrelationsdf_filtered,
        )


def _process_project(
    config: Config,
    project: str,
    mappingrelationsdf: pd.DataFrame,
) -> None:

    # create "original" columns first (if not already existing)

    new_columns = []
    importedcolumnsdf = getImportedColumns(config=config, projectname=project)
    importedcolumnslist = importedcolumnsdf["displayName"].to_list()
    mapping_columns = mappingrelationsdf["matching_field_display_name"].to_list()
    for mapping_column in mapping_columns:
        mapcol = f"Mapped_{mapping_column}"
        if not mapcol in importedcolumnslist:
            new_columns.append(
                {
                    "displayName": get_display_name(mapcol),
                    "importName": get_import_name(mapcol),
                    "internalName": get_internal_name(mapcol),
                    "description": f"Original value of {mapping_column}",
                    "dataType": "string",
                }
            )

    if new_columns:
        createImportedColumns(
            config=config,
            projectname=project,
            columns=new_columns,
        )
        logging.info(
            f"project '{project}': columns created\n{json.dumps(new_columns,indent=2)}"
        )

    # now lets fill these values
    _apply_mapping(
        config=config,
        project=project,
        importedcolumnsdf=importedcolumnsdf,
        mappingrelationsdf=mappingrelationsdf,
    )

    # couple attributes
    _focus_couple_attributes(
        config=config,
        project=project,
        mappingrelationsdf=mappingrelationsdf,
    )


def _apply_mapping(
    config: Config,
    project: str,
    importedcolumnsdf: pd.DataFrame,
    mappingrelationsdf: pd.DataFrame,
) -> None:
    select_statement = _select_statement(
        config=config,
        importedcolumnsdf=importedcolumnsdf,
        mappingrelationsdf=mappingrelationsdf,
    )

    createOrUpdateReport(
        config=config,
        projectname=project,
        displayName="(MAPPING) map data",
        querySyntax=select_statement,
        internalName="MAPPING_map_data",
        description="Map data",
    )
    df = LoadReport(
        config=config,
        projectname=project,
        report_name="(MAPPING) map data",
    )

    ReUploadDataFrame(
        config=config,
        projectname=project,
        df=df,
        update_project_settings=False,
        version=3,
        datasource_ids=[{"key": "datasource_id", "value": project}],
    )


def _focus_couple_attributes(
    config: Config,
    project: str,
    mappingrelationsdf: pd.DataFrame,
) -> None:

    for idx, row in mappingrelationsdf.iterrows():
        focusCoupleAttributes(
            config=config,
            projectname=project,
            attributenames=[
                row["matching_field_display_name"],
                "Mapped_" + row["matching_field_display_name"],
            ],
            previous_attribute=row["matching_field_display_name"],
        )


def _select_statement(
    config: Config,
    importedcolumnsdf: pd.DataFrame,
    mappingrelationsdf: pd.DataFrame,
) -> str:

    # filter original-values, they will be re-created again
    importedcolumnsdf = importedcolumnsdf[
        ~importedcolumnsdf["displayName"].str.startswith("Mapped_")
    ]

    # start with easy things: select fields that are not touched
    selectfrags = [
        f'data.{row["internalName"]} as "{row["displayName"]}"'
        for idx, row in importedcolumnsdf.iterrows()
    ]

    # add mapped fields now
    selectfrags.extend(
        [
            f"""COALESCE(mapping_{get_internal_name(row["mapping_field"])}.{get_internal_name("target_" + row["mapping_field"])},
                   data.{row["matching_field_internal_name"]}) as "Mapped_{row["matching_field_display_name"]}" """
            for idx, row in mappingrelationsdf.iterrows()
        ]
    )
    joinfrags = []
    for idx, row in mappingrelationsdf.iterrows():
        joinfrag = f"""LEFT JOIN
    $schema.{get_internal_name("PROJECT_MAPPING_" + row["mapping_field"])} mapping_{get_internal_name(row["mapping_field"])}
ON
    mapping_{get_internal_name(row["mapping_field"])}.{get_internal_name("source_" + row["mapping_field"])} = data.{row["matching_field_internal_name"]}"""

        additional_fields = row["additional_fields"]
        if any(additional_fields):
            additional_fields_defined = config.get_migman_additional_fields()
            additional_field_global_definition = additional_fields_defined.get(
                row["mapping_field"], []
            )

            for (label, name), definition in zip(
                additional_fields, additional_field_global_definition
            ):
                joinfrag += f"\n\tAND mapping_{get_internal_name(row["mapping_field"])}.{get_internal_name("source_" + definition)} = data.{name}"
        joinfrags.append(joinfrag)

    select = f"""SELECT
    {"\n\t, ".join(selectfrags)}
FROM
    $schema.$table data
{"\n".join(joinfrags)}
"""

    return select
