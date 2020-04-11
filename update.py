import git

# https://www.devdungeon.com/content/working-git-repositories-python
if __name__ == "__main__":
    # so isto daqui atualiza repositorio local
    # g = git.Git('/home/ferlete/gitAAA/')
    # g.pull('origin', 'origin/master')

    repo = git.Repo("/home/ferlete/gitAAA/")

    # List remotes
    print('Remotes:')
    for remote in repo.remotes:
        print("{}:{}".format(remote.name, remote.url))
        #print(repo.head.commit.tree)

    print(repo.git.diff("origin/master", "version.txt"))