from appcore.DatabaseIngest.DBIngestRunner import DBIngestRunner
from appcore.Testing.GitUtilsTester import GitUtilsTester


def dry_run():
    gitutils_dryrun = GitUtilsTester()
    filename, filetree = gitutils_dryrun.get_sample_filetree("Adri-Noir", "open-pixel-art", "556aa0b7280c4746da057da8bafe18675350960d")
    DBIngestRunner.run_filetree(filetree)
    DBIngestRunner.run_finishing_methods(filename, filetree[0].filename)


if __name__ == "__main__":
    dry_run()
