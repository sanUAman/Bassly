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

// Switch between Discover and Featured tabs
function switchTab(tab, event) {
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(t => t.classList.remove('active'));
    
    const clickedTab = Array.from(tabs).find(t => t.textContent.toLowerCase().includes(tab));
    if (clickedTab) {
        clickedTab.classList.add('active');
    }
    
    const cardsContainer = document.querySelector('.trending-cards');
    if (!cardsContainer) return;
    
    if (tab === 'featured') {
        // Fetch featured events from API
        fetchFeaturedEvents();
    } else {
        // Reload discover events
        filterEvents('all');
    }
}

// Fetch featured events from API
async function fetchFeaturedEvents() {
    const cardsContainer = document.querySelector('.trending-cards');
    if (!cardsContainer) return;
    
    try {
        const response = await fetch('/events/featured');
        const events = await response.json();
        
        if (events.length === 0) {
            cardsContainer.innerHTML = '<p class="no-events"><i class="fa-solid fa-heart-crack"></i> No featured events yet. Click the star on any event to add it here!</p>';
            return;
        }
        
        // Generate cards HTML
        let cardsHTML = '';
        events.forEach(event => {
            const imageUrl = event.image ? event.image : '/static/images/trending/card1.png';
            const date = new Date(event.date).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' });
            cardsHTML += `
                <div class="trending-card">
                    <img src="${imageUrl}" alt="Event image">
                    <div class="trending-card-content">
                        <h3 class="trending-title-h3">${event.title}</h3>
                        <p class="trending-location">${event.location}</p>
                        <div class="trending-footer">
                            <div class="trending-date">
                                <i class="fa-regular fa-calendar"></i>
                                ${date}
                            </div>
                            <div class="trending-actions">
                                <i class="fas fa-star star featured" data-event-id="${event.id}" onclick="toggleFeatured(this)"></i>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        });
        cardsContainer.innerHTML = cardsHTML;
        
        // Smooth scroll to the events section
        const eventsSection = document.querySelector('.tabs-bar');
        if (eventsSection) {
            eventsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    } catch (error) {
        console.error('Error fetching featured events:', error);
        cardsContainer.innerHTML = '<p class="no-events"><i class="fa-solid fa-heart-crack"></i> Error loading featured events.</p>';
    }
}

// Toggle featured status
async function toggleFeatured(element) {
    const eventId = element.getAttribute('data-event-id');
    if (!eventId) return;
    
    try {
        const response = await fetch(`/events/${eventId}/featured`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.status === 401) {
            // User not authenticated, show sign in modal
            alert('Please sign in to save events to your featured list');
            openSigninModal();
            return;
        }
        
        if (response.ok) {
            const data = await response.json();
            // Toggle the star class based on is_featured
            if (data.is_featured) {
                element.classList.remove('far');
                element.classList.add('fas');
                element.classList.add('featured');
            } else {
                element.classList.remove('fas');
                element.classList.add('far');
                element.classList.remove('featured');
            }
            
            // If we're on the featured tab, refresh the featured events
            const featuredTab = document.querySelector('.tab.active');
            if (featuredTab && featuredTab.textContent.toLowerCase().includes('featured')) {
                fetchFeaturedEvents();
            }
        }
    } catch (error) {
        console.error('Error toggling featured:', error);
    }
}

// Render a single event card
function renderEventCard(event) {
    const imageUrl = event.image ? event.image : '/static/images/trending/card1.png';
    const date = new Date(event.date).toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric', year: 'numeric', hour: 'numeric', minute: '2-digit' });
    const starClass = event.is_featured ? 'fas fa-star star featured' : 'far fa-star star';
    
    return `
        <div class="trending-card">
            <img src="${imageUrl}" alt="Event image">
            <div class="trending-card-content">
                <h3 class="trending-title-h3">${event.title}</h3>
                <p class="trending-location">${event.location}</p>
                <div class="trending-footer">
                    <div class="trending-date">
                        <i class="fa-regular fa-calendar"></i>
                        ${date}
                    </div>
                    <div class="trending-actions">
                        <i class="${starClass}" data-event-id="${event.id}" onclick="toggleFeatured(this)"></i>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Filter events by date (AJAX - no page reload)
async function filterEvents(filter, event) {
    // Prevent default behavior if event is passed
    if (event) {
        event.preventDefault();
        event.stopPropagation();
    }
    
    try {
        let apiUrl = '/events/';
        if (filter !== 'all') {
            apiUrl += '?filter=' + filter;
        }
        
        const response = await fetch(apiUrl);
        const events = await response.json();
        
        const cardsContainer = document.querySelector('.trending-cards');
        if (!cardsContainer) return;
        
        if (events.length === 0) {
            cardsContainer.innerHTML = '<p class="no-events"><i class="fa-solid fa-heart-crack"></i> No events found.</p>';
            return;
        }
        
        // Generate cards HTML
        let cardsHTML = '';
        events.forEach(event => {
            cardsHTML += renderEventCard(event);
        });
        cardsContainer.innerHTML = cardsHTML;
        
        // Smooth scroll to the events section
        const eventsSection = document.querySelector('.tabs-bar');
        if (eventsSection) {
            eventsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    } catch (error) {
        console.error('Error filtering events:', error);
    }
}