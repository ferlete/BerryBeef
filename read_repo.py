import git

if __name__ == "__main__":
   #git.Repo.clone_from("https://github.com/ferlete/BERRYBEEF/","/home/ferlete/gitAAA")
   repo = git.Repo('/home/ferlete/gitAAA')
   o = repo.remotes.origin
   o.pull()
