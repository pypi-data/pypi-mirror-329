from setuptools import setup, find_packages

setup(
    name="zeusback",
    version="2.1",
    packages=find_packages(),
    install_requires=[
        "colorama",
        "requests",
        "validators",
    ],
    entry_points={
        "console_scripts": [
            "zeusback = zeusback.core:run"  # هيخلّي الأمر `zeusback` يشتغل من الترمينال
        ]
    },
    author="ZeUsVuLn (Hesham)",
    author_email="he4am3id66@gmail.com",  # ضيف ايميلك
    description="A tool to fetch archived files from Wayback Machine",
    url="https://github.com/zeusvuln/zeusback",  # ضيف لينك GitHub لو عندك
)
