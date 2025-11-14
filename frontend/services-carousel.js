(function () {
  // Simple, dependency-free carousel for .services-carousel
  const sel = '.services-carousel';
  const carousel = document.querySelector(sel);
  if (!carousel) return;

  const track = carousel.querySelector('.carousel-track');
  const slides = Array.from(carousel.querySelectorAll('.carousel-slide'));
  const prevBtn = carousel.querySelector('.carousel-btn.prev');
  const nextBtn = carousel.querySelector('.carousel-btn.next');
  const indicatorsContainer = carousel.querySelector('.carousel-indicators');
  const mediaImg = carousel.querySelector('.carousel-image');

  let current = 0;
  let timer = null;
  const interval = 4000; // ms

  // Create indicators
  const indicators = slides.map((_, idx) => {
    const btn = document.createElement('button');
    btn.className = 'indicator';
    btn.setAttribute('role', 'tab');
    btn.setAttribute('aria-selected', 'false');
    btn.setAttribute('aria-label', `Slide ${idx + 1}`);
    btn.dataset.index = idx;
    indicatorsContainer.appendChild(btn);
    return btn;
  });

  function setActive(index) {
    if (index < 0) index = slides.length - 1;
    if (index >= slides.length) index = 0;
    current = index;

    slides.forEach((s, i) => {
      const on = i === current;
      s.classList.toggle('is-active', on);
      indicators[i].classList.toggle('is-active', on);
      indicators[i].setAttribute('aria-selected', on ? 'true' : 'false');
    });

    // Update media image (uses data-image attribute on slide or fallback to src)
    const imgSrc = slides[current].dataset.image || mediaImg.src;
    if (mediaImg && mediaImg.src !== imgSrc) {
      mediaImg.src = imgSrc;
      mediaImg.alt = slides[current].querySelector('h3')?.textContent || 'Service image';
    }

    // Move track to show the current slide (basic transform)
    const slideWidth = slides[0].getBoundingClientRect().width || 0;
    if (track) track.style.transform = `translateX(-${current * slideWidth}px)`;
  }

  function next() { setActive(current + 1); }
  function prev() { setActive(current - 1); }

  // Event listeners
  nextBtn && nextBtn.addEventListener('click', () => { next(); resetTimer(); });
  prevBtn && prevBtn.addEventListener('click', () => { prev(); resetTimer(); });

  indicators.forEach(btn => {
    btn.addEventListener('click', (e) => {
      const idx = Number(e.currentTarget.dataset.index);
      setActive(idx);
      resetTimer();
    });
  });

  // Keyboard navigation
  carousel.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowRight') { next(); resetTimer(); }
    if (e.key === 'ArrowLeft') { prev(); resetTimer(); }
  });

  // Autoplay
  function startTimer() {
    if (timer) return;
    timer = setInterval(() => next(), interval);
  }
  function stopTimer() {
    if (!timer) return;
    clearInterval(timer);
    timer = null;
  }
  function resetTimer() { stopTimer(); startTimer(); }

  // Pause on hover / focus
  carousel.addEventListener('mouseenter', stopTimer);
  carousel.addEventListener('mouseleave', startTimer);
  carousel.addEventListener('focusin', stopTimer);
  carousel.addEventListener('focusout', startTimer);

  // Resize -> recalc slide translation
  window.addEventListener('resize', () => setActive(current));

  // Initial setup: set widths on slides for inline track sliding
  function prepare() {
    const trackContainer = carousel.querySelector('.carousel-track-container');
    if (!trackContainer) return;
    const containerWidth = trackContainer.getBoundingClientRect().width || 0;
    slides.forEach(s => { s.style.width = containerWidth + 'px'; });
    track.style.width = `${containerWidth * slides.length}px`;
    track.style.display = 'flex';
    track.style.transition = 'transform 0.45s ease';
    // make carousel focusable for keyboard
    carousel.tabIndex = 0;

    setActive(0);
    startTimer();
  }

  // Wait until images/layout stabilize
  window.requestAnimationFrame(() => prepare());
})();
