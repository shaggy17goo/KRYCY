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
            'do_sniff = main_app:sniff',
            'getPcapList = main_app:get_pcap_list',
            'getPcap = main_app:get_pcap',
            'getLogList = main_app:get_log_list',
            'getLog = main_app:get_log',
            'do_command = main_app:exec_command',
        ],
    },
)

