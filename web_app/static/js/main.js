const navbarMenu = document.querySelector(".navbar .links");
const hamburgerBtn = document.querySelector(".hamburger-btn");
const hideMenuBtn = navbarMenu.querySelector(".close-btn");
const formPopup = document.querySelector(".form-popup");
// Show mobile menu
hamburgerBtn.addEventListener("click", () => {
    navbarMenu.classList.toggle("show-menu");
});
// Hide mobile menu
hideMenuBtn.addEventListener("click", () =>  hamburgerBtn.click());
// By default, show login
formPopup.querySelector('.form-box.login').style.display = 'flex';

// Handle login form submission
const loginForm = document.querySelector('.form-box.login form');
loginForm.addEventListener('submit', async function(e) {
    e.preventDefault();
    const identifier = loginForm.elements[0].value; // can be username or email
    const password = loginForm.elements[1].value; // password field
    try {
        const res = await fetch('/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ identifier, password })
        });
        const data = await res.json();
        if (res.ok && data.success) {
            // Hide login form and popup
            formPopup.querySelector('.form-box.login').style.display = 'none';
            document.body.classList.remove('show-popup');
            // Optionally, show user info or redirect
        } else {
            alert(data.detail || data.error || 'Login failed.');
        }
    } catch (err) {
        alert('Network error.');
    }
});