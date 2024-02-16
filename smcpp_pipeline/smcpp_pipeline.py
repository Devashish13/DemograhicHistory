#vcf2smc converts chromosomewise vcf to smc format for each population

def vcf2smc(popfile,chromosome_info,gaps_bed=None,num_workers=None):
        import pandas as pd
        import os
        import concurrent.futures
        import itertools
        import multiprocessing
        import re

        os.system("mkdir out"); os.system("mkdir analysis"); os.system("mkdir plots")
        if num_workers is None:
                num_workers = multiprocessing.cpu_count()-1

        df = pd.read_csv(popfile,sep = "\t")
        unique_pops = df.loc[:,"population"].unique()
        for pop in unique_pops:
                popids = df[df["population"] == pop]
                df1 = pd.DataFrame(popids.iloc[:,0])
                df1.to_csv('popid_'+pop+'.txt', sep='\t',header = False,index=False)

        df4 = pd.read_csv(chromosome_info,sep = "\t")
        combs = list(itertools.product(df4['chromosome'], unique_pops))
        def process_chromosome(i, j):
                contig = int(re.search(r'\d+', i).group())
                df4 = pd.read_csv(chromosome_info,sep = "\t")
                chr_len_bp = df4[df4['chromosome'] == i]['length_bp'].values[0]
                df1 = pd.read_csv(f"popid_{j}.txt",header = None)
                popls = ",".join(df1.iloc[:,0].tolist())
                d_ids = " ".join(df1.iloc[0:2,0].tolist())
                os.system(f"tabix -f -p vcf {j}/{i}.vcf.gz")
                os.system(f"mkdir out/{j}")
                if gaps_bed is None:
                        os.system(f"docker run --rm -v $PWD:/mnt terhorst/smcpp:latest vcf2smc -d {d_ids} --length {chr_len_bp} {j}/{i}.vcf.gz out/{j}/{i}.smc.gz {contig} {j}:{popls}")
                else:
                        os.system(f"docker run --rm -v $PWD:/mnt terhorst/smcpp:latest vcf2smc -d {d_ids} -m {gaps_bed} --length {chr_len_bp} {j}/{i}.vcf.gz out/{j}/{i}.smc.gz {contig} {j}:{popls}")

        # Parallelize over combinations of i and j
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
                executor.map(lambda x: process_chromosome(x[0], x[1]), combs)

def estimate(popfile,mu = 1.25e-8,spline = "piecewise",start_time = 100, end_time=100000,knots = 8):
        import pandas as pd
        import os
        df = pd.read_csv(popfile,sep = "\t")
        unique_pops = df.iloc[:,1].unique()

        for j in unique_pops:
                os.system(f"mkdir analysis/{j}")
                os.system(f"docker run --rm -v $PWD:/mnt terhorst/smcpp:latest estimate {mu} -o analysis/{j}/ out/{j}/chr*.smc.gz --knots {knots} --timepoints {start_time} {end_time} --spline {spline}")

def plot(popfile,time_start=100,time_end=15000):
        import pandas as pd
        import os
        df = pd.read_csv(popfile,sep = "\t")
        unique_pops = df.iloc[:,1].unique()

        s = "docker run --rm -v $PWD:/mnt terhorst/smcpp:latest plot plots/demography_all.png "
        for k in unique_pops:
                z = f"docker run --rm -v $PWD:/mnt terhorst/smcpp:latest plot plots/{k}.png analysis/{k}/model.final.json -x {time_start} {time_end} -c"
                os.system(z)
                s = s+f"analysis/{k}/model.final.json "

        s = s+f"-x {time_start} {time_end} -c"
#        print(s)
        os.system(s)
