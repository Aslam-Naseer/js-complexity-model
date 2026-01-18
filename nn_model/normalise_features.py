import numpy as np

feature_cols = ['parameter_count', 'statement_count',
                'variable_count', 'max_nesting_depth']


def normalise_features(data, scaler):
    mat = np.array([data[col] for col in feature_cols]).reshape(1, -1)
    scaled_mat = scaler.transform(mat)
    return {"features": scaled_mat}
