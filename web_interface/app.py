import os
from flask import Flask, render_template, request, jsonify, send_from_directory, url_for
import cv2
import numpy as np
from processor import apply_processing
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        filename = str(uuid.uuid4()) + ".png" # Save all as PNG for simplicity
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'filename': filename, 'url': url_for('static', filename=f'uploads/{filename}')})

@app.route('/download/<filename>')
def download_file(filename):
    """Secure download endpoint for processed images"""
    try:
        # Validate filename to prevent directory traversal
        if '..' in filename or '/' in filename or '\\' in filename:
            return jsonify({'error': 'Invalid filename'}), 400
        
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Determine file extension for proper content type
        if filename.lower().endswith('.jpg') or filename.lower().endswith('.jpeg'):
            mimetype = 'image/jpeg'
        elif filename.lower().endswith('.png'):
            mimetype = 'image/png'
        else:
            mimetype = 'application/octet-stream'
        
        return send_from_directory(
            app.config['UPLOAD_FOLDER'], 
            filename, 
            as_attachment=True,
            download_name=f"processed_image.{filename.split('.')[-1]}",
            mimetype=mimetype
        )
    except Exception as e:
        print(f"Download error: {e}")
        return jsonify({'error': 'Download failed'}), 500

@app.route('/process', methods=['POST'])
def process_image():
    data = request.json
    filename = data.get('filename')
    action = data.get('action')
    params = data.get('params', {})
    
    if not filename or not action:
        return jsonify({'error': 'Missing filename or action'}), 400
    
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(input_path):
        return jsonify({'error': 'File not found'}), 404
        
    try:
        # Generate new filename for result - handle compression extension
        if action.startswith('compress_') or action == 'compress':
            # For compression, change extension to .jpg
            base_filename = filename.rsplit('.', 1)[0]  # Remove extension
            output_filename = f"processed_{action}_{base_filename}.jpg"
        else:
            output_filename = f"processed_{action}_{filename}"
        
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Apply processing logic
        success, message, details = apply_processing(input_path, output_path, action, params)
        
        if success:
            return jsonify({
                'status': 'success',
                'url': url_for('static', filename=f'uploads/{output_filename}'),
                'message': message,
                'details': details
            })
        else:
            return jsonify({'error': message}), 500
            
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
