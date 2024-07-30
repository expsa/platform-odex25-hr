$(document).ready(function () {
    // contact Container

    let ctaTitleContact = document.querySelector(".cta-title-contact");
    let ctaTitleContentContact = document.querySelector(".cta-title-content-contact");

    let contactEntrance = gsap.timeline({})
    contactEntrance.from(ctaTitleContact, { duration: .5, y: "100%", opacity: 0 }, 3)
        .from(ctaTitleContentContact, { duration: .8, y: "100%", opacity: 0 })
        .from(".explore-contact p", { duration: .5, y: "100%", opacity: 0 })
        .from(".scroll-explore-container-contact", { duration: .5, opacity: 0 })

    // scroll to explore
    let scrollRoller = document.querySelector(".scroll-roller-contact");

    let scrollRollerAnimation = gsap.timeline({})
    scrollRollerAnimation.from(scrollRoller, { duration: 1.5, y: "-100%", repeat: -1 })

    //////////////////////////////////////////////////////////////////////////////////////////

    // branches entrance
    let branchesEntrance = gsap.timeline({
        scrollTrigger: {
            trigger: ".branches-container",
            start: "top 70%",
            end: "top 60%",
        }
    });
    branchesEntrance.from('.branches-title p', { duration: .5, opacity: 0, y: 80, stagger: .2 })
        .from('.branch', { duration: .5, y: 80, opacity: 0, stagger: .2 })

    //////////////////////////////////////////////////////////////////////////////////////////

    // Contact Form entrance
    let contactEntranceForm = gsap.timeline({
        scrollTrigger: {
            trigger: ".reach",
            start: "top 70%",
            end: "top 60%",
        }
    });
    contactEntranceForm.from('.form p', { duration: .5, opacity: 0, y: 80, stagger: .2 })
        .from('form', { duration: .5, y: 80, opacity: 0, stagger: .2 })
        .from('.mapouter', { duration: .5, opacity: 0, scale: 3 }, 0)

});
