$(document).ready(function () {
    // Activites Container

    let ctaTitleActivites = document.querySelector(".cta-title-activites");
    let ctaTitleContentActivites = document.querySelector(".cta-title-content-activites");

    let activitesEntrance = gsap.timeline({})
    activitesEntrance.from(ctaTitleActivites, { duration: .5, y: "100%", opacity: 0 }, 3)
        .from(ctaTitleContentActivites, { duration: .8, y: "100%", opacity: 0 })
        .from(".explore-activites p", { duration: .5, y: "100%", opacity: 0 })
        .from(".explore-activites .scroll-explore-container-activites", { duration: .5, opacity: 0 })

    // scroll to explore

    let scrollRoller = document.querySelector(".scroll-roller-activites");

    let scrollRollerAnimation = gsap.timeline({})
    scrollRollerAnimation.from(scrollRoller, { duration: 1.5, y: "-100%", repeat: -1 })


    // Activites Cards Hover Animation

    // Primary
    let activitePrimaryCards = document.querySelectorAll(".activite-primary");
    activitePrimaryCards.forEach(box3 => {
        let activitePrimaryBoxImage = box3.querySelector(".activite-img");
        let activitePrimaryInfoLine = box3.querySelector(".activite-primary .line");
        let activitePrimaryInfoTitle = box3.querySelector(".activite-primary .activite-info .activite-title p");

        let activitePrimaryBoxAnimation = gsap.timeline({ paused: true })
            .fromTo(activitePrimaryBoxImage, { "width": "55%" }, { duration: .5, "width": "50%" })
            .to(activitePrimaryInfoLine, { duration: .5, backgroundColor: "#DDC03B" }, 0)
            .to(activitePrimaryInfoTitle, { duration: .5, color: "#DDC03B" }, 0)


        if (box3) {
            box3.addEventListener("mouseenter", () => {
                activitePrimaryBoxAnimation.play();
            });
        }
        if (box3) {
            box3.addEventListener("mouseleave", () => {
                activitePrimaryBoxAnimation.timeScale(1.5);
                activitePrimaryBoxAnimation.reverse();
            });
        }
    })

    // Secondary
    let activiteSecondaryCards = document.querySelectorAll(".activite-secondary");
    activiteSecondaryCards.forEach(box4 => {
        let activiteSecondaryBoxImage = box4.querySelector(".activite-img");
        let activiteSecondaryInfoLine = box4.querySelector(".activite-secondary .line");
        let activiteSecondaryInfoTitle = box4.querySelector(".activite-secondary .activite-info .activite-title p");

        let activiteSecondaryBoxAnimation = gsap.timeline({ paused: true })
            .fromTo(activiteSecondaryBoxImage, { "width": "55%" }, { duration: .5, "width": "50%" })
            .to(activiteSecondaryInfoLine, { duration: .5, backgroundColor: "#DDC03B" }, 0)
            .to(activiteSecondaryInfoTitle, { duration: .5, color: "#DDC03B" }, 0)

        if (box4) {
            box4.addEventListener("mouseenter", () => {
                activiteSecondaryBoxAnimation.play();
            });
        }
        if (box4) {
            box4.addEventListener("mouseleave", () => {
                activiteSecondaryBoxAnimation.timeScale(1.5);
                activiteSecondaryBoxAnimation.reverse();
            });
        }
    })

});

