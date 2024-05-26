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


function openModal(card) {

    // Get card information from data attributes
    var cardImageSrc = card.style.backgroundImage.slice(5, -2);
    var cardPoints = card.dataset.points;
    var cardWhite = card.dataset.white;
    var cardGreen = card.dataset.green;
    var cardBlue = card.dataset.blue;
    var cardBlack = card.dataset.black;
    var cardRed = card.dataset.red;
    var cardProduction = card.dataset.production;

    // Set the modal content
    document.getElementById('modal-card-image').src = cardImageSrc;
    document.getElementById('modal-card-points').textContent = cardPoints;
    // Set costs, hiding those with a value of 0
    setCost('modal-card-cost-white', cardWhite);
    setCost('modal-card-cost-green', cardGreen);
    setCost('modal-card-cost-blue', cardBlue);
    setCost('modal-card-cost-black', cardBlack);
    setCost('modal-card-cost-red', cardRed);

    // Display the modal
    document.getElementById('cardModal').style.display = 'block';
}

function setCost(elementId, value) {
    var element = document.getElementById(elementId);
    if (value && value != '0') {
        element.textContent = value;
        element.style.display = 'inline-block';
    } else {
        element.style.display = 'none';
    }
}

function closeModal() {
    document.getElementById('cardModal').style.display = 'none';
}

// Close the modal when clicking outside of it
window.onclick = function(event) {
    var modal = document.getElementById('cardModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}


// RESERVED CARD MODAL - pewnie to mozna zrobic lepiej


function openReservedModal(card) {

    // Get card information from data attributes
    var cardImageSrc = card.style.backgroundImage.slice(5, -2);
    var cardPoints = card.dataset.points;
    var cardWhite = card.dataset.white;
    var cardGreen = card.dataset.green;
    var cardBlue = card.dataset.blue;
    var cardBlack = card.dataset.black;
    var cardRed = card.dataset.red;

    // Set the modal content
    document.getElementById('modal-r-card-image').src = cardImageSrc;
    document.getElementById('modal-r-card-points').textContent = cardPoints;
    // Set costs, hiding those with a value of 0
    setCost('modal-r-card-cost-white', cardWhite);
    setCost('modal-r-card-cost-green', cardGreen);
    setCost('modal-r-card-cost-blue', cardBlue);
    setCost('modal-r-card-cost-black', cardBlack);
    setCost('modal-r-card-cost-red', cardRed);

    // Display the modal
    document.getElementById('reservedCardModal').style.display = 'block';
}

function closeReservedModal() {
    document.getElementById('reservedCardModal').style.display = 'none';
}

// Close the modal when clicking outside of it
window.onclick = function(event) {
    var modal = document.getElementById('reservedCardModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

