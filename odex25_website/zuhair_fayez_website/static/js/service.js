$(document).ready(function () {

  gsap.registerPlugin(ScrollTrigger);

  // Cards Entrance
  gsap.from(".service-card", { duration: .5, opacity: 0, y: 100, stagger: .1, delay: 3 });

  //Swiper architectural

  const swiperArchitectural = new Swiper('.swiper.architectural-grid', {
    // Optional parameters
    // slidesPerView: 4,
    // slidesPerGroup: 4,
    // spaceBetween: 0,
    // grabCursor: true,
    // grid: {
    //   rows: 2,
    // },
    breakpoints: {
      1: {
        slidesPerView: 2,
        slidesPerGroup: 2,
        spaceBetween: 0,
        grabCursor: true,
        grid: {
          rows: 2,
        },
      },
      320: {
        slidesPerView: 2,
        slidesPerGroup: 2,
        spaceBetween: 0,
        grabCursor: true,
        grid: {
          rows: 2,
        },
      },
      421: {
        slidesPerView: 2,
        slidesPerGroup: 2,
        spaceBetween: 0,
        grabCursor: true,
        grid: {
          rows: 2,
        },
      },
      768: {
        slidesPerView: 3,
        slidesPerGroup: 3,
        spaceBetween: 0,
        grabCursor: true,
        grid: {
          rows: 2,
        },
      },
      1025: {
        slidesPerView: 4,
        slidesPerGroup: 4,
        spaceBetween: 0,
        grabCursor: true,
        grid: {
          rows: 2,
        },
      },
    },
    // // If we need pagination
    pagination: {
      el: '.swiper-pagination',
      clickable: true,
    },
    // // Navigation arrows
    // navigation: {
    //   nextEl: '.swiper-button-next',
    //   prevEl: '.swiper-button-prev',
    // },

    // // And if we need scrollbar
    // scrollbar: {
    //     el: '.swiper-scrollbar',
    // },
  });


  // Swiper architectural Animation

  let servicesBoxes = document.querySelectorAll(".swiper-slide.service");
  servicesBoxes.forEach(serviceBox => {
    let serviceName = serviceBox.querySelector(".project-name");
    let magnifier = serviceBox.querySelector(".zoom-in");
    let serviceOverlay = serviceBox.querySelector(".projects");

    let servicesBoxesAnimation = gsap.timeline({ paused: true })
    servicesBoxesAnimation.to(serviceName, { duration: .5, opacity: 0 })
    servicesBoxesAnimation.from(magnifier, { duration: .5, opacity: 0 }, 0);
    servicesBoxesAnimation.to(serviceOverlay, { duration: .5, backgroundColor: "transparent" }, 0);


    serviceBox.addEventListener("mouseenter", () => {
      servicesBoxesAnimation.play();
    });
    serviceBox.addEventListener("mouseleave", () => {
      servicesBoxesAnimation.timeScale(1.5);
      servicesBoxesAnimation.reverse();
    });
  })

});



