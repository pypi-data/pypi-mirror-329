FROM tahv/mayapy:2025
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_PYTHON=/usr/autodesk/maya/bin/mayapy
ENV PYTHONPATH=/app/.venv/lib/python3.11/site-packages
WORKDIR /app
RUN uv venv && uv pip install gnureadline
CMD ["mayapy", "-ic", "import maya.standalone; import gnureadline; maya.standalone.initialize()"]
