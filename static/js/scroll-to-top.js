// static/js/scroll-to-top.js
(function() {
    document.addEventListener('DOMContentLoaded', function() {
        const scrollBtn = document.getElementById("scrollToTopBtn");
        
        // Проверяем, есть ли кнопка на странице
        if (!scrollBtn) {
            console.log('Scroll button not found on this page');
            return;
        }
        
        scrollBtn.addEventListener("click", () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });

        window.addEventListener("scroll", () => {
            if (window.scrollY > 300) {
                scrollBtn.classList.add("visible"); // Используем класс 'visible' как в CSS
            } else {
                scrollBtn.classList.remove("visible");
            }
        });
    });
})();