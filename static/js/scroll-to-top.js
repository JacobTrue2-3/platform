const scrollBtn = document.getElementById("scrollToTopBtn");

scrollBtn.addEventListener("click", () => {
    window.scrollTo({
        top: 0
    })
})

window.addEventListener("scroll", () => {
    if (window.scrollY > 300) {
        scrollBtn.classList.add("show");
    } else {
        scrollBtn.classList.remove("show");
    }
})