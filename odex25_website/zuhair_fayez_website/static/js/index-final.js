$(document).ready(function () {

    gsap.registerPlugin(ScrollTrigger);

    // video Container
    let zuhair = document.querySelector(".zu");
    let companyIntro = document.querySelector(".company-intro");

    let companyName = gsap.timeline({})
    companyName.from(zuhair, { duration: .5, y: "100%" }, 3.5)
        .from(companyIntro, { duration: 1, y: "100%", opacity: 0 })
        .from(".explore p", { duration: 1, y: "100%", opacity: 0 })
        .from(".scroll-explore-container", { duration: 1, opacity: 0 }, "-=.5")

    // scroll to explore
    let scrollRoller = document.querySelector(".scroll-roller");

    let scrollRollerAnimation = gsap.timeline({})
    scrollRollerAnimation.from(scrollRoller, { duration: 1.5, y: "-100%", repeat: -1 })

    // Entrance Video autoplay

    let playEntranceVideo = document.querySelector("#entrance-video");

    function EntranceplayVideo() {
        if (playEntranceVideo) {
            playEntranceVideo.play();
            playEntranceVideo.currentTime = 0;
        }
        // playEntranceVideo.play();
        // playEntranceVideo.currentTime = 0;
    }

    // Our Project Video autoplay

    let ourProjectEntranceVideo = document.querySelector("#our-project-video");

    function ourProjectplayVideo() {
        if (ourProjectEntranceVideo) {
            ourProjectEntranceVideo.play();
            ourProjectEntranceVideo.currentTime = 0;
        }
        // ourProjectEntranceVideo.play();
        // ourProjectEntranceVideo.currentTime = 0;
    }

    window.onload = function () {
        EntranceplayVideo();
        ourProjectplayVideo();
    };


    // Services Cards
    let service1 = document.querySelector(".service1");
    let service2 = document.querySelector(".service2");
    let service3 = document.querySelector(".service3");
    let service4 = document.querySelector(".service4");
    // let whiteOverlay1 = document.querySelector(".white-overlay1");
    // let whiteOverlay2 = document.querySelector(".white-overlay2");
    // let whiteOverlay3 = document.querySelector(".white-overlay3");
    // let whiteOverlay4 = document.querySelector(".white-overlay4");

    // Cards Entrance
    gsap.from(".service", {
        duration: .5, opacity: 0, y: 50, stagger: .2, scrollTrigger: {
            start: "top 80%",
            end: "top 70%",
            scrub: 1,
            trigger: ".services-container"
        }
    });

    // Set default 
    gsap.set(service1, { "width": "25%" })
    gsap.set(service2, { "width": "25%" })
    gsap.set(service3, { "width": "25%" })
    gsap.set(service4, { "width": "25%" })

    // Service 1
    let boxAnimation1 = gsap.timeline({ paused: true })
    boxAnimation1.set(service1, { clearProps: true })
        .set(service2, { clearProps: true })
        .set(service3, { clearProps: true })
        .set(service4, { clearProps: true })
        .to(".service1 .service-overlay", { duration: .5, opacity: 0 })
        .to(".services-section-title", { opacity: 0 }, 0)
        .to(".service2 .service-content", { opacity: 0 }, 0)
        .to(".service3 .service-content", { opacity: 0 }, 0)
        .to(".service4 .service-content", { opacity: 0 }, 0)
        .fromTo(service1, { "width": "25%" }, { duration: .5, "width": "40%", immediateRender: false }, 0)
        // .fromTo(".service1 .service-overlay", { "background": "linear-gradient(0deg, rgba(0, 0, 0, 1) 0%, rgba(0,212,255,0) 80%)" },
        //     { "background": "linear-gradient(0deg, rgb(204, 139, 0) 0%, rgba(0,212,255,0) 100%)", duration: .2, immediateRender: false }, 0)
        // .to(whiteOverlay2, { duration: 1, "right": "0%" })
        // .to(whiteOverlay3, { duration: 1, "right": "0%" })
        // .to(whiteOverlay4, { duration: 1, "right": "0%" })
        .fromTo(service2, { "width": "25%" }, { duration: 1, "width": "0%" }, .5)
        .fromTo(service3, { "width": "25%" }, { duration: 1, "width": "0%" }, .5)
        .fromTo(service4, { "width": "25%" }, { duration: 1, "width": "0%" }, .5)
        .fromTo(service1, { "width": "40%" }, { duration: 1, "width": "100%", immediateRender: false }, .5)
        .to(".service1 .service-content", { duration: .5, opacity: 0 }, .5)
        // .fromTo(".service1 .service-overlay", { "background": "linear-gradient(0deg, rgb(204, 139, 0) 0%, rgba(0,212,255,0) 100%)" },
        //     { "background": "linear-gradient(0deg, rgba(0, 0, 0, 1) 0%, rgba(0,212,255,0) 80%)", duration: .2, immediateRender: false }, "-=.5")
        .to(".service1 img", { duration: 1, "left": "0vw" }, "-=1")
        .from(".project-name-1", { duration: .5, opacity: 0, y: 20 })
        .fromTo(".underline", { x: "-100%" }, { duration: .8, x: "100%" })
        .from(".project-link-1", { duration: .5, opacity: 0, y: 20 }, "-=1")
        .from(".Cards", { duration: .5, opacity: 0 }, .5)


    // Service 2
    let boxAnimation2 = gsap.timeline({ paused: true })
    boxAnimation2.set(service1, { clearProps: true })
        .set(service2, { clearProps: true })
        .set(service3, { clearProps: true })
        .set(service4, { clearProps: true })
        .to(".service2 .service-overlay", { duration: .5, opacity: 0 })
        .to(".services-section-title", { opacity: 0 }, 0)
        .to(".service1 .service-content", { opacity: 0 }, 0)
        .to(".service3 .service-content", { opacity: 0 }, 0)
        .to(".service4 .service-content", { opacity: 0 }, 0)
        .fromTo(service2, { "width": "25%" }, { duration: .5, "width": "40%", immediateRender: false }, 0)
        // .fromTo(".service2 .service-overlay", { "background": "linear-gradient(0deg, rgba(0, 0, 0, 1) 0%, rgba(0,212,255,0) 80%)" },
        //     { "background": "linear-gradient(0deg, rgb(204, 139, 0) 0%, rgba(0,212,255,0) 100%)", duration: .2, immediateRender: false }, 0)
        // .to(whiteOverlay1, { duration: 1, "right": "0%" })
        // .to(whiteOverlay3, { duration: 1, "right": "0%" })
        // .to(whiteOverlay4, { duration: 1, "right": "0%" })
        .fromTo(service1, { "width": "25%" }, { duration: 1, "width": "0%" }, .5)
        .fromTo(service3, { "width": "25%" }, { duration: 1, "width": "0%" }, .5)
        .fromTo(service4, { "width": "25%" }, { duration: 1, "width": "0%" }, .5)
        .fromTo(service2, { "width": "40%" }, { duration: 1, "width": "100%", immediateRender: false }, .5)
        .to(".service2 .service-content", { duration: .5, opacity: 0 }, .5)
        // .fromTo(".service2 .service-overlay", { "background": "linear-gradient(0deg, rgb(204, 139, 0) 0%, rgba(0,212,255,0) 100%)" },
        //     { "background": "linear-gradient(0deg, rgba(0, 0, 0, 1) 0%, rgba(0,212,255,0) 80%)", duration: .2, immediateRender: false }, "-=.5")
        .to(".service2 img", { duration: 1, "left": "0vw" }, "-=1")
        .from(".project-name-2", { duration: .5, opacity: 0, y: 20 })
        .fromTo(".underline", { x: "-100%" }, { duration: .8, x: "100%" })
        .from(".project-link-2", { duration: .5, opacity: 0, y: 20 }, "-=1")


    // Service 3
    let boxAnimation3 = gsap.timeline({ paused: true })
    boxAnimation3.set(service1, { clearProps: true })
        .set(service2, { clearProps: true })
        .set(service3, { clearProps: true })
        .set(service4, { clearProps: true })
        .to(".service3 .service-overlay", { duration: .5, opacity: 0 })
        .to(".services-section-title", { opacity: 0 }, 0)
        .to(".service1 .service-content", { opacity: 0 }, 0)
        .to(".service2 .service-content", { opacity: 0 }, 0)
        .to(".service4 .service-content", { opacity: 0 }, 0)
        .fromTo(service3, { "width": "25%" }, { duration: .5, "width": "40%", immediateRender: false }, 0)
        // .fromTo(".service3 .service-overlay", { "background": "linear-gradient(0deg, rgba(0, 0, 0, 1) 0%, rgba(0,212,255,0) 80%)" },
        //     { "background": "linear-gradient(0deg, rgb(204, 139, 0) 0%, rgba(0,212,255,0) 100%)", duration: .2, immediateRender: false }, 0)
        // .to(whiteOverlay1, { duration: 1, "right": "0%" })
        // .to(whiteOverlay2, { duration: 1, "right": "0%" })
        // .to(whiteOverlay4, { duration: 1, "right": "0%" })
        .fromTo(service1, { "width": "25%" }, { duration: 1, "width": "0%" }, .5)
        .fromTo(service2, { "width": "25%" }, { duration: 1, "width": "0%" }, .5)
        .fromTo(service4, { "width": "25%" }, { duration: 1, "width": "0%" }, .5)
        .fromTo(service3, { "width": "40%" }, { duration: 1, "width": "100%", immediateRender: false }, .5)
        .to(".service3 .service-content", { duration: .5, opacity: 0 }, .5)
        // .fromTo(".service3 .service-overlay", { "background": "linear-gradient(0deg, rgb(204, 139, 0) 0%, rgba(0,212,255,0) 100%)" },
        //     { "background": "linear-gradient(0deg, rgba(0, 0, 0, 1) 0%, rgba(0,212,255,0) 80%)", duration: .2, immediateRender: false }, "-=.5")
        .to(".service3 img", { duration: 1, "left": "0vw" }, "-=1")
        .from(".project-name-3", { duration: .5, opacity: 0, y: 20 })
        .fromTo(".underline", { x: "-100%" }, { duration: .8, x: "100%" })
        .from(".project-link-3", { duration: .5, opacity: 0, y: 20 }, "-=1")


    // Service 4
    let boxAnimation4 = gsap.timeline({ paused: true })
    boxAnimation4.set(service1, { clearProps: true })
        .set(service2, { clearProps: true })
        .set(service3, { clearProps: true })
        .set(service4, { clearProps: true })
        .to(".service4 .service-overlay", { duration: .5, opacity: 0 })
        .to(".services-section-title", { opacity: 0 }, 0)
        .to(".service1 .service-content", { opacity: 0 }, 0)
        .to(".service2 .service-content", { opacity: 0 }, 0)
        .to(".service3 .service-content", { opacity: 0 }, 0)
        .fromTo(service4, { "width": "25%" }, { duration: .5, "width": "40%", immediateRender: false }, 0)
        // .fromTo(".service4 .service-overlay", { "background": "linear-gradient(0deg, rgba(0, 0, 0, 1) 0%, rgba(0,212,255,0) 80%)" },
        //     { "background": "linear-gradient(0deg, rgb(204, 139, 0) 0%, rgba(0,212,255,0) 100%)", duration: .2, immediateRender: false }, 0)
        // .to(whiteOverlay1, { duration: 1, "right": "0%" })
        // .to(whiteOverlay2, { duration: 1, "right": "0%" })
        // .to(whiteOverlay3, { duration: 1, "right": "0%" })
        .fromTo(service1, { "width": "25%" }, { duration: 1, "width": "0%" }, .5)
        .fromTo(service2, { "width": "25%" }, { duration: 1, "width": "0%" }, .5)
        .fromTo(service3, { "width": "25%" }, { duration: 1, "width": "0%" }, .5)
        .fromTo(service4, { "width": "40%" }, { duration: 1, "width": "100%", immediateRender: false }, .5)
        .to(".service4 .service-content", { duration: .5, opacity: 0 }, .5)
        // .fromTo(".service4 .service-overlay", { "background": "linear-gradient(0deg, rgb(204, 139, 0) 0%, rgba(0,212,255,0) 100%)" },
        //     { "background": "linear-gradient(0deg, rgba(0, 0, 0, 1) 0%, rgba(0,212,255,0) 80%)", duration: .2, immediateRender: false }, "-=.5")
        .to(".service4 img", { duration: 1, "left": "0vw" }, "-=1")
        .from(".project-name-4", { duration: .5, opacity: 0, y: 20 })
        .fromTo(".underline", { x: "-100%" }, { duration: .8, x: "100%" })
        .from(".project-link-4", { duration: .5, opacity: 0, y: 20 }, "-=1")


    // Service 1
    if (service1) {
        service1.addEventListener("mouseenter", (e) => {
            e.preventDefault();
            boxAnimation1.revert();
            boxAnimation2.revert();
            boxAnimation3.revert();
            boxAnimation4.revert();
            boxAnimation1.play()
        });
    }
    if (service1) {
        service1.addEventListener("mouseleave", (e) => {
            e.preventDefault();
            boxAnimation1.timeScale(1.5);
            boxAnimation1.reverse();
        });
    }


    // Service 2
    if (service2) {
        service2.addEventListener("mouseenter", (e) => {
            e.preventDefault();
            boxAnimation1.revert();
            boxAnimation2.revert();
            boxAnimation3.revert();
            boxAnimation4.revert();
            boxAnimation2.play()
        });
    }
    if (service2) {
        service2.addEventListener("mouseleave", (e) => {
            e.preventDefault();
            boxAnimation2.timeScale(1.5);
            boxAnimation2.reverse();

        });
    }


    // Service 3
    if (service3) {
        service3.addEventListener("mouseenter", (e) => {
            e.preventDefault();
            boxAnimation1.revert();
            boxAnimation2.revert();
            boxAnimation3.revert();
            boxAnimation4.revert();
            boxAnimation3.play()
        });
    }
    if (service3) {
        service3.addEventListener("mouseleave", (e) => {
            e.preventDefault();
            boxAnimation3.timeScale(1.5);
            boxAnimation3.reverse();
        });
    }


    // Service 4
    if (service4) {
        service4.addEventListener("mouseenter", (e) => {
            e.preventDefault();
            boxAnimation1.revert();
            boxAnimation2.revert();
            boxAnimation3.revert();
            boxAnimation4.revert();
            boxAnimation4.play()
        });
    }
    if (service4) {
        service4.addEventListener("mouseleave", (e) => {
            e.preventDefault();
            boxAnimation4.timeScale(1.5);
            boxAnimation4.reverse();
        });
    }

    ////////////////////////////////////////////////////////////////////////////////

    //Swiper Services Cards 
    const swiper = new Swiper('.swiper.Cards', {
        // Optional parameters
        loop: true,
        effect: "fade",
        autoplay: {
            delay: 3000,
            disableOnInteraction: false,
        },
        // // If we need pagination
        // pagination: {
        //   el: '.swiper-pagination',
        // },

        // // Navigation arrows
        // navigation: {
        //   nextEl: '.swiper-button-next',
        //   prevEl: '.swiper-button-prev',
        // },

        // // And if we need scrollbar
        // scrollbar: {
        //   el: '.swiper-scrollbar',
        // },
    });

    ////////////////////////////////////////////////////////////////////////////////

    //Swiper Our Projects
    const swiperProjects = new Swiper('.swiper.our-projects-slider', {
        // Optional parameters
        slidesPerView: 2.5,
        spaceBetween: 50,
        freeMode: true,
        grabCursor: true,
        breakpoints: {
            1: {
                slidesPerView: 1,
                spaceBetween: 10,
                freeMode: true,
                grabCursor: true,
            },
            320: {
                slidesPerView: 1,
                spaceBetween: 20,
                freeMode: true,
                grabCursor: true,
            },
            421: {
                slidesPerView: 1,
                spaceBetween: 50,
                freeMode: true,
                grabCursor: true,
            },
            768: {
                slidesPerView: 2,
                spaceBetween: 30,
                freeMode: true,
                grabCursor: true,
            },
            1025: {
                slidesPerView: 2,
                spaceBetween: 30,
                freeMode: true,
                grabCursor: true,
            },
            1201: {
                slidesPerView: 2,
                spaceBetween: 40,
                freeMode: true,
                grabCursor: true,
            },
            1600: {
                slidesPerView: 2.5,
                spaceBetween: 50,
                freeMode: true,
                grabCursor: true,
            },
        },
        // // If we need pagination
        // pagination: {
        //   el: '.swiper-pagination',
        // },

        // // Navigation arrows
        navigation: {
            nextEl: '.swiper-button-next.our-project-slider',
            prevEl: '.swiper-button-prev.our-project-slider',
        },

        // // And if we need scrollbar
        // scrollbar: {
        //     el: '.swiper-scrollbar',
        // },
    });

    // Swiper Our Projects Entrance
    // Primary Slider Entrance
    const ourProjectEntrance = gsap.timeline({
        scrollTrigger: {
            trigger: ".our-projects-titles",
            start: "top 70%",
            end: "top 30%",
        }
    });
    ourProjectEntrance.from('.proj', { duration: .5, opacity: 0, y: 20, stagger: .2 })
        .from('.our-projects-slider .swiper-wrapper .swiper-slide', { duration: .5, opacity: 0, x: 50, stagger: .2 })

    //Swiper Our Projects thumb
    const swiperProjectsThumb = new Swiper('.swiper.our-projects-slider-thumb', {
        // Optional parameters
        spaceBetween: 0,
        slidesPerView: 1,
        watchSlidesProgress: true,
        allowTouchMove: false,
        // // If we need pagination
        // pagination: {
        //   el: '.swiper-pagination',
        // },

        // // Navigation arrows
        navigation: {
            nextEl: '.swiper-button-next.thumb',
            prevEl: '.swiper-button-prev.thumb',
        },

        // // And if we need scrollbar
        // scrollbar: {
        //     el: '.swiper-scrollbar',
        // },
    });

    swiperProjects.controller.control = swiperProjectsThumb;
    swiperProjectsThumb.controller.control = swiperProjects;


    // thumb Animation
    let openThumb = document.querySelector(".our-projects-slider .swiper-wrapper");
    let thumbClose = document.querySelector("#thumb-close");

    const thumb = gsap.timeline({ paused: true })
    thumb.to('.our-projects-thumb-container', { duration: .1, display: "block" })
        .from('.our-projects-slider-thumb', { duration: .5, opacity: 0 }, .2)
        .from('.swiper-button-prev.thumb', { duration: .5, opacity: 0 }, .2)
        .from('.swiper-button-next.thumb', { duration: .5, opacity: 0 }, .2)
        .from(thumbClose, { duration: .5, opacity: 0 }, .2)

    // Open thumb slider

    if (openThumb) {
        openThumb.addEventListener("click", (e) => {
            e.preventDefault();
            thumb.play()
        });
    }

    // Close thumb slider
    if (thumbClose) {
        thumbClose.addEventListener("click", (e) => {
            e.preventDefault();
            thumb.reverse()
        });
    }

    ////////////////////////////////////////////////////////////////////////////////

    //Swiper News Slider Primary
    const swiperNewsPrimary = new Swiper('.swiper.slider-news-primary', {
        // Optional parameters
        // loop: true,
        breakpoints: {
            1: {
                spaceBetween: 20,
                speed: 1000,
                slidesPerView: 1,
                grabCursor: true,
            },
            320: {
                spaceBetween: 30,
                speed: 1000,
                slidesPerView: 1,
                grabCursor: true,
            },
            421: {
                spaceBetween: 30,
                speed: 1000,
                slidesPerView: 1,
                grabCursor: true,
            },
            501: {
                spaceBetween: 15,
                speed: 1000,
                slidesPerView: 2,
                grabCursor: true,
            },
            601: {
                spaceBetween: 30,
                speed: 1000,
                slidesPerView: 2,
                grabCursor: true,
            },
            768: {
                spaceBetween: 40,
                speed: 1000,
                slidesPerView: 2.3,
                grabCursor: true,
            },
            1025: {
                spaceBetween: 30,
                speed: 1000,
                slidesPerView: 3,
                grabCursor: true,
            },
            1201: {
                spaceBetween: 20,
                speed: 1000,
                slidesPerView: 4,
                grabCursor: true,
            },
            1600: {
                spaceBetween: 30,
                speed: 1000,
                slidesPerView: 4,
                grabCursor: true,
            },
            1920: {
                spaceBetween: 30,
                speed: 1000,
                slidesPerView: 4,
                grabCursor: true,
            },
            2560: {
                spaceBetween: 30,
                speed: 1000,
                slidesPerView: 4,
                grabCursor: true,
            },
            3840: {
                spaceBetween: 50,
                speed: 1000,
                slidesPerView: 4,
                grabCursor: true,
            },
        },
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
            nextEl: '.swiper-button-next.latest-news',
            prevEl: '.swiper-button-prev.latest-news',
        },

        // // And if we need scrollbar
        // scrollbar: {
        //   el: '.swiper-scrollbar',
        // },
    });

    // Primary Slider Entrance
    const newsSection = gsap.timeline({
        scrollTrigger: {
            trigger: ".latest-news-titles-container",
            start: "top 70%",
            end: "top 30%",
        }
    });
    newsSection.from('.latest-news-primary-container .latest-news-title', { duration: .5, opacity: 0, y: 20 })
        .from('.latest-news-primary-container .latest-news-more', { duration: .5, opacity: 0, y: 20 })
        .from('.news', { duration: 1, opacity: 0, x: 40, stagger: .1 })



    // Primary Slider Hover
    let newsBoxes = document.querySelectorAll(".swiper-slide.news");
    newsBoxes.forEach(newsBox => {
        let newsImage = newsBox.querySelector(".news-img");
        let newsDescription = newsBox.querySelector(".news-description");

        let newsBoxesAnimation = gsap.timeline({ paused: true })
            .to(newsImage, { duration: .5, scale: 1.1 })
            .to(newsDescription, { duration: .5, y: -10 }, 0);

        if (newsBox) {
            newsBox.addEventListener("mouseenter", () => {
                newsBoxesAnimation.play();
            });
        }

        if (newsBox) {
            newsBox.addEventListener("mouseleave", () => {
                newsBoxesAnimation.timeScale(1.5);
                newsBoxesAnimation.reverse();
            });
        }
    })



    // Counter // First Without Decimals


    // var timeline = gsap.timeline({});
    // gsap.utils.toArray(".counter").forEach(function(el) {
    //   var target = {val: 0};
    //   timeline.to(target, {
    //     val: el.getAttribute("data-number"),
    //     duration: 4,
    //     onUpdate: function() {
    //       el.innerText = target.val.toFixed(1);
    //     }
    //   }, 0);
    // });

    // document.querySelector(".animate").addEventListener("click", function() {
    //   timeline.play();
    // });

    $(".counter").each(function () {
        var count = $(this),
            zero = { val: 0 },
            num = count.data("number"),
            split = (num + "").split("."),
            decimals = split.length > 1 ? split[1].length : 0;

        gsap.to(zero, {
            val: num, duration: 4, scrollTrigger: {
                trigger: ".counter",
                start: "top 80%",
                end: "top 10%",
            }, onUpdate: function () {
                count.text(zero.val.toFixed(decimals));
            }
        });
    });

});

