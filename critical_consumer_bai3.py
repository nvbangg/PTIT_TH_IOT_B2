import pika

EXCHANGE = "iot_alert_exchange"
QUEUE = "critical_queue"
ROUTING_KEY = "critical"
LOG_FILE = "alerts.log"

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct")
channel.queue_declare(queue=QUEUE)
channel.queue_bind(exchange=EXCHANGE, queue=QUEUE, routing_key=ROUTING_KEY)


def callback(ch, method, properties, body):
    msg = body.decode()
    line = f"[{QUEUE}] Da nhan: {msg}"
    print(line)
    with open(LOG_FILE, "a", encoding="utf-8") as f:  # mo rong: ghi log ra file
        f.write(line + "\n")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(queue=QUEUE, on_message_callback=callback)
print(f"[{QUEUE}] Dang cho canh bao '{ROUTING_KEY}'. Nhan CTRL+C de thoat.")
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
    connection.close()
