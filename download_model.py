import requests, os, sys, shutil
MODEL_URL = "https://huggingface.co/Fuyucchi/yolov8_animeface/resolve/main/yolov8n-animeface.onnx"
# Note: If the file name at the URL is different, update MODEL_URL.
out = 'models'
os.makedirs(out, exist_ok=True)
dest = os.path.join(out, 'yolov8_animeface.onnx')
print('Downloading model to', dest)
with requests.get(MODEL_URL, stream=True) as r:
    r.raise_for_status()
    total = int(r.headers.get('content-length', 0))
    with open(dest, 'wb') as f:
        from tqdm import tqdm
        for chunk in tqdm(r.iter_content(chunk_size=8192), total=total//8192, unit='KB'):
            if chunk:
                f.write(chunk)
print('Downloaded model. File size:', os.path.getsize(dest))
print('If the download fails, please visit the model page and download the ONNX model manually: https://huggingface.co/Fuyucch1/yolov8_animeface')
