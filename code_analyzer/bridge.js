import codeAnalyzer from "./src/index.js";

const codeString = process.argv[2];

try {
  if (!codeString) throw Error("No Args");

  const result = codeAnalyzer(codeString);
  console.log(JSON.stringify(result));
} catch (e) {
  console.error(e);
  process.exit(1);
}
