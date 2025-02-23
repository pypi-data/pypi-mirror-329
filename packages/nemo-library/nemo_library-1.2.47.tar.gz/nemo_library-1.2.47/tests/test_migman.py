import os
import shutil
import pytest


from nemo_library import NemoLibrary

def getNL():
    return NemoLibrary(
        config_file="tests/config.ini",
    )


def test_MigManCreateProjectTemplates():
    nl = getNL()
    test_dir = nl.config.get_migman_local_project_directory()
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    assert not os.path.exists(test_dir)
    
    nl.MigManCreateProjectTemplates()

    assert os.path.exists(test_dir)

def test_MigManLoadData():
    nl = getNL()
    shutil.copy("./tests/Sales Tax ID.csv",os.path.join(nl.config.get_migman_local_project_directory(),"srcdata"))
    nl.MigManLoadData()

def test_MigManExportData():
    nl = getNL()
    nl.MigManExportData()
    assert os.path.exists(os.path.join(nl.config.get_migman_local_project_directory(),"to_customer","Sales Tax ID_with_messages.csv"))
    assert os.path.exists(os.path.join(nl.config.get_migman_local_project_directory(),"to_proalpha","Sales Tax ID.csv"))
    
def test_final():
    nl = getNL()
    test_dir = nl.config.get_migman_local_project_directory()
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    