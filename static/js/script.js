document.addEventListener("DOMContentLoaded", function () {
  // --- TYPEWRITER EFFECT ---
  const typewriterElement = document.getElementById("typewriter");
  if (typewriterElement) {
    const roles = [
      "Data Scientist",
      "MLOps Enthusiast",
      "Full Stack Developer",
      "Artist",
      "Python Developer",
      "Traveller"
    ];
    let roleIndex = 0;
    let charIndex = 0;
    let isDeleting = false;
    const typingSpeed = 150; // Milliseconds per character
    const deletingSpeed = 100;
    const delayBetweenRoles = 1500; // Pause after typing a role

    function type() {
      const currentRole = roles[roleIndex];
      // Determine current action: deleting or typing
      if (isDeleting) {
        // Deleting
        typewriterElement.textContent = currentRole.substring(0, charIndex - 1);
        charIndex--;
        // If fully deleted, switch to typing next role
        if (charIndex === 0) {
          isDeleting = false;
          roleIndex = (roleIndex + 1) % roles.length; // Move to next role
          setTimeout(type, 500); // Pause before typing next role
        } else {
          setTimeout(type, deletingSpeed); // Continue deleting
        }
      } else {
        // Typing
        typewriterElement.textContent = currentRole.substring(0, charIndex + 1);
        charIndex++;
        // If fully typed, switch to deleting
        if (charIndex === currentRole.length) {
          isDeleting = true;
          setTimeout(type, delayBetweenRoles); // Wait before deleting
        } else {
          setTimeout(type, typingSpeed); // Continue typing
        }
      }
    }
    // Initial call to start the effect
    setTimeout(type, 500); // Start after a short delay
  }

  // --- SMOOTH SCROLLING ---
  const navLinks = document.querySelectorAll('nav ul li a[href^="#"]'); // Select only hash links

  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      const targetId = this.getAttribute("href"); // Get the href value (e.g., "#about")
      // Check if it's actually an ID selector and not just "#"
      if (targetId && targetId.length > 1 && targetId.startsWith("#")) {
        e.preventDefault(); // Prevent default anchor jump ONLY for valid section links
        const targetElement = document.querySelector(targetId); // Find the element with that ID

        if (targetElement) {
          // Calculate offset for fixed navbar height
          const navHeight = document.querySelector("nav")?.offsetHeight || 70; // Get nav height or default
          const elementPosition = targetElement.getBoundingClientRect().top;
          const offsetPosition =
            elementPosition + window.pageYOffset - navHeight;

          window.scrollTo({
            top: offsetPosition,
            behavior: "smooth",
          });
        }
      }
      // Allow default behavior for non-hash links (like /travel/)
    });
  });

  // --- DYNAMIC NUMBER COUNT-UP ---
  const dynamicNumbers = document.querySelectorAll(".dynamic-number");

  dynamicNumbers.forEach((numberSpan) => {
    const targetString = numberSpan.getAttribute("data-target");
    const target = parseFloat(targetString); // Use parseFloat for decimals
    const suffix = targetString.replace(/[\d.-]/g, ""); // Extract suffix like '%' or ' FPS' - IMPROVED
    const speed = 20; // Speed of count-up
    let count = 0;
    let animationInterval = null;
    const decimals = (targetString.split(".")[1] || "").length; // Check for decimal places

    const updateCount = () => {
      // More robust increment calculation
      let increment = target / (1000 / speed);
      increment = Math.max(increment, 0.1); // Ensure a minimum increment for small numbers
      if (decimals > 0) {
        increment = Math.max(increment, Math.pow(10, -decimals)); // Ensure increment respects decimals
      } else {
        increment = Math.ceil(increment); // Ceil for integers
      }

      count += increment;

      if (count >= target) {
        numberSpan.innerText = target.toFixed(decimals) + suffix; // Use target value exactly, format decimals
        clearInterval(animationInterval);
        animationInterval = null;
      } else {
        numberSpan.innerText = count.toFixed(decimals) + suffix; // Format decimals during count
      }
    };

    numberSpan.addEventListener("mouseenter", () => {
      // Check if already at target to prevent re-animation if not resetting
      const currentDisplayValue = parseFloat(
        numberSpan.innerText.replace(suffix, "")
      );
      if (!animationInterval && currentDisplayValue !== target) {
        count = 0; // Reset count
        numberSpan.innerText = (0).toFixed(decimals) + suffix; // Start from 0, formatted
        animationInterval = setInterval(updateCount, speed);
      }
    });

    // Optional: Reset on mouse leave (uncomment if desired)
    // numberSpan.addEventListener('mouseleave', () => {
    //     if (animationInterval) {
    //         clearInterval(animationInterval);
    //         animationInterval = null;
    //     }
    //     // Reset text only if you want it to re-animate every time
    //     // numberSpan.innerText = (0).toFixed(decimals) + suffix;
    //     // count = 0;
    // });
  });

  // --- CARD TILT EFFECT ---
  const cards = document.querySelectorAll(".project-card"); // Select the cards directly

  cards.forEach((card) => {
    const maxTilt = 10; // Max tilt angle in degrees

    card.addEventListener("mousemove", (e) => {
      const cardRect = card.getBoundingClientRect();
      // Calculate mouse position relative to the card center
      const x = e.clientX - cardRect.left - cardRect.width / 2;
      const y = e.clientY - cardRect.top - cardRect.height / 2;

      // Calculate rotation angles (adjust multiplier for sensitivity)
      const rotateY = (x / (cardRect.width / 2)) * maxTilt; // Normalize position before multiplying
      const rotateX = -(y / (cardRect.height / 2)) * maxTilt; // Normalize position (inverted)

      // Apply the 3D transform
      // Request animation frame for smoother updates
      window.requestAnimationFrame(() => {
        card.style.transform = `rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.03)`; // Add slight scale up
      });
    });

    card.addEventListener("mouseleave", () => {
      // Reset transform smoothly via CSS transition
      window.requestAnimationFrame(() => {
        card.style.transform = "rotateX(0deg) rotateY(0deg) scale(1)";
      });
    });
  });
}); // End of SINGLE DOMContentLoaded listener

