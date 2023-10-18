# Cách chạy chương trình
1. Clone code từ github về
- git clone https://github.com/anhpham21u/connection.git
2. Cài các thư viện trong requirements.txt
Lưu ý: cài pipenv nếu chưa cài: pip install pipenv
- pipenv install --ignore-pipfile
(nếu chạy lỗi thì xóa file Pipfle và Pipfile.lock cũ đi)
3. Vào môi trường ảo
- pipenv shell
4. Chạy chương trình
- python manage.py runserver

# Các thư viện
crispy-bootstrap5, django-crispy-forms: design form theo chuẩn bootstrap 5
django-tinymce: trình chỉnh sửa text trong form