from code_analyzer import analyze


def _get_recursive_stats(node):
    """Helper to get features in nested functions"""
    if not node:
        return {'statementCount': -1, 'variableCount': -1, 'maxNestingDepth': -1}

    features = node.get('features') or {}
    nested_funcs = node.get('nestedFunctions') or []

    total_statements = features.get('statementCount', -1)
    total_variables = features.get('variableCount', -1)
    max_depth = features.get('maxNestingDepth', -1)

    for child in nested_funcs:
        child_stats = _get_recursive_stats(child)

        total_statements += child_stats['statementCount']
        total_variables += child_stats['variableCount']
        max_depth = max(max_depth, child_stats['maxNestingDepth'] + 1)

    return {
        'statementCount': total_statements,
        'variableCount': total_variables,
        'maxNestingDepth': max_depth
    }


def extract_full_features(node):
    try:
        aggregated_stats = _get_recursive_stats(node)
        local_feats = node.get('features') or {}

        return {
            'param_count': local_feats.get('parameterCount', -1),
            'local_statement_count': local_feats.get('statementCount', -1),
            'total_statement_count': aggregated_stats['statementCount'],
            'local_variable_count': local_feats.get('variableCount', -1),
            'total_variable_count': aggregated_stats['variableCount'],
            'local_nesting_depth': local_feats.get('maxNestingDepth', -1),
            'total_nesting_depth': aggregated_stats['maxNestingDepth']
        }

    except Exception as e:
        print(f"Analyzer Error: {e}")
        return None
