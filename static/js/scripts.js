document.addEventListener('scroll', function () {
    const header = document.querySelector('header');
    if (window.scrollY > 50) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

document.querySelector('.back-to-top-btn').addEventListener('click', function (e) {
    e.preventDefault();
    window.scrollTo({
        top: 0,
        behavior: 'smooth',
    });
});

document.addEventListener("DOMContentLoaded", () => {
const track = document.querySelector(".hero-logos .track");
const originalContent = Array.from(track.children);

originalContent.forEach((node) => {
    track.appendChild(node.cloneNode(true));
});

let position = 0;
const speed = 2;

function animateScroll() {
    position -= speed;
    if (Math.abs(position) >= track.scrollWidth / 2 + 15) {
    position = 0;
    }
    track.style.transform = `translateX(${position}px)`;
    requestAnimationFrame(animateScroll);
}

animateScroll();
});

const images = [
    'url("../static/images/header/first.png")',
    'url("../static/images/header/second.png")',
    'url("../static/images/header/third.png")',
    'url("../static/images/header/fourth.png")',
    'url("../static/images/header/fifth.png")'
  ];

const randomIndex = Math.floor(Math.random() * images.length);
const selectedImage = images[randomIndex];

const heroContent = document.getElementById('heroContent');
heroContent.style.backgroundImage = selectedImage;


const rating = 4; // 1-5
const totalReviews = 14022;

const starsContainer = document.getElementById("stars");
const reviewsContainer = document.getElementById("reviews");

function renderStars(rating) {
    let output = '';
    for (let i = 1; i <= 5; i++) {
    if (i <= rating) {
        output += '★'; // filled star
    } else {
        output += '☆'; // empty star
    }
    }
    return output;
}

starsContainer.innerHTML = renderStars(rating);
reviewsContainer.textContent = `${totalReviews.toLocaleString()} reviews`;