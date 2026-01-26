export const exitFunctionNode = (node, context) => {
  const { functionStore } = context;
  functionStore.exitFunction(node);
};

export const exitScope = (node, context) => {
  const { scopeStack } = context;

  if (scopeStack.length > 0 && scopeStack[scopeStack.length - 1] === node) {
    scopeStack.pop();
  }
};

export const decrementNestingDepth = (node, context) => {
  const { functionStore, parent } = context;

  if (functionStore.isGlobalScope || !parent) return;
  if (parent.type === "IfStatement" && parent.alternate === node) return;

  const currentFunction = functionStore.getCurrentFunction();
  currentFunction.currentDepth--;
};
