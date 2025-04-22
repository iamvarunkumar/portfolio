document.addEventListener("DOMContentLoaded", () => {
  const percentageElements = document.querySelectorAll(".percentage");

  const animateValue = (element, start, end, duration) => {
    let current = start;
    const range = end - start;
    const increment = end > start ? 1 : -1;
    const stepTime = Math.abs(Math.floor(duration / range));
    const timer = setInterval(() => {
      current += increment;
      element.textContent = current;
      if (current == end) {
        clearInterval(timer);
      }
    }, stepTime);
  };

  percentageElements.forEach((element) => {
    const target = parseInt(element.dataset.target, 10);
    animateValue(element, 0, target, 1500); // Faster animation
  });
});


document.addEventListener("DOMContentLoaded", () => {
  const carousels = document.querySelectorAll(".artwork-carousel");
  const prevButtons = document.querySelectorAll(".carousel-nav.prev");
  const nextButtons = document.querySelectorAll(".carousel-nav.next");

  carousels.forEach((carousel, index) => {
    let currentSlide = 0;
    const slides = carousel.querySelectorAll(".artwork-slide");
    const slideCount = slides.length;
    const carouselName = carousel.parentElement
      .querySelector(".artwork-category-header")
      .textContent.toLowerCase()
      .replace(/\s+/g, ""); // Get category name

    prevButtons.forEach((button) => {
      if (button.dataset.carousel === carouselName) {
        button.addEventListener("click", (e) => {
          e.preventDefault();
          currentSlide = (currentSlide - 1 + slideCount) % slideCount;
          carousel.scrollLeft = slides[currentSlide].offsetLeft;
        });
      }
    });

    nextButtons.forEach((button) => {
      if (button.dataset.carousel === carouselName) {
        button.addEventListener("click", (e) => {
          e.preventDefault();
          currentSlide = (currentSlide + 1) % slideCount;
          carousel.scrollLeft = slides[currentSlide].offsetLeft;
        });
      }
    });
  });
});