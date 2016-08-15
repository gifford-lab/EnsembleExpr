from os.path import join,exists,dirname,abspath,realpath,exists
from os import system,makedirs,getcwd,chdir,makedirs
import sys

cwd = dirname(abspath(__file__))

fafile = realpath(sys.argv[1])
topdir = realpath(sys.argv[2])
deepbind_sourcedir = realpath(sys.argv[3])

if not exists(topdir):
    makedirs(topdir)

outfile = join(topdir,'deepbind_927feature')
chdir(deepbind_sourcedir)
cmd = ' '.join(['./deepbind','all.ids','<',fafile,'>',outfile])
print cmd
system(cmd)
chdir(cwd)
