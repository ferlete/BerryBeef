import git
import os

if __name__ == "__main__":
   g = git.Git('/home/ferlete/gitAAA/')
   g.pull('origin', 'origin/master')