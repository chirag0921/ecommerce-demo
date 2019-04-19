
from fabric.api import *
from flask import Flask,render_template,jsonify,json,request
from fabric.api import *

import pymysql
import json

connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='ecommerce-app',
)

application = Flask(__name__)


@application.route("/addItem", methods=['POST'])
def addItem():
    try:
        json_data = request.json['info']
        itemName = json_data['item_name']
        itemPrice = json_data['item_price']
        itemQuantity = json_data['item_quantity']

        with connection.cursor() as cursor:
            sql = "INSERT INTO items (`name`, `price`, `quantity`) VALUES (%s, %s, %s)"

            cursor.execute(sql, (itemName, itemPrice, itemQuantity))
            return jsonify(status='OK', message='Inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route('/getItem', methods=['POST'])
def getItem():
    try:
        itemId = request.json['item_id']
        with connection.cursor() as cursor:
            sql = "SELECT * from items where id="+str(itemId)+""
            cursor.execute(sql)
            data = cursor.fetchone()
            if data is None:
                return jsonify(status='ERROR', message='Item is not exist')
            else:
                itemData = {
                        'item_id': data[0],
                        'item_name': data[1],
                        'item_price': data[2],
                        'item_quantity': data[3],
                        }
                return json.dumps(itemData)

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route('/updateItem', methods=['POST'])
def updateItem():
    try:
        json_data = request.json['info']
        itemId = json_data['item_id']
        itemName = json_data['item_name']
        itemPrice = json_data['item_price']
        itemQuantity = json_data['item_quantity']
        with connection.cursor() as cursor:
            sql = "UPDATE items SET name = '"+str(itemName)+"', price = "+str(itemPrice)+",  " \
                        "quantity = "+str(itemQuantity)+" WHERE id = "+str(itemId)+""

            cursor.execute(sql)
            return jsonify(status='OK', message='Item updated')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route("/getItemList", methods=['POST'])
def getItemList():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from items"
            cursor.execute(sql)
            data = cursor.fetchall()
            if data is None:
                return jsonify(status='ERROR', message='Items is not exist')
            else:
                itemList = []
                for dt in data:
                    itemData = {
                            'item_id': dt[0],
                            'item_name': dt[1],
                            'item_price': dt[2],
                            'item_quantity': dt[3],
                            }
                    itemList.append(itemData)
                return json.dumps(itemList)

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route("/deleteItem", methods=['POST'])
def deleteItem():
    try:
        itemId = request.json['item_id']

        with connection.cursor() as cursor:
            sql = "DELETE FROM items WHERE id="+str(itemId)+""

            cursor.execute(sql)
            return jsonify(status='OK', message='Item deleted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


#---------------Order Apis------------------------------------------------------------------------------------------


@application.route("/placeOrder", methods=['POST'])
def placeOrder():
    try:
        json_data = request.json['info']
        itemId = json_data['item_id']
        itemQuantity = json_data['item_quantity']
        userEmail = json_data['user_email']

        with connection.cursor() as cursor:
            sql = "SELECT quantity from items where id="+str(itemId)+""

            cursor.execute(sql)
            data = cursor.fetchone()
            if data is None:
                return jsonify(status='ERROR', message='Item is not exist')
            else:
                availquant = int(str(data[0]))
                orderquant = int(itemQuantity)
                if availquant < orderquant:
                    return jsonify(status='ERROR', message='Specified number of quantity is not available')
                else:
                    sql = "UPDATE items SET quantity = " + str(availquant - orderquant) + " WHERE id = " + str(itemId) + ""
                    cursor.execute(sql)

                    sql = "INSERT INTO orders (`itemid`, `quantity`, `useremail`) VALUES (%s, %s, %s)"

                    cursor.execute(sql, (itemId, itemQuantity, userEmail))
                    return jsonify(status='OK', message='Inserted successfully')

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route('/getOrder', methods=['POST'])
def getOrder():
    try:
        orderId = request.json['order_id']
        with connection.cursor() as cursor:
            sql = "SELECT * from orders where id='"+orderId+"'"

            cursor.execute(sql)
            data = cursor.fetchone()
            if data is None:
                return jsonify(status='ERROR', message='Order is not exist')
            else:
                orderData = {
                        'order_id': data[0],
                        'item_id': data[1],
                        'item_quantity': data[2],
                        'user_email': data[3],
                        }
                return json.dumps(orderData)

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


@application.route("/getOrderList", methods=['POST'])
def getOrderList():
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * from orders"

            cursor.execute(sql)
            data = cursor.fetchall()
            if data is None:
                return jsonify(status='OK', message='No order available')
            else:
                orderList = []
                for dt in data:
                    orderData = {
                            'order_id': dt[0],
                            'item_id': dt[1],
                            'item_quantity': dt[2],
                            'user_email': dt[3],
                            }
                    orderList.append(orderData)

                return json.dumps(orderList)

    except Exception as e:
        return jsonify(status='ERROR', message=str(e))


if __name__ == "__main__":
    application.run(host='0.0.0.0')
