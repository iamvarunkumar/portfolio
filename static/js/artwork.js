document.addEventListener("DOMContentLoaded", () => {
  const carousels = document.querySelectorAll(".artwork-carousel");
  const prevButtons = document.querySelectorAll(".carousel-nav.prev");
  const nextButtons = document.querySelectorAll(".carousel-nav.next");

  carousels.forEach((carousel, index) => {
    let currentSlide = 0;
    const slides = carousel.querySelectorAll(".artwork-slide");
    const slideCount = slides.length;
    const carouselName = carousel.parentElement.querySelector(
      ".artwork-category-header"
    ).textContent;

    prevButtons.forEach((button) => {
      if (
        button.dataset.carousel ===
        carouselName.toLowerCase().replace(/\s+/g, "")
      ) {
        button.addEventListener("click", (e) => {
          e.preventDefault(); // Prevent default button behavior
          currentSlide = (currentSlide - 1 + slideCount) % slideCount;
          carousel.scrollLeft = slides[currentSlide].offsetLeft;
        });
      }
    });

    nextButtons.forEach((button) => {
      if (
        button.dataset.carousel ===
        carouselName.toLowerCase().replace(/\s+/g, "")
      ) {
        button.addEventListener("click", (e) => {
          e.preventDefault(); // Prevent default button behavior
          currentSlide = (currentSlide + 1) % slideCount;
          carousel.scrollLeft = slides[currentSlide].offsetLeft;
        });
      }
    });
  });
});
