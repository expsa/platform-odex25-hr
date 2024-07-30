odoo.define("point_of_sale_logo.image", function (require) {
    "use strict";

    const Chrome = require("point_of_sale.Chrome");
    const Registries = require("point_of_sale.Registries");

    const ScreenLogo = (Chrome) =>
        class extends Chrome {
            async start() {
                await super.start();
                if (this.env.pos.config && this.env.pos.config.image) {
                    $('.pos-logo').attr('src', window.location.origin + "/web/image?model=pos.config&field=image&id=" + this.env.pos.config.id);
                }
            }
        };

    Registries.Component.extend(Chrome, ScreenLogo);

    return Chrome;
});
