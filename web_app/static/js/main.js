const navbarMenu = document.querySelector(".navbar .links");
const hamburgerBtn = document.querySelector(".hamburger-btn");
const hideMenuBtn = navbarMenu ? navbarMenu.querySelector(".close-btn") : null;

// Show/hide mobile menu
if (hamburgerBtn && navbarMenu) {
    hamburgerBtn.addEventListener("click", () => {
        navbarMenu.classList.toggle("show-menu");
    });
}
if (hideMenuBtn && hamburgerBtn) {
    hideMenuBtn.addEventListener("click", () => hamburgerBtn.click());
}

// Handle login popup if it exists
const formPopup = document.querySelector(".form-popup");
if (formPopup) {
    const loginForm = formPopup.querySelector("form");
    if (loginForm) {
        loginForm.addEventListener("submit", async function(e) {
            e.preventDefault();
            const identifier = loginForm.elements[0].value;
            const password = loginForm.elements[1].value;
            try {
                const res = await fetch("/login", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ identifier, password })
                });
                const data = await res.json();
                if (res.ok && data.success) {
                    // 🔄 Reload the page to refresh session-dependent content
                    window.location.reload();
                } else {
                    alert(data.detail || data.error || "Login failed.");
                }
            } catch (err) {
                alert("Network error.");
            }
        });
    }
}
