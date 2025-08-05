document.addEventListener("DOMContentLoaded", () => {
    const moveInput = document.getElementById("moveInput");

    moveInput.addEventListener("input", () => {
        const move = moveInput.value;

        fetch("/validate_move", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ move })
        })
        .then(res => res.json())
        .then(data => {
            // Change only border color so original style stays
            if (move.length > 0) {
                moveInput.style.borderColor = data.valid ? "green" : "red";
            } else {
                moveInput.style.borderColor = ""; // reset to default
            }
        })
        .catch(err => console.error("Validation error:", err));
    });
});
