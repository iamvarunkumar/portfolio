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
