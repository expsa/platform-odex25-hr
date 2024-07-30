$(document).ready(function () {
    // careers Container

    let ctaTitleCareers = document.querySelector(".cta-title-careers");
    let ctaTitleContentCareers = document.querySelector(".cta-title-content-careers");

    let careersEntrance = gsap.timeline({})
    careersEntrance.from(ctaTitleCareers, { duration: .5, y: "100%", opacity: 0 }, 3)
        .from(ctaTitleContentCareers, { duration: .8, y: "100%", opacity: 0 })
        .from(".careers-cta a", { duration: .8, y: "100%", opacity: 0 })
        .from(".explore-careers p", { duration: .5, y: "100%", opacity: 0 })
        .from(".scroll-explore-container-careers", { duration: .5, opacity: 0 })

    // scroll to explore
    let scrollRoller = document.querySelector(".scroll-roller-careers");

    let scrollRollerAnimation = gsap.timeline({})
    scrollRollerAnimation.from(scrollRoller, { duration: 1.5, y: "-100%", repeat: -1 })

    ////////////////////////////////////////////////////////////////////////////////////////

    // Why Join Us entrance
    let whyJoinUsEntrance = gsap.timeline({
        scrollTrigger: {
            trigger: ".why-join",
            start: "top 70%",
            end: "top 60%",
        }
    });
    whyJoinUsEntrance.from('.why-join p', { duration: .5, opacity: 0, y: 80, stagger: .2 })
        .from('.why-join img', { duration: .5, y: 80, opacity: 0 })

    ////////////////////////////////////////////////////////////////////////////////////////

    // Current Jobs entrance
    let currentJobsEntrance = gsap.timeline({
        scrollTrigger: {
            trigger: ".vacancies-container",
            start: "top 70%",
            end: "top 60%",
        }
    });
    currentJobsEntrance.from('.title-search', { duration: .5, opacity: 0, y: 80 })
        .from('.vacancie', { duration: .5, y: 80, opacity: 0, stagger: .2 })
        .from('.load-more', { duration: .5, y: 80, opacity: 0, stagger: .2 })
});
