const getCodeSnippet = (lines, startLine, endLine) => {
  const codeLines = lines.slice(startLine, endLine);
  return codeLines.join("\n");
};

export class FunctionStore {
  constructor(code) {
    this.details = [];
    this.stack = [];
    this.lines = code.split("\n");
    this.idCountMap = new Map();
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

  generateId = (node, parent) => {
    // rem
    let name = this.getFunctionName(node, parent);
    if (name.startsWith("anonymous")) {
      name = "anonymous";
    }
    const params =
      node.params?.map((p) => {
        if (p.type === "Identifier") return p.name;
        if (p.type === "AssignmentPattern" && p.left.type === "Identifier")
          return `${p.left.name}=default`;
        if (p.type === "RestElement" && p.argument.type === "Identifier")
          return `...${p.argument.name}`;
        return "param";
      }) || [];

    const scopeNames = this.stack.map((fn) => fn.name).join("::");
    const signature = `${
      scopeNames ? scopeNames + "::" : ""
    }${name}(${params.join(",")})`;

    let hash = 0;
    for (let i = 0; i < signature.length; i++) {
      hash = (hash * 31 + signature.charCodeAt(i)) >>> 0;
    }

    const baseId = `${name}_${hash.toString(36)}`;
    const count = this.idCountMap.get(baseId) || 0;
    this.idCountMap.set(baseId, count + 1);

    if (count > 0) {
      return `${baseId}${count + 1}`;
    }

    return baseId;
  };

  getCurrentFunction = () => {
    if (this.isGlobalScope()) return null;

    return this.stack[this.stack.length - 1];
  };

  getFunctionDetailsForAPI = () => {
    const formatter = (func) => {
      func.lintIssues.sort(
        (a, b) => a.range.startLineNumber - b.range.startLineNumber,
      );

      return {
        id: func.id, // rem
        name: func.name,
        loc: func.source.loc,
        code: func.source.code,

        analysis: {
          prediction: null,
          features: func.analysis.features,
        },

        lintIssues: func.lintIssues,
        suggestion: null,

        nestedFunctions: func.nestedFunctions.map(formatter),
      };
    };

    return this.details.map(formatter);
  };

  processFunctionNode = (node, parent) => {
    const newFunctionDetail = {
      name: this.getFunctionName(node, parent),
      id: this.generateId(node, parent),

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

      lintIssues: [], // rem
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
