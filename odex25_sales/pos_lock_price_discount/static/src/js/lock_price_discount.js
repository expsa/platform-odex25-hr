odoo.define('pos_lock_price_discount.NumpadWidget', function (require) {
    "use strict";

    const NumpadWidget = require('point_of_sale.NumpadWidget');
    const Registries = require('point_of_sale.Registries');

    const NumpadWidgetDiscount= NumpadWidget => class extends NumpadWidget {
        async changeMode(mode) {

            if(mode === 'price' && this.env.pos.config.lock_price){
                const { confirmed, payload } = await this.showPopup('NumberPopup', {
                    title: this.env._t('Password'),
                    body: this.env._t(
                        'Password ?'
                    ),
                });
                if(confirmed){
                    if(payload !== this.env.pos.config.price_password){
                        this.showPopup('ErrorPopup', {
                            title: this.env._t('Error'),
                            body: this.env._t('Incorrect password. Please try again'),
                        });
                        return;
                    }
                }
                else{
                    return;
                }
            }

            if(mode === 'discount' && this.env.pos.config.lock_discount){
                const { confirmed, payload } = await this.showPopup('NumberPopup', {
                    title: this.env._t('Password'),
                    body: this.env._t(
                        'Password ?'
                    ),
                });
                if(confirmed){
                    if(payload !== this.env.pos.config.discount_password){
                        this.showPopup('ErrorPopup', {
                            title: this.env._t('Error'),
                            body: this.env._t('Incorrect password. Please try again'),
                        });
                        return;
                    }
                }
                else{
                    return;
                }
            }
            return super.changeMode(...arguments);
        }
    }
    Registries.Component.extend(NumpadWidget , NumpadWidgetDiscount);
    return NumpadWidget;
});

