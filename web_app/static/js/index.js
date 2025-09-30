// Hide logout link
document.getElementById('logout-link').addEventListener('click', function(e) {
  e.preventDefault();
  fetch('/logout', { method: 'GET' })
    .then(() => window.location.href = '/')
    .catch(() => window.location.href = '/');
});