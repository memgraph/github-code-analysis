from appcore.DatabaseIngest.DBIngestImpls.FileTreeGraphCreator import FileTreeCreator
from appcore.DatabaseIngest.DBIngestImpls.RepoBranchesAndCommitsGraphCreator import RepoBranchesAndCommitsCreator
from appcore.DatabaseIngest.DBIngestImpls.DependencyGraphCreator import DependencyGraphCreator
from appcore.DatabaseIngest.DBIngestInterface import DBIngestInterface
from enum import Enum


class DBIngestImplsList(Enum):
    filetree_impls_list: [DBIngestInterface] = [
        FileTreeCreator,
        DependencyGraphCreator,
    ]

    commits_impls_list: [DBIngestInterface] = [
        RepoBranchesAndCommitsCreator,
    ]
