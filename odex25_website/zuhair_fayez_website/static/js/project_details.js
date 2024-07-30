
$(document).ready(function () {

    gsap.registerPlugin(ScrollTrigger);

    // Services Container Animation
    let projectDetails = gsap.timeline({})
    projectDetails.from(".project-name", { duration: .5, opacity: 0, y: 20, delay: 3.8 })
        .from(".project-details-container", { duration: .7, opacity: 0, y: 80 })
        .from('.gallery-thumbs', { duration: .5, y: 80, opacity: 0 }, "-=.5")

    // related projects entrance
    const relatedProjectsAnimation = gsap.timeline({
        scrollTrigger: {
            trigger: ".related-projects-container",
            start: "top 70%",
            end: "top 60%",
        }
    });
    relatedProjectsAnimation.from('.related-projects-title', { duration: .5, opacity: 0, y: 20 })
        .from('.related-project', { duration: .5, y: 80, opacity: 0, stagger: .2 })


    var galleryTop = new Swiper('.gallery-main', {
        slidesPerView: 1,
        loop: true,
        effect: "fade",
        loopedSlides: 50,
        // navigation: {
        //     nextEl: '.swiper-button-next',
        //     prevEl: '.swiper-button-prev',
        // },
    });

    var galleryThumbs = new Swiper('.gallery-thumbs', {
        direction: 'vertical',
        slidesPerView: 4,
        slideToClickedSlide: true,
        spaceBetween: 10,
        loopedSlides: 50,
        loop: true,
    });
    galleryTop.controller.control = galleryThumbs;
    galleryThumbs.controller.control = galleryTop;

    // small devices horizontal thumbs 
    var galleryThumbsSmall = new Swiper('.gallery-thumbs-small', {
        //direction: 'vertical',
        slidesPerView: 4,
        slideToClickedSlide: true,
        spaceBetween: 10,
        loopedSlides: 50,
        loop: true,
    });
    galleryTop.controller.control = galleryThumbsSmall;
    galleryThumbsSmall.controller.control = galleryTop;

});

