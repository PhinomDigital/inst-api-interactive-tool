FROM python:3.8.13-buster
EXPOSE 8080
# set working directory in container
WORKDIR /usr/src/app

# Copy and install packages
COPY requirements.txt /

RUN pip install --no-cache-dir -r /requirements.txt

# Copy app folder to app folder in container
COPY . /usr/src/app/

# Changing to non-root user
RUN addgroup --system app && adduser --system --group app
RUN chown -R app:app /usr/src/app
USER app

# Run locally on port 80
CMD ["python", "dash_phd_api.py"]
#gunicorn --bind 0.0.0.0:80 main:server
