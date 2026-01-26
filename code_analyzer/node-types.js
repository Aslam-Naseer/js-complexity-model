export const FUNCTION_NODES = [
  "FunctionDeclaration",
  "ArrowFunctionExpression",
  "FunctionExpression",
];

export const NESTING_NODES = [
  "ForStatement", "ForOfStatement", "ForInStatement", "IfStatement",
  "WhileStatement", "DoWhileStatement", "SwitchStatement",
];

export const STATEMENT_NODES = [
  "ExpressionStatement", "VariableDeclaration", "ReturnStatement", "IfStatement",
  "ForStatement", "ForOfStatement", "ForInStatement", "WhileStatement",
  "DoWhileStatement", "SwitchStatement", "BreakStatement", "ContinueStatement",
  "ThrowStatement", "TryStatement",
];

export const LEXICAL_SCOPE_NODES = [
  "FunctionDeclaration", "ArrowFunctionExpression", "FunctionExpression",
  "ForStatement", "ForOfStatement", "ForInStatement", "IfStatement",
  "WhileStatement", "DoWhileStatement", "SwitchStatement", "BlockStatement",
];

export const LOOP_NODES = [
  "ForStatement", "WhileStatement", "DoWhileStatement",
  "ForOfStatement", "ForInStatement",
];

export const JUMP_STATEMENTS = [
  "ReturnStatement", "ThrowStatement", "BreakStatement", "ContinueStatement",
];

export const STRUCTURAL_PARENTS = [
  "ObjectExpression", "ObjectPattern", "ArrayExpression",
  "ArrayPattern", "Property", "RestElement", "SpreadElement",
];