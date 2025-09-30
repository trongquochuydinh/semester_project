document.querySelector('.btn.btn-primary').addEventListener('click', function() {
    const email = document.querySelector('input[type="email"]').value;
    const password = document.querySelector('input[type="password"]').value;

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ identifier: email, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            window.location.href = '/';
        } else {
            alert('Login failed: ' + (data.error || 'Invalid credentials'));
        }
    })
    .catch(err => {
        alert('Error: ' + err);
    });
});