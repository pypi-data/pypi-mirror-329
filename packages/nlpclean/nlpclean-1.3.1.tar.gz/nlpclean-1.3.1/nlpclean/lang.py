import fasttext
import iso639
import logging
import os
import requests
import tempfile
import tqdm


def _download_fasttext():
    remote_url = 'https://huggingface.co/cis-lmu/glotlid/resolve/main/model.bin'
    expected_size = 1687094687

    model_dir = os.path.expanduser(os.path.join('~', '.nlpclean'))
    model_dir = os.getenv("DATA_DIR") or model_dir
    os.makedirs(model_dir, exist_ok=True)

    model_name = 'model.bin'
    model_path = os.path.join(model_dir, model_name)

    if os.path.exists(model_path) and os.path.getsize(model_path) == expected_size:
        return model_path

    remote_size = int(
        requests.head(remote_url, allow_redirects=True).headers['Content-Length'])
    if expected_size != remote_size:
        raise AssertionError('Unexpected remote model size')

    with tqdm.tqdm(initial=0, total=remote_size, unit='B', unit_scale=True, desc=model_name) as bar:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_name = f.name

            request = requests.get(remote_url, allow_redirects=True, stream=True)
            for chunk in request.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    bar.update(1024)

    os.rename(temp_name, model_path)

    return model_path


def detect_main_lang():
    _fasttext_model = fasttext.load_model(_download_fasttext())

    def _detect_fn(text):
        if not text.strip():
            return '??', 1.0

        try:
            scores = _fasttext_model.predict(text.replace('\n', ' '))
        except Exception as e:
            logging.warning(e)
            return '??', 0.0

        if not scores or not scores[0]:
            return '??', 0.0

        lang = scores[0][0].replace('__label__', '').split('_')[0]
        lang = iso639.Lang(lang).pt1
        if not lang:
            return '??', scores[1][0]

        return lang, scores[1][0]

    return _detect_fn
