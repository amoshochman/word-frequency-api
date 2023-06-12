# Word Frequency Stats

### A web app built with Python and Flask

Two endpoint are exposed:
1. _/words (post)_ </br>
should include a string of comma-separated words in the body</br>

2. _/stats (get)_ </br>
returns stats about the frequency of the words received until this point in time
The second endpoint should return stats about the frequency of the words received until this point in time: </br>
top5 words (with their respective frequency) and both the minimum and median frequency among all words

The code is written allowing for concurrency and expecting more "post" requests than "get" ones.


**Use one of the following options in order to run**
- through file gunicorn_start.sh
- through "flask run" (it would run then without gunicorn and therefore without workers support)
- through Dockerfile (don't forget to redirect to port 5000. That is, run for example "docker build -t freq ." and then "docker run -p 5000:5000 freq"