import copy
from code_analyzer import analyze


class FeatureExtractor():
    """
      Encapsulates analysis logic to ensure safe pickling 
      during multiprocessing.
    """

    def extract(self, js_code, show_logs=True):
        try:
            data = analyze(js_code)

            if not data or not isinstance(data, list):
                return None

            root_node = data[0]

            aggregated_stats = self._get_recursive_stats(root_node)
            local_feats = root_node.get('features') or {}

            return {
                'paramCount': local_feats.get('parameterCount', -1),
                'statementCount_local': local_feats.get('statementCount', -1),
                'statementCount_total': aggregated_stats['statementCount'],
                'variableCount_local': local_feats.get('variableCount', -1),
                'variableCount_total': aggregated_stats['variableCount'],
                'nestingDepth_local': local_feats.get('maxNestingDepth', -1),
                'nestingDepth_total': aggregated_stats['maxNestingDepth']
            }

        except Exception as e:
            if show_logs:
                print(f"Analyzer Error: {e}")
            return None

    def _get_recursive_stats(self, node):
        """Helper to get features in nested functions"""
        if not node:
            return {'statementCount': -1, 'variableCount': -1, 'maxNestingDepth': -1}

        features = node.get('features') or {}
        nested_funcs = node.get('nestedFunctions') or []

        total_statements = features.get('statementCount', -1)
        total_variables = features.get('variableCount', -1)
        max_depth = features.get('maxNestingDepth', -1)

        for child in nested_funcs:
            child_stats = self._get_recursive_stats(child)

            total_statements += child_stats['statementCount']
            total_variables += child_stats['variableCount']
            max_depth = max(max_depth, child_stats['maxNestingDepth'] + 1)

        return {
            'statementCount': total_statements,
            'variableCount': total_variables,
            'maxNestingDepth': max_depth
        }
