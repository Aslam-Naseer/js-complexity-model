const func = (msg) => {
  console.log(msg);
  return;
};

const args = process.argv[2] || "No args";

try {
  func(args);
} catch (e) {
  console.log;
}
