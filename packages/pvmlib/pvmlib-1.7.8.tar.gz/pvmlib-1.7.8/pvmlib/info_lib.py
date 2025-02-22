class LibraryInfo:
    version_lib = 'v1.7.8'
    name = 'pvmlib'
    author = "Jesus Lizarraga"
    author_email = "jesus.lizarragav@coppel.com"
    description = "Python library for PVM"
    python_requires = '>=3.12'
    env = 'development'
    
    install_requires = [
        "pydantic-settings",
        "pydantic",
        "fastapi",
        "uvicorn",
        "pytz",
        "circuitbreaker",
        "requests",
        "tenacity",
        "pybreaker",
        "aiohttp",
        "starlette>=0.13.0",
        "urllib3>=1.26.5,<2.0.0",
        "charset_normalizer>=2.0.0,<3.0.0",
        "motor",
        "colorama",
    ]