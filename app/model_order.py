
# Order Component
from app import mongo

class Order:

    @staticmethod
    def view_order():
        order_list =[]
        
        

        try:
            order_data = list(mongo.db.order_data.find({}))
            for order in order_data:
                
                    order_dict = {
                    "id": order.get("id"),
                    "orderdate": order.get("orderdate"),
                    "webinardate": order.get("webinardate"),
                    "topic": order.get("topic"),
                    "session": order.get("session", []),  # Array, defaults to an empty list if not found
                    "customername": order.get("customername"),
                    "customeremail": order.get("customeremail"),
                    "billingemail": order.get("billingemail"),
                    "orderamount": order.get("orderamount"),
                    "paymentstatus": order.get("paymentstatus"),
                    "country": order.get("country"),
                    "state": order.get("state"),
                    "city": order.get("city"),
                    "zipcode": order.get("zipcode"),
                    "address": order.get("address"),
                    "document": order.get("document"),
                    "website": order.get("website")
                }

                    order_list.append(order_dict)
    
        except Exception as e:
            order_list = {"error": str(e)}
        
        return order_list
        

    @staticmethod
    def order_data(o_id):
        order_dict={}
        try:
            order_data = list(mongo.db.order_data.find({"id": o_id}))
            order = order_data[0]
            order_dict = {
                "id": order.get("id"),
                "orderdate": order.get("orderdate"),
                "webinardate": order.get("webinardate"),
                "topic": order.get("topic"),
                "session": order.get("session"), # Array
                "customername": order.get("customerName"),
                "customeremail": order.get("customerEmail"),
                "billingemail": order.get("billingEmail"),
                "orderamount": order.get("orderamount"),
                "paymentstatus": order.get("paymentstatus"),
                "country" : order.get("country"),
                "state" : order.get("state"),
                "city" : order.get("city"),
                "zipcode" : order.get("zipcode"),
                "address": order.get("address"),
                "document": order.get("document"),
                "website" : order.get("website")

            }

        except Exception as e:
            order_dict = {}
            
        return order_dict
        
