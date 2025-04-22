document.addEventListener("DOMContentLoaded", () => {
  const carousels = document.querySelectorAll(".tools-carousel");
  const prevButtons = document.querySelectorAll(".carousel-nav.prev");
  const nextButtons = document.querySelectorAll(".carousel-nav.next");

  carousels.forEach((carousel) => {
    let currentSlide = 0;
    const slides = carousel.querySelectorAll(".tool-slide");
    const slideCount = slides.length;

    prevButtons.forEach((button) => {
      button.addEventListener("click", () => {
        currentSlide = (currentSlide - 1 + slideCount) % slideCount;
        carousel.scrollLeft = slides[currentSlide].offsetLeft;
      });
    });

    nextButtons.forEach((button) => {
      button.addEventListener("click", () => {
        currentSlide = (currentSlide + 1) % slideCount;
        carousel.scrollLeft = slides[currentSlide].offsetLeft;
      });
    });
  });
});

document.addEventListener("DOMContentLoaded", () => {
  const toolCards = document.querySelectorAll(".tool-card");

  toolCards.forEach((card) => {
    card.addEventListener("click", () => {
      // Get the tool name from the data-tool attribute (if you want)
      const toolName = card.dataset.tool;
      console.log(`Tool clicked: ${toolName}`); // For debugging

      // You can add logic here to navigate to the tool's page
      // For example:
      // window.location.href = `/tools/${toolName}/`;
    });
  });
});

document.addEventListener('DOMContentLoaded', () => {
    const uploadForm = document.getElementById('resume-upload-form');
    const resultsDiv = document.getElementById('resume-results');
    const resumeScore = document.getElementById('resume-score');
    const resumeRecommendations = document.getElementById('resume-recommendations');

    uploadForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        console.log("Form submitted!"); // Debugging

        const formData = new FormData(uploadForm);

        try {
            console.log("Starting fetch..."); // Debugging
            const response = await fetch('/tools/resume-wizard/analyze/', {
                method: 'POST',
                body: formData,
            });

            console.log("Response received:", response);

            if (response.ok) {
                const data = await response.json();
                console.log("Parsed JSON:", data);
                resumeScore.textContent = data.score;
                resumeRecommendations.innerHTML = '';
                data.recommendations.forEach(rec => {
                    const li = document.createElement('li');
                    li.textContent = rec;
                    resumeRecommendations.appendChild(li);
                });
                resultsDiv.style.display = 'block';
            } else {
                console.error("Server error:", response.status, response.statusText);
                resultsDiv.innerHTML = '<p class="error-message">Error analyzing resume. Please try again.</p>';
                resultsDiv.style.display = 'block';
            }
        } catch (error) {
            console.error("Fetch error:", error);
            resultsDiv.innerHTML = '<p class="error-message">Network error. Please try again.</p>';
            resultsDiv.style.display = 'block';
        }
    });
});