odoo.define("pos_orders_history.OrdersHistoryScreen", function (require) {
    "use strict";
    const Registries = require("point_of_sale.Registries");
    const IndependentToOrderScreen = require("point_of_sale.IndependentToOrderScreen");
    const { useListener } = require("web.custom_hooks");
    const SearchBar = require("point_of_sale.SearchBar");

    class OrdersHistoryScreen extends IndependentToOrderScreen {
        constructor() {
            super(...arguments);
            useListener("close-screen", this.close);
            useListener("filter-selected", this._onFilterSelected);
            useListener("search", this._onSearch);
            const { AllOrders } = this.getOrderStates();
            this.searchDetails = {};
            this.filter = AllOrders;
            this.selectedOrder = false;
            // this.subscribe();
            this._initializeSearchFieldConstants();
        }
        _onFilterSelected(event) {
            this.filter = event.detail.filter;
            this.render();
        }
        _onSearch(event) {
            const searchDetails = event.detail;
            Object.assign(this.searchDetails, searchDetails);
            this.render();
        }
        // subscribe() {
        //     const subscriber = {
        //         context: this,
        //         callback: this.receive_updates,
        //     };
        //     this.env.pos.add_subscriber(subscriber);
        // }
        get orders() {
            const orderStates = this.getOrderStates();
            const sessionFilters = this.getSessionFilters();
            const filterCheck = (order) => {
                if (this.filter) {
                    if (Object.keys(orderStates).includes(this.filter))
                        return this.OrderStatesMapping[this.filter] === order.state;
                    else if (Object.keys(sessionFilters).includes(this.filter)){
                        if (this.filter === sessionFilters.User){
                            let cashier = this.env.pos.get_cashier();
                            let user_id = cashier ? cashier.user_id[0]: this.env.pos.user.id;
                            return order.user_id[0] === user_id;
                        }
                        else if (this.filter === sessionFilters.POS){
                            return order.config_id[0] === this.env.pos.config.id;
                        }
                    }
                } 
                return true;
            };
            const { fieldValue, searchTerm } = this.searchDetails;
            const fieldAccessor = this._searchFields[fieldValue];
            const searchCheck = (order) => {
                if (!fieldAccessor) return true;
                const fieldValue = fieldAccessor(order);
                if (fieldValue === null) return true;
                if (!searchTerm) return true;
                return fieldValue && fieldValue.toString().toLowerCase().includes(searchTerm.toLowerCase());
            };

            const predicate = (order) => {
                return filterCheck(order) && searchCheck(order);
            };
            let orders = this.env.pos.db.get_sorted_orders_history(1000);
            return orders.filter(predicate);
        }
        mounted() {
            $(".line-element-container").addClass("line-element-hidden");
            if (this.env.pos.config.load_barcode_order_only) {
                // Open popup automatically
                this.scanBarcode();
            }
        }
        get_datetime_format(datetime) {
            let d = new Date(datetime);
            let res = new Date(d.getTime() - d.getTimezoneOffset() * 60000).toLocaleString();
            return res;
        }
        lineSelect(ev) {
            let line = $(ev.target).closest(".order-row");
            $(".order-row").not(line).removeClass("active");
            $(".line-element-container").addClass("line-element-hidden");
            if (line.hasClass("active")) {
                line.removeClass("active");
                line.next().addClass("line-element-hidden");
                this.selectedOrder = false;
            } else {
                line.addClass("active");
                line.next().removeClass("line-element-hidden");
                this.selectedOrder = this.env.pos.db.orders_history_by_id[parseInt(line.data("id"), 10)];
            }
        }
        async scanBarcode() {
            const { confirmed, payload: barcode } = await this.showPopup("TextInputPopup", {
                title: this.env._t("Enter/Scan barcode"),
            });
            if (confirmed) this.confirm_barcode(barcode);
            self.pos.barcode_reader.restore_callbacks();
        }

        confirm_barcode(barcode) {
            if (barcode) {
                this.load_order_by_barcode(barcode);
            } else {
                this.showPopup("ErrorPopup", {
                    title: _t("No Barcode"),
                });
            }
        }
        load_order_by_barcode(barcode) {
            let self = this;
            this.rpc({
                model: "pos.order",
                method: "search_read",
                args: [[["ean13", "=", barcode]]],
            }).then(
                function (res) {
                    if (res && res.length) {
                        self.env.pos.update_orders_history(res);
                        if (res instanceof Array) {
                            res = res[0];
                        }
                        self.env.pos.fetch_order_history_lines_by_order_ids(res.id).done(function (lines) {
                            self.env.pos.update_orders_history_lines(lines);
                            self.search_order_on_history(res);
                        });
                    } else {
                        self.showPopup("ErrorPopup", {
                            title: _t("Error: Could not find the Order"),
                            body: _t("There is no order with this barcode."),
                        });
                    }
                },
                function (err, event) {
                    event.preventDefault();
                    console.error(err);
                    self.showPopup("ErrorPopup", {
                        title: _t("Error: Could not find the Order"),
                        body: err.data,
                    });
                }
            );
        }

        // receive_updates(action, ids) {
        //     switch (action) {
        //         case "update":
        //             this.update_list_items(ids);
        //             break;
        //         default:
        //             break;
        //     }
        // }
        // update_list_items(ids) {
        //     let self = this;
        //     _.each(ids, function (id) {
        //         let $el = $(".order-list").find("[data-id=" + id + "]");
        //         let data = self.env.pos.db.orders_history_by_id[id];
        //         let selected = false;
        //         if ($el.length === 0 || !data) {
        //             return;
        //         }
        //         let new_el_html = this.env.qweb.renderToString("OrderHistoryLine", {
        //             widget: self,
        //             order: data,
        //         });
        //         if ($el.hasClass("active")) {
        //             selected = true;
        //         }
        //         let orderline = document.createElement("tbody");
        //         orderline.innerHTML = new_el_html;
        //         orderline = orderline.childNodes[1];
        //         $el.replaceWith(orderline);
        //         self.ordersHistoryCache[id] = orderline;
        //         if (selected) {
        //             orderline.classList.add("active", "highlight");
        //         }
        //     });
        // }

        getSearchFieldNames() {
            return {
                ReceiptNumber: this.env._t("Receipt Number"),
                Date: this.env._t("Date"),
                Customer: this.env._t("Customer"),
            };
        }
        getOrderStates() {
            return {
                AllOrders: this.env._t("All Orders"),
                Ongoing: this.env._t("Ongoing"),
                Payment: this.env._t("Payment"),
                Receipt: this.env._t("Receipt"),
            };
        }
        get OrderStatesMapping() {
            let All = this.env._t("All Orders");
            let Ongoing = this.env._t("Ongoing");
            let Payment = this.env._t("Payment");
            let Receipt = this.env._t("Receipt");
            return {
                All: true,
                Ongoing: "new",
                Payment: "paid",
                Receipt: "done",
            };
        }
        get filterOptions() {
            const { AllOrders, Ongoing, Payment, Receipt } = this.getOrderStates();
            const { POS, User } = this.getSessionFilters();
            return [AllOrders, Ongoing, Payment, Receipt, POS, User];
        }
        getSessionFilters() {
            return {
                POS: this.env._t("POS"),
                User: this.env._t("User"),
            };
        }
        get _searchFields() {
            const { ReceiptNumber, Date, Customer } = this.getSearchFieldNames();
            var fields = {
                [ReceiptNumber]: (order) => order.pos_reference,
                [Date]: (order) => moment(order.creation_date).format("YYYY-MM-DD hh:mm A"),
                [Customer]: (order) => order.partner_id[1],
            };
            return fields;
        }
        get _screenToStatusMap() {
            const { Ongoing, Payment, Receipt } = this.getOrderStates();
            return {
                ProductScreen: Ongoing,
                PaymentScreen: Payment,
                ReceiptScreen: Receipt,
            };
        }
        _initializeSearchFieldConstants() {
            this.constants = {};
            Object.assign(this.constants, {
                searchFieldNames: Object.keys(this._searchFields),
                screenToStatusMap: this._screenToStatusMap,
            });
        }
        get searchBarConfig() {
            return {
                searchFields: this.constants.searchFieldNames,
                filter: { show: true, options: this.filterOptions },
            };
        }
        search_order_on_history(order) {
            $(".searchbox input").val(order.pos_reference);
            $(".searchbox input").keypress();
        }
    }
    OrdersHistoryScreen.template = "OrdersHistoryScreen";
    OrdersHistoryScreen.components = { SearchBar };
    Registries.Component.add(OrdersHistoryScreen);
    return OrdersHistoryScreen;
});
