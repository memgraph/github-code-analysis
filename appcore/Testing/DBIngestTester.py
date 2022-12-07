from appcore.DatabaseIngest.DBIngestRunner import DBIngestRunner
from appcore.Testing.GitUtilsTester import GitUtilsTester


def dry_run():
    gitutils_dryrun = GitUtilsTester()
    filename, filetree = gitutils_dryrun.get_sample_filetree("memgraph", "gqlalchemy", "7fbec93709fb1fb91a484d36fc063a1f4ee903f3")
    DBIngestRunner.run_filetree(filetree)
    DBIngestRunner.run_finishing_methods(filename, filetree[0].filename, "7fbec93709fb1fb91a484d36fc063a1f4ee903f3")


if __name__ == "__main__":
    dry_run()
