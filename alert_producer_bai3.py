import pika

EXCHANGE = "iot_alert_exchange"

ALERTS = [
    ("info", "Nhiet do phong may binh thuong"),
    ("warning", "Nhiet do phong may vuot nguong warning"),
    ("critical", "Cam bien kho lanh mat ket noi critical"),
]

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# dinh tuyen theo routing key khop chinh xac
channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct")

for level, text in ALERTS:
    channel.basic_publish(exchange=EXCHANGE, routing_key=level, body=text)
    print(f"[producer] Da gui [{level}]: {text}")

connection.close()
