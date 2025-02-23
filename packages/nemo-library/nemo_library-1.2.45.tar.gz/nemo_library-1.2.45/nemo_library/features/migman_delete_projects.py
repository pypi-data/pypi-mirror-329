import logging
from nemo_library.utils.config import Config
from nemo_library.features.projects import deleteProject, getProjectList

__all__ = ["MigManDeleteProjects"]


def MigManDeleteProjects(config: Config) -> None:
    projects = getProjectList(config)["displayName"].to_list()
    for project in projects:
        if not project in ["Business Processes","Master Data"]:
            logging.info(f"Delete project {project}...")
            deleteProject(config=config,projectname=project)

    