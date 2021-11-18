from setuptools import setup

setup(
    name='main',
    version='0.1.0',
    py_modules=['main'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'getIfconfig = main_app:get_ifconfig',
            'getPcapList = main_app:get_pcap_list',
            'getPcap = main_app:get_pcap',
            'sniff = main_app:sniff',
        ],
    },
)