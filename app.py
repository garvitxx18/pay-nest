from flask import Flask, request, jsonify
import pika
import threading
import queue
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)

# Shared queues to pass OTPs between threads
platform_otp_queue = queue.Queue()
credit_card_otp_queue = queue.Queue()

# RabbitMQ consumer to consume OTP asynchronously
def consume_otp(queue_name, otp_queue):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        otp = body.decode()
        print(f" [x] Received OTP from {queue_name}: {otp}")
        # Put the OTP into the shared queue
        otp_queue.put(otp)

    # Set up consumption of the queue
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(f' [*] Waiting for OTP messages from {queue_name}. To exit press CTRL+C')
    channel.start_consuming()

# Flask route to publish platform OTP
@app.route('/send-otp', methods=['POST'])
def send_otp():
    try:
        data = request.json
        otp_value = data.get('otp')

        if otp_value:
            publish_otp('otp_queue', otp_value)
            return jsonify({"message": "OTP published successfully", "otp": otp_value}), 200
        else:
            return jsonify({"error": "No OTP provided in the request body"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask route to publish credit card OTP
@app.route('/send-cc-otp', methods=['POST'])
def send_credit_card_otp():
    try:
        data = request.json
        otp_value = data.get('otp')

        if otp_value:
            publish_otp('credit_card_otp_queue', otp_value)
            return jsonify({"message": "Credit card OTP published successfully", "otp": otp_value}), 200
        else:
            return jsonify({"error": "No OTP provided in the request body"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# RabbitMQ publisher to publish OTP to the respective queue
def publish_otp(queue_name, otp_value):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    channel.basic_publish(exchange='',
                          routing_key=queue_name,
                          body=otp_value)
    print(f" [x] Sent OTP to {queue_name}: {otp_value}")

    connection.close()

# Flask route to consume platform OTP
@app.route('/consume-otp', methods=['GET'])
def consume_otp_endpoint():
    try:
        # Start the OTP consumer in a separate thread for platform OTP
        threading.Thread(target=consume_otp, args=('otp_queue', platform_otp_queue)).start()

        print("Waiting for OTP...")
        # Wait for OTP from the queue (with a timeout to avoid indefinite waiting)
        otp = platform_otp_queue.get(timeout=60)  # Timeout in seconds

        return jsonify(otp)

    except queue.Empty:
        return jsonify({"error": "Timeout waiting for OTP"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Flask route to consume credit card OTP
@app.route('/consume-cc-otp', methods=['GET'])
def consume_credit_card_otp_endpoint():
    try:
        # Start the OTP consumer in a separate thread for credit card OTP
        threading.Thread(target=consume_otp, args=('credit_card_otp_queue', credit_card_otp_queue)).start()

        print("Waiting for Credit Card OTP...")
        # Wait for OTP from the queue (with a timeout to avoid indefinite waiting)
        otp = credit_card_otp_queue.get(timeout=60)  # Timeout in seconds

        return jsonify(otp)

    except queue.Empty:
        return jsonify({"error": "Timeout waiting for OTP"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
