services:
  - type: web
    name: mini-course-platform
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn run:app