odoo.define("block_by_pin.pos", function (require) {
    "use strict";

    const PaymentScreen = require("point_of_sale.PaymentScreen");
    const Registries = require("point_of_sale.Registries");

    let core = require("web.core");

    let _t = core._t;

    const paymentScreenAddPin = (PaymentScreen) =>
        class extends PaymentScreen {
            sudo_custom(options) {
                options = options || {};
                let user = options.user || this.env.pos.get_cashier();

                if ($.inArray(options.special_group, user.groups_id) >= 0) {
                    return new $.Deferred().resolve(user);
                } else {
                    return this.select_user_custom(
                        _.extend(options, {
                            security: true,
                            current_user: this.env.pos.get_cashier(),
                        })
                    );
                }
            }
            select_user_custom(options) {
                options = options || {};
                let self = this;
                let def = new $.Deferred();

                let list = [];
                for (let i = 0; i < this.env.pos.users.length; i++) {
                    let user = this.env.pos.users[i];
                    if ($.inArray(options.special_group, user.groups_id) >= 0) {
                        list.push({
                            label: user.name,
                            item: user,
                        });
                    }
                }

                this.showPopup("SelectionPopup", {
                    title: options.title || _t("Select User"),
                    list: list,
                    confirm: function (cashier) {
                        def.resolve(cashier);
                    },
                    cancel: function () {
                        def.reject();
                    },
                });
                return def
                    .then(function (cashier) {
                        if (options.security && cashier !== options.current_user && cashier.pos_security_pin) {
                            return self.ask_password(cashier.pos_security_pin, options.arguments).then(function () {
                                return cashier;
                            });
                        }
                        return cashier;
                    })
                    .done(function (res) {
                        if (!res) {
                            return;
                        }
                        return self.check_then_set_and_render_cashier(options, res);
                    });
            }
            check_then_set_and_render_cashier(options, user) {
                if (options.do_not_change_cashier) {
                    return user;
                }
                if (this.env.pos.get_cashier().id !== user.id) {
                    this.env.pos.set_cashier(user);
                    this.env.pos.chrome.widget.username.renderElement();
                }
                return user;
            }
            show_password_popup(password, lock, cancel_function) {
                let self = this;
                this.showPopup("NumberPopup", {
                    title: _t("Password ?"),
                    isPassword: true,
                    confirm: function (pw) {
                        if (pw === password) {
                            lock.resolve();
                        } else {
                            self.showPopup("ErrorPopup", {
                                title: _t("Incorrect Password"),
                                confirm: _.bind(self.show_password_popup, self, password, lock, cancel_function),
                                cancel: _.bind(self.show_password_popup, self, password, lock, cancel_function),
                            });
                        }
                    },
                    cancel: function () {
                        if (cancel_function) {
                            cancel_function.call(self);
                        }
                        lock.reject();
                    },
                });
                return lock;
            }
            ask_password(password, options) {
                let self = this;
                let lock = new $.Deferred();

                if (options && options.ask_untill_correct && password) {
                    this.show_password_popup(password, lock, options.cancel_function);
                    return lock;
                }

                return this._super(password);
            }
        };
    Registries.Component.extend(PaymentScreen, paymentScreenAddPin);
    return PaymentScreen;
});
