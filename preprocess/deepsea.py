from os.path import join,exists,realpath
from os import system,makedirs,getcwd,chdir,remove
from tempfile import NamedTemporaryFile,mkdtemp
import sys

fafile = realpath(sys.argv[1])
topdir = realpath(sys.argv[2])

padding =  ''.join(['N']*425)
fasta_n = 80

def convert(infile,outfile):
    with open(infile,'r') as fin, open(outfile,'w') as fout:
        cnt = 0
        for x in fin:
            cnt = (cnt + 1) % 2
            if cnt == 1:
                fout.write(x)
            else:
                line = ''.join([padding,x.strip(),padding])
                outstring = [line[i:i+fasta_n] for i in range(0, len(line), fasta_n)]
                for item in outstring:
                    fout.write('%s\n' % item)

infile = '/script/test.fasta'
convert(fafile,infile)

tmpoutdir = '/script/deepsea_tmp'
chdir('/root/DeepSEA-v0.94/')
system(' '.join(['python','rundeepsea.py',infile,tmpoutdir]))

outfile = join(tmpoutdir,'infile.fasta.out')
outfile_final = join(topdir,'deepsea_919feature')
system(' '.join(['cut -d \",\" -f 3- --output-delimiter=\'\t\' ',outfile,'>',outfile_final]))

system('rm -r ' + tmpoutdir)
remove(infile)

