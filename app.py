import threading
from flask import Flask, request, jsonify
from collections import Counter

app = Flask(__name__)
words_counter = Counter()
lock = threading.Lock()

MOST_COMMON = 5
TOP = 'top' + str(MOST_COMMON)
MINIMUM = 'minimum'
MEDIAN = 'median'


def process_words_async(data):
    with lock:
        words = [elem.strip() for elem in data.split(",")]
        words_counter.update(words)


@app.route('/words', methods=['POST'])
def process_words():
    try:
        data = request.data.decode('utf-8')
    except (UnicodeDecodeError, AttributeError):
        return jsonify("Please provide a valid UTF-8 encoded string", 400)
    thread = threading.Thread(target=process_words_async, args=(data,))
    thread.start()
    return jsonify("processing started")


@app.route('/stats', methods=['GET'])
def get_stats():
    with lock:
        top_words = words_counter.most_common(MOST_COMMON)
        min_frequency = min(words_counter.values(), default=None)
        frequencies = sorted(words_counter.values())
        n = len(frequencies)
        if n == 0:
            median_frequency = None
        elif n % 2 == 0:
            median_frequency = (frequencies[n // 2 - 1] + frequencies[n // 2]) / 2
        else:
            median_frequency = frequencies[n // 2]

    dict_response = {
        TOP: [' '.join([str(elem) for elem in my_tuple]) for my_tuple in top_words],
        MINIMUM: min_frequency,
        MEDIAN: median_frequency
    }

    return jsonify(dict_response)


if __name__ == '__main__':
    app.run()