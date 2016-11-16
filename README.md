# EnsembleExpr
Winner algorithm for CAGI4 eQTL-causal SNP challenge. EnsembleExpr can predict MPRA reporter expression level from sequence, and predict which sequence varaints will lead to significant allele-specific expression. 

## Dependencies
+	[Docker](https://www.docker.com/)

## Usage
```
docker pull haoyangz/ensembleexpr
docker run -v VCF_FILE:/infile.vcf -v OUTPUT_DIR:/outdir -v /etc/passwd:/etc/passwd -u $(id -u) -it --rm 
				haoyangz/ensembleexpr python main.py /infile.vcf /outdir ORDER
```
+ `VCF_FILE`: the *absolte path* to a list of sequence variants in VCF format ([example](https://github.com/gifford-lab/EnsembleExpr/blob/master/example/test.vcf))
+ `OUTPUT_DIR`: the *absolute path* to the output directory, under which the expression predictions from each components in the ensemble and the average will be saved.
+ `ORDER`: several orders can be concatenated separated by space
	+	`-f`: feature generation
	+	`-e`: predict expression for both alleles of each variant
	+	`-v`: predict which variant will lead to significant allele-specific expression

Type `python main.py -h` for detail descriptions of the options.
