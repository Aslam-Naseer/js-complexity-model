import numpy as np

feature_cols = [
    'parameterCount',
    'statementCount',
    'variableCount',
    'maxNestingDepth'
]


def normalise_features(data, scaler):
    mat = np.array([data[col] for col in feature_cols]).reshape(1, -1)
    scaled_mat = scaler.transform(mat)
    return {"features": scaled_mat}
