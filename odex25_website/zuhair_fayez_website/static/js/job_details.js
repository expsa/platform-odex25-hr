$(document).ready(function () {
    // Popup Form
    /////////////////

    let applyNow = document.querySelector("#apply-now");
    let applyNowClose = document.querySelector("#apply-now-close");
    let applyNowOverlay = document.querySelector(".form-popup-overlay");

    // Popup Apply
    const applyNowTimeline = gsap.timeline({ paused: true })
    applyNowTimeline.to('.form-popup-container', { duration: .1, display: "block" })
        .to(applyNowOverlay, { duration: .4, opacity: 1 })
        .from('.form-popup-section-container', { duration: .4, display: "block" })
        .from('.applyNowSequence', { stagger: .1, y: 20, opacity: 0 }, "-=1")

    // Open Popup Apply
    if (applyNow) {
        applyNow.addEventListener("click", (e) => {
            e.preventDefault();
            applyNowTimeline.play()
        });
    }

    // Close Popup Apply
    if (applyNowClose) {
        applyNowClose.addEventListener("click", (e) => {
            e.preventDefault();
            //memberOne.timeScale(1.5);
            applyNowTimeline.reverse()
        });
    }

    // Close All By Overlay
    if (applyNowOverlay) {
        applyNowOverlay.addEventListener("click", (e) => {
            e.preventDefault();
            applyNowTimeline.timeScale(1.5);
            applyNowTimeline.reverse()
        });
    }

    /////////////////////////////////////////////////////////////////////////////////////

    // Page Content Entrance
    let jobDetailsEntrance = gsap.timeline({})
    jobDetailsEntrance.from(".job-title p", { duration: .5, y: 40, opacity: 0, delay: 3 })
        .from(".job-title a", { duration: .5, y: 40, opacity: 0 })
        .from(".job-info", { duration: .5, y: 40, opacity: 0 })
});
