import sys,numpy as np

fafile = sys.argv[1]
samplefile = sys.argv[2]
outfile = sys.argv[3]

dict = {}
with open(samplefile,'r') as f:
    cnt = 0
    for x in f:
        line = x.strip().split()
        dict['-'.join(['chr'+line[0],line[1]])] = cnt
        cnt = cnt + 1

idx = []
with open(fafile,'r') as f:
    for x in f:
        idx.append(dict['-'.join(x.strip().split(':')[1:3])])

idx = np.asarray(idx)

reorder = np.argsort(idx,kind='quicksort')

with open(fafile,'r') as f:
    fa = [x for x in f]

with open(outfile,'w') as f:
    for i in range(len(fa)):
        f.write(fa[reorder[i]])


