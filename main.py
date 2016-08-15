import sys,cPickle,numpy as np,argparse
from os.path import dirname,join,exists,realpath
from os import system,makedirs

def parse_args():
    parser = argparse.ArgumentParser(description="Launch a list of commands on EC2.")
    parser.add_argument("vcffile",  type=str, help="The vcffile to predict on ")
    parser.add_argument("outdir",  type=str, help="The output directory")
    parser.add_argument("-f", "--feature", action="store_true", dest="feature", default=False, help="Prepare features")
    parser.add_argument("-e", "--expression", action="store_true", dest="expression", default=False, help="Predict expression on the features")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    vcffile = realpath(args.vcffile)
    outdir = realpath(args.outdir)

    featuredir = join(outdir,'features')
    if args.feature:
        if not exists(featuredir):
            makedirs(featuredir)
        system(' '.join([ 'python preprocess/preprocess.py',vcffile,featuredir]))

    if args.expression:
        models = ['deepsea','deepbind','ksm_deepsea','ksm_deepsea_roadmap']
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


