# SMCPP_pipeline
A python pipeline for implementing smcpp to decipher demographic history of populations of interest

All the functions assume that the user has generated population population-specific chromosome file and stored it in a directory popname_vcf present in the current working directory. all the chromosome files should be bgzipped and tabix indexed.

If the user has a single genotype file, then user can make use of bcftools script provided here to generate population-specific bgzipped and tabix index VCFs.


from smcpp_pipeline import vcf2smc,estimate,plot
1) Function to convert vcf file to smc format
  def vcf2smc(popfile,chromosome_info,gaps_bed,num_workers)
2) Function to estimate the demographic history of a single population
   def estimate(popfile,mu = 1.25e-8,spline = "piecewise",start_time = 100, end_time=100000,knots = 8
3) Function to generate plots from the model.json file obtained using estimate function
   def plot(popfile,time_start=100,time_end=15000)

popfile should be a tab separated file containing two columns

sample.id  population
i1          pop1
i2          pop1
i3          pop2  
