document.getElementById("priceForm").addEventListener("submit", function(event) {
    event.preventDefault();

    // Fetch values from the form
    const productUrl = document.getElementById("url").value; // Corrected the id to match HTML
    const targetPrice = document.getElementById("price").value; // Corrected the id to match HTML

    // Send POST request to track price
    fetch('/track-price', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: productUrl, price: targetPrice }),
    })
    .then(response => response.json())
    .then(data => {
        const alertMessage = document.getElementById('alertMessage');
        alertMessage.innerText = data.message; // Display the response message
        if (data.success) {
            alertMessage.className = 'success'; // Apply success styling
        } else {
            alertMessage.className = 'error'; // Apply error styling
        }
    })
    .catch(error => {
        console.error("Error:", error);
        const alertMessage = document.getElementById('alertMessage');
        alertMessage.innerText = "Failed to track product.";
        alertMessage.className = 'error'; // Apply error styling
    });
});
