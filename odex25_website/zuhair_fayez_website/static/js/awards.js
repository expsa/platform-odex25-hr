$(document).ready(function () {
    // awards Container

    let ctaTitleAwards = document.querySelector(".cta-title-awards");
    let ctaTitleContentAwards = document.querySelector(".cta-title-content-awards");

    let awardsEntrance = gsap.timeline({})
    awardsEntrance.from(ctaTitleAwards, { duration: .5, y: "100%", opacity: 0 }, 3)
        .from(ctaTitleContentAwards, { duration: .8, y: "100%", opacity: 0 })
        .from(".explore-awards p", { duration: .5, y: "100%", opacity: 0 })
        .from(".scroll-explore-container-awards", { duration: .5, opacity: 0 })

    // scroll to explore

    let scrollRoller = document.querySelector(".scroll-roller-awards");

    let scrollRollerAnimation = gsap.timeline({})
    scrollRollerAnimation.from(scrollRoller, { duration: 1.5, y: "-100%", repeat: -1 })



    // Awards Cards Hover Animation

    // Primary
    let awardsPrimaryCards = document.querySelectorAll(".award-primary");
    awardsPrimaryCards.forEach(box => {
        let awardsPrimaryBoxImage = box.querySelector(".award-img");
        let awardsPrimaryInfoLine = box.querySelector(".award-primary .line");
        let awardsPrimaryInfoTitle = box.querySelector(".award-primary .award-info .award-title p");

        let awardsPrimaryBoxAnimation = gsap.timeline({ paused: true })
            .fromTo(awardsPrimaryBoxImage, { "width": "55%" }, { duration: .5, "width": "50%" })
            .to(awardsPrimaryInfoLine, { duration: .5, backgroundColor: "#DDC03B" }, 0)
            .to(awardsPrimaryInfoTitle, { duration: .5, color: "#DDC03B" }, 0)

        if (box) {
            box.addEventListener("mouseenter", () => {
                awardsPrimaryBoxAnimation.play();
            });
        }
        if (box) {
            box.addEventListener("mouseleave", () => {
                awardsPrimaryBoxAnimation.timeScale(1.5);
                awardsPrimaryBoxAnimation.reverse();
            });
        }
    })

    // Secondary
    let awardsSecondaryCards = document.querySelectorAll(".award-secondary");
    awardsSecondaryCards.forEach(box2 => {
        let awardsSecondaryBoxImage = box2.querySelector(".award-img");
        let awardsSecondaryInfoLine = box2.querySelector(".award-secondary .line");
        let awardsSecondaryInfoTitle = box2.querySelector(".award-secondary .award-info .award-title p");

        let awardsSecondaryBoxAnimation = gsap.timeline({ paused: true })
            .fromTo(awardsSecondaryBoxImage, { "width": "55%" }, { duration: .5, "width": "50%" })
            .to(awardsSecondaryInfoLine, { duration: .5, backgroundColor: "#DDC03B" }, 0)
            .to(awardsSecondaryInfoTitle, { duration: .5, color: "#DDC03B" }, 0)

        if (box2) {
            box2.addEventListener("mouseenter", () => {
                awardsSecondaryBoxAnimation.play();
            });
        }
        if (box2) {
            box2.addEventListener("mouseleave", () => {
                awardsSecondaryBoxAnimation.timeScale(1.5);
                awardsSecondaryBoxAnimation.reverse();
            });
        }
    })
});
