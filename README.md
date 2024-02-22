# Static Python Perf


Running the Docker:

```
docker run -v "$PWD/cinder:/vol" -w /vol -it --rm ghcr.io/facebookincubator/cinder/python-build-env:latest bash
```
Steps to Run Static Python
1. `cd` Ensure you're in the correct empty directory 
2. Run the docker command above
3. pull the changes (git pull)
4. ls, and navigate to the file that needs to be run (./call-method/shallow)
5. Run the following command:
```
/vol/python.exe -m compiler --static main.py
```



## Related Work

Static Python: <https://users.cs.utah.edu/~blg/publications/publications.html#lgmvpk-pj-2023>

Reticulated Python (Retic): <https://dl.acm.org/doi/10.1145/3093333.3009849>

Retic Performance: <https://users.cs.utah.edu/~blg/publications/publications.html#gm-pepm-2018>

More Retic Performance: <https://dl.acm.org/doi/10.1145/3359619.3359742>

Grift, sampling performance: <https://akuhlens.github.io/paper/pldi19.pdf>

Blog post, mypy frustrations: <https://www.uninformativ.de/blog/postings/2022-04-21/0/POSTING-en.html>

