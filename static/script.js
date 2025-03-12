document.getElementById("priceForm").addEventListener("submit", function(event) {
    event.preventDefault();
    console.log('Form submitted');  // Debugging log

    // Fetch values from the form
    const productUrl = document.getElementById("url").value.trim(); // Trim whitespace from URL
    const targetPrice = document.getElementById("price").value.trim(); // Trim whitespace from price
    
    console.log('Product URL:', productUrl);  // Debugging log
    console.log('Target Price:', targetPrice);  // Debugging log

    // Validate the inputs
    if (!productUrl || !targetPrice || isNaN(targetPrice) || parseFloat(targetPrice) <= 0) {
        const alertMessage = document.getElementById('alertMessage');
        alertMessage.innerText = "Please provide a valid product URL and target price.";
        alertMessage.className = 'error'; // Apply error styling
        return; // Exit the function if validation fails
    }

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
