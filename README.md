# Static Python Perf


Running the Docker:

```
docker run -v "$PWD/cinder:/vol" -w /vol -it --rm ghcr.io/facebookincubator/cinder/python-build-env:latest bash
```
Steps to Run Static Python
1. Clone the `cinder` respotory.
```bash
git clone https://github.com/facebookincubator/cinder.git
```
2. Checkout to the commit `c085ffc4d8dd84da3a871666c596f31c6e979bcb`
```bash
cd cinder
git checkout c085ffc4d8dd84da3a871666c596f31c6e979bcb
```
3. `cd` out of `/cinder` and run the docker command above.
3. pull the changes (git pull).
4. ls, and navigate to the file that needs to be run (./call-method/shallow).
5. Run the following command:

```
/vol/python -m cinderx.compiler --static module.py
```

(old command used `-m compiler`)


## Related Work

Static Python: <https://users.cs.utah.edu/~blg/publications/publications.html#lgmvpk-pj-2023>

Reticulated Python (Retic): <https://dl.acm.org/doi/10.1145/3093333.3009849>

Retic Performance: <https://users.cs.utah.edu/~blg/publications/publications.html#gm-pepm-2018>

More Retic Performance: <https://dl.acm.org/doi/10.1145/3359619.3359742>

Grift, sampling performance: <https://akuhlens.github.io/paper/pldi19.pdf>

Blog post, mypy frustrations: <https://www.uninformativ.de/blog/postings/2022-04-21/0/POSTING-en.html>
