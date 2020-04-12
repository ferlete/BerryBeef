import git

# https://www.devdungeon.com/content/working-git-repositories-python
if __name__ == "__main__":
    # so isto daqui atualiza repositorio local
    g = git.Git('/home/ferlete/gitAAA/')
    g.pull('origin', 'origin/master')

    # repo = git.Repo("/home/ferlete/gitAAA/")
    # heads = repo.heads
    # print(heads)
    # headcommit = repo.head.commit
    # import time
    # time.asctime(time.gmtime(headcommit.committed_date))
    # print(time.strftime("%a,%d%b %Y %H:%M", time.gmtime(headcommit.committed_date)))



