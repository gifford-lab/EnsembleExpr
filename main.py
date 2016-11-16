import sys,cPickle,numpy as np,argparse,sklearn,pandas as pd
from os.path import dirname,join,exists,realpath
from os import system,makedirs

def parse_args():
    parser = argparse.ArgumentParser(description="Launch a list of commands on EC2.")
    parser.add_argument("vcffile",  type=str, help="The vcffile to predict on ")
    parser.add_argument("outdir",  type=str, help="The output directory")
    parser.add_argument("-f", "--feature", action="store_true", dest="feature", default=False, help="Prepare features")
    parser.add_argument("-e", "--expression", action="store_true", dest="expression", default=False, help="Predict expression on the features")
    parser.add_argument("-v", "--emvar", action="store_true", dest="emvar", default=False, help="Predict variant significant allele-specific expression")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    vcffile = realpath(args.vcffile)
    outdir = realpath(args.outdir)
    exprdir = join(outdir,'expr_pred')
    emvardir = join(outdir,'emvar_pred')

    featuredir = join(outdir,'features')
    if args.feature:
        if not exists(featuredir):
            makedirs(featuredir)
        system(' '.join([ 'python preprocess/preprocess.py',vcffile,featuredir]))

    if args.expression:
        if not exists(exprdir):
            makedirs(exprdir)
        models = ['deepsea','deepbind','ksm_deepsea','ksm_deepsea_roadmap']
        preds = []
        for model in models:
            with open(join('trained_model','model',model+'.model.pkl'),'rb') as f:
                mymodel = cPickle.load(f)
            with open(join(featuredir,model+'.ready')) as f:
                myfeature  = [map(float,x.split()) for x in f]
            pred  = mymodel.predict(myfeature)
            preds.append(pred)
            np.savetxt(join(exprdir,model+'.pred'),pred)
        pd.DataFrame(np.asarray(preds).mean(axis=0).reshape(-1,2),columns=['Ref_Allele','Alt_Allele']).to_csv(join(exprdir,'avg.tsv'),sep='\t',index=False)

    if args.emvar:
        if not exists(emvardir):
            makedirs(emvardir)
        expr = pd.read_csv(join(exprdir,'avg.tsv'),sep='\t')
        expr['diff'] = expr['Ref_Allele'] - expr['Alt_Allele']
        expr['absdiff'] = np.abs(expr['diff'])
        models = ["LR (l1, C=1)","LR (l2, RBF kernel)","SVM (RBF)","SVM (linear)","k-NN (k=25)"]
        preds = []
        for model in models:
            with open(join('trained_model','model','emVar',model+'.pkl'),'rb') as f:
                mymodel = cPickle.load(f)
            if type(mymodel) is list:
                pred = mymodel[0].predict_proba(sklearn.metrics.pairwise.rbf_kernel(expr.values[:],mymodel[1]))[:,1]
            else:
                pred = mymodel.predict_proba(expr.values[:])[:,1]
            preds.append(pred)
            np.savetxt(join(emvardir,model+'.pred'),pred)
        pd.DataFrame(np.asarray(preds).mean(axis=0),columns=['emVar_proba']).to_csv(join(emvardir,'avg.tsv'),sep='\t',index=False)