// document.addEventListener("DOMContentLoaded", function () {
//   // Typewriter Effect (Existing Code)
//   const typewriter = document.getElementById("typewriter");
//   const words = ["Data Scientist", "MLOps Engineer", "Problem Solver"];
//   let wordIndex = 0;
//   let charIndex = 0;
//   let isDeleting = false;

//   function type() {
//     if (wordIndex < words.length) {
//       let currentWord = words[wordIndex];
//       if (!isDeleting) {
//         typewriter.textContent = currentWord.substring(0, charIndex + 1);
//         charIndex++;
//         if (charIndex === currentWord.length) {
//           isDeleting = true;
//           setTimeout(type, 2000);
//         } else {
//           setTimeout(type, 100);
//         }
//       } else {
//         typewriter.textContent = currentWord.substring(0, charIndex - 1);
//         charIndex--;
//         if (charIndex === 0) {
//           isDeleting = false;
//           wordIndex++;
//           if (wordIndex === words.length) wordIndex = 0;
//           setTimeout(type, 500);
//         } else {
//           setTimeout(type, 50);
//         }
//       }
//     }
//   }

//   type();
// });

document.addEventListener("DOMContentLoaded", function () {
  const downloadButton = document.getElementById("download-resume-btn");

  if (downloadButton) {
    const logUrl = downloadButton.dataset.logUrl;
    // The URL to fetch the actual file. Get this from the log response or directly if known.
    // let fileUrl = downloadButton.dataset.fileUrl; // Get initial file URL if needed

    // Check local storage if the user has already downloaded
    const resumeDownloaded = localStorage.getItem("resumeDownloaded");
    if (resumeDownloaded === "true") {
      downloadButton.textContent = "Downloaded";
      downloadButton.disabled = true;
    }

    downloadButton.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent default button action if any

      // Disable button immediately to prevent multiple clicks
      this.disabled = true;
      this.textContent = "Processing..."; // Optional: give feedback

      // 1. Log the download attempt on the backend
      fetch(logUrl, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"), // Important for Django POST requests
          "Content-Type": "application/json",
          // Add other headers if needed
        },
        // body: JSON.stringify({}), // Add body if your view expects data
      })
        .then((response) => {
          if (!response.ok) {
            // Throw error to be caught by the .catch block
            throw new Error(`Network response was not ok (${response.status})`);
          }
          return response.json(); // Parse JSON response from the log view
        })
        .then((data) => {
          if (data.status === "success" && data.resume_url) {
            console.log("Download logged successfully.");

            // 2. Initiate the actual file download using the URL from the response
            const actualFileUrl = data.resume_url; // URL provided by the backend
            const link = document.createElement("a");
            link.href = actualFileUrl;
            // Extract filename from URL or use a default
            link.download = actualFileUrl.split("/").pop() || "resume.pdf";
            document.body.appendChild(link); // Required for Firefox
            link.click();
            document.body.removeChild(link); // Clean up

            // 3. Update button state and store in local storage
            this.textContent = "Downloaded";
            this.disabled = true; // Keep disabled
            localStorage.setItem("resumeDownloaded", "true"); // Mark as downloaded for this user session/browser
          } else {
            // Handle cases where logging was successful but no URL provided, or status was error
            console.error(
              "Backend logging failed or did not provide resume URL:",
              data.message || "Unknown error"
            );
            this.textContent = "Error Logging"; // Indicate error
            // Re-enable after a delay? Or keep disabled? Depends on desired UX
            // setTimeout(() => {
            //    this.disabled = false;
            //    this.textContent = 'Download Resume';
            // }, 3000);
          }
        })
        .catch((error) => {
          console.error("Error logging or initiating download:", error);
          this.textContent = "Download Failed"; // Update button text on error
          // Optionally re-enable the button after a delay so the user can retry
          setTimeout(() => {
            this.disabled = false;
            this.textContent = "Download Resume";
          }, 3000);
        });
    });
  }
});

// Function to get CSRF token (needed for Django POST requests)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}