FROM python:3

# Create api directory
RUN mkdir -p /usr/src/api
WORKDIR /usr/src/api

# Install api dependencies
COPY requirements.txt /usr/src/api
RUN pip install -r requirements.txt

# Bundle api source
COPY . /usr/src/api

# Run api
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
