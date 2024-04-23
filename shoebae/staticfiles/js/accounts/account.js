document.getElementById('open-delete-payment-popup').addEventListener('click', function() {
    console.log("Open delete payment popup");
    document.getElementById('delete-payment-popup').style.display = 'block';
});

document.getElementById('close-delete-payment-popup').addEventListener('click', function() {
    console.log("Close delete payment popup");
    document.getElementById('delete-payment-popup').style.display = 'none';
});

document.getElementById('open-edit-payment-popup').addEventListener('click', function() {
    console.log("Open edit payment popup");
    document.getElementById('edit-payment-popup').style.display = 'block';
});

document.getElementById('close-edit-payment-popup').addEventListener('click', function() {
    console.log("Close edit payment Clicked");
    document.getElementById('edit-payment-popup').style.display = 'none';
});

document.getElementById('open-add-payment-popup').addEventListener('click', function() {
    console.log("Open add paymet clicked");
    document.getElementById('add-payment-popup').style.display = 'block';
});

document.getElementById('close-add-payment-popup').addEventListener('click', function() {
    console.log("Close add payment popup");
    document.getElementById('add-payment-popup').style.display = 'none';
});

document.addEventListener('DOMContentLoaded', function () {
    const paymentPrevBtn = document.getElementById('payment-prev-btn');
    const paymentNextBtn = document.getElementById('payment-next-btn');
    const cardsPayment = document.getElementById('payment-cards').querySelectorAll('.card');

    let currentIndex = 0;

    paymentPrevBtn.addEventListener('click', () => {
        cardsPayment[currentIndex].classList.remove('active'); // Hide current active card
        currentIndex = (currentIndex - 1 + cardsPayment.length) % cardsPayment.length; // Update index
        cardsPayment[currentIndex].classList.add('active'); // Show new active card
    });

    paymentNextBtn.addEventListener('click', () => {
        cardsPayment[currentIndex].classList.remove('active'); // Hide current active card
        currentIndex = (currentIndex + 1) % cardsPayment.length; // Update index
        cardsPayment[currentIndex].classList.add('active'); // Show new active card
    });
});

document.getElementById('open-edit-shipping-popup').addEventListener('click', function() {
    console.log("Open edit shipping popup");
    document.getElementById('edit-shipping-popup').style.display = 'block';
});

document.getElementById('close-edit-shipping-popup').addEventListener('click', function() {
    console.log("Close edit shipping Clicked");
    document.getElementById('edit-shipping-popup').style.display = 'none';
});

document.getElementById('open-delete-shipping-popup').addEventListener('click', function() {
    console.log("Open delete shipping popup");
    document.getElementById('delete-shipping-popup').style.display = 'block';
});

document.getElementById('close-shipping-payment-popup').addEventListener('click', function() {
    console.log("Close delete shipping popup");
    document.getElementById('delete-shipping-popup').style.display = 'none';
});

document.getElementById('open-add-shipping-popup').addEventListener('click', function() {
    console.log("Open add shipping clicked");
    document.getElementById('add-shipping-popup').style.display = 'block';
});

document.getElementById('close-add-shipping-popup').addEventListener('click', function() {
    console.log("Close add shipping popup");
    document.getElementById('add-shipping-popup').style.display = 'none';
});

document.addEventListener('DOMContentLoaded', function () {
    const shippingPrevBtn = document.getElementById('shipping-prev-btn');
    const shippingNextBtn = document.getElementById('shipping-next-btn');
    const cardsShipping = document.getElementById('shipping-cards').querySelectorAll('.card');

    let currentIndex = 0;

    shippingPrevBtn.addEventListener('click', () => {
        cardsShipping[currentIndex].classList.remove('active'); // Hide current active card
        currentIndex = (currentIndex - 1 + cardsShipping.length) % cardsShipping.length; // Update index
        cardsShipping[currentIndex].classList.add('active'); // Show new active card
    });

    shippingNextBtn.addEventListener('click', () => {
        cardsShipping[currentIndex].classList.remove('active'); // Hide current active card
        currentIndex = (currentIndex + 1) % cardsShipping.length; // Update index
        cardsShipping[currentIndex].classList.add('active'); // Show new active card
    });
});