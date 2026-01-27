import numpy as np

feature_cols = ['parameterCount', 'statementCount',
                'variableCount', 'maxNestingDepth']

feature_cols_camel = ['parameter_count', 'statement_count',
                      'variable_count', 'max_nesting_depth']


def normalise_features(data, scaler, use_camel_case=False):
    if use_camel_case:
        cols = feature_cols_camel
    else:
        cols = feature_cols

    mat = np.array([data[col] for col in cols]).reshape(1, -1)
    scaled_mat = scaler.transform(mat)
    return {"features": scaled_mat}
