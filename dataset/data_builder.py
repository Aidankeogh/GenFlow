# Pipeline for building SNP dataset and facilitating geome-scale AI with HS rat WGS data

# by Zach Wallace

import sgkit as sg
from sgkit.io import plink
import pandas as pd
import numpy as np
import math
import pickle
import xarray as xr


class training_data(object):

    # Filter the genotypes data based on phenotypes labels, missing variants, and GWAS statistical association
    # Also needed is the phenotype data and a possible select list of traits to choose from.
    # NOTE: If filter_unknowns is set to False, GWAS filtering WILL NOT be carried out
    def __init__(self, 
        geno_bed = 'ratgenes_pruned/ratgenes_pruned_0.8.bed', 
        geno_bim = 'ratgenes_pruned/ratgenes_pruned_0.8.bim', 
        geno_fam = 'ratgenes_pruned/ratgenes_pruned_0.8.fam', 
        phenotypes = 'phenotypes/pheno_loco_clean.txt', 
        select_traits = ['loco_maxcent', 'loco_maxdis', 'loco_maxrear', 'loco_maxact'],
        filter_unknowns = True):

        # Read in plink version of genotypes
        ds = plink.read_plink(bed_path = geno_bed, bim_path = geno_bim, fam_path = geno_fam)
        ds = ds.set_index({"samples": "sample_id"})
        
        if phenotypes[-4:] == ".csv": # Support CSV and TSV
            pheno_sep = ","
        else:
            pheno_sep = "\t"

        # Read in phenotypes data and ensure it's clean, no missing data
        phenotypes = pd.read_csv(phenotypes, sep = pheno_sep)
        phenotypes = phenotypes.set_index('rfid')
        if select_traits:
            phenotypes = phenotypes[select_traits]
        phenotypes = phenotypes.select_dtypes(['number'])
        limit = math.floor(len(phenotypes) * 0.80)
        phenotypes = phenotypes.dropna(axis=1, thresh=limit).dropna(axis=0)

        # Filter phenotypes to only include rats in the genotype dataset
        rat_ids = ds['samples'].values
        phenotypes = phenotypes.filter(items = rat_ids, axis=0)
        phenotypes.index.name = 'samples'

        # Merge genotypes data with the phenotypes data
        ds_phenotypes = pd.DataFrame.to_xarray(phenotypes)
        ds = ds.drop_duplicates(dim = ['samples'])
        ds = ds.sel(samples = list(phenotypes.index))
        ds = ds.merge(ds_phenotypes, join="left")

        # Filter out missing SNPs for GWAS, only keeping known genotypes
        if filter_unknowns:
            print("Filtering out unknown SNPs (takes a while) ...")
            ds = sg.stats.pca.count_call_alternate_alleles(ds)
            variant_mask = ((ds.call_alternate_allele_count < 0).any(dim="samples")) | \
            (ds.call_alternate_allele_count.std(dim="samples") <= 0.0)
            ds_known = ds.sel(variants=~variant_mask)
            print("Done filtering unknown SNPs\n")
            ds_gwas = self.gwas_lin_reg(ds_known, list(phenotypes.columns))
        # Else, keep all the uknowns, don't perfomr GWAS
        else:
            ds_known = ds
            ds_gwas = ds

        self.phenotypes = phenotypes
        self.filter_unknowns = filter_unknowns
        self.ds_known = ds_known
        self.ds_gwas = ds_gwas


    # Return matrix format of the genotypes data filtered by gwas_pvalues
    def gwas_filtered(self, gwas_pvalue = 0.05):
        
        # Only carry out GWAS filtering if filter_unknowns is True gwas_pvalue is not None
        if (self.filter_unknowns and gwas_pvalue):
            print("Filtering based on GWAS statisical association with p-value", gwas_pvalue)
            ds_filtered = self.ds_gwas.sel(variants=((self.ds_gwas.variant_linreg_p_value < gwas_pvalue).any('traits')))
            print("Done filtering based on GWAS\n")
        else:
            ds_filtered = self.ds_gwas

        # Convert the genotypes xarray to a numpy matrix
        print("Building genotypes matrix ...")
        call_g_mask = ds_filtered["call_genotype_mask"].any(dim = "ploidy")
        call_g = xr.where(call_g_mask, -1, ds_filtered["call_genotype"].sum(dim = "ploidy"))
        genotypes = call_g.values
        genotypes = np.transpose(genotypes)
        print("Done building genotypes matrix\n")
        
        # Create X genotypes matrix and Y phenotypes matrix ensuring they're the proper
        # genotype to phenotype mapping based on the rat id
        rat_ids = ds_filtered["samples"].values
        genotypes_df = pd.DataFrame(data = genotypes, index = rat_ids)
        genotypes_df.index.name = 'samples'
        geno_with_pheno = pd.merge(genotypes_df, self.phenotypes, left_index=True, right_index=True)
        X_geno = geno_with_pheno.drop(columns = self.phenotypes.columns)
        Y_pheno = geno_with_pheno[self.phenotypes.columns]

        return(X_geno, Y_pheno)

    # Save the dataset filtered with known genotypes to a pickel
    def save_to_pickle(self, filename = 'ds_known.pkl'):

        with open(filename, 'wb') as handle:
            pickle.dump(self.ds_known, handle)

    # Run GWAS linear regression
    @staticmethod
    def gwas_lin_reg(ds, traits):

        ds["call_dosage"] = ds.call_genotype.sum(dim="ploidy")
        ds_gwas = sg.gwas_linear_regression(ds, dosage="call_dosage",
                                            add_intercept=True, covariates=[], traits=traits)

        return(ds_gwas)


