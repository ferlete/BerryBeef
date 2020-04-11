import git
import os

if __name__ == "__main__":
   #repo = git.Repo('/home/ferlete/PycharmProjects/BERRYBEEF/')
   #repo = git.Repo.clone_from("https://github.com/ferlete/BERRYBEEF", os.path.join('/home/ferlete/PycharmProjects/', 'BERRYBEEF'), branch='master')
   #origin = repo.remotes.origin
   #origin.pull()
   #print(origin)
   g = git.Git('/home/ferlete/PycharmProjects/BERRYBEEF/')
   print(g.version_info)
   g.pull('origin', 'master')