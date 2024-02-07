# Use an official Python runtime as a parent image
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the requirements file into the container at /code
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN python3 manage.py collectstatic
# Copy the current directory contents into the container at /code
COPY . .
CMD ["gunicorn", "Pianano.wsgi"]
EXPOSE 8000
