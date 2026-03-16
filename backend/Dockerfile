FROM astral/uv:python3.13-trixie
COPY . .
RUN uv sync
ENTRYPOINT ["uv", "run","python","backend/app.py"]

# "djangoapp/manage.py","runserver", "0.0.0.0:8000"
