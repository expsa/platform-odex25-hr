gsap.registerPlugin(ScrollTrigger);

// Sub Service Entrance
gsap.from(".project-card", { duration: .8, opacity: 0, y: 100, stagger: .2, delay: 3 });