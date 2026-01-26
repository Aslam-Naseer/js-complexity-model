export class HandlerMap {
  constructor() {
    this.handlers = new Map();
  }

  addHandlers = (types, handlersToAdd) => {
    for (const handler of handlersToAdd) {
      if (typeof handler !== "function") {
        throw new TypeError(
          `Invalid handler provided for types [${types.join(
            ", "
          )}]. Expected a function but received ${typeof handler}.`
        );
      }
    }

    for (const type of types) {
      const existing = this.handlers.get(type) || [];
      this.handlers.set(type, [...existing, ...handlersToAdd]);
    }
  };

  get = (type) => {
    return this.handlers.get(type) || [];
  };

  entries = () => {
    return this.handlers.entries();
  };
}
