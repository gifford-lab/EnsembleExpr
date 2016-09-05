from signal import signal, SIGPIPE, SIG_DFL
import sys,cPickle,subprocess,numpy as np
from os.path import join,abspath,dirname,exists,basename
from os import system,chdir,makedirs
from tempfile import NamedTemporaryFile

vcffile = abspath(sys.argv[1])
outdir = abspath(sys.argv[2])
cwd = dirname(abspath(__file__))
if not exists(outdir):
    makedirs(outdir)

# Generate sequence feature
print '#### Getting 150bp sequence from VCF ####'
vcffile_processed = join(outdir,basename(vcffile)+'_woheader')
system(' '.join(['sed \'/^#/ d\'','<',vcffile,'>',vcffile_processed]))
chdir(cwd)
system(' '.join(['Rscript',join(cwd,'sample2fa.R'), vcffile_processed, outdir]))

# Generate DeepBind feature
print '#### Getting DeepBind features ####'
system(' '.join(['python',join(cwd,'deepbind.py'),join(outdir,'150nt.fa'),outdir,join(cwd,'../data','deepbind')]))

# Generate DeepSEA feature
print '#### Getting DeepSEA features ####'
system(' '.join(['python',join(cwd,'deepsea.py'),join(outdir,'150nt.fa'),outdir]))

# Generate KSM feature
print '#### Getting KSM features ####'
ksm_folder = join(cwd,'ksm')
chdir(ksm_folder)
system(' '.join([join(ksm_folder,'scan_ksm.sh'),'input',join(outdir,'150nt.fa')]))
system(' '.join(['cp',join(ksm_folder,'input.m0.scorematrix.txt'),join(outdir,'ksm')]))

# Generate ChromHMM feature files.
print '#### Getting ChromHMM features ####'
chdir(cwd)
cmd = ' '.join([join(cwd,'chromHMM.sh'), vcffile,join(cwd,'../data/E116_18_core_K27ac_mnemonics.bed.gz'),'>',join(outdir,'roadmap_E116_chromatin_states')])
subprocess.call(cmd ,shell = True,preexec_fn = lambda: signal(SIGPIPE, SIG_DFL))

# Combile features for each component in the ensemble
filemapping = {'deepsea':'deepsea_919feature','deepbind':'deepbind_927feature','roadmap':'roadmap_E116_chromatin_states','ksm':'ksm'}
models = ['deepsea','deepbind','ksm_deepsea','ksm_deepsea_roadmap']
for model in models:
    print '#### Combining features for',model,' ####'
    outfile = join(outdir,model+'.ready')
    tmpfile = NamedTemporaryFile(delete=False).name

    featurefile = model.split('_')
    featurefile_cat = ''
    for feature in featurefile:
    	featurefile_cat = featurefile_cat + ' ' + join(outdir,filemapping[feature])
    cmd = ' '.join(['paste -d\'\\t\'',featurefile_cat,'| tail -n+2','>',tmpfile])
    system(cmd)

    with open(join(cwd,'../trained_model/feature_scaler_test',model+'.scaler.pkl'),'rb') as f:
	scaler = cPickle.load(f)

    with open(tmpfile) as f,open(outfile,'w') as fout:
        data =  scaler.transform([map(float,x.strip().split()) for x in f])
	for x in data:
	    fout.write('%s\n' % '\t'.join(map(str,x)))
    system('rm '+tmpfile)

