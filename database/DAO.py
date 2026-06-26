from database.DB_connect import DBConnect
from model.order import Order

from model.store import Store


class DAO():

    @staticmethod
    def getAllStores():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from stores"

        cursor.execute(query)

        for row in cursor:
            results.append(Store(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllOrders():
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * from orders"

        cursor.execute(query)

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllNodes(id: int):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select * from orders 
                    where store_id=%s"""

        cursor.execute(query, (id,))

        for row in cursor:
            results.append(Order(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getAllWeightedEdges(id: int, k: int, idMapOrders: dict):
        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """with ordernum as (select oi.order_id, sum(oi.quantity) as num
                                    from order_items oi
                                    join orders o on oi.order_id = o.order_id
                                    where o.store_id=%s
                                    group by order_id)		
                    select o1.order_id as id1, on1.num as num1, o2.order_id as id2, on2.num as num2, datediff(o2.order_date, o1.order_date) as diff
                    from ordernum on1, ordernum on2, orders o1, orders o2
                    where o1.order_id<o2.order_id
                    and on1.order_id=o1.order_id and on2.order_id=o2.order_id
                    group by id1, num1, id2, num2
                    having diff<=%s and diff>0"""

        cursor.execute(query, (id, k,))

        for row in cursor:
            results.append((idMapOrders[row["id1"]], int(row["num1"]),
                            idMapOrders[row["id2"]], int(row["num2"]),int(row["diff"])))
            # tuple ordine1, q1, ordine2, q2, giorni

        cursor.close()
        conn.close()
        return results