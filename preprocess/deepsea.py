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

infile = NamedTemporaryFile(delete=False).name
convert(fafile,infile)

#tmpoutdir = mkdtemp()
tmpoutdir = join(topdir,'deepsea_tmp')
system('docker pull haoyangz/deepsea-predict-docker')
system(' '.join(['docker run ','-v',infile+':/infile.fasta','-v',tmpoutdir+':/output --rm haoyangz/deepsea-predict-docker python rundeepsea.py /infile.fasta /output']))

outfile = join(tmpoutdir,'infile.fasta.out')
outfile_final = join(topdir,'deepsea_919feature')
system(' '.join(['cut -d \",\" -f 3- --output-delimiter=\'\t\' ',outfile,'>',outfile_final]))

#system('rm -r ' + tmpoutdir)
remove(infile)

