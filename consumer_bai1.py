from datetime import datetime
import pika

BROKER = "localhost"
QUEUE = "iot_lab_queue"

def on_message(ch, method, properties, body):
    message = body.decode("utf-8")
    thoi_gian = datetime.now().strftime("%H:%M:%S")

    print(f"Da nhan message: {message}")
    print(f"Thoi gian nhan: {thoi_gian}\n")

connection = pika.BlockingConnection(pika.ConnectionParameters(host=BROKER))
channel = connection.channel()

# Đảm bảo queue đã tồn tại trước khi lắng nghe
channel.queue_declare(queue=QUEUE)
channel.basic_consume(queue=QUEUE, on_message_callback=on_message, auto_ack=True)
print(f"Dang lang nghe queue: {QUEUE}...")

try:
    # Mở rộng: chạy liên tục cho tới khi dừng bằng Ctrl+C
    channel.start_consuming()
except KeyboardInterrupt:
    print("\nKet thuc Consumer")
finally:
    if connection.is_open:
        connection.close()
