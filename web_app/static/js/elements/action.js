export const ACTIONS = {};

export function registerAction(name, callback) {
  ACTIONS[name] = callback;
}

document.addEventListener("click", (e) => {
  const action = e.target.dataset.action;
  const id = e.target.dataset.id;
  if (action && ACTIONS[action]) {
    ACTIONS[action](id);
  }
});
