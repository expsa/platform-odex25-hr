$(document).ready(function () {

    gsap.registerPlugin(ScrollTrigger);

    // about Container

    let ctaUpper = document.querySelector(".upper");
    let ctaBottom = document.querySelector(".bottom");

    let companyName = gsap.timeline({})
    companyName.from(ctaUpper, { duration: .5, x: -50, opacity: 0 }, 3)
        .from(ctaBottom, { duration: .5, x: 50, opacity: 0 })
        .from(".hr", { duration: .5, opacity: 0 }, "-=.5")
        .from(".explore-about p", { duration: .5, y: "100%", opacity: 0 })
        .from(".scroll-explore-container-about", { duration: .5, opacity: 0 })

    // scroll to explore
    let scrollRoller = document.querySelector(".scroll-roller-about");

    let scrollRollerAnimation = gsap.timeline({})
    scrollRollerAnimation.from(scrollRoller, { duration: 1.5, y: "-100%", repeat: -1 })

    ////////////////////////////////////////////////////////////////////////////////////////////

    // who we are Entrance
    const whoWeAreEntrance = gsap.timeline({
        scrollTrigger: {
            trigger: ".who-we-are",
            start: "top 60%",
            end: "top 30%",

        }
    });

    whoWeAreEntrance.from('.who-img img', { duration: 1, opacity: 0, x: -80 })
        .from('.who-content p', { duration: 1, y: 80, opacity: 0, stagger: .2 }, .5)

    // Mission & Vision Entrance
    const missVisiEntrance = gsap.timeline({
        scrollTrigger: {
            trigger: ".miss-visi",
            start: "top 60%",
            end: "top 30%",

        }
    });

    missVisiEntrance.from('.vision img', { duration: 1, opacity: 0, scale: 0 })
        .from('.vision p', { duration: 1, y: 80, opacity: 0, stagger: .2 }, .5)
        .from('.miss-visi-divider', { duration: 1, scale: 0, opacity: 0 }, 0)
        .from('.mission img', { duration: 1, opacity: 0, scale: 0 }, 0)
        .from('.mission p', { duration: 1, y: 80, opacity: 0, stagger: .2 }, .5)

    // Our values Entrance
    const valuesEntrance = gsap.timeline({
        scrollTrigger: {
            trigger: ".values-container",
            start: "top 60%",
            end: "top 30%",

        }
    });

    valuesEntrance.from('.values-title', { duration: .5, opacity: 0, y: 40 })
        .from('.value', { duration: 1, y: 80, opacity: 0, stagger: .2 })


    // Members Popup
    /////////////////
    let member1 = document.querySelector(".member1");
    let member2 = document.querySelector(".member2");
    let member3 = document.querySelector(".member3");
    let member1Close = document.querySelector("#member1-close");
    let member2Close = document.querySelector("#member2-close");
    let member3Close = document.querySelector("#member3-close");
    let member11Close = document.querySelector("#member1-1-close");
    let member22Close = document.querySelector("#member2-2-close");
    let member33Close = document.querySelector("#member3-3-close");
    let memberOverlay = document.querySelector(".member-popup-overlay");

    // Member 1
    const memberOne = gsap.timeline({ paused: true })
    memberOne.to('.member-popup-section2', { duration: .1, display: "none" })
        .to('.member-popup-section3', { duration: .1, display: "none" })
        .to('.member-popup-container', { duration: .1, display: "block" })
        .to(memberOverlay, { duration: .4, opacity: 1 })
        .from('.member-popup-section1', { duration: .4, display: "block" })
        .from('.sequence1', { stagger: .1, y: 20, opacity: 0 }, "-=1")

    // Member 2
    const memberTwo = gsap.timeline({ paused: true })
    memberTwo.to('.member-popup-section1', { duration: .1, display: "none" })
        .to('.member-popup-section3', { duration: .1, display: "none" })
        .to('.member-popup-container', { duration: .1, display: "block" })
        .to(memberOverlay, { duration: .4, opacity: 1 })
        .from('.member-popup-section2', { duration: .4, display: "block" })
        .from('.sequence2', { stagger: .1, y: 20, opacity: 0 }, "-=1")

    // Member 3
    const memberThree = gsap.timeline({ paused: true })
    memberThree.to('.member-popup-section1', { duration: .1, display: "none" })
        .to('.member-popup-section2', { duration: .1, display: "none" })
        .to('.member-popup-container', { duration: .1, display: "block" })
        .to(memberOverlay, { duration: .4, opacity: 1 })
        .from('.member-popup-section3', { duration: .4, display: "block" })
        .from('.sequence3', { stagger: .1, y: 20, opacity: 0 }, "-=1")

    // Open member 1
    if (member1) {
        member1.addEventListener("click", (e) => {
            e.preventDefault();
            memberOne.play()
        });
    }

    // Close member 1
    if (member1Close) {
        member1Close.addEventListener("click", (e) => {
            e.preventDefault();
            //memberOne.timeScale(1.5);
            memberOne.reverse()
        });
    }

    if (member11Close) {
        member11Close.addEventListener("click", (e) => {
            e.preventDefault();
            //memberOne.timeScale(1.5);
            memberOne.reverse()
        });
    }

    // Open member 2
    if (member2) {
        member2.addEventListener("click", (e) => {
            e.preventDefault();
            memberTwo.play()
        });
    }

    // Close member 2
    if (member2Close) {
        member2Close.addEventListener("click", (e) => {
            e.preventDefault();
            //memberTwo.timeScale(1.5);
            memberTwo.reverse()
        });
    }

    if (member22Close) {
        member22Close.addEventListener("click", (e) => {
            e.preventDefault();
            //memberTwo.timeScale(1.5);
            memberTwo.reverse()
        });
    }

    // Open member 3
    if (member3) {
        member3.addEventListener("click", (e) => {
            e.preventDefault();
            memberThree.play()
        });
    }

    // Close member 3
    if (member3Close) {
        member3Close.addEventListener("click", (e) => {
            e.preventDefault();
            //memberThree.timeScale(1.5);
            memberThree.reverse()
        });
    }

    if (member33Close) {
        member33Close.addEventListener("click", (e) => {
            e.preventDefault();
            //memberThree.timeScale(1.5);
            memberThree.reverse()
        });
    }

    // Close All By Overlay
    if (memberOverlay) {
        memberOverlay.addEventListener("click", (e) => {
            e.preventDefault();
            memberOne.timeScale(1.5);
            memberOne.reverse()
            memberTwo.timeScale(1.5);
            memberTwo.reverse()
            memberThree.timeScale(1.5);
            memberThree.reverse()
        });
    }

    //Swiper About Slider Primary Image

    const swiperAboutPrimary = new Swiper('.swiper.slider-about', {
        // Optional parameters
        loop: true,
        spaceBetween: 0,
        effect: "creative",
        creativeEffect: {
            prev: {
                shadow: true,
                translate: ["-20%", 0, -1],
            },
            next: {
                translate: ["100%", 0, 0],
            },
        },
        speed: 500,
        slidesPerView: 1,
        grabCursor: false,
        allowTouchMove: false,
        // autoplay: {
        //     delay: 3000,
        //     disableOnInteraction: false,
        // },
        // // If we need pagination
        // pagination: {
        //   el: '.swiper-pagination',
        //   dynamicBullets: true,
        // },

        // Navigation arrows
        navigation: {
            nextEl: '.swiper-button-next-about',
            prevEl: '.swiper-button-prev-about',
        },

        // // And if we need scrollbar
        // scrollbar: {
        //   el: '.swiper-scrollbar',
        // },
    });

    //Swiper About Slider Primary info

    const swiperAboutPrimaryInfo = new Swiper('.swiper.slider-about-info', {
        // Optional parameters
        loop: true,
        spaceBetween: 100,
        effect: "fade",
        speed: 500,
        slidesPerView: 1,
        grabCursor: false,
        allowTouchMove: false,
        preventClicks: false,
        // Navigation arrows
        navigation: {
            nextEl: '.swiper-button-next-about',
            prevEl: '.swiper-button-prev-about',
        },
    });

    // // info Animation

    // slideChange -- slideChangeTransitionStart - slideChangeTransitionEnd
    // slideNextTransitionStart - slideNextTransitionEnd -- slidePrevTransitionStart - slidePrevTransitionEnd


    swiperAboutPrimaryInfo.on('slideChange', function () {
        gsap.set(".about-animation", { clearProps: true })
    })

    // swiperAboutPrimaryInfo.on('slideChangeTransitionStart', function () {
    //     gsap.set(".about-animation", { clearProps: true })
    //     gsap.from(".about-animation", { duration: .5, opacity: 0, x: 40, delay: .2})
    // })

    swiperAboutPrimaryInfo.on('slideNextTransitionStart', function () {
        gsap.set(".about-animation", { clearProps: true })
        gsap.from(".about-animation", { duration: .5, opacity: 0, x: 40, delay: .2 })
    })

    swiperAboutPrimaryInfo.on('slidePrevTransitionStart', function () {
        gsap.set(".about-animation", { clearProps: true })
        gsap.from(".about-animation", { duration: .5, opacity: 0, x: -60, delay: .2 })
    })

    ///////////////////////////////////////////////////////////////////////////////

    //Swiper About Slider img Prev
    const swiperAboutPrimaryImgPrev = new Swiper('.swiper.slider-about-img-prev', {
        // Optional parameters
        loop: true,
        spaceBetween: 0,
        effect: "creative",
        creativeEffect: {
            prev: {
                shadow: true,
                translate: ["-20%", 0, -1],
            },
            next: {
                translate: ["100%", 0, 0],
            },
        },
        speed: 500,
        slidesPerView: 1,
        grabCursor: false,
        allowTouchMove: false,
        // Navigation arrows
        navigation: {
            nextEl: '.swiper-button-next-about',
            prevEl: '.swiper-button-prev-about',
        },
    });

    //Swiper About Slider name Prev
    const swiperAboutPrimaryNamePrev = new Swiper('.swiper.slider-about-name-prev', {
        // Optional parameters
        loop: true,
        spaceBetween: 0,
        // effect: "creative",
        // creativeEffect: {
        //     prev: {
        //         shadow: true,
        //         translate: ["-20%", 0, -1],
        //     },
        //     next: {
        //         translate: ["100%", 0, 0],
        //     },
        // },
        speed: 500,
        slidesPerView: 1,
        grabCursor: false,
        allowTouchMove: false,
        // Navigation arrows
        navigation: {
            nextEl: '.swiper-button-next-about',
            prevEl: '.swiper-button-prev-about',
        },
    });

    // Prev Names Animation

    swiperAboutPrimaryNamePrev.on('slideChange', function () {
        gsap.set(".about-animation-names-prev", { clearProps: true })
    })

    swiperAboutPrimaryNamePrev.on('slideNextTransitionStart', function () {
        gsap.set(".about-animation-names-prev", { clearProps: true })
        gsap.from(".about-animation-names-prev", { duration: .5, opacity: 0, x: 40, delay: .4 })
    })

    swiperAboutPrimaryNamePrev.on('slidePrevTransitionStart', function () {
        gsap.set(".about-animation-names-prev", { clearProps: true })
        gsap.from(".about-animation-names-prev", { duration: .5, opacity: 0, x: -40, delay: .4 })
    })

    ///////////////////////////////////////////////////////////////////////////////

    //Swiper About Slider img next
    const swiperAboutPrimaryImgNext = new Swiper('.swiper.slider-about-img-next', {
        // Optional parameters
        loop: true,
        spaceBetween: 0,
        effect: "creative",
        creativeEffect: {
            prev: {
                shadow: true,
                translate: ["-20%", 0, -1],
            },
            next: {
                translate: ["100%", 0, 0],
            },
        },
        speed: 500,
        slidesPerView: 1,
        grabCursor: false,
        allowTouchMove: false,
        // Navigation arrows
        navigation: {
            nextEl: '.swiper-button-next-about',
            prevEl: '.swiper-button-prev-about',
        },
    });

    //Swiper About Slider name next
    const swiperAboutPrimaryNameNext = new Swiper('.swiper.slider-about-name-next', {
        // Optional parameters
        loop: true,
        spaceBetween: 50,
        // effect: "creative",
        // creativeEffect: {
        //     prev: {
        //         shadow: true,
        //         translate: ["-20%", 0, -1],
        //     },
        //     next: {
        //         translate: ["100%", 0, 0],
        //     },
        // },
        speed: 500,
        slidesPerView: 1,
        grabCursor: false,
        allowTouchMove: false,
        // Navigation arrows
        navigation: {
            nextEl: '.swiper-button-next-about',
            prevEl: '.swiper-button-prev-about',
        },
    });

    // Next Names Animation

    swiperAboutPrimaryNameNext.on('slideChange', function () {
        gsap.set(".about-animation-names-next", { clearProps: true })
    })

    swiperAboutPrimaryNameNext.on('slideNextTransitionStart', function () {
        gsap.set(".about-animation-names-next", { clearProps: true })
        gsap.from(".about-animation-names-next", { duration: .5, opacity: 0, x: 40, delay: .4 })
    })

    swiperAboutPrimaryNameNext.on('slidePrevTransitionStart', function () {
        gsap.set(".about-animation-names-next", { clearProps: true })
        gsap.from(".about-animation-names-next", { duration: .5, opacity: 0, x: -40, delay: .4 })
    })

    // About Slider Entrance
    const aboutSliderEntrance = gsap.timeline({
        scrollTrigger: {
            trigger: ".about-container",
            start: "top 60%",
            end: "top 30%",

        }
    });
    aboutSliderEntrance.from('.slider-about', { duration: 1, opacity: 0, y: 80 })
        .from('.slider-about-info', { duration: 1, y: 80, opacity: 0 }, 0)
        .from('.swiper-button-prev-about', { duration: 1, x: -80, opacity: 0 }, 0)
        .from('.swiper-button-next-about', { duration: 1, x: 80, opacity: 0 }, 0)

});


