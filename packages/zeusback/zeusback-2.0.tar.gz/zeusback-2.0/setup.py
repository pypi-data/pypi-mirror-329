from setuptools import setup, find_packages

setup(
    name="zeusback",
    version="2.0",
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
    author_email="your-email@example.com",  # ضيف ايميلك
    description="A tool to fetch archived files from Wayback Machine",
    url="https://github.com/yourusername/zeusback",  # ضيف لينك GitHub لو عندك
)
