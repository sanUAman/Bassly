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

document.querySelectorAll(".faq-question").forEach(button => {
    button.addEventListener("click", () => {
        const item = button.closest(".faq-item");
        const answer = item.querySelector(".faq-answer");

        document.querySelectorAll(".faq-item").forEach(el => {
            if (el !== item) {
                el.classList.remove("active");
                const a = el.querySelector(".faq-answer");
                a.style.height = "0px";
            }
        });

        const isOpen = item.classList.contains("active");

        if (isOpen) {
            answer.style.height = "0px";
            item.classList.remove("active");
        } else {
            item.classList.add("active");
            answer.style.height = answer.scrollHeight + "px";
        }
    });
});