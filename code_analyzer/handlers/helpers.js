import { browserGlobals } from "../environments.js";

// --- Helper Functions ---

export const addIdentifierReference = (node, parent, context) => {
  // rem
  const { scopeStack, symbolTable } = context;

  const symbol = symbolTable.findInScope(node.name, scopeStack);

  if (symbol) {
    symbol.references.push({ node, parent });
  } else if (!browserGlobals.has(node.name)) {
    const currentScope = scopeStack[scopeStack.length - 1];
    symbolTable.addUndeclared(node, currentScope);
  }
};

export const getDeclaredNames = (idNode) => {
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

export const isDeclarationOrProperty = (node, parent) => {
  // rem
  if (!parent) return false;

  // Rule 1: It's a property access, not a variable (e.g., the 'log' in console.log)
  if (
    parent.type === "MemberExpression" &&
    parent.property === node &&
    !parent.computed
  ) {
    return true;
  }

  // Rule 2: It's part of an import statement (handled by another function)
  if (parent.type.startsWith("Import")) {
    return true;
  }

  // Rule 3: It's a function parameter
  if (parent.type.includes("Function") && parent.params.includes(node)) {
    return true;
  }

  // Rule 4: It's the name of a function or variable being declared
  if (
    (parent.type === "VariableDeclarator" ||
      parent.type === "FunctionDeclaration") &&
    parent.id === node
  ) {
    return true;
  }

  return false;
};
