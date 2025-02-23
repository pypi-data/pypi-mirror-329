from setuptools import setup, find_packages

setup(
    name="prompt-ai",  # Replace with your package name
    version="0.2.1",
    description="A powerful library for managing AI-driven prompt handling and response generation, featuring structured database management and seamless Node.js integration.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Gaurav-Codetek/chatflow.git",  # Replace with your GitHub URL
    author="Gaurav Patel (CodersTek)",
    author_email="gauravpatel29@outlook.in",
    install_requires=['google.genai', 'requests', 'beautifulsoup4'],
    keywords=['python', 'chatbot', 'genai', 'generative ai', 'gemini api', 'chat ai'],
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
