from sklearn.metrics import r2_score

def evaluate_model(model, X_val, y_val):
    y_pred = model.predict(X_val)
    r2 = r2_score(y_val, y_pred, multioutput = 'raw_values')
    return r2