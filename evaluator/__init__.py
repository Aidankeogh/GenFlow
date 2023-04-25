from sklearn.metrics import r2_score

def evaluate_model(config, model, dataset):
    y_pred = model.predict(dataset.genotype)
    r2 = r2_score(dataset.phenotype, y_pred)
    return r2