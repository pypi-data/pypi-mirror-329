from setuptools import setup, find_packages

setup(
    name="ytml-toolkit",  # ✅ Ensure correct package name
    version="0.1.2",
    packages=find_packages(include=["ytml", "ytml.*"]),  # ✅ Explicitly include `ytml`
    entry_points={
        "console_scripts": [
            "ytml=ytml.cli:main",  # ✅ CLI command
        ],
    },
    install_requires=[
        "fastapi",
        "uvicorn",
        "websockets",
        "boto3",
        "gtts",
        "pydub",
        "moviepy",
        "imageio",
        "imageio-ffmpeg",
        "playwright",
        "numpy",
        "requests",
        "python-dotenv",
        "beautifulsoup4",
        "lxml",
        "tqdm",
        "pyttsx3",
        "starlette",
        "colorama",
    ],
    python_requires=">=3.7",
)
