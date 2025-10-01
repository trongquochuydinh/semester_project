function createButton({ id, text, classes, onClick }) {
    const button = document.createElement("button");
    button.id = id;
    button.className = classes;
    button.textContent = text;

    if (onClick && typeof onClick === "function") {
    button.addEventListener("click", onClick);
    }

    return button;
}