from appcore.DatabaseIngest.DBIngestRunner import DBIngestRunner
from appcore.Testing.GitUtilsTester import GitUtilsTester


def dry_run():
    gitutils_dryrun = GitUtilsTester()
    filetree = gitutils_dryrun.get_sample_filetree()
    DBIngestRunner.run_filetree(filetree)


if __name__ == "__main__":
    dry_run()
