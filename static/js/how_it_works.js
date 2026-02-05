document.addEventListener('scroll', function () {
    const header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Cursor-following light effect on first section
const firstSection = document.querySelector('.first');
if (firstSection) {
    document.addEventListener('mousemove', (e) => {
        const rect = firstSection.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        firstSection.style.setProperty('--x', `${x}px`);
        firstSection.style.setProperty('--y', `${y}px`);
    });
}

document.querySelector('.back-to-top-btn').addEventListener('click', function (e) {
    e.preventDefault();
    window.scrollTo({
        top: 0,
        behavior: 'smooth',
    });
});