# Makefile to generate test results from sequence files

REF=chr11.fa
S1_SORT_BAM=s1.sort.bam




bcftools/s1.vcf.gz: ${S1_SORT_BAM} ${REF}
	samtools mpileup -ug -f ${REF} ${S1_SORT_BAM} | bcftools call -vmO z -o $@

%.vcf.gz.stats: %.vcf.gz ${REF}
	bcftools stats -f ${REF} $< > $@ 
