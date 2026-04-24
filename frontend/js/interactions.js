// ========================================
// PREMIUM INTERACTIVE FEATURES
// ========================================

// Smooth scroll on page load
document.addEventListener('DOMContentLoaded', () => {
  // Initialize all interactive features
  initSmoothScroll();
  initScrollAnimations();
  initParallax();
  initHoverEffects();
  initCounterAnimations();
  initFormEnhancements();
  initNavbarEffects();
  initMouseTracker();
  initLoadingAnimation();
});

// ── SMOOTH SCROLL ──
function initSmoothScroll() {
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
      }
    });
  });
}

// ── SCROLL ANIMATIONS ──
function initScrollAnimations() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        // Add stagger effect for multiple elements
        if (entry.target.classList.contains('step-card')) {
          const cards = document.querySelectorAll('.step-card');
          cards.forEach((card, index) => {
            if (card.classList.contains('visible')) {
              card.style.animationDelay = `${index * 0.1}s`;
            }
          });
        }
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  });

  document.querySelectorAll('.fade-up, .step-card, .charity-card, .impact-card, .pricing-card').forEach(el => {
    observer.observe(el);
  });
}

// ── PARALLAX SCROLLING ──
function initParallax() {
  const parallaxElements = document.querySelectorAll('[data-parallax]');
  
  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;
    
    parallaxElements.forEach(el => {
      const speed = el.dataset.parallax || 0.5;
      el.style.transform = `translateY(${scrollY * speed}px)`;
    });
  });
}

// ── HOVER EFFECTS ──
function initHoverEffects() {
  // Card hover effect
  document.querySelectorAll('.step-card, .charity-card, .stat-card').forEach(card => {
    card.addEventListener('mouseenter', function() {
      this.style.transform = 'translateY(-8px) scale(1.02)';
    });
    
    card.addEventListener('mouseleave', function() {
      this.style.transform = 'translateY(0) scale(1)';
    });
  });

  // Button ripple effect
  document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
      const ripple = document.createElement('span');
      const rect = this.getBoundingClientRect();
      const size = Math.max(rect.width, rect.height);
      const x = e.clientX - rect.left - size / 2;
      const y = e.clientY - rect.top - size / 2;

      ripple.style.width = ripple.style.height = size + 'px';
      ripple.style.left = x + 'px';
      ripple.style.top = y + 'px';
      ripple.classList.add('ripple');

      this.appendChild(ripple);
      
      setTimeout(() => ripple.remove(), 600);
    });
  });
}

// ── COUNTER ANIMATIONS ──
function initCounterAnimations() {
  const animateCounter = (element) => {
    const target = parseInt(element.textContent);
    const increment = target / 30;
    let current = 0;

    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        element.textContent = target;
        clearInterval(timer);
      } else {
        element.textContent = Math.floor(current);
      }
    }, 30);
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
        entry.target.classList.add('animated');
        animateCounter(entry.target);
      }
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.stat-value, .hero-stat-num').forEach(el => {
    observer.observe(el);
  });
}

// ── FORM ENHANCEMENTS ──
function initFormEnhancements() {
  const forms = document.querySelectorAll('form');
  
  forms.forEach(form => {
    const inputs = form.querySelectorAll('input, select, textarea');
    
    inputs.forEach(input => {
      // Floating label effect
      input.addEventListener('focus', function() {
        this.parentElement.classList.add('focused');
      });
      
      input.addEventListener('blur', function() {
        if (!this.value) {
          this.parentElement.classList.remove('focused');
        }
      });

      // Real-time validation
      input.addEventListener('input', function() {
        validateField(this);
      });
    });

    // Form submit animation
    form.addEventListener('submit', function(e) {
      const btn = this.querySelector('button[type="submit"]');
      if (btn) {
        btn.innerHTML = '<span class="spinner"></span> Processing...';
        btn.disabled = true;
      }
    });
  });
}

// Field validation with feedback
function validateField(field) {
  let isValid = true;
  
  if (field.type === 'email') {
    isValid = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(field.value);
  } else if (field.type === 'password') {
    isValid = field.value.length >= 8;
  } else if (field.name === 'fullName') {
    isValid = field.value.length >= 2;
  }

  if (field.value) {
    field.style.borderColor = isValid ? '#10b981' : '#ef4444';
    field.style.boxShadow = isValid 
      ? '0 0 0 3px rgba(16,185,129,0.1)' 
      : '0 0 0 3px rgba(239,68,68,0.1)';
  }
}

