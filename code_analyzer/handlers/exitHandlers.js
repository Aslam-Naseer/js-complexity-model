import { addIdentifierReference, getDeclaredNames } from "./helpers.js";

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

// rem
export const addExportReference = (node, context) => {
  if (node.type !== "ExportNamedDeclaration") return;

  const { declaration } = node;

  // --- Case 1: export const/let/var ---
  if (declaration?.type === "VariableDeclaration") {
    for (const declarator of declaration.declarations) {
      const names = getDeclaredNames(declarator.id);
      for (const name of names) {
        addIdentifierReference({ type: "Identifier", name }, node, context);
      }
    }
  }

  // --- Case 2: export function foo() {}, export class Bar {} ---
  else if (
    declaration &&
    (declaration.type === "FunctionDeclaration" ||
      declaration.type === "ClassDeclaration")
  ) {
    if (declaration.id) {
      addIdentifierReference(declaration.id, node, context);
    }
  }
};
