import pytest

from nemo_library import NemoLibrary
from datetime import datetime

HS_PROJECT_NAME = "gs_unit_test_HubSpot"


def getNL():
    return NemoLibrary(
        config_file="tests/config.ini",
    )


def test_FetchDealFromHubSpotAndUploadToNEMO():
    nl = getNL()

    # check if project exists (should not)
    projects = nl.getProjectList()["displayName"].to_list()
    if HS_PROJECT_NAME in projects:
        nl.deleteProject(HS_PROJECT_NAME)

    nl.createProject(HS_PROJECT_NAME, "project for unit tests")
    new_columns = []
    new_columns.append(
        {
            "displayName": "deal_id",
            "importName": "deal_id",
            "internalName": "deal_id",
            "description": "",
            "dataType": "float",
        }
    )
    new_columns.append(
        {
            "displayName": "update_closedate_new_value",
            "importName": "update_closedate_new_value",
            "internalName": "update_closedate_new_value",
            "description": "",
            "dataType": "date",
        }
    )
    nl.createImportedColumns(
        projectname=HS_PROJECT_NAME,
        columns=new_columns,
    )
    nl.setProjectMetaData(
        projectname=HS_PROJECT_NAME,
        processid_column="deal_id",
        processdate_column="update_closedate_new_value",
        corpcurr_value="EUR",
    )
    nl.FetchDealFromHubSpotAndUploadToNEMO(HS_PROJECT_NAME)
    nl.deleteProject(HS_PROJECT_NAME)
    assert True
