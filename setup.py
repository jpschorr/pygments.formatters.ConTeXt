"""
ConTeXt verbatim output for pygments
"""
from setuptools import setup
entry_points = """
[pygments.formatters]
context = context:ContextFormatter
"""
setup(
    name         = 'pygments.formatters.context',
    version      = '0.1',
    description  = __doc__,
    packages     = ['context'],
    entry_points = entry_points
)
