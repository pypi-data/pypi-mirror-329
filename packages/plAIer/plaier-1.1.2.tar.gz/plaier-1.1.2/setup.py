from distutils.core import setup

setup(
    name = "plAIer",
    version          = "1.1.2",
    description      = "A Python library that uses a reinforcement learning AI to play board games such as Chess, Tic Tac Toe, and Reversi.",
    long_description_content_type = "text/markdown",
    long_description = open("README.md", encoding="utf8").read(),
    author           = "L-Martin7",
    license          = "BSD 3-Clause \"New\" or \"Revised\" License",
    url              = "https://github.com/L-Martin7/plAIer",
    download_url     = "https://pypi.python.org/pypi/plAIer",
    project_urls = {
        "Source": "https://github.com/L-Martin7/plAIer",
        "Issues": "https://github.com/L-Martin7/plAIer/issues"
        },
    platforms        = ["Linux", "macOS", "Windows"],
    keywords         = ["AI", "artificial intelligence",
                        "play", "game", "reinforcement AI",
                        "player", "board games"],
    py_modules       = ["plAIer"],
    packages         = ["plAIer"],
    include_package_data = True,
    install_requires = []
)
