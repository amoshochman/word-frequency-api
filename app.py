import threading
from flask import Flask, request, jsonify
from collections import Counter, defaultdict

app = Flask(__name__)
counter = Counter()
top_words = []
distribution_dict = defaultdict(int)
lock = threading.Lock()

MOST_COMMON = 5
TOP = 'top' + str(MOST_COMMON)
MINIMUM = 'minimum'
MEDIAN = 'median'


def update_top_words(new_words):
    if top_words:
        smaller_top_count = min(counter[word] for word in top_words)
    else:
        new_word = new_words[0]
        smaller_top_count = counter[new_word]
        top_words.append(new_word)
        new_words = new_words[1:]

    for new_word in new_words:
        if new_word in top_words:
            continue
        if len(top_words) < MOST_COMMON:
            top_words.append(new_word)
            smaller_top_count = min(counter[top_word] for top_word in top_words)
            continue
        if counter[new_word] <= smaller_top_count:
            continue
        smaller_top_word = next(top_word for top_word in top_words if counter[top_word] == smaller_top_count)
        smaller_index = top_words.index(smaller_top_word)
        top_words[smaller_index] = new_word


def update_distribution_dict(new_words, previous_values):
    for word in set(new_words):
        appearances = counter[word]
        distribution_dict[appearances] += 1
    for value in [elem for elem in previous_values.values() if elem]:
        distribution_dict[value] -= 1



def process_words_async(data):
    with lock:
        new_words = [elem.strip() for elem in data.split(",")]
        if not new_words:
            return
        previous_values = {}
        for word in new_words:
            previous_values[word] = counter[word]
        counter.update(new_words)
        update_top_words(new_words)
        update_distribution_dict(new_words, previous_values)


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
        frequencies = sorted(counter.values())
        n = len(frequencies)
        if n == 0:
            median_frequency = None
        elif n % 2 == 0:
            median_frequency = (frequencies[n // 2 - 1] + frequencies[n // 2]) / 2
        else:
            median_frequency = frequencies[n // 2]

    dict_response = {
        TOP: [word + " " + str(counter[word]) for word in top_words],
        MINIMUM: min(elem for elem in distribution_dict if distribution_dict[elem]),
        MEDIAN: median_frequency
    }

    return jsonify(dict_response)
