/* ==========================================================================
   PALGRIMIZER UPLOAD, OCR AND VOICE DICTATION LOGIC
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    const dropzone = document.getElementById('uploadDropzone');
    const fileInput = document.getElementById('documentFileInput');
    const filePreview = document.getElementById('filePreviewCard');
    const fileNameText = document.getElementById('fileNameText');
    const fileSizeText = document.getElementById('fileSizeText');
    const removeFileBtn = document.getElementById('removeFileBtn');

    if (dropzone && fileInput) {
        // Drag & Drop events
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, preventDefaults, false);
        });

        function preventDefaults(e) {
            e.preventDefault();
            e.stopPropagation();
        }

        ['dragenter', 'dragover'].forEach(eventName => {
            dropzone.addEventListener(eventName, () => dropzone.classList.add('drag-over'), false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropzone.addEventListener(eventName, () => dropzone.classList.remove('drag-over'), false);
        });

        dropzone.addEventListener('drop', (e) => {
            const dt = e.dataTransfer;
            const files = dt.files;
            if (files.length > 0) {
                fileInput.files = files;
                showFilePreview(files[0]);
            }
        });

        fileInput.addEventListener('change', () => {
            if (fileInput.files.length > 0) {
                showFilePreview(fileInput.files[0]);
            }
        });

        function showFilePreview(file) {
            if (filePreview && fileNameText && fileSizeText) {
                fileNameText.innerText = file.name;
                fileSizeText.innerText = (file.size / 1024).toFixed(1) + ' KB';
                filePreview.style.display = 'flex';
                dropzone.style.display = 'none';
            }
        }

        if (removeFileBtn) {
            removeFileBtn.addEventListener('click', () => {
                fileInput.value = '';
                if (filePreview) filePreview.style.display = 'none';
                dropzone.style.display = 'flex';
            });
        }
    }

    // 2. Voice Input Dictation (Web Speech API)
    const voiceBtn = document.getElementById('startVoiceDictationBtn');
    const pastedTextArea = document.getElementById('pastedTextArea');
    const voiceStatus = document.getElementById('voiceStatusBadge');

    if (voiceBtn && pastedTextArea) {
        let recognition = null;
        let isListening = false;
        let _intentionalStop = false;   // true when user clicks Stop — suppress aborted toast
        let _recognitionActive = false; // true between start() and onend() — prevents double-start

        // Track the last committed text so interim results don't duplicate
        let committedText = '';

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

        // ── Helper: render Lucide icons that were injected via innerHTML ──────────
        function _refreshIcons(element) {
            if (typeof lucide === 'undefined') return;
            // lucide.createIcons() with a {nodes} list is supported in all modern builds;
            // fall back to full document scan if nodes API is unavailable (older CDN builds).
            try {
                if (typeof lucide.createIcons === 'function') {
                    const iconEls = element.querySelectorAll('[data-lucide]');
                    if (iconEls.length > 0) {
                        iconEls.forEach(el => {
                            const iconName = el.getAttribute('data-lucide');
                            if (iconName && lucide[iconName.replace(/-([a-z])/g, (_, c) => c.toUpperCase())]) {
                                // Build SVG using lucide's icon data directly
                            }
                        });
                    }
                    lucide.createIcons(); // full document re-scan — safe, fast, always works
                }
            } catch (_) {
                // Silently ignore any lucide API errors — icons are cosmetic only
            }
        }

        // ── Helper: reset button and badge to idle state ───────────────────────
        function _resetVoiceUI() {
            isListening = false;
            _recognitionActive = false;
            voiceBtn.innerHTML = '<i data-lucide="mic"></i> Dictate Text with Voice';
            if (voiceStatus) voiceStatus.style.display = 'none';
            _refreshIcons(voiceBtn);
        }

        // ── Helper: switch to Paste Text tab so user sees dictated text ────────
        function _switchToPasteTab() {
            const pasteBtn = document.querySelector('.tab-btn[data-tab="paste-text"]');
            const pastePanel = document.getElementById('tab-paste-text');
            if (pasteBtn && pastePanel) {
                document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
                pasteBtn.classList.add('active');
                pastePanel.classList.add('active');
                pastedTextArea.focus();
            }
        }

        if (SpeechRecognition) {
            recognition = new SpeechRecognition();
            recognition.continuous    = true;   // keep listening until user stops
            recognition.interimResults = true;  // show live partial results in textarea
            recognition.lang          = 'en-US';
            recognition.maxAlternatives = 1;

            // ── onresult: append final transcripts; show interim live ──────────
            recognition.onresult = (event) => {
                let finalTranscript   = '';
                let interimTranscript = '';

                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    const t = event.results[i][0].transcript;
                    if (event.results[i].isFinal) {
                        finalTranscript += t;
                    } else {
                        interimTranscript += t;
                    }
                }

                if (finalTranscript.trim() !== '') {
                    // Append finalized speech with a space separator
                    committedText += (committedText ? ' ' : '') + finalTranscript.trim();
                    pastedTextArea.value = committedText;
                    // Switch to Paste Text tab so user sees dictated text immediately
                    _switchToPasteTab();
                } else if (interimTranscript.trim() !== '') {
                    // Live preview — shown but NOT committed yet
                    pastedTextArea.value = committedText + (committedText ? ' ' : '') + interimTranscript;
                }
            };

            // ── onstart: update UI to "listening" state ────────────────────────
            recognition.onstart = () => {
                isListening        = true;
                _recognitionActive = true;
                // Seed committedText with whatever is already in the textarea
                committedText = pastedTextArea.value.trim();

                voiceBtn.innerHTML = '<i data-lucide="square" style="color:#ef4444;"></i> Stop Listening';
                if (voiceStatus) {
                    voiceStatus.innerHTML = '&#x1F534; Listening&hellip; Speak clearly into your microphone';
                    voiceStatus.style.display = 'inline-block';
                }
                _refreshIcons(voiceBtn);
            };

            // ── onend: called after recognition stops (for any reason) ─────────
            recognition.onend = () => {
                // Only reset UI here when onerror did NOT already reset it.
                // (onerror sets _recognitionActive = false before onend fires)
                if (_recognitionActive) {
                    _resetVoiceUI();
                }
                _intentionalStop = false; // always clear the flag
            };

            // ── onerror: handle recognition failures gracefully ───────────────
            recognition.onerror = (event) => {
                _recognitionActive = false; // signal onend that we already handled this

                const intentional = _intentionalStop;
                _intentionalStop = false;

                // Reset UI immediately
                _resetVoiceUI();

                // 'aborted' fires when recognition.stop() is called by user — not an error
                if (event.error === 'aborted' || intentional) return;

                // 'no-speech' in continuous mode is a recoverable timeout — just inform gently
                if (event.error === 'no-speech') {
                    window.showToast('No speech detected. Click the mic button and try again.', 'info');
                    return;
                }

                const errorMessages = {
                    'not-allowed':         'Microphone permission denied. Please allow microphone access and try again.',
                    'audio-capture':       'No microphone found. Please connect a microphone and try again.',
                    'network':             'Network error during speech recognition. Please check your connection.',
                    'service-not-allowed': 'Speech recognition service is blocked in this browser.',
                    'bad-grammar':         'Speech grammar error. Please try again.',
                    'language-not-supported': 'Language not supported by your browser\'s speech engine.',
                };
                const msg = errorMessages[event.error] || ('Speech recognition error: ' + event.error);
                window.showToast(msg, 'warning');
            };

            // ── Button click: toggle start / stop ────────────────────────────
            voiceBtn.addEventListener('click', () => {
                if (isListening) {
                    // User intentionally stops — set flag BEFORE calling stop()
                    // so onerror('aborted') knows not to show a toast
                    _intentionalStop = true;
                    recognition.stop();
                } else {
                    // Guard: don't call start() if the engine hasn't fully stopped yet
                    if (_recognitionActive) return;
                    try {
                        _intentionalStop = false;
                        recognition.start();
                    } catch (e) {
                        if (e.name === 'InvalidStateError') {
                            // Engine still shutting down — brief debounce then retry
                            setTimeout(() => {
                                try { recognition.start(); } catch (_) { /* ignore */ }
                            }, 300);
                        } else {
                            window.showToast('Could not start voice recognition: ' + e.message, 'danger');
                        }
                    }
                }
            });

        } else {
            // ── Browser does not support Web Speech API ───────────────────────
            voiceBtn.disabled = true;
            voiceBtn.title    = 'Voice Input is not supported in this browser. Please use Chrome or Edge.';
            voiceBtn.style.opacity = '0.5';
            voiceBtn.style.cursor  = 'not-allowed';
            voiceBtn.addEventListener('click', () => {
                window.showToast(
                    'Voice Input requires Google Chrome or Microsoft Edge. Please switch browsers.',
                    'warning'
                );
            });
        }
    }

    // 3. Image OCR Scan Handler
    const ocrFileInput = document.getElementById('ocrImageInput');
    const ocrBtn = document.getElementById('runOcrScanBtn');
    const ocrResultBox = document.getElementById('ocrResultBox');

    if (ocrBtn && ocrFileInput && pastedTextArea) {
        ocrBtn.addEventListener('click', async () => {
            if (!ocrFileInput.files || ocrFileInput.files.length === 0) {
                window.showToast('Please select an image file to scan with OCR.', 'warning');
                return;
            }

            ocrBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Scanning Image OCR...';
            ocrBtn.disabled = true;

            const formData = new FormData();
            formData.append('image_file', ocrFileInput.files[0]);

            try {
                const res = await fetch('/ocr-scan', {
                    method: 'POST',
                    body: formData
                });
                const data = await res.json();

                if (data.status === 'success') {
                    pastedTextArea.value = data.extracted_text;
                    if (ocrResultBox) {
                        ocrResultBox.innerText = "OCR Extracted Text:\n" + data.extracted_text;
                        ocrResultBox.style.display = 'block';
                    }
                    window.showToast('OCR Text Extracted successfully!', 'success');
                }
            } catch (err) {
                window.showToast('OCR scan failed.', 'danger');
            } finally {
                ocrBtn.innerHTML = '<i class="fas fa-camera"></i> Run OCR Scan';
                ocrBtn.disabled = false;
            }
        });
    }
});
