import time
import pika

BROKER = "localhost"
QUEUE = "iot_lab_queue"
HO_TEN = "Nguyễn Văn Bằng"
MA_SV = "B23DCCN067"
LOI_CHAO = "Xin chao tu ung dung Python AMQP"

connection = pika.BlockingConnection(pika.ConnectionParameters(host=BROKER))
channel = connection.channel()
channel.queue_declare(queue=QUEUE)

try:
    # Mở rộng: gửi nhiều message liên tiếp
    while True:
        message = f"{LOI_CHAO} - {MA_SV} - {HO_TEN}"
        channel.basic_publish(exchange="", routing_key=QUEUE, body=message.encode("utf-8"))
        print(f"Da gui message: {message}")
        time.sleep(5)

except KeyboardInterrupt:
    print("\nKet thuc Producer")
finally:
    if connection.is_open:
        connection.close()