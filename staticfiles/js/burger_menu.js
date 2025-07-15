document.addEventListener('DOMContentLoaded', function() {
    const menuButton = document.getElementById('menu-button');
    const dropdownMenu = document.getElementById('dropdown-menu');
    const burgerIcon = document.getElementById('burger-icon');
    const closeIcon = document.getElementById('close-icon');
    const overlay = document.getElementById('overlay');
    const body = document.body; // Get a reference to the <body> element

    if (menuButton && dropdownMenu && burgerIcon && closeIcon && overlay) {
        const openMenu = () => {
            dropdownMenu.classList.remove('translate-x-full', 'opacity-0', 'hidden');
            dropdownMenu.classList.add('translate-x-0', 'opacity-100');
            burgerIcon.classList.add('hidden');
            closeIcon.classList.remove('hidden');
            overlay.classList.remove('hidden');
            body.classList.add('overflow-hidden'); // Lock scroll
        };

        const closeMenu = () => {
            dropdownMenu.classList.remove('translate-x-0', 'opacity-100');
            dropdownMenu.classList.add('translate-x-full', 'opacity-0');
            burgerIcon.classList.remove('hidden');
            closeIcon.classList.add('hidden');
            overlay.classList.add('hidden');
            body.classList.remove('overflow-hidden'); // Unlock scroll
        };

        const toggleMenu = () => {
            if (dropdownMenu.classList.contains('translate-x-0')) {
                closeMenu();
            } else {
                openMenu();
            }
        };

        menuButton.addEventListener('click', toggleMenu);
        overlay.addEventListener('click', closeMenu);

        dropdownMenu.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', closeMenu);
        });
    } else {
        console.error("Nie znaleziono jednego lub więcej elementów menu.");
    }
});