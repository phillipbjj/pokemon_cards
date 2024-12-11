// Function to handle button click and navigate to a new page
function navigateTo(url) {
    window.location.href = url;
}

// Add event listeners to buttons
document.addEventListener('DOMContentLoaded', function () {
    const loginRegisterButton = document.getElementById('loginRegisterButton');
    const homeButton = document.getElementById('homeButton');
    const cardsButton = document.getElementById('cardsButton');

    if (homeButton) {
        homeButton.addEventListener('click', function() {
            navigateTo('/');
        });
    }

    if (cardsButton) {
        cardsButton.addEventListener('click', function() {
            navigateTo('/cards');
        });
    }

    if (loginRegisterButton) {
        loginRegisterButton.addEventListener('click', function() {
            navigateTo('/users/register');
        });
    }
 
});