// ── NAVBAR EFFECTS ──
function initNavbarEffects() {
  const navbar = document.getElementById('navbar');
  let lastScrollTop = 0;

  window.addEventListener('scroll', () => {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    // Show/hide navbar on scroll
    if (scrollTop > lastScrollTop) {
      navbar.style.transform = 'translateY(-100%)';
    } else {
      navbar.style.transform = 'translateY(0)';
    }
    
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
  });

  // Navbar link active state
  const navLinks = document.querySelectorAll('.nav-menu a');
  navLinks.forEach(link => {
    link.addEventListener('click', function() {
      navLinks.forEach(l => l.style.color = 'inherit');
      this.style.color = 'var(--primary)';
    });
  });
}

// ── MOUSE TRACKER ──
function initMouseTracker() {
  const hero = document.querySelector('.hero');
  if (!hero) return;

  document.addEventListener('mousemove', (e) => {
    const x = (e.clientX / window.innerWidth) * 100;
    const y = (e.clientY / window.innerHeight) * 100;
    
    hero.style.backgroundPosition = `${x}% ${y}%`;
  });
}

// ── LOADING ANIMATION ──
function initLoadingAnimation() {
  window.addEventListener('load', () => {
    document.body.style.opacity = '1';
  });
}

// ── NOTIFICATION SYSTEM ──
function showNotification(message, type = 'success', duration = 4000) {
  const notif = document.createElement('div');
  notif.className = `notification ${type}`;
  notif.textContent = message;
  document.body.appendChild(notif);

  setTimeout(() => {
    notif.style.opacity = '0';
    setTimeout(() => notif.remove(), 300);
  }, duration);
}

// ── PARALLAX TEXT EFFECT ──
function initParallaxText() {
  const parallaxTexts = document.querySelectorAll('.hero h1, .hero p');
  
  window.addEventListener('scroll', () => {
    const scrollY = window.pageYOffset;
    
    parallaxTexts.forEach((el, index) => {
      const speed = 0.5 + (index * 0.1);
      el.style.transform = `translateY(${scrollY * speed}px)`;
    });
  });
}

// ── DRAW ANIMATION (for dashboard) ──
function animateDrawNumbers(numbers) {
  return numbers.map((num, i) => {
    setTimeout(() => {
      const element = document.createElement('span');
      element.className = 'draw-number';
      element.textContent = num;
      element.style.animation = `slideInUp 0.3s ease ${i * 0.1}s both`;
      return element;
    }, i * 100);
    return num;
  });
}

// ── CONFETTI EFFECT (for wins) ──
function celebrateWin() {
  const confettiPieces = 50;
  const container = document.body;

  for (let i = 0; i < confettiPieces; i++) {
    const confetti = document.createElement('div');
    confetti.style.cssText = `
      position: fixed;
      left: ${Math.random() * 100}%;
      top: -10px;
      width: 10px;
      height: 10px;
      background: ${['#6366f1', '#10b981', '#f59e0b'][Math.floor(Math.random() * 3)]};
      border-radius: 50%;
      animation: fall ${2 + Math.random() * 1}s linear forwards;
      z-index: 9999;
    `;
    container.appendChild(confetti);
    
    setTimeout(() => confetti.remove(), 3000);
  }
}

// ── SCROLL PROGRESS BAR ──
function initScrollProgressBar() {
  const progressBar = document.createElement('div');
  progressBar.className = 'scroll-progress-bar';
  progressBar.style.cssText = `
    position: fixed;
    top: 0;
    left: 0;
    height: 3px;
    background: linear-gradient(90deg, #6366f1, #10b981);
    z-index: 9999;
    transition: width 0.2s ease;
  `;
  document.body.appendChild(progressBar);

  window.addEventListener('scroll', () => {
    const scrollPercent = (window.scrollY / (document.documentElement.scrollHeight - window.innerHeight)) * 100;
    progressBar.style.width = scrollPercent + '%';
  });
}

// ── CURSOR GLOW EFFECT ──
function initCursorGlow() {
  const glow = document.createElement('div');
  glow.style.cssText = `
    position: fixed;
    width: 30px;
    height: 30px;
    border: 2px solid rgba(99, 102, 241, 0.4);
    border-radius: 50%;
    pointer-events: none;
    z-index: 9998;
    box-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
  `;
  document.body.appendChild(glow);

  document.addEventListener('mousemove', (e) => {
    glow.style.left = (e.clientX - 15) + 'px';
    glow.style.top = (e.clientY - 15) + 'px';
  });

  document.addEventListener('mouseleave', () => {
    glow.style.opacity = '0';
  });

  document.addEventListener('mouseenter', () => {
    glow.style.opacity = '1';
  });
}

// ── PAGE TRANSITION ──
function pageTransition(href) {
  document.body.style.opacity = '0';
  setTimeout(() => {
    window.location.href = href;
  }, 300);
}

// Export for use in other files
window.InteractiveEffects = {
  showNotification,
  celebrateWin,
  animateDrawNumbers,
  pageTransition
};
