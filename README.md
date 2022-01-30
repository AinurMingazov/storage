# storage - это программа складского учета. Приложение позволяет:
- просматривать наличие товаров у владельца;
- передавать товары между владельцами;
- следить за операциями владельцев;
- фильтровать товары по владельцами и категориям;
- импортировать и экспортировать модель товаров в Excel и другие форматы.

Некорректно настроен пакет import_export
для его настройки нужно проделать следующие операции.

раскомментируем
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
закоментируем
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]

python manage.py collectstatic

закоментируем
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
раскомментируем
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"),]

P.S. если знаете как сделать проще, направляйте на pull requests
