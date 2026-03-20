FROM astral/uv:python3.13-trixie
COPY frontend/ .
RUN uv sync
ENTRYPOINT ["uv", "run","python","main.py"]