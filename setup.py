from setuptools import setup


long_description = open("README.md").read()
requirements = []
with open("./requirements.txt", "r") as fp:
    requirements = fp.readlines()

setup(
    name="llama-client-aic",
    packages=[
        "client_aic",
        "client_aic.config",
        "client_aic.models",
        "client_aic.req",
        "client_aic.req.ai",
        "client_aic.req.auth",
        "client_aic.req.job",
        "client_aic.req.user",
        "client_aic.tls",
    ],
    scripts=[
        "examples/ask-llm.py",
        "examples/get-ai-result.py",
        "examples/review-answer.py",
    ],
    version="1.0.2",
    license="Apache 2.0",
    description=(
        "python client for redten - "
        "a platform for building and testing "
        "distributed, self-hosted LLMs "
        "with native RAG and Reinforcement "
        "Learning with Human Feedback (RLHF) "
        "https://api.redten.io"
    ),
    author="redten-llamas",
    author_email="info@redten.io",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/redten-ai/llama-client-aic",
    keywords=[
        "artificial intelligence",
        "deep learning",
        "transformers",
        "attention mechanism",
        "reinforcement learning",
        "human feedback",
    ],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],
)
