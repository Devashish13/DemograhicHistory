# SMCPP_pipeline
A python pipeline for implementing smcpp to decipher demographic history of populations of interest

All the functions assume that the user has generated population population-specific chromosome file and stored it in a directory popname_vcf present in the current working directory. all the chromosome files should be bgzipped and tabix indexed.

If the user has a single genotype file, then user can make use of bcftools script provided here to generate population-specific bgzipped and tabix index VCFs.
