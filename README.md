# Word Frequency Stats

### A web app built with Python and Flask for analyzing word statistics.

The app exposes two endpoints:

1. _/words (post)_ </br>
Call it with a string of comma-separated words in the body</br>

2. _/stats (get)_ </br>
It Returns stats about the frequency of the words received until this point in time:
top5 words (with their respective frequency) and both the minimum and median frequency among all words.

The code is written allowing for concurrency and expecting more POSTs than GETs.


**Instructions to run**</br>
You can either run gunicorn_start.sh or through the Dockerfile (don't forget to redirect to port 5000. That is, run for example "docker build -t freq ." and then "docker run -p 5000:5000 freq")
