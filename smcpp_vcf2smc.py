import pandas as pd
import os
import concurrent.futures
import itertools


df = pd.read_csv("/data/sata_data1/ab1/devashish/GI_smcpp/metadata_5698_rmNA_rmduplicates_rmoutlier.txt",sep = "\t")
unique_pops = df.iloc[:,1].unique()
unique_pops = [pop for pop in unique_pops if pop not in ("Khatri", "Shakaldipi_Brahmin")]
print(unique_pops)

combs = list(itertools.product(range(1, 23), unique_pops))
#print(combs)

def process_chromosome(i, j):
	df4 = pd.read_csv("/data/sata_data1/ab1/devashish/GI_smcpp/chromosome_table.txt",sep = "\t")
	chr_len_bp = df4[df4['chromosome'] == "chr"+str(i)]['length_bp'].values[0]
	df1 = pd.read_csv(f"popid_{j}.txt",header = None)
	popls = ",".join(df1.iloc[:,0].tolist())
	d_ids = " ".join(df1.iloc[0:2,0].tolist())
	os.system(f"tabix -f -p vcf {j}_vcf/chr{i}.phased.{j}.vcf.gz")
	os.system(f"mkdir out/{j}")
	os.system(f"docker run --rm -v $PWD:/mnt terhorst/smcpp:latest vcf2smc -d {d_ids} -m hg38_gaps_sorted.gz --length {chr_len_bp} {j}_vcf/chr{i}.phased.{j}.vcf.gz out/{j}/chr{i}.smc.gz {i} {j}:{popls}")


num_workers = 15
# Parallelize over combinations of i and j
with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
	executor.map(lambda x: process_chromosome(x[0], x[1]), combs)

