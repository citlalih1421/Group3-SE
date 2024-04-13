document.addEventListener('DOMContentLoaded', function () {
    const accordionBtns = document.querySelectorAll('.accordion-btn');

    accordionBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            const content = this.nextElementSibling;
            content.classList.toggle('active');

            // Collapse other accordions
            accordionBtns.forEach(acc => {
                if (acc !== this) {
                    acc.nextElementSibling.classList.remove('active');
                }
            });
        });
    });

    const filterButtons = document.querySelectorAll('.filter-btn');
    const products = document.querySelectorAll('.product');

    filterButtons.forEach(button => {
        button.addEventListener('click', function () {
            // Toggle active class on clicked button
            this.classList.toggle('active');

            const filterValue = this.getAttribute('data-filter');

            products.forEach(product => {
                // Show all products if filter is 'all' or if product has the selected filter class
                if (filterValue === 'all' || product.classList.contains(filterValue)) {
                    product.classList.add('show');
                } else {
                    product.classList.remove('show');
                }
            });
        });
    });
});
