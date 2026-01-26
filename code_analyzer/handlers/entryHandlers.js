// Helpers

const getDeclaredNames = (idNode) => {
  if (!idNode) return [];

  if (idNode.type === "Identifier") return [idNode.name];

  if (idNode.type === "ObjectPattern") {
    return idNode.properties.flatMap((prop) => {
      if (prop.type === "RestElement") {
        return getDeclaredNames(prop.argument);
      }
      return getDeclaredNames(prop.value);
    });
  }

  if (idNode.type === "ArrayPattern") {
    return idNode.elements.flatMap((elem) => {
      if (!elem) return [];
      if (elem.type === "RestElement") {
        return getDeclaredNames(elem.argument);
      }
      return getDeclaredNames(elem);
    });
  }

  if (idNode.type === "RestElement") {
    return getDeclaredNames(idNode.argument);
  }

  return [];
};

// Handlers

export const enterFunctionNode = (node, context) => {
  const { functionStore, parent } = context;
  functionStore.processFunctionNode(node, parent);
};

export const enterScope = (node, context) => {
  const { scopeStack, parent } = context;

  if (parent && parent.type === "IfStatement" && parent.alternate === node) {
    scopeStack.pop();
  }
  scopeStack.push(node);
};

export const addFunctionDeclarator = (node, context) => {
  const { functionStore, parent } = context;

  const name = functionStore.getFunctionName(node, context);
  if (name.startsWith("anonymous")) return;

  const isFunctionExpression =
    node.type === "ArrowFunctionExpression" ||
    node.type === "FunctionExpression";

  let declarationNode = node;
  if (isFunctionExpression && parent && parent.type === "VariableDeclarator") {
    declarationNode = parent;
  }
};

export const processVariableDeclarator = (node, context) => {
  const { functionStore } = context;

  if (
    node.init &&
    (node.init.type === "ArrowFunctionExpression" ||
      node.init.type === "FunctionExpression")
  ) {
    return;
  }

  const currentFunction = functionStore.getCurrentFunction();

  const declaredNames = getDeclaredNames(node.id);
  if (currentFunction)
    currentFunction.analysis.features.variableCount += declaredNames.length;
};

export const incrementNestingDepth = (node, context) => {
  const { functionStore, parent } = context;

  if (functionStore.isGlobalScope()) return;
  if (parent && parent.type === "IfStatement" && parent.alternate === node)
    return;

  const currentFunction = functionStore.getCurrentFunction();
  currentFunction.currentDepth++;

  currentFunction.analysis.features.maxNestingDepth = Math.max(
    currentFunction.analysis.features.maxNestingDepth,
    currentFunction.currentDepth,
  );
};

export const incrementStatementCount = (node, context) => {
  const { functionStore, parent } = context;

  if (functionStore.isGlobalScope() || !parent) return;
  if (node.type === "VariableDeclaration" && parent.type.startsWith("For"))
    return;

  const currentFunction = functionStore.getCurrentFunction();
  currentFunction.analysis.features.statementCount++;
};
