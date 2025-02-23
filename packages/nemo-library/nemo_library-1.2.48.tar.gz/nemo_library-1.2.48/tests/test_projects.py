from datetime import datetime
import pytest
import pandas as pd

from nemo_library import NemoLibrary

IC_PROJECT_NAME = "gs_unit_test_Intercompany"

def getNL():
    return NemoLibrary(
        config_file="tests/config.ini",
    )


def test_getProjectList():
    nl = getNL()
    df = nl.getProjectList()
    assert len(df) > 0
    first_row = df.iloc[0]
    assert first_row["id"] == "00000000-0000-0000-0000-000000000001"


def test_getProjectID():
    nl = getNL()
    assert (
        nl.getProjectID("Business Processes") == "00000000-0000-0000-0000-000000000001"
    )


def test_getProjectProperty():
    nl = getNL()
    val = nl.getProjectProperty(
        projectname="Business Processes", propertyname="ExpDateFrom"
    )

    assert val is not None, "API call did not return any value"

    try:
        date_val = datetime.strptime(val, "%Y-%m-%d")
    except ValueError:
        pytest.fail(f"Returned value ({val}) is not in the format YYYY-MM-DD")

    assert (
        2000 <= date_val.year <= 2100
    ), "Year is out of the acceptable range (2000-2100)"


def test_createProject():
    nl = getNL()

    # check if project exists (should not)
    projects = nl.getProjectList()["displayName"].to_list()
    if IC_PROJECT_NAME in projects:
        nl.deleteProject(IC_PROJECT_NAME)

    # now we can create the project
    nl.createProject(
        IC_PROJECT_NAME,
        "used for unit tests of nemo_library",
    )
    projects = nl.getProjectList()["displayName"].to_list()
    assert IC_PROJECT_NAME in projects
    
    


def test_createImportedColumn():
    nl = getNL()
    nl.createImportedColumn(
        projectname=IC_PROJECT_NAME,
        displayName="Rechnungsdatum",
        dataType="date",
        description="Rechnungsdatum",
    )
    importedColumns = nl.getImportedColumns(IC_PROJECT_NAME)
    assert "Rechnungsdatum" in importedColumns["displayName"].to_list()


def test_getImportedColumns():
    nl = getNL()
    df = nl.getImportedColumns(IC_PROJECT_NAME)
    assert (
        len(df) == 1
    )  # we have checked the behavior in test_createImportedColumn already...


def test_synchronizeCsvColsAndImportedColumns():
    nl = getNL()
    nl.synchronizeCsvColsAndImportedColumns(
        projectname=IC_PROJECT_NAME,
        filename="./tests/intercompany_NEMO.csv",
    )

    importedColumns = nl.getImportedColumns(IC_PROJECT_NAME)
    assert len(importedColumns) == 21


def test_setProjectMetaData():
    nl = getNL()
    nl.setProjectMetaData(
        IC_PROJECT_NAME,
        processid_column="seriennummer",
        processdate_column="rechnungsdatum",
        corpcurr_value="EUR",
    )
    assert True

def test_ReUploadDataFrame():
    nl = getNL()
    df = pd.read_csv("./tests/intercompany_NEMO.csv",sep=";")
    nl.ReUploadDataFrame(projectname=IC_PROJECT_NAME,df=df,update_project_settings=False)
    assert True
    
def test_ReUploadFile():
    nl = getNL()

    nl.ReUploadFile(
        projectname=IC_PROJECT_NAME,
        filename="./tests/intercompany_NEMO.csv",
        update_project_settings=False,
    )

    assert True

def test_focusMoveAttributeBefore():
    nl = getNL()
    nl.focusMoveAttributeBefore(IC_PROJECT_NAME,"Mandant",None)
    assert True

def test_createOrUpdateReport():
    nl = getNL()
    select = """WITH Params AS (
    SELECT ADD_MONTHS(
               TO_DATE(CONCAT(YEAR(CURRENT_DATE), '-01-01'), 'YYYY-MM-DD'),
               (FLOOR((MONTH(CURRENT_DATE) - 1) / 3) - 2) * 3
           ) AS ReportStartDate
    FROM DUMMY
),
Invoices AS (
    SELECT
        MANDANT      AS Company,
        ENDKUNDE     AS CUSTOMER_I_D,
        LIZENZNEHMER AS CUSTOMER_NAME,
        Rechnungsdatum AS InvoiceDocDate,
        to_decimal(preis_mit_rabatt) AS InvoiceAmount
    FROM 
        $schema.$table
    WHERE 
        ABRECHNUNGSART = 'SaaS/Cloud'
),
FilteredInvoices AS (
    SELECT
        i1.*
    FROM 
        Invoices i1
    LEFT JOIN 
        Invoices i2 ON i1.CUSTOMER_I_D = i2.CUSTOMER_I_D 
                        AND i1.Company = i2.Company 
                        AND i2.InvoiceDocDate < (SELECT ReportStartDate FROM Params)
    WHERE 
        i2.CUSTOMER_I_D IS NULL 
),
CustomerPayments AS (
    SELECT
        Company,
        CUSTOMER_I_D,
        CUSTOMER_NAME,
        COUNT(DISTINCT InvoiceDocDate) AS NumberOfPayments,
        SUM(InvoiceAmount) AS TotalRevenue,
        MIN(InvoiceDocDate) AS FirstInvoiceDate
    FROM
        FilteredInvoices
    GROUP BY
        Company,
        CUSTOMER_I_D,
        CUSTOMER_NAME
),
CustomerACV AS (
    SELECT
        Company,
        CUSTOMER_I_D,
        CUSTOMER_NAME,
        TotalRevenue,
        NumberOfPayments,
        FirstInvoiceDate,
        (TotalRevenue / NumberOfPayments) * 12 AS AnnualContractValue
    FROM
        CustomerPayments
)
SELECT 
    Company,
    CUSTOMER_I_D,
    CUSTOMER_NAME,
    FirstInvoiceDate,
    AnnualContractValue AS ACV
FROM 
    CustomerACV
ORDER BY 
	ACV DESC 
"""
    nl.createOrUpdateReport(projectname=IC_PROJECT_NAME,displayName="(BI DATA) 21 NNN Reporting SaaS IC",querySyntax=select,internalName="bi_data_21_nnn_reporting_saas_ic",description="unit test")

def test_createOrUpdateRule():
    nl = getNL()
    # ml.createOrUpdateRule()


def test_LoadReport():
    nl = getNL()
    df = nl.LoadReport(
        projectname=IC_PROJECT_NAME,
        report_name="(BI DATA) 21 NNN Reporting SaaS IC",
    )

    assert len(df) == 50


def test_deleteProject():
    nl = getNL()
    nl.deleteProject(IC_PROJECT_NAME)
    projects = nl.getProjectList()["displayName"].to_list()
    assert not IC_PROJECT_NAME in projects


    