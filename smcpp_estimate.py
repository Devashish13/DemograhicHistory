import pandas as pd
import os

df = pd.read_csv("/data/sata_data1/ab1/devashish/GI_smcpp/metadata_5698_rmNA_rmduplicates_rmoutlier.txt",sep = "\t")
unique_pops = df.iloc[:,1].unique()
unique_pops = [pop for pop in unique_pops if pop not in ("Khatri", "Shakaldipi_Brahmin","Dongri_Bhil","Marathas","Meitei")]
print(unique_pops)


for j in unique_pops:
	os.system("mkdir analysis/"+j)
	os.system("docker run --rm -v $PWD:/mnt terhorst/smcpp:latest estimate -o analysis/"+j+"/"+ " 1.25e-8 out/"+j+"/"+"chr*.smc.gz --knots 12 --timepoints 100 100000 --spline cubic")

