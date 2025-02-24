from setuptools import setup, find_packages

setup(
    name="streamlit-audio-queue-player",
    version="0.1.2",
    author="neon izm",
    author_email="jj.y0sh1da@gmail.com",
    description="A Streamlit component for sequential audio playback with an internal queue.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/neon-izm/streamlit-audio-queue-player",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        # streamlit_audio_queue_player  frontend/build
        "streamlit_audio_queue_player": ["frontend/build/**/*"],
    },
    install_requires=[
        "streamlit>=1.0.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
