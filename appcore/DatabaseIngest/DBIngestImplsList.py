from typing import List
from appcore.DatabaseIngest.DBIngestImpls.FileTreeGraphCreator import FileTreeCreator
from appcore.DatabaseIngest.DBIngestImpls.RepoBranchesAndCommitsGraphCreator import RepoBranchesAndCommitsCreator
from appcore.DatabaseIngest.DBIngestImpls.DependencyGraphCreator import DependencyGraphCreator
from appcore.DatabaseIngest.DBIngestImpls.RemoveDownloadedFiles import RemoveDownloadedFiles
from appcore.DatabaseIngest.DBIngestImpls.ConnectCommitAndFiles import ConnectCommitAndFiles
from appcore.DatabaseIngest.DBIngestImpls.UpdateStatusToReady import UpdateStatusToReady
from appcore.DatabaseIngest.DBIngestImpls.CreateRootDirectory import CreateRootDirectory
from appcore.DatabaseIngest.DBIngestInterface import DBIngestInterface
from enum import Enum


class DBIngestImplsList(Enum):
    beginning_impls_list: List[DBIngestInterface] = [
        CreateRootDirectory,
        ConnectCommitAndFiles,
    ]

    filetree_impls_list: List[DBIngestInterface] = [
        FileTreeCreator,
        DependencyGraphCreator,
    ]

    commits_impls_list: List[DBIngestInterface] = [
        RepoBranchesAndCommitsCreator,
    ]

    finishing_impls_list: List[DBIngestInterface] = [
        RemoveDownloadedFiles,
        UpdateStatusToReady,
    ]