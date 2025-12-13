export function t(key) {
  if (!window._translations) {
    const element = document.getElementById("js-translations");
    window._translations = JSON.parse(element.textContent);
  }
  return window._translations[key] || key;
}
