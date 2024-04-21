

// Wait for the document to be fully loaded
    document.addEventListener('DOMContentLoaded', function () {
        // Find the carousel element by its ID
        var carousel = document.getElementById('testimonialCarousel');

        // Initialize the Bootstrap Carousel component
        var carouselInstance = new bootstrap.Carousel(carousel, {
            interval: 4500, // Set the interval for auto-sliding (in milliseconds), or false for no auto-sliding
            wrap: true, // Set to true to enable continuous loop of the carousel items
            keyboard: true // Set to true to enable keyboard navigation for the carousel
        });
    });

