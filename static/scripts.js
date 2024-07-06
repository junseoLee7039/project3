let currentPage = 1;
        const totalPages = 9;
        let isScrolling = false;

        window.addEventListener('wheel', (event) => {
            if (isScrolling) return;

            if (event.deltaY > 0) {
                // Scroll down
                if (currentPage < totalPages) {
                    ++currentPage;
                    scrollPage();
                }
            } else {
                // Scroll up
                if (currentPage > 1) {
                    --currentPage;
                    scrollPage();
                }
            }

            isScrolling = true;
            setTimeout(() => {
                isScrolling = false;
            }, 1000); // Adjust delay as needed
        });

        function scrollPage() {
            const offset = (currentPage - 1) * window.innerHeight;
            document.body.style.transform = `translateY(-${offset}px)`;
        }

        window.addEventListener('scroll', function() {
            const nav = document.querySelector('nav');
            if (window.scrollY > 0) {
                nav.style.backgroundColor = 'rgba(0, 0, 0, 0.7)'; // Add a semi-transparent background on scroll
            } else {
                nav.style.backgroundColor = 'transparent'; // Make it transparent at the top
            }
        });