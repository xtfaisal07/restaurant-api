from flask import jsonify, request
from datetime import datetime
from db import get_db

def home():
    return {"message": "Restaurant API Running"}

def list_menu():
    conn = get_db()
    rows = conn.execute("""
        SELECT mc.name AS category, mi.id, mi.name,
               mi.description, mi.price_cents
        FROM menu_categories mc
        JOIN menu_items mi ON mc.id = mi.category_id
        WHERE mi.available = 1
        ORDER BY mc.sort_order, mi.id
    """).fetchall()
    conn.close()

    result = {}
    for r in rows:
        result.setdefault(r["category"], []).append({
            "id": r["id"],
            "name": r["name"],
            "description": r["description"],
            "price_cents": r["price_cents"]
        })
    return jsonify(result)

def get_menu_item(item_id):
    conn = get_db()
    item = conn.execute("""
        SELECT mi.id, mc.name AS category, mi.name,
               mi.description, mi.price_cents, mi.available
        FROM menu_items mi
        JOIN menu_categories mc ON mc.id = mi.category_id
        WHERE mi.id=?
    """, (item_id,)).fetchone()
    conn.close()

    if not item:
        return jsonify({"error":"Menu item not found"}),404

    return jsonify(dict(item))

def create_customer():
    data=request.get_json()
    conn=get_db()

    dup=conn.execute(
        "SELECT id FROM customers WHERE email=?",
        (data["email"],)
    ).fetchone()

    if dup:
        conn.close()
        return jsonify({"error":"Email already exists"}),409

    cur=conn.execute("""
        INSERT INTO customers(name,email,phone)
        VALUES(?,?,?)
    """,(data["name"],data["email"],data["phone"]))

    conn.commit()

    customer=conn.execute(
        "SELECT * FROM customers WHERE id=?",
        (cur.lastrowid,)
    ).fetchone()

    conn.close()
    return jsonify(dict(customer)),201

def list_tables():
    conn=get_db()
    tables=conn.execute("""
        SELECT id,label,seats
        FROM dining_tables
        WHERE active=1
        ORDER BY seats,label
    """).fetchall()
    conn.close()
    return jsonify([dict(t) for t in tables])

def create_reservation():
    data=request.get_json()
    conn=get_db()

    table=conn.execute(
        "SELECT seats,active FROM dining_tables WHERE id=?",
        (data["dining_table_id"],)
    ).fetchone()

    if not table:
        conn.close()
        return jsonify({"error":"Table not found"}),404

    if data["party_size"]>table["seats"]:
        conn.close()
        return jsonify({"error":"Party size exceeds table capacity"}),400

    dup=conn.execute("""
        SELECT id FROM reservations
        WHERE dining_table_id=?
        AND reservation_time=?
        AND status='BOOKED'
    """,(data["dining_table_id"],data["reservation_time"])).fetchone()

    if dup:
        conn.close()
        return jsonify({"error":"Table already reserved for this time"}),409

    cur=conn.execute("""
        INSERT INTO reservations(
            customer_id,dining_table_id,
            reservation_time,party_size,status)
        VALUES(?,?,?,?, 'BOOKED')
    """,(
        data["customer_id"],
        data["dining_table_id"],
        data["reservation_time"],
        data["party_size"]
    ))

    conn.commit()

    res=conn.execute(
        "SELECT * FROM reservations WHERE id=?",
        (cur.lastrowid,)
    ).fetchone()

    conn.close()
    return jsonify(dict(res)),201

def get_reservation(reservation_id):
    conn=get_db()
    res=conn.execute("SELECT * FROM reservations WHERE id=?",(reservation_id,)).fetchone()
    conn.close()

    if not res:
        return jsonify({"error":"Reservation not found"}),404

    return jsonify(dict(res))

def create_order():
    data=request.get_json()
    conn=get_db()

    try:
        conn.execute("BEGIN")
        cur=conn.execute("""
            INSERT INTO orders(
                customer_id,dining_table_id,
                reservation_id,status,total_cents,created_at)
            VALUES(?,?,?,'NEW',0,?)
        """,(
            data["customer_id"],
            data["dining_table_id"],
            data.get("reservation_id"),
            datetime.now().isoformat()
        ))

        order_id=cur.lastrowid
        total=0

        for i in data["items"]:
            menu=conn.execute("""
                SELECT price_cents,available
                FROM menu_items WHERE id=?
            """,(i["menu_item_id"],)).fetchone()

            if not menu or menu["available"]==0:
                raise Exception("Menu item unavailable")

            line=i["quantity"]*menu["price_cents"]
            total+=line

            conn.execute("""
                INSERT INTO order_items(
                    order_id,menu_item_id,quantity,
                    unit_price_cents,line_total_cents)
                VALUES(?,?,?,?,?)
            """,(
                order_id,
                i["menu_item_id"],
                i["quantity"],
                menu["price_cents"],
                line
            ))

        conn.execute(
            "UPDATE orders SET total_cents=? WHERE id=?",
            (total,order_id)
        )

        conn.commit()
        return jsonify({
            "order_id":order_id,
            "status":"NEW",
            "total_cents":total
        }),201

    except Exception as e:
        conn.rollback()
        return jsonify({"error":str(e)}),400

    finally:
        conn.close()

def get_order(order_id):
    conn=get_db()
    order=conn.execute("SELECT * FROM orders WHERE id=?",(order_id,)).fetchone()

    if not order:
        conn.close()
        return jsonify({"error":"Order not found"}),404

    items=conn.execute("""
        SELECT oi.menu_item_id,mi.name,
               oi.quantity,
               oi.unit_price_cents,
               oi.line_total_cents
        FROM order_items oi
        JOIN menu_items mi ON mi.id=oi.menu_item_id
        WHERE order_id=?
    """,(order_id,)).fetchall()

    conn.close()

    return jsonify({
        **dict(order),
        "items":[dict(i) for i in items]
    })

def update_order_status(order_id):
    data=request.get_json()
    conn=get_db()

    order=conn.execute(
        "SELECT status FROM orders WHERE id=?",
        (order_id,)
    ).fetchone()

    if not order:
        conn.close()
        return jsonify({"error":"Order not found"}),404

    allowed={
        "NEW":["PREPARING","CANCELLED"],
        "PREPARING":["READY"],
        "READY":["COMPLETED"],
        "COMPLETED":[],
        "CANCELLED":[]
    }

    if data["status"] not in allowed[order["status"]]:
        conn.close()
        return jsonify({"error":"Invalid transition"}),409

    conn.execute(
        "UPDATE orders SET status=? WHERE id=?",
        (data["status"],order_id)
    )

    conn.commit()
    conn.close()

    return jsonify({"new_status":data["status"]})

def customer_orders(customer_id):
    conn = get_db()

    # Check customer exists
    customer = conn.execute("""
        SELECT id, name, email, phone
        FROM customers
        WHERE id = ?
    """, (customer_id,)).fetchone()

    if not customer:
        conn.close()
        return jsonify({"error": "Customer not found"}), 404

    # Get customer's orders
    orders = conn.execute("""
        SELECT
            o.id,
            o.status,
            o.total_cents,
            o.created_at,
            dt.label AS table_label
        FROM orders o
        LEFT JOIN dining_tables dt
            ON o.dining_table_id = dt.id
        WHERE o.customer_id = ?
        ORDER BY o.created_at DESC
    """, (customer_id,)).fetchall()

    conn.close()

    return jsonify({
        "customer": dict(customer),
        "orders": [dict(order) for order in orders]
    })