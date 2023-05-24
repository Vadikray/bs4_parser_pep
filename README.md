# Парсер документации Python

## Описание
Проект парсера позволяет получать информацию о новостях и всех версиях Python, скачивать документацию по последней версии Python и информацию по статусам и количеству PEP.

## Запуск парсера
Склонируйте проект
```
git@github.com:Vadikray/bs4_parser_pep.git
```
Cоздать и активировать виртуальное окружение:
```
python -m venv venv
source venv/Scripts/activate
```
Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

## Парсер может работать в четырех режимах работы:
- whats-new (Парсер выводящий спсок изменений в python)
```
python main.py whats-new [аргументы]
```
- latest-versions (Парсер выводящий список версий python и ссылки на их документацию)
```
python main.py latest-versions [аргументы]
```
- download (Парсер скачивающий zip архив с документацией python в pdf формате)
```
python main.py download [аргументы]
```
- pep (Парсер выводящий список статусов документов pep и количество документов в каждом статусе)
```
python main.py pep [аргументы]
```

## Аргументы
- -h, --help Общая информация о командах
- -c, --clear-cache Очистка кеша перед выполнением парсинга
- -o {pretty,file}, --output {pretty,file}
Дополнительные способы вывода данных
pretty - выводит данные в командной строке в таблице
file - сохраняет информацию в формате csv в папке ./results/

## Автор
Конюшков В.А.