FROM python:3.12-slim@sha256:a6e34c598f2467ed0e9a8d349809fcd8b5c603269512df273a0bb1784edc11b1
WORKDIR /app
COPY track_2b/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY track_2b /app/track_2b
ENV PYTHONDONTWRITEBYTECODE=1 BIND=0.0.0.0 PORT=19564
USER 65534:65534
EXPOSE 19564
CMD ["python","track_2b/src/server.py"]
