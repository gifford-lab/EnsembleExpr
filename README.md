# EnsembleExpr
Winner algorithm for CAGI4 eQTL-causal SNP challenge. EnsembleExpr can predict the MPRA reporter expression level from sequence, and predict which sequence varaints will lead to significant allele-specific expression. 

# Dependencies
+	[Docker](https://www.docker.com/)

# MPRA reporter expression prediction 
Predict the MPRA reporter expression level for both alleles of a list of variants in [VCF](http://www.1000genomes.org/wiki/Analysis/vcf4.0/) format.
```
python main.py VCF_FILE OUTPUT_DIR
```
+ VCF_FILE: a list of sequence variants in VCF format ([example](https://github.com/gifford-lab/EnsembleExpr/blob/master/example/test.vcf))
+ OUTPUT_DIR: the output directory, under which the expression predictions from each components in the ensemble and the average will be saved.

# Significant allele-specific reporter expression prediction
To be uploaded.
