import pymake2


@pymake2.target
def test(venv):
    pymake2.sh('. .venv/bin/activate && nosetests --with-doctest pymake2 tests.unit')
