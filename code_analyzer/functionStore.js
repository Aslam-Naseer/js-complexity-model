const getCodeSnippet = (lines, startLine, endLine) => {
  const codeLines = lines.slice(startLine, endLine);
  return codeLines.join("\n");
};

export class FunctionStore {
  constructor(code) {
    this.details = [];
    this.stack = [];
    this.lines = code.split("\n");
  }

  isGlobalScope = () => {
    return this.stack.length === 0;
  };

  getFunctionName = (node, parent) => {
    if (node.id) return node.id.name;
    if (parent && parent.type === "VariableDeclarator") {
      return parent.id.name;
    }
    if (node.loc && node.loc.start) {
      return `anonymous at L${node.loc.start.line}`;
    }
    return "anonymous";
  };

  getCurrentFunction = () => {
    if (this.isGlobalScope()) return null;

    return this.stack[this.stack.length - 1];
  };

  getFunctionDetails = () => {
    const formatter = (func) => {
      return {
        name: func.name,
        loc: func.source.loc,
        code: func.source.code,
        features: func.analysis.features,
        nestedFunctions: func.nestedFunctions.map(formatter),
      };
    };

    return this.details.map(formatter);
  };

  processFunctionNode = (node, parent) => {
    const newFunctionDetail = {
      name: this.getFunctionName(node, parent),

      source: {
        loc: { start: node.loc.start.line, end: node.loc.end.line },
        node: node,
        code: getCodeSnippet(
          this.lines,
          node.loc.start.line - 1,
          node.loc.end.line,
        ),
      },

      analysis: {
        features: {
          parameterCount: node.params.length,
          statementCount: 0,
          variableCount: 0,
          maxNestingDepth: 0,
        },
      },

      nestedFunctions: [],

      currentDepth: 0,
    };

    if (this.stack.length === 0) {
      this.details.push(newFunctionDetail);
    } else {
      const parentFunction = this.stack[this.stack.length - 1];
      parentFunction.nestedFunctions.push(newFunctionDetail);
    }

    this.stack.push(newFunctionDetail);
    return newFunctionDetail;
  };

  enterFunction = (node) => {
    const parentFunction = this.getCurrentFunction();

    const functionArrray = parentFunction
      ? parentFunction.nestedFunctions
      : this.details;

    const currentFunction = functionArrray.find(
      (func) => func.source.node === node,
    );
    this.stack.push(currentFunction);
  };

  exitFunction = (node) => {
    if (
      this.stack.length > 0 &&
      this.stack[this.stack.length - 1].source.node === node
    ) {
      this.stack.pop();
    }
  };
}
