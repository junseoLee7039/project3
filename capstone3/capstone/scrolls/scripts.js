let currentPage = 1;
const totalPages = 6;
let isScrolling = false;

window.addEventListener('wheel', (event) => {
    if (isScrolling) return;

    if (event.deltaY > 0) {
        // Scroll down
        if (currentPage < totalPages) {
            currentPage++;
            scrollPage();
        }
    } else {
        // Scroll up
        if (currentPage > 1) {
            currentPage--;
            scrollPage();
        }
    }

    isScrolling = true;
    setTimeout(() => {
        isScrolling = false;
    }, 500); // Adjust delay as needed
});

function scrollPage() {
    const offset = (currentPage - 1) * window.innerHeight;
    document.body.style.transform = `translateY(-${offset}px)`;
}
