document.addEventListener("DOMContentLoaded", () => {
  // Typewriter Effect
  const typewriter = document.getElementById("typewriter");
  const words = ["Vietnam", "Azerbaijan", "Georgia"];
  let wordIndex = 0;
  let charIndex = 0;
  let isDeleting = false;

  function typeWriter() {
    let currentWord = words[wordIndex];
    if (!isDeleting) {
      typewriter.textContent = currentWord.substring(0, charIndex + 1);
      charIndex++;
      if (charIndex === currentWord.length) {
        isDeleting = true;
        setTimeout(typeWriter, 1500); // Pause before deleting
      } else {
        setTimeout(typeWriter, 100); // Typing speed
      }
    } else {
      typewriter.textContent = currentWord.substring(0, charIndex - 1);
      charIndex--;
      if (charIndex === 0) {
        isDeleting = false;
        wordIndex = (wordIndex + 1) % words.length; // Next word (loop)
        setTimeout(typeWriter, 500); // Pause before typing
      } else {
        setTimeout(typeWriter, 50); // Deleting speed
      }
    }
  }

  typeWriter();
});
