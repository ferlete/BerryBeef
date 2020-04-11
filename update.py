import git

# https://www.devdungeon.com/content/working-git-repositories-python
if __name__ == "__main__":
    # so isto daqui atualiza repositorio local
    # g = git.Git('/home/ferlete/gitAAA/')
    # g.pull('origin', 'origin/master')

    repo = git.Repo("/home/ferlete/gitAAA/")
if repo.is_dirty(untracked_files=True):
    print('Changes detected.')
else:
    print('not changes detected')
