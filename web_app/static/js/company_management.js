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

            const result = await res.json();

            if (res.ok) {
                alert(result.message || "Company created successfully!");
            } else {
                alert("Failed: " + (result.error || result.message || "Unknown error"));
            }

        } catch (err) {
            console.error("Error creating company:", err);
            alert("Error creating company");
        }
    });
});
