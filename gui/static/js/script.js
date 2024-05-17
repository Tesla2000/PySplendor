document.addEventListener('DOMContentLoaded', function() {
    // Add click event listener to all images
    document.querySelectorAll('img').forEach(function(image) {
        image.addEventListener('click', function() {
            var imageClass = this.className;
            sendImageClass(imageClass);
        });
    });
});

function sendImageClass(imageClass) {
    fetch('/click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ class: imageClass }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
