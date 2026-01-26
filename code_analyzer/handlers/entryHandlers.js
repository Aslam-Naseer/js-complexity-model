import { STRUCTURAL_PARENTS } from "../node-types.js";
import {
  addIdentifierReference,
  getDeclaredNames,
  isDeclarationOrProperty,
} from "./helpers.js";

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
  const { scopeStack, functionStore, parent } = context;

  const name = functionStore.getFunctionName(node, context);
  if (name.startsWith("anonymous")) return;

  const isFunctionExpression =
    node.type === "ArrowFunctionExpression" ||
    node.type === "FunctionExpression";

  let declarationNode = node;
  if (isFunctionExpression && parent && parent.type === "VariableDeclarator") {
    declarationNode = parent;
  }

  const currentScope =
    scopeStack.length !== 0 ? scopeStack[scopeStack.length - 1] : null;
  const currentFunction = functionStore.getCurrentFunction();

  const symtabData = { node: declarationNode, currentScope, currentFunction }; // rem
  symbolTable.add(name, "function", symtabData);
};

export const addFunctionParams = (node, context) => {
  const { symbolTable, scopeStack, functionStore } = context; // rem

  const currentScope =
    scopeStack.length !== 0 ? scopeStack[scopeStack.length - 1] : null;
  const currentFunction = functionStore.getCurrentFunction();

  for (const param of node.params) {
    // rem
    const paramNames = getDeclaredNames(param);
    const symtabData = { node: param, currentScope, currentFunction };

    for (const name of paramNames) {
      symbolTable.add(name, "param", symtabData);
    }
  }
};

export const processVariableDeclarator = (node, context) => {
  const { functionStore, scopeStack, symbolTable, parent } = context;

  if (
    node.init &&
    (node.init.type === "ArrowFunctionExpression" ||
      node.init.type === "FunctionExpression")
  ) {
    return;
  }

  const currentScope =
    scopeStack.length !== 0 ? scopeStack[scopeStack.length - 1] : null;
  const currentFunction = functionStore.getCurrentFunction();

  const declaredNames = getDeclaredNames(node.id);
  if (currentFunction)
    currentFunction.analysis.features.variableCount += declaredNames.length;

  for (const name of declaredNames) {
    // rem
    const symtabData = { node, currentScope, currentFunction };
    symbolTable.add(name, parent.kind, symtabData);
  }
};

export const processImportDeclaration = (node, context) => {
  // rem
  const { symbolTable, scopeStack } = context;
  const currentScope = scopeStack[scopeStack.length - 1];

  for (const specifier of node.specifiers) {
    const name = specifier.local.name;

    if (name) {
      const symtabData = {
        node: specifier,
        currentScope,
        currentFunction: null,
      };
      symbolTable.add(name, "import", symtabData);
    }
  }
};

export const processIdentifier = (node, context) => {
  // rem
  const { parent } = context;

  if (
    isDeclarationOrProperty(node, parent) ||
    STRUCTURAL_PARENTS.includes(parent.type)
  ) {
    return;
  }

  addIdentifierReference(node, parent, context);
};

export const processObjectExpression = (node, context) => {
  // rem
  for (const prop of node.properties) {
    if (prop.type === "Property") {
      if (prop.value.type === "Identifier") {
        addIdentifierReference(prop.value, prop, context);
      }
    } else if (prop.type === "SpreadElement") {
      if (prop.argument.type === "Identifier") {
        addIdentifierReference(prop.argument, prop, context);
      }
    }
  }
};

export const processArrayExpression = (node, context) => {
  // rem
  for (const element of node.elements) {
    if (!element) continue;

    if (element.type === "Identifier") {
      addIdentifierReference(element, node, context);
    } else if (element.type === "SpreadElement") {
      if (element.argument.type === "Identifier") {
        addIdentifierReference(element.argument, element, context);
      }
    }
  }
};

export const processSpreadElement = (node, context) => {
  // rem
  const { parent } = context;

  if (["CallExpression", "NewExpression"].includes(parent.type)) {
    if (node.argument.type === "Identifier") {
      addIdentifierReference(node.argument, node, context);
    }
  }
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
