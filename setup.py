from setuptools import setup, find_packages

setup(
    name='certbot-dns-yandex-360',
    version='0.1.0',  
    description='Certbot plugin for Yandex 360 DNS to automate the process of completing a dns-01 challenge.',
    author='Yury Petrov',
    author_email='yuv@yuriypetrov.net',
    url='https://github.com/siameseoriental',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='Apache License 2.0', 
    classifiers=[
        'Development Status :: 5 - Production/Stable',  
        'Intended Audience :: System Administrators',
        'Topic :: Internet :: Name Service (DNS)',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'certbot',
        'requests',
    ],
    entry_points={
        'certbot.plugins': [
            'dns-yandex-360 = certbot_dns_yandex_360.dns_yandex_360:Yandex360DNSAuthenticator'
        ]
    },
    keywords='certbot dns plugin yandex 360',
    python_requires='>=3.6',
    project_urls={
        'Source': 'https://github.com/siameseoriental/certbot-dns-yandex-360',
        'Bug Reports': 'https://github.com/siameseoriental/certbot-dns-yandex-360/issues',
    },
)