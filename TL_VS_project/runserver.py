import os
from TL_flask import app    # Imports the code from TL-flask/__init__.py

if __name__ == '__main__':  # ������ ���������� ������� (�� production ������� __name__ != '__main__' � ������ ��� �������)
    # ����������� HOST � PORT �� ���������� VS
    HOST = os.environ.get('SERVER_HOST', 'localhost')

    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    app.run(HOST, PORT)     # ������ ���������� �� ��������� �������