FROM python:3.12
LABEL authors="duchi"


# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Copy project requirements files
COPY requirements.txt /app/requirements.txt


# Install project dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /app/

EXPOSE 8000
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["gunicorn", "flashcards.wsgi", "--bind", "0.0.0.0:8000"]