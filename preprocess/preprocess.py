from signal import signal, SIGPIPE, SIG_DFL
import sys,cPickle,subprocess
from os.path import join,abspath,dirname,exists
from os import system,chdir,makedirs
from tempfile import NamedTemporaryFile

vcffile = abspath(sys.argv[1])
outdir = abspath(sys.argv[2])
cwd = dirname(abspath(__file__))
if not exists(outdir):
    makedirs(outdir)

# Generate sequence feature
chdir(cwd)
system(' '.join(['Rscript',join(cwd,'sample2fa.R'), vcffile, outdir]))

# Generate DeepBind feature
system(' '.join(['python',join(cwd,'deepbind.py'),join(outdir,'150nt.fa'),outdir,join(cwd,'../data','deepbind')]))

# Generate DeepSEA feature
system(' '.join(['python',join(cwd,'deepsea.py'),join(outdir,'150nt.fa'),outdir]))


# Generate ChromHMM feature files.
cmd = ' '.join(['./chromHMM.sh', vcffile,'>',join(outdir,'roadmap_E116_chromatin_states')])
subprocess.call(cmd ,shell = True,preexec_fn = lambda: signal(SIGPIPE, SIG_DFL))

filemapping = {'deepsea':'deepsea_919feature','deepbind':'deepbind_927feature','roadmap':'roadmap_E116_chromatin_states','ksm':'ksm'}
models = ['deepsea','deepbind']
#models = ['deepsea','deepbind','ksm_deepsea','ksm_deepsea_roadmap']
for model in models:
    outfile = join(outdir,model+'.ready')
    #tmpfile = outfile+'.tmp'
    tmpfile = NamedTemporaryFile(delete=False).name
    featurefile = model.split('_')
    featurefile_cat = ''
    for feature in featurefile:
    	featurefile_cat = featurefile_cat + ' ' + join(outdir,filemapping[feature])
    cmd = ' '.join(['paste -d\'\\t\'',featurefile_cat,'| tail -n+2','>',tmpfile])
    system(cmd)

    with open(join(cwd,'../trained_model/feature_scaler',model+'.scaler.pkl'),'rb') as f:
	scaler = cPickle.load(f)
    with open(tmpfile) as f,open(outfile,'w') as fout:
	data =  scaler.transform([map(float,x.strip().split()) for x in f])
	for x in data:
	    fout.write('%s\n' % '\t'.join(map(str,x)))
    system('rm '+tmpfile)

