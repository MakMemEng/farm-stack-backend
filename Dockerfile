FROM python:3.10-buster
# 標準出力と標準エラー出力をバッファリングせずに出力
ENV PYTHONUNBUFFERED 1
WORKDIR /src

RUN pip install poetry

COPY pyproject.toml* poetry.lock* ./

RUN poetry config virtualenvs.create true
RUN if [ -f pyproject.toml ]; then poetry install --no-root; fi

EXPOSE 8000

# 実行コマンド
ENTRYPOINT ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
