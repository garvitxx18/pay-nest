from flask import Flask, request, jsonify  # Added 'request'
import pika
import threading
import queue

app = Flask(__name__)

# Shared queue to pass OTP between threads
otp_queue = queue.Queue()

# RabbitMQ consumer to consume OTP asynchronously
def consume_otp():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='otp_queue')

    def callback(ch, method, properties, body):
        otp = body.decode()
        print(f" [x] Received OTP: {otp}")
        # Put the OTP into the shared queue
        otp_queue.put(otp)

    # Set up consumption of the queue
    channel.basic_consume(queue='otp_queue', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for OTP messages. To exit press CTRL+C')
    channel.start_consuming()


# Flask route to publish OTP
@app.route('/send-otp', methods=['POST'])
def send_otp():
    try:
        data = request.json  # Using 'request' to get the POST data
        otp_value = data.get('otp')

        if otp_value:
            publish_otp(otp_value)
            return jsonify({"message": "OTP published successfully", "otp": otp_value}), 200
        else:
            return jsonify({"error": "No OTP provided in the request body"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# RabbitMQ publisher to publish OTP
def publish_otp(otp_value):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='otp_queue')

    channel.basic_publish(exchange='',
                          routing_key='otp_queue',
                          body=otp_value)
    print(f" [x] Sent OTP: {otp_value}")

    connection.close()


@app.route('/consume-otp', methods=['GET'])
def consume_otp_endpoint():
    try:
        # Start the OTP consumer in a separate thread
        threading.Thread(target=consume_otp).start()

        print("Waiting for OTP...")
        # Wait for OTP from the queue (with a timeout to avoid indefinite waiting)
        otp = otp_queue.get(timeout=60)  # Timeout in seconds

        return jsonify({"otp": otp}), 200

    except queue.Empty:
        return jsonify({"error": "Timeout waiting for OTP"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
