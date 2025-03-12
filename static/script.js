document.getElementById("price-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const productUrl = document.getElementById("product-url").value;
    const targetPrice = document.getElementById("target-price").value;

    fetch('/track-price', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url: productUrl, price: targetPrice }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Product is now being tracked!");
        } else {
            alert("Failed to track product.");
        }
    })
    .catch(error => {
        console.error("Error:", error);
        alert("Failed to track product.");
    });
});
