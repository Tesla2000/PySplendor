document.addEventListener('DOMContentLoaded', function() {
    // Add click event listener to all images
    document.querySelectorAll('img').forEach(function(image) {
        image.addEventListener('click', function(event) {
            var imageClass = this.className;
            var clickType = event.button === 0 ? 'left' : 'unknown'; // 0 indicates a left click
            sendImageClass(imageClass, clickType);
        });

        image.addEventListener('contextmenu', function(event) {
            event.preventDefault(); // Prevent the context menu from appearing
            var imageClass = this.className;
            var clickType = 'right';
            sendImageClass(imageClass, clickType);
        });
    });
});

function sendImageClass(imageClass, clickType) {
    fetch('/click', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ class: imageClass, clickType: clickType }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
