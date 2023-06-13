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

Implementation notes:
1. For retrieving the top words, we use an additional list of size 5. 
This makes the POSTs slower by a constant time -as the size of this additional list is constant-. 
That is, we add the overhead of inserting to and removing from this additional list with the top words. 
On other hand, this way we make the GETs faster, as we'll always just retrieve the data from the short list, instead
of iterating over the whole data, which appears to be not bounded.
Being that the POSTs are supposed to be much more than the GETs, we'd need more information in order to take a wiser decision.
Instead of that list of size 5, we could use a data structure that keeps sorted (heapq, sortedlist, etc). That would make the code faster by a constant rate.</br>

2. We could split the contents of app.py into two modules, being one "the driver" and the other the one responsible of the logic. I decided to do it this way being that the whole file is less than 100 lines.
That is, I think this way is a bit simpler.

Suboptimal stuff, potential improvements, etc:

- The top-5 words is calculated in a pretty efficient way. We store, as we said, a top-5 list, and could be improved using for example a heap.
- The minimum is calculated through a dictionary with the distributions. It could be probably improved: 
right now, in order to retrieve the minimum we need to go over all the values in the dictionary.
(The different frequencies that can be found.)
- The median is calculated in a suboptimal way: going over all the elements in the counter
(That's what we avoided using the top-5 list and therefore this needs to be changed in order to take advantage from the other optimization). 
In order to make it more efficient, we could probably store two heaps: one for the frequencies bigger than the median and one for the smaller ones.
- More tests should be added.
- I think the code as it is it's pretty mantainable but I think I'd do a light refactor.
