import { HandlerMap } from "./handlerMap.js";
import * as entryHandlers from "./handlers/entryHandlers.js";
import * as exitHandlers from "./handlers/exitHandlers.js";
import {
  FUNCTION_NODES,
  NESTING_NODES,
  STATEMENT_NODES,
} from "./node-types.js";

// --- Map Creation ---
const entryHandlerMap = new HandlerMap();
const exitHandlerMap = new HandlerMap();

// --- Build the Maps ---
entryHandlerMap.addHandlers(FUNCTION_NODES, [
  entryHandlers.addFunctionDeclarator,
  entryHandlers.enterFunctionNode,
  entryHandlers.enterScope,
]);
entryHandlerMap.addHandlers(NESTING_NODES, [
  entryHandlers.incrementNestingDepth,
  entryHandlers.enterScope,
]);
entryHandlerMap.addHandlers(STATEMENT_NODES, [
  entryHandlers.incrementStatementCount,
]);

entryHandlerMap.addHandlers(
  ["VariableDeclarator"],
  [entryHandlers.processVariableDeclarator],
);

entryHandlerMap.addHandlers(["BlockStatement"], [entryHandlers.enterScope]);

exitHandlerMap.addHandlers(FUNCTION_NODES, [
  exitHandlers.exitFunctionNode,
  exitHandlers.exitScope,
]);
exitHandlerMap.addHandlers(NESTING_NODES, [
  exitHandlers.decrementNestingDepth,
  exitHandlers.exitScope,
]);

exitHandlerMap.addHandlers(["BlockStatement"], [exitHandlers.exitScope]);

// --- Export the Maps ---
export { entryHandlerMap, exitHandlerMap };
