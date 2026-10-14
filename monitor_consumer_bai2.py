import json
import pika

BROKER = "localhost"
QUEUE = "sensor_data_queue"


def on_message(ch, method, properties, body):
    try:
        data = json.loads(body.decode("utf-8"))
        device_id = data.get("device_id", "Unknown")
        temperature = data.get("temperature")
        humidity = data.get("humidity")
        timestamp = data.get("timestamp")

        print(f"Device: {device_id}")
        if timestamp:
            print(f"Timestamp: {timestamp}")
        print(f"Temperature: {temperature}")
        print(f"Humidity: {humidity}")

        # Kiểm tra ngưỡng cảnh báo theo yêu cầu đề bài
        if temperature is not None and temperature > 35:
            print("CANH BAO: Nhiet do cao")
        if humidity is not None and humidity < 40:
            print("CANH BAO: Do am thap")

        print("-" * 35)
    except json.JSONDecodeError:
        print(f"[!] Khong the parse JSON tu message: {body}")
    except Exception as e:
        print(f"[!] Loi xu ly message: {e}")


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=BROKER))
    channel = connection.channel()

    # Đảm bảo queue đã tồn tại trước khi lắng nghe
    channel.queue_declare(queue=QUEUE)
    channel.basic_consume(queue=QUEUE, on_message_callback=on_message, auto_ack=True)

    print(f"[*] Monitoring Consumer da ket noi toi RabbitMQ ({BROKER})")
    print(f"[*] Dang lang nghe queue: {QUEUE} (Nhan Ctrl+C de thoat)...")
    print("=" * 35)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\n[!] Ket thuc Monitoring Consumer")
    finally:
        if connection.is_open:
            connection.close()


if __name__ == "__main__":
    main()
