import unittest
import os
import coverage
from app import app
from flask_script import Manager

manager = Manager(app)
#nosetests --with-cov --cov-report term-missing --cov app tests/
#coverage report -m

@manager.command
def test():
    """Runs the unit tests without coverage."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    cov = coverage.coverage(
        branch=True,
        include='app/*',
    )
    cov.start()
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
    cov.stop()
    cov.save()
    print('Coverage Summary:')
    cov.report(show_missing=True)
    cov.html_report()
    cov.erase()


if __name__ == '__main__':
    manager.run()