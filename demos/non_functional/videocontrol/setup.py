from setuptools import setup

setup(
    name = 'cbvideocontrol',
    version = '0.1',
    description = "Crossbar.io Demo: Real-time Web Video Controller",
    platforms = ['Any'],
    packages = ['cbvideocontrol'],
    include_package_data = True,
    zip_safe = False,
    entry_points = {
        'autobahn.twisted.wamplet': [
            'backend = cbvideocontrol.backend:app'
        ],
    }
)