document.addEventListener('DOMContentLoaded', () => {
    // State
    let currentFile = null;
    let currentFilename = null;
    let currentLang = 'en';

    // Elements
    const dropZone = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    const previewArea = document.getElementById('preview-area');
    const originalImg = document.getElementById('original-image');
    const processedImg = document.getElementById('processed-image');
    const loader = document.getElementById('loader');
    const detailsPanel = document.getElementById('details-panel');
    const actionBar = document.getElementById('action-bar');
    const downloadBtn = document.getElementById('download-btn');
    const resetBtn = document.getElementById('reset-btn');
    const langToggle = document.getElementById('lang-toggle');
    const langLabel = document.getElementById('lang-label');
    const toolBtns = document.querySelectorAll('.tool-btn');
    const canvasContainer = document.querySelector('.canvas-container');
    
    // Compression slider
    const compressionSlider = document.getElementById('compression-slider');
    const qualityValue = document.getElementById('quality-value');
    const compressBtn = document.getElementById('compress-btn');

    // Compression slider handler
    compressionSlider.addEventListener('input', (e) => {
        qualityValue.textContent = e.target.value + '%';
    });

    // Drag & Drop on canvas container
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        canvasContainer.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        canvasContainer.addEventListener(eventName, () => {
            dropZone.classList.add('dragover');
        }, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        canvasContainer.addEventListener(eventName, () => {
            dropZone.classList.remove('dragover');
        }, false);
    });

    canvasContainer.addEventListener('drop', (e) => {
        const dt = e.dataTransfer;
        const files = dt.files;
        if (files.length > 0) {
            uploadFile(files[0]);
        }
    }, false);

    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) {
            uploadFile(this.files[0]);
        }
    });

    // Upload Logic
    async function uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        loader.classList.remove('hidden');

        try {
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });

            if (response.ok) {
                const data = await response.json();
                currentFilename = data.filename;

                originalImg.src = data.url;
                processedImg.src = data.url;

                dropZone.classList.add('hidden');
                previewArea.classList.remove('hidden');
                actionBar.classList.remove('hidden');
                detailsPanel.classList.add('hidden');

                toolBtns.forEach(b => b.classList.remove('active'));
            } else {
                alert(translations[currentLang].error_upload);
            }
        } catch (error) {
            console.error('Error:', error);
            alert(translations[currentLang].error_upload);
        } finally {
            loader.classList.add('hidden');
        }
    }

    // Tool/Filter Logic
    toolBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const action = btn.dataset.action;
            
            if (!currentFilename) return;

            // Handle compress button with slider value
            if (action === 'compress') {
                const quality = compressionSlider.value;
                processImage(`compress_${quality}`);
            } else {
                processImage(action);
            }

            toolBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    async function processImage(action) {
        loader.classList.remove('hidden');
        toolBtns.forEach(btn => btn.disabled = true);

        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    filename: currentFilename,
                    action: action,
                    params: {}
                })
            });

            if (response.ok) {
                const data = await response.json();
                
                processedImg.src = data.url + '?t=' + Date.now();

                downloadBtn.onclick = () => {
                    const urlParts = data.url.split('/');
                    const filename = urlParts[urlParts.length - 1];
                    window.open(`/download/${filename}`, '_blank');
                };

                // Update details panel
                if (data.details) {
                    detailsPanel.classList.remove('hidden');
                    
                    document.getElementById('detail-action').textContent = formatAction(action);
                    document.getElementById('detail-size').textContent = data.details.image_size || '-';
                    document.getElementById('detail-time').textContent = data.details.processing_time || '-';
                    
                    // Extra info based on action
                    const extraContainer = document.getElementById('detail-extra-container');
                    const extraLabel = document.getElementById('detail-extra-label');
                    const extraValue = document.getElementById('detail-extra');
                    
                    if (data.details.circles_detected !== undefined) {
                        extraLabel.textContent = 'Circles';
                        extraValue.textContent = data.details.circles_detected;
                        extraContainer.style.display = 'flex';
                    } else if (data.details.corners_detected !== undefined) {
                        extraLabel.textContent = 'Corners';
                        extraValue.textContent = data.details.corners_detected;
                        extraContainer.style.display = 'flex';
                    } else if (data.details.lines_detected !== undefined) {
                        extraLabel.textContent = 'Lines';
                        extraValue.textContent = data.details.lines_detected;
                        extraContainer.style.display = 'flex';
                    } else if (data.details.size_reduction !== undefined) {
                        extraLabel.textContent = 'Reduced';
                        extraValue.textContent = data.details.size_reduction;
                        extraContainer.style.display = 'flex';
                    } else {
                        extraContainer.style.display = 'none';
                    }
                }

            } else {
                const errorData = await response.json().catch(() => ({}));
                alert(errorData.error || translations[currentLang].error_process);
            }
        } catch (error) {
            console.error('Error:', error);
            alert(translations[currentLang].error_process);
        } finally {
            loader.classList.add('hidden');
            toolBtns.forEach(btn => btn.disabled = false);
        }
    }

    function formatAction(action) {
        const names = {
            'custom_filter': 'Blur',
            'grayscale': 'B&W',
            'laplacian_edge_sharp1': 'Sharpen',
            'laplacian_edge_sharp2': 'Sharpen+',
            'circle_detection': 'Circles',
            'corner_detection': 'Corners',
            'line_detection': 'Lines',
            'dilate': 'Dilate',
            'erode': 'Erode'
        };
        if (action.startsWith('compress_')) {
            return 'Compress ' + action.split('_')[1] + '%';
        }
        return names[action] || action;
    }

    // Reset
    resetBtn.addEventListener('click', () => {
        currentFilename = null;
        fileInput.value = '';
        previewArea.classList.add('hidden');
        detailsPanel.classList.add('hidden');
        actionBar.classList.add('hidden');
        dropZone.classList.remove('hidden');
        originalImg.src = '';
        processedImg.src = '';
        toolBtns.forEach(b => b.classList.remove('active'));
    });

    // Localization
    langToggle.addEventListener('click', () => {
        currentLang = currentLang === 'en' ? 'ar' : 'en';
        updateLanguage();
    });

    function updateLanguage() {
        document.documentElement.dir = currentLang === 'ar' ? 'rtl' : 'ltr';
        langLabel.textContent = currentLang.toUpperCase();

        document.querySelectorAll('[data-i18n]').forEach(el => {
            const key = el.dataset.i18n;
            if (translations[currentLang][key]) {
                el.textContent = translations[currentLang][key];
            }
        });
    }
});
