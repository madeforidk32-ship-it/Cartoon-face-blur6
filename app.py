\
    import os
    import cv2
    import numpy as np
    import onnxruntime as ort
    from tkinter import Tk, filedialog, Button, Label, StringVar
    from PIL import Image, ImageTk

    MODEL_PATH = os.path.join('models', 'yolov8_animeface.onnx')

    class App:
        def __init__(self, root):
            self.root = root
            root.title('Cartoon Face Blurrer — Extreme (Ready-to-build)')
            self.status = StringVar(value='No file loaded.')
            Label(root, textvariable=self.status).pack(pady=8)
            Button(root, text='Open Video', command=self.open_video).pack(pady=4)
            Button(root, text='Process & Save', command=self.process_video).pack(pady=4)
            self.loaded_video = None

            # load model session lazily
            self.session = None

        def open_video(self):
            path = filedialog.askopenfilename(filetypes=[('Video files', '*.mp4 *.mov *.avi *.mkv')])
            if path:
                self.loaded_video = path
                self.status.set('Loaded: ' + os.path.basename(path))

        def ensure_model(self):
            if not os.path.exists(MODEL_PATH):
                self.status.set('Model not found. Run download_model.py first.')
                raise FileNotFoundError('Model not found: ' + MODEL_PATH)
            if self.session is None:
                self.status.set('Loading model...')
                self.session = ort.InferenceSession(MODEL_PATH)
                self.status.set('Model loaded. Ready.')

        def preprocess(self, frame, size=640):
            # resize & normalize to 640x640, returns float32 CHW
            h, w = frame.shape[:2]
            r = size / max(h, w)
            new_w, new_h = int(w * r), int(h * r)
            resized = cv2.resize(frame, (new_w, new_h))
            canvas = np.full((size, size, 3), 114, dtype=np.uint8)
            canvas[0:new_h, 0:new_w] = resized
            img = canvas[:, :, ::-1].astype(np.float32) / 255.0
            img = np.transpose(img, (2, 0, 1))[np.newaxis, :]
            return img, r, new_w, new_h

        def postprocess(self, preds, orig_w, orig_h, scale):
            # preds parsing placeholder — model-specific. Returns boxes in xywh (pixel coordinates on original image)
            # You must implement decoding according to the model output format.
            boxes = []
            # NOTE: This is a simplified placeholder. For many ONNX YOLO models you need to decode anchors / grids.
            return boxes

        def process_video(self):
            if not self.loaded_video:
                self.status.set('No video loaded')
                return
            try:
                self.ensure_model()
            except Exception as e:
                return
            in_path = self.loaded_video
            out_path = os.path.splitext(in_path)[0] + '_blurred.mp4'
            cap = cv2.VideoCapture(in_path)
            fps = cap.get(cv2.CAP_PROP_FPS) or 25.0
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(out_path, fourcc, fps, (w, h))
            frame_idx = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                if frame_idx % 1 == 0:
                    img, scale, new_w, new_h = self.preprocess(frame)
                    ort_inputs = {self.session.get_inputs()[0].name: img.astype('float32')}
                    preds = self.session.run(None, ort_inputs)
                    boxes = self.postprocess(preds, w, h, scale)
                    # apply blur for each box
                    for box in boxes:
                        x, y, bw, bh = box
                        x1 = max(0, int(x - bw/2))
                        y1 = max(0, int(y - bh/2))
                        x2 = min(w, int(x + bw/2))
                        y2 = min(h, int(y + bh/2))
                        roi = frame[y1:y2, x1:x2]
                        if roi.size == 0: continue
                        k = max(31, (x2-x1)//2 | 1)
                        blurred = cv2.GaussianBlur(roi, (k,k), 0)
                        frame[y1:y2, x1:x2] = blurred
                out.write(frame)
                frame_idx += 1
            cap.release()
            out.release()
            self.status.set('Saved: ' + out_path)

    if __name__ == '__main__':
        root = Tk()
        app = App(root)
        root.mainloop()
