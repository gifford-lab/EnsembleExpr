import sys,cPickle,numpy as np
from os.path import dirname,join,exists,realpath
from os import system,makedirs

vcffile = realpath(sys.argv[1])
outdir = realpath(sys.argv[2])

featuredir = join(outdir,'features')
if not exists(featuredir):
    makedirs(featuredir)
system(' '.join([ 'python preprocess/preprocess.py',vcffile,featuredir]))

models = ['deepsea','deepbind']
preds = []
for model in models:
    with open(join('trained_model','model',model+'.model.pkl'),'rb') as f:
        mymodel = cPickle.load(f)
    with open(join(featuredir,model+'.ready')) as f:
        myfeature  = [map(float,x.split()) for x in f]
    pred  = mymodel.predict(myfeature)
    preds.append(pred)
    with open(join(outdir,model+'.out'),'w') as f:
        for x in pred:
            f.write('%f\n' % x)

with open(join(outdir,'avg.out'),'w') as f:
    for x in np.asarray(preds).mean(axis=0):
        f.write('%f\n' % x)


