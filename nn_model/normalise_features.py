import numpy as np

# feature_cols = ['parameterCount', 'statementCount',
#                 'variableCount', 'maxNestingDepth']

# feature_cols_camel = ['parameter_count', 'statement_count',
#                       'variable_count', 'max_nesting_depth']


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
