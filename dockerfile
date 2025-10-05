FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app.manage
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1

WORKDIR /usr/src/app

# Copier requirements et installer
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copier tout le projet
COPY . .

# Rendre l'entrypoint exécutable
RUN chmod +x /usr/src/app/entrypoint.sh

EXPOSE 5000

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
