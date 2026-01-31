import numpy as np

cols = [
    'param_count',
    'local_statement_count',
    'total_statement_count',
    'local_variable_count',
    'total_variable_count',
    'local_nesting_depth',
    'total_nesting_depth'
]


def normalise_features(data, scaler):
    mat = np.array([data[col] for col in cols]).reshape(1, -1)
    scaled_mat = scaler.transform(mat)
    return {"features": scaled_mat}
