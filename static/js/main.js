// ============================================================
//  HrVr Digital Solutions — Main JavaScript
//  Fixed: EmailJS removed, Flask /api/contact use ho raha hai
// ============================================================

document.addEventListener('DOMContentLoaded', () => {

  // ── 1. Loader ──────────────────────────────────────────────
  setTimeout(() => {
    const loader = document.getElementById('loader');
    if (loader) loader.classList.add('hidden');
  }, 1600);

  // ── 2. Navbar scroll behaviour ────────────────────────────
  const navbar = document.getElementById('navbar');
  window.addEventListener('scroll', () => {
    navbar?.classList.toggle('scrolled', window.scrollY > 60);
    scrollTopBtn?.classList.toggle('visible', window.scrollY > 400);
  });

  // ── 3. Hamburger / Nav Drawer ─────────────────────────────
  const hamburger  = document.getElementById('hamburger');
  const navDrawer  = document.getElementById('navDrawer');
  const drawerClose= document.getElementById('drawerClose');
  hamburger?.addEventListener('click',  () => navDrawer?.classList.add('open'));
  drawerClose?.addEventListener('click',() => navDrawer?.classList.remove('open'));
  navDrawer?.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => navDrawer?.classList.remove('open'))
  );

  // ── 4. Scroll Reveal ──────────────────────────────────────
  const revealObserver = new IntersectionObserver(
    (entries) => entries.forEach(e => { if (e.isIntersecting) e.target.classList.add('visible'); }),
    { threshold: 0.12, rootMargin: '0px 0px -50px 0px' }
  );
  document.querySelectorAll('.reveal').forEach(el => revealObserver.observe(el));

  // ── 5. Skill-bar animation ────────────────────────────────
  const barObserver = new IntersectionObserver(
    (entries) => entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.querySelectorAll('.skill-bar-fill').forEach(bar => {
          bar.style.width = bar.dataset.width || '80%';
        });
        barObserver.unobserve(e.target);
      }
    }),
    { threshold: 0.3 }
  );
  document.querySelectorAll('.skill-bar-wrapper').forEach(w => barObserver.observe(w));

  // ── 6. Animated Counters ──────────────────────────────────
  function animateCounter(el, target, suffix = '+') {
    let start = 0;
    const duration = 1800;
    const step = Math.ceil(target / (duration / 16));
    const timer = setInterval(() => {
      start = Math.min(start + step, target);
      el.textContent = start + suffix;
      if (start >= target) clearInterval(timer);
    }, 16);
  }
  const counterObserver = new IntersectionObserver(
    (entries) => entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.querySelectorAll('[data-count]').forEach(el => {
          animateCounter(el, parseInt(el.dataset.count), el.dataset.suffix || '+');
        });
        counterObserver.unobserve(e.target);
      }
    }),
    { threshold: 0.4 }
  );
  document.querySelectorAll('.hero-stats').forEach(s => counterObserver.observe(s));

  // ── 7. Active nav link ────────────────────────────────────
  const sections  = document.querySelectorAll('section[id]');
  const navAnchors= document.querySelectorAll('.nav-links a');
  const sectionObserver = new IntersectionObserver(
    (entries) => entries.forEach(e => {
      if (e.isIntersecting) {
        navAnchors.forEach(a => {
          a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id);
        });
      }
    }),
    { threshold: 0.4 }
  );
  sections.forEach(s => sectionObserver.observe(s));

  // ── 8. Contact Form — Flask /api/contact se mail jaayegi ──
  const form      = document.getElementById('contactForm');
  const formMsg   = document.getElementById('formMessage');
  const submitBtn = document.getElementById('submitBtn');

  form?.addEventListener('submit', async function(e) {
    e.preventDefault();

    const name    = document.getElementById('name').value.trim();
    const email   = document.getElementById('email').value.trim();
    const project = document.getElementById('project').value.trim();
    const message = document.getElementById('message').value.trim();

    // Basic validation
    if (!name || !email || !message) {
      formMsg.textContent = 'Please fill all required fields ❗';
      formMsg.className   = 'form-message error';
      return;
    }

    submitBtn.disabled    = true;
    submitBtn.textContent = '⏳ Sending...';
    formMsg.className     = 'form-message';
    formMsg.textContent   = '';

    try {
      const response = await fetch('/api/contact', {
        method : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body   : JSON.stringify({ name, email, project, message })
      });

      const result = await response.json();

      if (result.success) {
        showToast('✅ Message Sent Successfully!', 'success');
        formMsg.textContent = '✅ ' + result.message;
        formMsg.className   = 'form-message success';
        form.reset();
      } else {
        showToast('❌ Failed to send message', 'error');
        formMsg.textContent = '❌ ' + (result.error || 'Something went wrong. Try again.');
        formMsg.className   = 'form-message error';
      }
    } catch (err) {
      showToast('❌ Network error', 'error');
      formMsg.textContent = '❌ Network error. Please email directly: hrvrdigitalsolutions@gmail.com';
      formMsg.className   = 'form-message error';
      console.error(err);
    } finally {
      submitBtn.disabled    = false;
      submitBtn.textContent = '🚀 Send Message';
      setTimeout(() => {
        if (formMsg.classList.contains('success')) {
          formMsg.className = 'form-message';
        }
      }, 6000);
    }
  });

  // ── 9. Scroll-to-Top ─────────────────────────────────────
  const scrollTopBtn = document.getElementById('scrollTop');
  scrollTopBtn?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  // ── 10. Toast Notification ────────────────────────────────
  function showToast(msg, type = 'success') {
    const t = document.getElementById('toast');
    if (!t) return;
    t.textContent = msg;
    t.className   = `toast ${type} show`;
    setTimeout(() => t.classList.remove('show'), 4000);
  }
  window.showToast = showToast;

  // ── 11. Particle Canvas ───────────────────────────────────
  const canvas = document.getElementById('particles-canvas');
  if (canvas) {
    const ctx = canvas.getContext('2d');
    let W, H, particles = [];
    const resize = () => {
      W = canvas.width  = window.innerWidth;
      H = canvas.height = window.innerHeight;
    };
    window.addEventListener('resize', resize);
    resize();

    const N = 60;
    for (let i = 0; i < N; i++) {
      particles.push({
        x: Math.random() * W, y: Math.random() * H,
        vx: (Math.random() - .5) * .4,
        vy: (Math.random() - .5) * .4,
        r: Math.random() * 2 + .5,
        alpha: Math.random() * .5 + .1,
        color: Math.random() > .5 ? '#7c3aed' : '#06b6d4',
      });
    }

    function drawParticles() {
      ctx.clearRect(0, 0, W, H);
      particles.forEach(p => {
        p.x += p.vx; p.y += p.vy;
        if (p.x < 0 || p.x > W) p.vx *= -1;
        if (p.y < 0 || p.y > H) p.vy *= -1;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2);
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.alpha;
        ctx.fill();
      });
      // Lines between nearby particles
      for (let i = 0; i < particles.length; i++) {
        for (let j = i + 1; j < particles.length; j++) {
          const dx = particles[i].x - particles[j].x;
          const dy = particles[i].y - particles[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 120) {
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = '#7c3aed';
            ctx.globalAlpha = (1 - dist / 120) * .15;
            ctx.lineWidth = .6;
            ctx.stroke();
          }
        }
      }
      ctx.globalAlpha = 1;
      requestAnimationFrame(drawParticles);
    }
    drawParticles();
  }

  // ── 12. Typing effect ─────────────────────────────────────
  const typingEl = document.getElementById('typingText');
  if (typingEl) {
    const phrases = [
      'Custom Business Websites',
      'Python Automations',
      'Mobile Apps',
      'Management Systems',
      'UI/UX Designs in Figma',
    ];
    let pi = 0, ci = 0, deleting = false;
    function typeLoop() {
      const phrase = phrases[pi];
      typingEl.textContent = deleting ? phrase.slice(0, ci--) : phrase.slice(0, ci++);
      if (!deleting && ci > phrase.length) { deleting = true; setTimeout(typeLoop, 1500); return; }
      if (deleting && ci < 0)             { deleting = false; pi = (pi + 1) % phrases.length; }
      setTimeout(typeLoop, deleting ? 40 : 70);
    }
    typeLoop();
  }

});
