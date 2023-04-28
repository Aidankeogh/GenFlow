# Data generator object for facilitating MLFlow pipeline presenting geome-scale AI with HS rat WGS data

# by Zach Wallace

import sgkit as sg
from sgkit.io import plink
import pandas as pd
import numpy as np
import math
import pickle
import xarray as xr


# Filter the genotypes data based on phenotype labels, missing variants, and GWAS statistical association
# If pre-filtered pickeled version of the sgkit xarray is not passed in, the object will need the plink
# version of the genotype data.  Also needed is the phenotype data and a possible select list of 
# traits to choose from.
def training_set(ds_pkl = None, gwas_pvalue = 0.05, geno_bed = 'dataset/ratgenes_pruned/ratgenes_pruned.bed', 
	geno_bim = 'dataset/ratgenes_pruned/ratgenes_pruned.bim', geno_fam = 'dataset/ratgenes_pruned/ratgenes_pruned.fam', 
	phenotypes = 'dataset/pheno_loco_clean.txt', select_traits = ['loco_maxcent', 'loco_maxdis', 'loco_maxrear', 'loco_maxact']):

	try: 
		phenotypes = pd.read_csv(phenotypes, sep = '\t')
	except:
		raise Exception("ERROR: Unable to open phenotypes file.")

	# Passing in a pickeled dataset pre-filtered for unknown variants will speed things up a lot
	if ds_pkl:
		try:
			with open(ds_pkl, 'rb') as handle:
				ds = pickle.load(handle)
		except:
			raise Exception("ERROR: Unable to open pickeled sgkit genotypes file.")

		# Laod in clean phenotypes matrix
		phenotypes = load_phenotypes(ds, phenotypes, select_traits)

		if select_traits:
			ds = gwas_lin_reg(ds, select_traits)
		else:
			ds = gwas_lin_reg(ds, list(phenotypes.columns))

		if gwas_pvalue:
			print("Filtering based on GWAS statisical association ...")
			ds = ds.sel(variants=((ds.variant_linreg_p_value < gwas_pvalue).any('traits')))
			print("Done filtering based on GWAS\n")

		X_geno, Y_pheno = geno_pheno_matrix(ds, phenotypes)

		return(X_geno, Y_pheno)


	# If no pre-filtered Sgkit dataset ...

	# Read in plink version of genotypes
	ds = plink.read_plink(bed_path = geno_bed, bim_path = geno_bim, fam_path = geno_fam)
	ds = ds.set_index({"samples": "sample_id"})

	# Load in clean phenotypes matrix
	phenotypes = load_phenotypes(ds, phenotypes, select_traits)

	# Merge genotypes data with the phenotypes data
	ds_phenotypes = pd.DataFrame.to_xarray(phenotypes)
	ds = ds.drop_duplicates(dim = ['samples'])
	ds = ds.sel(samples = list(phenotypes.index))
	ds = ds.merge(ds_phenotypes, join="left")

	# Filter out missing SNPs for GWAS, only keeping known genotypes
	print("Filtering out unknown SNPs (takes a while) ...")
	ds = sg.stats.pca.count_call_alternate_alleles(ds)
	variant_mask = ((ds.call_alternate_allele_count < 0).any(dim="samples")) | \
		(ds.call_alternate_allele_count.std(dim="samples") <= 0.0)
	ds = ds.sel(variants=~variant_mask)
	print("Done filtering unknown SNPs\n")

	# Compute GWAS satistical regression pvalues
	if select_traits:
		ds = gwas_lin_reg(ds, select_traits)
	else:
		ds = gwas_lin_reg(ds, list(phenotypes.columns))

	if gwas_pvalue:
		print("Filtering based on GWAS statisical association ...")
		ds = ds.sel(variants=((ds.variant_linreg_p_value < gwas_pvalue).any('traits')))
		print("Done filtering based on GWAS\n")

	X_geno, Y_pheno = geno_pheno_matrix(ds, phenotypes)

	return(X_geno, Y_pheno)


# Generate the clean phenotypes matrix
def load_phenotypes(ds, phenotypes, select_traits):

	# Build appropriate phenotypes matrix and ensure it's clean, no missing data
	phenotypes = phenotypes.set_index('rfid')
	if select_traits:
		phenotypes = phenotypes[select_traits]
	phenotypes = phenotypes.select_dtypes(['number'])
	limit = math.floor(len(phenotypes) * 0.80)
	phenotypes = phenotypes.dropna(axis=1, thresh=limit).dropna(axis=0)

	# Filter phenotypes to only include rats in the genotypes dataset
	rat_ids = ds['samples'].values
	phenotypes = phenotypes.filter(items = rat_ids, axis=0)
	phenotypes.index.name = 'samples'

	return(phenotypes)


# Run GWAS linear regression to get phenotype association pvalues 
def gwas_lin_reg(ds, traits):

	ds["call_dosage"] = ds.call_genotype.sum(dim="ploidy")
	ds = sg.gwas_linear_regression(ds, dosage="call_dosage", add_intercept=True, covariates=[], traits=traits)

	return(ds)


# Return two matrices: a genotypes matrix (X) and it's corresponding phenotypes matrix (Y)
def geno_pheno_matrix(ds, phenotypes):

	# Convert the genotypes xarray to a numpy matrix
	print("Building genotypes matrix ...")
	call_g_mask = ds["call_genotype_mask"].any(dim = "ploidy")
	call_g = xr.where(call_g_mask, -1, ds["call_genotype"].sum(dim = "ploidy"))
	genotypes = call_g.values
	genotypes = np.transpose(genotypes)
	print("Done building genotypes matrix\n")

	# Create X genotypes matrix and y phenotypes matrix ensuring they're the proper
	# genotype to phenotype mapping based on the rat id
	rat_ids = ds["samples"].values
	genotypes_df = pd.DataFrame(data = genotypes, index = rat_ids)
	genotypes_df.index.name = 'Sample'
	geno_with_pheno = pd.merge(genotypes_df, phenotypes, left_index=True, right_index=True)
	X_geno = geno_with_pheno.drop(columns = phenotypes.columns).to_numpy()
	Y_pheno = geno_with_pheno[phenotypes.columns].to_numpy()

	return(X_geno, Y_pheno)







	