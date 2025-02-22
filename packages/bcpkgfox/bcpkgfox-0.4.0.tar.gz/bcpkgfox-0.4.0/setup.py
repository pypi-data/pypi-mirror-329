from setuptools import setup, find_packages

setup(
    name="bcpkgfox",
    version="0.4.0",
    author="Guilherme Neri",
    author_email="guilherme.neri@bcfox.com.br",
    description="Biblioteca BCFOX",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/robotsbcfox/PacotePythonBCFOX",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        'selenium',
        'undetected-chromedriver',
        'selenium-stealth',
        'requests',
        'pyautogui',
        'setuptools',
        'opencv-python',
        'pygetwindow ',
        'pyscreeze',
        'Pillow'
    ],
)