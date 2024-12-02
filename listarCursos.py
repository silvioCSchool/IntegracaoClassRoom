from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import os

SCOPES = ['https://www.googleapis.com/auth/classroom.courses.readonly']

def listar_cursos():
    credenciais = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('classroom', 'v1', credentials=credenciais)
    results = service.courses().list(pageSize=10).execute()
    courses = results.get('courses', [])
    for course in courses:
        print(f"Curso: {course['name']}, ID: {course['id']}")

listar_cursos()
