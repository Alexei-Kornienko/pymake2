import pymake2

requirements = pymake2.file('requirements.txt')
test_requirements = pymake2.file('test-requirements.txt')


@pymake2.target()
def test(venv):
    pymake2.sh('. .venv/bin/activate && python .venv/bin/nosetests --with-doctest pymake2 tests.unit')


@pymake2.target()
def flake8(venv):
    pymake2.sh('. .venv/bin/activate && flake8 pymake2')


@pymake2.target(name='.venv')
def venv(requirements, test_requirements):
    pymake2.sh('python3 -m virtualenv .venv')
    pymake2.sh('. .venv/bin/activate && pip install -r requirements.txt')
    pymake2.sh('. .venv/bin/activate && pip install -r test-requirements.txt')


@pymake2.target()
def clean():
    pymake2.sh('rm -rf .venv')
