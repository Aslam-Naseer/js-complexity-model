// A starting list of common browser and JS globals.

export const browserGlobals = new Set([
  // Globals from Browser
  'console', 'window', 'document', 'navigator', 'localStorage', 'sessionStorage',
  'alert', 'prompt', 'confirm', 'setTimeout', 'setInterval', 'clearInterval',
  'requestAnimationFrame', 'cancelAnimationFrame', 'fetch', 'Headers', 'Request', 'Response',

  // Built-in Types and Constructors
  'Object', 'Array', 'String', 'Number', 'Boolean', 'Function', 'Promise',
  'Map', 'Set', 'Symbol', 'Error', 'Date', 'RegExp', 'ArrayBuffer',

  // Other common globals
  'JSON', 'Math', 'Intl', 'undefined'
]);