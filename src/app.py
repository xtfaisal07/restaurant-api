from flask import Flask
import handlers

app = Flask(__name__)

app.add_url_rule("/", "home", handlers.home)

app.add_url_rule("/menu", "list_menu", handlers.list_menu, methods=["GET"])
app.add_url_rule("/menu/<int:item_id>", "get_menu_item", handlers.get_menu_item, methods=["GET"])

app.add_url_rule("/customers", "create_customer", handlers.create_customer, methods=["POST"])
app.add_url_rule("/customers/<int:customer_id>/orders",
                 "customer_orders",
                 handlers.customer_orders,
                 methods=["GET"])

app.add_url_rule("/tables", "list_tables", handlers.list_tables, methods=["GET"])

app.add_url_rule("/reservations", "create_reservation",
                 handlers.create_reservation,
                 methods=["POST"])
app.add_url_rule("/reservations/<int:reservation_id>",
                 "get_reservation",
                 handlers.get_reservation,
                 methods=["GET"])

app.add_url_rule("/orders", "create_order",
                 handlers.create_order,
                 methods=["POST"])
app.add_url_rule("/orders/<int:order_id>",
                 "get_order",
                 handlers.get_order,
                 methods=["GET"])
app.add_url_rule("/orders/<int:order_id>/status",
                 "update_order_status",
                 handlers.update_order_status,
                 methods=["PATCH"])

if __name__ == "__main__":
    app.run(debug=True)