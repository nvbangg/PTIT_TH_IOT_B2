## Bài 1

Môi trường: Python 3.x, [Erlang](https://github.com/erlang/otp/releases/tag/OTP-28.5.0.7), [RabbitMQ](https://github.com/rabbitmq/rabbitmq-server/releases/latest), `pika` (`python -m pip install pika`).

Broker: `localhost:5672`; queue: `iot_lab_queue` (`durable=True`).

### Cách chạy

1. Đảm bảo RabbitMQ đang chạy.
2. Mở terminal tại thư mục project, chạy consumer:
   ```powershell
   python consumer_bai1.py
   ```
3. Mở terminal thứ hai tại cùng thư mục, chạy producer:
   ```powershell
   python producer_bai1.py
   ```
4. Producer gửi mỗi 5 giây. Nhấn `Ctrl+C` ở từng terminal để dừng.

### Kết quả chạy thực tế

Producer:

```text
Da gui message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
Da gui message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
Da gui message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
Da gui message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng

Ket thuc Producer
```

Consumer:

```text
Dang lang nghe queue: iot_lab_queue...
Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
Thoi gian nhan: 21:00:44

Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
Thoi gian nhan: 21:00:49

Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
Thoi gian nhan: 21:00:54

Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN067 - Nguyễn Văn Bằng
Thoi gian nhan: 21:00:59


Ket thuc Consumer
```

