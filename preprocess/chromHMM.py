import sys,tempfile,collections
from os.path import join,exists,dirname,realpath
from os import system

vcf_file = sys.argv[1]
outfile = sys.argv[2]

cwd = dirname(realpath(__file__))

## Convert VCF to BED
print 'VCF to BED'
mybed = tempfile.mkstemp()[1]
cmd = ' '.join(['Rscript',join(cwd,'vcf2bed.R'), vcf_file, mybed])
system(cmd)

## BED to chromHMM label
print 'BED to chromHMM'
hmmlabel = tempfile.mkstemp()[1]
cmd = ' '.join(['bedtools intersect -a ../data/E116_18_core_K27ac_mnemonics.bed.gz -b',mybed, '>',hmmlabel])
system(cmd)

## Reorder label
print 'Reorder'
hmmreordered = tempfile.mkstemp()[1]
mymapper = collections.defaultdict(str)
with open(hmmlabel) as f:
    for x in f:
        line = x.split()
        mymapper[line[0]+'-'+line[2]] = x

with open(vcf_file) as f,open(hmmreordered,'w') as fout:
    for x in f:
        if x[0]!='#':
            line = x.split()
            fout.write(mymapper['chr'+line[0]+'-'+line[1]])

## chromHMM label to output
print 'outputting'
cmd = ' '.join(['cut -f 4',hmmreordered,' | python chromHMM_one_hot_encode.py ../data/E116_18_core_K27ac_mnemonics.bed.gz >',outfile])
system(cmd)

for f2remove in [mybed,hmmlabel,hmmreordered]:
    system('rm -r ' + f2remove)

