pip3 install twine
python3 setup.py check
python3 setup.py sdist
python3 -m twine upload dist/*