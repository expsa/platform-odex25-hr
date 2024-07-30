$(document).ready(function () {
// news Entrance
const newsCardsEntrance = gsap.timeline({
    scrollTrigger: {
        trigger: ".news-container",
        start: "top 60%",
        end: "top 30%",
    }
});

newsCardsEntrance.from('.news-card', { duration: 1, y: 80, opacity: 0, stagger: .2 })

///////////////////////////////////////////////////////////////////////////////////////

// news Container
let ctaTitleNews = document.querySelector(".cta-title-news");
let ctaTitleContentNews = document.querySelector(".cta-title-content-news");

let newsEntrance = gsap.timeline({})
newsEntrance.from(ctaTitleNews, { duration: .5, y: "100%", opacity: 0 }, 3.5)
    .from(ctaTitleContentNews, { duration: .8, y: "100%", opacity: 0 })
    .from(".explore-news p", { duration: .5, y: "100%", opacity: 0 })
    .from(".scroll-explore-container-news", { duration: .5, opacity: 0 })

// scroll to explore
let scrollRoller = document.querySelector(".scroll-roller-news");

let scrollRollerAnimation = gsap.timeline({})
scrollRollerAnimation.from(scrollRoller, { duration: 1.5, y: "-100%", repeat: -1 })

});

