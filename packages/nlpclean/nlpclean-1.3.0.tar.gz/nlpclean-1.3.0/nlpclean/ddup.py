import re
from rbloom import Bloom
from unicodedata import normalize

def make_dedup_bloom(separator='\n', just_words=True, zero_digits=True, capacity=100000000, error=0.00001):
    bf = Bloom(capacity, error)

    def _dedup_fn(text):
        if not isinstance(text, str):
            raise TypeError(f'Expected "text" to be a sting, found: {type(text)}')

        text = normalize('NFKD', text)

        lines = []
        for line in text.split(separator):
            line = line.strip()

            if not line:
                lines.append(line)
                continue

            if just_words:
                line = ' '.join(re.findall(r'\w+', line))
            if zero_digits:
                line = re.sub(r'\d', '0', line)

            if line in bf:
                line = ''
            else:
                bf.add(line)

            lines.append(line)

        return separator.join(lines)

    return _dedup_fn