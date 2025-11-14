document.addEventListener("DOMContentLoaded", async () => {
    document.getElementById("create-company-form").addEventListener("submit", async (e) => {
        e.preventDefault();

        const payload = {
            company_name: document.getElementById("company_name").value,
            field: document.getElementById("field").value,
        };

        try {
            const res = await fetch("/companies/create", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });

            if (!res.ok) throw new Error("Failed to create company");

            const result = await res.json();

            if (result.success) {
                alert("New company was successfully created.")
            } else {
                alert("Failed: " + (result.message || "Unknown error"));
            }
            } catch (err) {
            console.error("Error creating company:", err);
            alert("Error creating company");
        }
    });
});

