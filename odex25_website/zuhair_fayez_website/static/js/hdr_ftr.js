$(document).ready(function () {
    gsap.registerPlugin(ScrollToPlugin);
    gsap.registerPlugin(ScrollTrigger);


    // nav on entrance
    let navLogo = document.querySelector(".website-logo");


    let navEntrance = gsap.timeline({})
    navEntrance.to(".animation-section-overlay", { duration: 2, x: "100%", ease: "expo.inOut" })
        .from(".animation", { duration: 2, scale: 1 }, "-=1.5")
        .from(".nav-container", { duration: .5, opacity: 0 }, "-=1.5")
        .from(navLogo, { duration: 1, opacity: 0 }, "-=.5")
        .from(".menu", { duration: .5, opacity: 0 }, "-=.5")
        .from(".language-selector", { duration: .5, opacity: 0 })
        .from(".hamburger-menu", { duration: .5, opacity: 0 })
        .from(".additional-extra-menu", { duration: .5, opacity: 0 })
        .from(".additional-menu", { duration: .5, opacity: 0 }, "-=1")
        .from(".breadcrumb", { duration: .5, opacity: 0 }, "-=1")

    // Nav on Scroll

    const showAnim = gsap.from(".nav-container", { yPercent: -100, paused: true, duration: 0.2 }).progress(1);

    ScrollTrigger.create({
        trigger: ".video",
        endTrigger: "body",
        start: "top top",
        end: "max",
        onUpdate: (self) => { self.direction === -1 ? showAnim.play() : showAnim.reverse(); }
    });

    gsap.to(".nav-container", {
        backgroundColor: "initial",
        //background: rgb(54,75,97),
        background: "linear-gradient(241deg, rgba(54,75,97,0.8) 0%, rgba(88,114,142,1) 21%, rgba(120,143,160,1) 60%, rgba(188,191,201,1) 100%)", scrollTrigger: {
            trigger: ".video",
            start: "5% top",
            end: "+=100px",
            scrub: true
        }
    });


    // menu icon animation

    let span1 = document.querySelector(".span1");
    let span3 = document.querySelector(".span3");
    let hamburgerMenu = document.querySelector(".hamburger-menu");


    let bamburgerMenu = gsap.timeline({ paused: true })
    bamburgerMenu.to(span1, { "width": "80%", duration: .2 })
        .to(span3, { "width": "80%", duration: .2 }, 0)

    if (hamburgerMenu) {
        hamburgerMenu.addEventListener("mouseenter", (e) => {
            e.preventDefault();
            bamburgerMenu.play()
        });
    }
    if (hamburgerMenu) {
        hamburgerMenu.addEventListener("mouseleave", (e) => {
            e.preventDefault();
            bamburgerMenu.timeScale(1.5);
            bamburgerMenu.reverse();
        });
    }
    
    

    // Popup Menu

    let closeAll = document.querySelector("#close");
    let close2 = document.querySelector(".popup-overlay");
    let serviceMedia = document.querySelector("#services-menu");
    let mediaCenterMenu = document.querySelector("#media-center-menu");
    let CloseSubMenu = document.querySelector(".back1");
    let CloseSubMenu2 = document.querySelector(".back2");

    const menu = gsap.timeline({ paused: true })
    menu.to('.popup-container', { duration: .1, display: "block" })
        .to('.popup-overlay', { duration: .5, x: 0, ease: "expo.inOut" })
        .to('.popup-menu', { duration: .5, x: 0, ease: "expo.inOut" }, .3)
        .from('.sequence', { stagger: .1, y: 20, opacity: 0 })

    const subMenuAnimation = gsap.timeline({ paused: true })
    subMenuAnimation.to('.popup-sub-menu', { duration: .5, x: 0, ease: "expo.inOut" })
        .from('.sequence-two', { stagger: .1, y: 20, opacity: 0 })

    const subMenuAnimation2 = gsap.timeline({ paused: true })
    subMenuAnimation2.to('.popup-sub-menu-2', { duration: .5, x: 0, ease: "expo.inOut" })
        .from('.sequence-three', { stagger: .1, y: 20, opacity: 0 })

    const closeIcon = gsap.timeline({ paused: true })
    closeIcon.to(closeAll, { duration: .5, rotation: 90, ease: "expo.inOut" })

    // Rotate X

    if (closeAll) {
        closeAll.addEventListener("mouseenter", (e) => {
            e.preventDefault();
            closeIcon.play()
        });
    }
    if (closeAll) {
        closeAll.addEventListener("mouseleave", (e) => {
            e.preventDefault();
            closeIcon.timeScale(1.5);
            closeIcon.reverse();
        });
    }

    // Open Popup Menu

    if (hamburgerMenu) {
        hamburgerMenu.addEventListener("click", (e) => {
            e.preventDefault();
            menu.play()
        });
    }

    // Open Sub Menu

    if (serviceMedia) {
        serviceMedia.addEventListener("click", (e) => {
            e.preventDefault();
            subMenuAnimation.play()
        });
    }

    // Open Sub Menu 2

    if (mediaCenterMenu) {
        mediaCenterMenu.addEventListener("click", (e) => {
            e.preventDefault();
            subMenuAnimation2.play()
        });
    }

    // Close Service Sub Menu

    if (CloseSubMenu) {
        CloseSubMenu.addEventListener("click", (e) => {
            e.preventDefault();
            subMenuAnimation.reverse()
        });
    }

    // Close Media Center Sub Menu

    if (CloseSubMenu2) {
        CloseSubMenu2.addEventListener("click", (e) => {
            e.preventDefault();
            subMenuAnimation2.reverse()
        });
    }

    // Main X Close
    if (closeAll) {
        closeAll.addEventListener("click", (e) => {
            e.preventDefault();
            closeIcon.timeScale(1.5);
            menu.reverse()
        });
    }

    // Close
    if (close2) {
        close2.addEventListener("click", (e) => {
            e.preventDefault();
            closeIcon.timeScale(1.5);
            subMenuAnimation2.reverse()
            subMenuAnimation.reverse()
            menu.reverse()
        });
    }


    // Scroll To Top

    let scrollToTop = document.querySelector(".go-top-inner");

    if (scrollToTop) {
        scrollToTop.addEventListener("click", () => {
            gsap.to(window, { duration: 1, scrollTo: 0 });
        });
    }

    // ScrollTrigger Tween & Timeline

    //Timeline
    // const work = gsap.timeline({
    //     scrollTrigger: {
    //         trigger: ".my-work",
    //         start: "top 30%",
    //         end: "top 30%"
    //     }
    // });
    // work.from('.work-title h1', { duration: 1.5, opacity: 0, scale: 0 })

    //Tween
    // gsap.from(scrollToTop, {
    //     duration: 1, opacity: 0, scrollTrigger: {
    //         trigger: ".clients",
    //         start: "top 30%",
    //         end: "top 10%",
    //         scrub: true
    //     }
    // })
});
