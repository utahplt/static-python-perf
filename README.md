# Static Python Perf

## Steps to Run Static Python
(Taken from [cinder/python-build-env](https://github.com/facebookincubator/cinder/pkgs/container/cinder%2Fpython-build-env).)

> [!NOTE]
> You must have already installed and set up Docker on your machine.

1. Clone the `cinder` respotory.
```bash
git clone https://github.com/facebookincubator/cinder.git
```
2. Run the following docker command.
```bash
docker run -v "$PWD/cinder:/vol" -w /vol -it --rm ghcr.io/facebookincubator/cinder/python-build-env:latest bash
```
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
