args = commandArgs(T)

infile = args[1]
outdir = args[2]

toVCF <- function(mat,vcffile){
	write.table(mat,file=vcffile,quote=F,row.names=F,col.names=F,sep='\t')
}


convert <- function(infile,outdir){ 
	vcfdir = tempfile()
	fadir = tempfile()

	dir.create(vcfdir,showWarnings=F,recursive=T)
	dir.create(fadir,showWarnings=F,recursive=T)

	mat <- read.delim(infile,stringsAsFactors=F,header=F)

	dir.create(outdir,showWarnings=F,recursive=T)
	uni_chr = unique(mat[,1])
	for (chr in uni_chr){
		part = mat[mat[,1]==chr,]
		toVCF(part,file.path(vcfdir,paste0('chr',chr,'.vcf')))
	}

	cmd = paste0('Rscript  /cluster/zeng/code/research/tools/REFORMAT/vcf2fasta.R ',vcfdir,' /cluster/zeng/research/hg19_data/hg19.in /cluster/zeng/research/hg19_data/seq_data/all.size.txt ',fadir,' 74.9 T')
	system(cmd)
	
	confa = tempfile()
	cmd = paste('paste - - - - -d\'!\' <',file.path(fadir,'all.fa'),'>',confa,sep=' ')
	system(cmd)

	sorted_confa = tempfile()
	cmd = paste('python matchFa2sample.py',confa,infile,sorted_confa,sep=' ')
	system(cmd)

	outfile = file.path(outdir,'150nt.fa')
	unlink(outfile)
	cmd = paste('awk -F"!" \'{print $1 "\\n" $2  "\\n"   $3  "\\n" $4 }\'',sorted_confa,'>',file.path(outdir,'150nt.fa'),sep=' ')
	system(cmd)
	
	cmd = paste('paste - - -d\'\\t\' <',file.path(outdir,'150nt.fa'),'>',file.path(outdir,'150.tsv'),sep=' ')
	system(cmd)

	system(paste('rm -r',vcfdir,sep=' '))
	system(paste('rm -r',fadir,sep=' '))
	system(paste('rm ',confa,sep=' '))
	system(paste('rm ',sorted_confa,sep=' '))
}

convert(infile,outdir)
