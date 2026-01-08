import unittest
import os
import shutil
from app import app
import cv2
import numpy as np

class TestWebApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = 'static/uploads_test'
        self.client = app.test_client()
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        # Create a dummy image
        self.test_img_path = os.path.join(app.config['UPLOAD_FOLDER'], 'test.png')
        self.img = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imwrite(self.test_img_path, self.img)

    def tearDown(self):
        if os.path.exists(app.config['UPLOAD_FOLDER']):
            shutil.rmtree(app.config['UPLOAD_FOLDER'])

    def test_index_route(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Image Processor', response.data)

    def test_upload_route(self):
        with open(self.test_img_path, 'rb') as img:
            data = {'file': (img, 'test.png')}
            response = self.client.post('/upload', data=data, content_type='multipart/form-data')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'filename', response.data)

    def test_process_route_failure(self):
        # Test processing non-existent file
        data = {'filename': 'nonexistent.png', 'action': 'grayscale'}
        response = self.client.post('/process', json=data)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
