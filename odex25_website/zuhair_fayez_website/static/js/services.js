
$(document).ready(function () {

// Services Container Animation

let servicesAnimation = gsap.timeline({})
servicesAnimation.from(".services-page-container .our-services-title", { duration: .5, opacity: 0, y: 20, delay: 3.8 })
    .from(".service-box", { duration: .7, opacity: 0, y: 80, stagger: .2 })

});