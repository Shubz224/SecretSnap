from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import os
from encryption import encrypt_message, decrypt_message

app = Flask(__name__)

# Configurations
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')  # Make sure you have an index.html

@app.route('/encrypt', methods=['POST'])
def encrypt():
    image = request.files.get('image')
    key = request.form.get('key')
    message = request.form.get('message')

    if image and key and message:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        # Call the encryption function
        encrypted_image_path = encrypt_message(image_path, key, message)

        # Return the encrypted image as a download
        return send_file(encrypted_image_path, as_attachment=True, download_name="encrypted_image.png")

    return "Error: Missing image or key/message", 400

@app.route('/decrypt', methods=['POST'])
def decrypt():
    image = request.files.get('image')
    key = request.form.get('key')

    if image and key:
        filename = secure_filename(image.filename)
        image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(image_path)

        # Call the decryption function to extract the hidden message
        hidden_message = decrypt_message(image_path, key)

        return f"Decrypted message: {hidden_message}"

    return "Error: Missing image or key", 400

if __name__ == '__main__':
    app.run(debug=True)
