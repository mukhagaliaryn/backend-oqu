document.addEventListener("DOMContentLoaded", function () {
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");

    const swiper = new Swiper(".userCoursesSwiper", {
        navigation: {
            nextEl: "#nextBtn",
            prevEl: "#prevBtn",
        },
        slidesPerView: 1,
        spaceBetween: 16,
        pagination: {
            el: ".swiper-pagination",
            clickable: true,
        },
        mousewheel: true,
        keyboard: true,
        breakpoints: {
            768: {
                slidesPerView: 2
            },
            1024: {
                slidesPerView: 3
            },
            1280: {
                slidesPerView: 4
            },
            1536: {
                slidesPerView: 5
            }
        },
        on: {
            slideChange: function () {
                const isBeginning = swiper.isBeginning;
                const isEnd = swiper.isEnd;

                if (isBeginning) {
                    prevBtn.classList.add("hidden");
                } else {
                    prevBtn.classList.remove("hidden");
                }

                if (isEnd) {
                    nextBtn.classList.add("hidden");
                } else {
                    nextBtn.classList.remove("hidden");
                }
            },
        },
    });

    if (swiper.isBeginning) {
        prevBtn.classList.add("hidden");
    }
});