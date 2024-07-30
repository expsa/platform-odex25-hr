// News Details Entrance

let newsFirstSection = gsap.timeline({})
newsFirstSection.from(".news-main-info", { duration: .5, opacity: 0, x: -40, delay: 3 })
    .from(".news-main-img", { duration: .5, opacity: 0, x: 40 })

//////////////////////////////////////////////////////////////////////////////////////////////

let newsSecondSection = gsap.timeline({
    scrollTrigger: {
        trigger: ".news-secondary",
        start: "top 60%",
        end: "top 30%",
    }
});

newsSecondSection.from('.news-secondary p', { duration: 1, y: 80, opacity: 0, stagger: .2 })

//////////////////////////////////////////////////////////////////////////////////////////////

// related news entrance
let relatedNewsEntrance = gsap.timeline({
    scrollTrigger: {
        trigger: ".other-news-container",
        start: "top 70%",
        end: "top 60%",
    }
});
relatedNewsEntrance.from('.other-news', { duration: .5, opacity: 0, y: 20 })
    .from('.other-news-card', { duration: .5, y: 80, opacity: 0, stagger: .2 })