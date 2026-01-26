import { parse } from "acorn";
import { entryHandlerMap, exitHandlerMap } from "./astVisitors.js";
import { SymbolTable } from "../structures/symbolTable.js"; // rem
import { FunctionStore } from "./functionStore.js";

const traverse = (node, context) => {
  if (!node || !node.type) return;

  let handlers = entryHandlerMap.get(node.type) || [];
  for (const handler of handlers) {
    handler(node, context);
  }

  for (const key in node) {
    if (key === "parent" || key === "loc") continue;

    if (node[key] && typeof node[key] === "object") {
      const children = Array.isArray(node[key]) ? node[key] : [node[key]];
      for (const child of children) {
        traverse(child, { ...context, parent: node });
      }
    }
  }

  handlers = exitHandlerMap.get(node.type) || [];
  for (const handler of handlers) {
    handler(node, context);
  }
};

const codeAnalyzer = (code) => {
  const ast = parse(code, {
    ecmaVersion: "latest",
    sourceType: "module",
    locations: true,
  });

  const functionStore = new FunctionStore(code);
  const symbolTable = new SymbolTable(); // rem

  const initialContext = {
    functionStore,
    symbolTable, // rem
    code,
    nestingDepth: 0,
    parent: null,
    scopeStack: [ast],
  };

  traverse(ast, initialContext);
  return { ast, functionStore, symbolTable, code }; // rem---
};

export default codeAnalyzer;
