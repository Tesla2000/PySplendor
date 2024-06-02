document.addEventListener('DOMContentLoaded', function () {
    // Add click event listener to all images
    document.querySelectorAll('.chips .chip img').forEach(function (image) {
        image.addEventListener('click', function (event) {
            var imageClass = this.className;
            var clickType = event.button === 0 ? 'left' : 'unknown'; // 0 indicates a left click
            sendImageClass(imageClass, clickType);
        });

        image.addEventListener('contextmenu', function (event) {
            event.preventDefault(); // Prevent the context menu from appearing
            var imageClass = this.className;
            var clickType = 'right';
            sendImageClass(imageClass, clickType);
        });
    });
});
if (parseInt(document.querySelector('.total-points').textContent, 10) >= 15)
    showWinOverlay()

if (parseInt(document.querySelector('.si-total-points').textContent, 10) >= 15)
    showLossOverlay()
function sendImageClass(imageClass, clickType) {
    fetch('/click_resource', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({class: imageClass, clickType: clickType}),
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                updateChipCount(imageClass, clickType);
                if (data.turn_finished) {
                    showTurnFinishedOverlay();
                    location.reload()
                }
            }
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

function updateChipCount(imageClass, clickType) {
    const chipElement = document.querySelector(`.${imageClass}`).closest('.chip');
    const chipCountElement = chipElement.querySelector('.chip-count');
    const resourceType = imageClass.split("_")[1]
    const chipElementPlayer = document.querySelector(`.${resourceType}_resource_player`).closest('.player-chip');
    const chipCountElementPlayer = chipElementPlayer.querySelector('.player-chip-count');

    let currentCount = parseInt(chipCountElement.textContent, 10);
    let currentPlayerCount = chipCountElementPlayer.textContent

    if (clickType === 'left') {
        currentCount -= 1;
        currentPlayerCount += " + 1";
    } else if (clickType === 'right') {
        currentCount += 1;
        currentPlayerCount = currentPlayerCount.split(" ")[0]
    }

    chipCountElement.textContent = currentCount;
    chipCountElementPlayer.textContent = currentPlayerCount;
}


function openModal(card) {

    var cardId = card.dataset.id;
    // Get the img element inside the card
    var cardImage = card.querySelector('img');
    var cardImageSrc = cardImage ? cardImage.src : '';

    // Get card information from data attributes
    var cardPoints = card.dataset.points;
    var cardWhite = card.dataset.white;
    var cardGreen = card.dataset.green;
    var cardBlue = card.dataset.blue;
    var cardBlack = card.dataset.black;
    var cardRed = card.dataset.red;
    var cardProduction = card.dataset.production;
    var cardTier = card.dataset.tier;

    // Set the modal content
    document.getElementById('modal-card-image').src = cardImageSrc;
    document.getElementById('modal-card-points').textContent = cardPoints;
    // Set costs, hiding those with a value of 0
    setCost('modal-card-cost-white', cardWhite);
    setCost('modal-card-cost-green', cardGreen);
    setCost('modal-card-cost-blue', cardBlue);
    setCost('modal-card-cost-black', cardBlack);
    setCost('modal-card-cost-red', cardRed);

    setCost('modal-card-production', cardProduction)
    setCost('modal-card-tier', cardTier)

    document.getElementById('cardModal').dataset.cardId = cardId;
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
window.onclick = function (event) {
    var modal = document.getElementById('cardModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}


// RESERVED CARD MODAL - pewnie to mozna zrobic lepiej


function openReservedModal(card) {

    // Get card information from data attributes
    var cardId = card.dataset.id;
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

    document.getElementById('reservedCardModal').dataset.cardId = cardId;
    // Display the modal
    document.getElementById('reservedCardModal').style.display = 'block';
}

function closeReservedModal() {
    document.getElementById('reservedCardModal').style.display = 'none';
}

// Close the modal when clicking outside of it
window.onclick = function (event) {
    var modal = document.getElementById('reservedCardModal');
    if (event.target == modal) {
        modal.style.display = 'none';
    }
}

function showTurnFinishedOverlay() {
    var overlay = document.getElementById('turnOverlay');
    overlay.style.display = 'flex';

    setTimeout(function () {
        overlay.style.display = 'none';
    }, 3000);
}

function showNotEnoughResourcesOverlay() {
    const overlay = document.getElementById('notEnoughOverlay');
    overlay.style.display = 'flex';

    setTimeout(function () {
        overlay.style.display = 'none';
    }, 3000);
}

function showWinOverlay() {
    const overlay = document.getElementById('winOverlay');
    overlay.style.display = 'flex';
}

function showLossOverlay() {
    const overlay = document.getElementById('lossOverlay');
    overlay.style.display = 'flex';
}

function buyCard() {
    var cardId = document.getElementById('cardModal').dataset.cardId;
    sendCardAction(cardId, 'buy');
}

function reserveCard() {
    var cardId = document.getElementById('cardModal').dataset.cardId;
    sendCardAction(cardId, 'reserve');
}

function buyReservedCard() {
    var cardId = document.getElementById('reservedCardModal').dataset.cardId;
    sendCardAction(cardId, 'buy');
}

function sendCardAction(cardId, action) {
    fetch('/click_card', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ card_id: cardId, action: action }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            closeModal();
            closeReservedModal();
            showTurnFinishedOverlay();
            location.reload()
        } else {
            showNotEnoughResourcesOverlay()
        }
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}
