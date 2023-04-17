from sgkit.io import plink
import numpy as np
import xarray as xr
from omegaconf import DictConfig
import pandas as pd


def load_dataset(cfg: DictConfig):
    ds = plink.read_plink(
        bed_path = cfg.bed,
        bim_path = cfg.bim,
        fam_path = cfg.fam
    )
    ds = ds.set_index({"samples": "sample_id"})
    ds = ds.set_index({"variants": "variant_id"})
    call_g_mask = ds["call_genotype_mask"].any(dim = "ploidy")
    call_g = xr.where(call_g_mask, -1, ds["call_genotype"].sum(dim = "ploidy"))
    genotypes_matrix = call_g.values
    genotypes_matrix = np.transpose(genotypes_matrix)
    phenotypes = pd.read_csv(cfg.pheno, sep = '\t')

    rat_ids = ds["samples"].values
    genotypes_df = pd.DataFrame(data = genotypes_matrix, index = rat_ids)
    genotypes_df.index.name = 'rfid'
    geno_with_pheno = pd.merge(genotypes_df, phenotypes, left_index=True, right_index=True)
    y_pheno = geno_with_pheno[phenotypes.columns].to_numpy()
    X_geno = geno_with_pheno.drop(columns = phenotypes.columns).to_numpy()
    
    return(X_geno, y_pheno)


