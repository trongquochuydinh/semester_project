export function t(key) {
  if (!window._translations) {
    const element = document.getElementById("js-translations");
    window._translations = JSON.parse(element.textContent);
  }
  return window._translations[key] || key;
}

export async function apiFetch(url, options = {}) {
  const res = await fetch(url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      "X-Requested-With": "XMLHttpRequest"
    }
  });

  if (res.status === 401) {
    // session expired → redirect to login
    window.location.href = "/";
    throw new Error("Session expired");
  }

  if (!res.ok) {
    let error = "API error";
    try {
      const data = await res.json();
      error = data.error || error;
    } catch (_) {}
    throw new Error(error);
  }

  return res.json();
}
