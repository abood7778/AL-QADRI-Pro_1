import cv2
import numpy as np
import time
import os

def apply_processing(input_path, output_path, action, params=None):
    start_time = time.time()
    try:
        # Validate input file
        if not input_path or not output_path:
            return False, "Invalid file paths provided", {
                "error_details": "Missing input or output path",
                "suggestions": ["Ensure file is properly uploaded"]
            }
        
        image = cv2.imread(input_path)
        if image is None:
            return False, "Could not load image", {
                "error_details": "Image file is corrupted or unsupported format",
                "suggestions": ["Try uploading a different image", "Ensure image is in PNG, JPEG, or other supported format"]
            }
        
        # Check image size for memory optimization
        height, width = image.shape[:2]
        if height * width > 10000000:  # 10MP limit
            # Resize large images to prevent memory issues
            scale = np.sqrt(10000000 / (height * width))
            new_width = int(width * scale)
            new_height = int(height * scale)
            image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
        processed_image = None

        if action == 'custom_filter':
            # Logic from lab4_custom_filter.py
            # Using a simple 3x3 mask
            mask = np.array([[1, 1, 1],
                             [1, 1, 1],
                             [1, 1, 1]], np.float32) / 9
            processed_image = cv2.filter2D(image, -1, mask)
            
        elif action == 'laplacian_edge_sharp1':
            # Logic from lab6_laplacian_edge_detection.py
            mask = np.array([[0, -1, 0],
                             [-1, 4, -1],
                             [0, -1, 0]])
            processed_image = cv2.filter2D(image, -1, mask)

        elif action == 'laplacian_edge_sharp2':
             # Logic from lab6_laplacian_edge_detection.py
            mask = np.array([[-1, -1, -1],
                             [-1, 8, -1],
                             [-1, -1, -1]])
            processed_image = cv2.filter2D(image, -1, mask)
            
        elif action == 'circle_detection':
            # Logic from lab7_circle_detection.py
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.medianBlur(gray, 5)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=120, param1=100, param2=30, minRadius=0, maxRadius=0)
            
            processed_image = image.copy()
            if circles is not None:
                circles = np.uint16(np.around(circles))
                for i in circles[0, :]:
                    # Draw the outer circle
                    cv2.circle(processed_image, (i[0], i[1]), i[2], (0, 255, 0), 2)
                    # Draw the center of the circle
                    cv2.circle(processed_image, (i[0], i[1]), 2, (0, 0, 255), 3)

        elif action == 'grayscale':
            processed_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Convert back to 3-channel for consistent saving
            processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)

        elif action == 'line_detection':
            # Enhanced line detection with configurable parameters and robust error handling
            if params is None:
                params = {}
            
            try:
                # Default parameters with validation
                threshold = max(10, min(100, params.get('threshold', 20)))
                min_line_length = max(10, min(200, params.get('min_line_length', 40)))
                max_line_gap = max(1, min(20, params.get('max_line_gap', 5)))
                canny_low = max(10, min(200, params.get('canny_low', 50)))
                canny_high = max(50, min(300, params.get('canny_high', 150)))
                
                # Ensure canny_high > canny_low
                if canny_high <= canny_low:
                    canny_high = canny_low + 50
                
                # Convert to grayscale with error handling
                if len(image.shape) == 3:
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                else:
                    gray = image.copy()
                
                # Apply noise reduction for better edge detection
                gray = cv2.GaussianBlur(gray, (3, 3), 0)
                
                # Edge detection with error handling
                edges = cv2.Canny(gray, canny_low, canny_high)
                
                # Check if edges were detected
                if np.sum(edges) == 0:
                    # No edges detected, try with lower thresholds
                    edges = cv2.Canny(gray, max(10, canny_low // 2), max(30, canny_high // 2))
                
                # Line detection
                lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi/180, 
                                      threshold=threshold, 
                                      minLineLength=min_line_length, 
                                      maxLineGap=max_line_gap)
                
                processed_image = image.copy()
                if lines is not None and len(lines) > 0:
                    for line in lines:
                        x1, y1, x2, y2 = line[0]
                        # Ensure coordinates are within image bounds
                        x1, y1 = max(0, min(image.shape[1]-1, x1)), max(0, min(image.shape[0]-1, y1))
                        x2, y2 = max(0, min(image.shape[1]-1, x2)), max(0, min(image.shape[0]-1, y2))
                        cv2.line(processed_image, (x1, y1), (x2, y2), (0, 255, 0), 2)
                else:
                    # No lines detected - this is not an error, just a result
                    lines = None
                    
            except Exception as line_error:
                print(f"Line detection error: {line_error}")
                return False, f"Line detection failed: {str(line_error)}", {
                    "error_details": "Failed to process image for line detection",
                    "suggestions": ["Try with a different image", "Ensure image has sufficient contrast"]
                }
        
        elif action.startswith('compress_'):
            # Enhanced compression with multiple quality levels and file size tracking
            try:
                # Extract quality level from action name
                quality_str = action.split('_')[1]
                quality = int(quality_str)
                
                # Get original file size
                original_size = os.path.getsize(input_path)
                
                # Force JPG for compression
                output_path = output_path.replace('.png', '.jpg')
                
                # Apply compression with specified quality
                cv2.imwrite(output_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
                processed_image = cv2.imread(output_path)  # Reload to confirm
                
                # Get compressed file size
                compressed_size = os.path.getsize(output_path)
                
                # Calculate compression ratio
                compression_ratio = round((1 - compressed_size / original_size) * 100, 1)
                
            except Exception as compress_error:
                print(f"Compression error: {compress_error}")
                return False, f"Compression failed: {str(compress_error)}", {
                    "error_details": "Failed to compress image",
                    "suggestions": ["Try with a different quality level", "Ensure image is valid"]
                }
        
        elif action == 'compress':
            # Legacy compress action - redirect to 50% quality
            try:
                # Get original file size
                original_size = os.path.getsize(input_path)
                
                # Force JPG for compression
                output_path = output_path.replace('.png', '.jpg')
                cv2.imwrite(output_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), 50])
                processed_image = cv2.imread(output_path)  # Reload to confirm
                
                # Get compressed file size
                compressed_size = os.path.getsize(output_path)
                compression_ratio = round((1 - compressed_size / original_size) * 100, 1)
                
            except Exception as compress_error:
                print(f"Compression error: {compress_error}")
                return False, f"Compression failed: {str(compress_error)}", {}

        elif action == 'corner_detection':
            # Logic from lab7_corner_detection.py
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            corners = cv2.goodFeaturesToTrack(gray, maxCorners=100, qualityLevel=0.01, minDistance=10)
            processed_image = image.copy()
            if corners is not None:
                corners = np.intp(corners)
                for c in corners:
                    x, y = c.ravel()
                    cv2.circle(processed_image, (x, y), 4, (0, 255, 0), -1)

        elif action == 'dilate':
            # Logic from lab8_dilate_erode.py
            kernel = np.ones((5, 5), np.uint8)
            processed_image = cv2.morphologyEx(image, cv2.MORPH_DILATE, kernel)
        
        elif action == 'erode':
            # Logic from lab8_dilate_erode.py
            kernel = np.ones((5, 5), np.uint8)
            processed_image = cv2.morphologyEx(image, cv2.MORPH_ERODE, kernel)
            
        elif action == 'morph_gradient':
            # Logic from lab8_dilate_erode.py
            kernel = np.ones((5, 5), np.uint8)
            processed_image = cv2.morphologyEx(image, cv2.MORPH_GRADIENT, kernel)

        else:
            print(f"Unknown action: {action}")
            return False, "Unknown action", {
                "error_details": f"Action '{action}' is not supported",
                "suggestions": ["Try using a different processing option", "Check if the feature is available"]
            }

        if processed_image is not None or action == 'compress' or action.startswith('compress_'):
            if action != 'compress' and not action.startswith('compress_'):
                # Ensure image is in correct format for saving
                if len(processed_image.shape) == 2:
                    # Convert grayscale to BGR for consistent saving
                    processed_image = cv2.cvtColor(processed_image, cv2.COLOR_GRAY2BGR)
                cv2.imwrite(output_path, processed_image)
            
            # Calculate processing time
            processing_time = round(time.time() - start_time, 2)
            
            # Prepare details
            details = {
                "action": action,
                "output_path": output_path,
                "image_size": f"{image.shape[1]}x{image.shape[0]}",
                "channels": processed_image.shape[2] if len(processed_image.shape) > 2 else 1,
                "processing_time": f"{processing_time}s"
            }
            
            message = "Processing successful"
            if action == 'circle_detection':
                count = 0 if circles is None else circles.shape[1]
                details['circles_detected'] = count
                message = f"Detected {count} circles"
            elif action == 'corner_detection':
                count = 0 if corners is None else len(corners)
                details['corners_detected'] = count
                message = f"Detected {count} corners"
            elif action == 'line_detection':
                count = 0 if lines is None else len(lines)
                details['lines_detected'] = count
                details['threshold'] = threshold
                details['min_line_length'] = min_line_length
                details['max_line_gap'] = max_line_gap
                details['canny_thresholds'] = f"{canny_low}-{canny_high}"
                message = f"Detected {count} lines"
            elif action == 'compress':
                message = "Compressed to JPEG (50% Quality)"
                details['compression'] = "50%"
                details['original_size'] = f"{round(original_size / 1024, 1)} KB"
                details['compressed_size'] = f"{round(compressed_size / 1024, 1)} KB"
                details['size_reduction'] = f"{compression_ratio}%"
            elif action.startswith('compress_'):
                quality = action.split('_')[1]
                message = f"Compressed to JPEG ({quality}% Quality)"
                details['compression'] = f"{quality}%"
                details['original_size'] = f"{round(original_size / 1024, 1)} KB"
                details['compressed_size'] = f"{round(compressed_size / 1024, 1)} KB"
                details['size_reduction'] = f"{compression_ratio}%"
            elif action == 'custom_filter':
                message = "Applied Low-Pass 3x3 Filter"
            elif 'laplacian' in action:
                message = "Applied Laplacian Sharpening"
                
            return True, message, details
            
        return False, "Processing failed", {
            "error_details": "Image processing completed but no result was generated",
            "suggestions": ["Try with a different image", "Check if the selected operation is appropriate for this image"]
        }

        
    except Exception as e:
        print(f"Processing error: {e}")
        return False, f"Processing error: {str(e)}", {
            "error_details": "An unexpected error occurred during processing",
            "suggestions": ["Try uploading a different image", "Contact support if the problem persists"]
        }
