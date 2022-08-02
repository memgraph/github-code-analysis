from appcore.DatabaseIngest.DBIngestRunner import DBIngestRunner
from appcore.Testing.GitUtilsTester import GitUtilsTester


def dry_run():
    gitutils_dryrun = GitUtilsTester()
    filename, filetree = gitutils_dryrun.get_sample_filetree("memgraph", "memgraph", "80e0e439b7c4de5f66fcbc3a949dfa7f0fdbb988")
    DBIngestRunner.run_filetree(filetree)
    DBIngestRunner.run_finishing_methods(filename, filetree[0].filename)


if __name__ == "__main__":
    dry_run()
