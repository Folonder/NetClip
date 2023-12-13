# NetClip (ru)
## Локальный буфер обмена

NetClip - проект по локальному буферу обмена. Для запуска проекта требуется:
- Python 3.11+
- Windows 10+
## Установка
- Клонировать проект:
```
git clone https://github.com/Folonder/NetClip.git
```
- Установка зависимостей:
```
pip install -r requirements.txt
```
## Запуск
- Проект должен быть запущен от имени администратора
- Компьютеры должны быть подключены к одной сети
- Запустить файл startup.py
```
python startup.py
```
## Как работать с приложением
### Отправка
- Вкладка отправки открыта по умолчанию
- Добавить в IP-Manager IP-адрес, на который нужно отправить 
- Выбрать данные из буфера обмена для отправки
- Нажать кнопку отправки
### Получение
- Открыть вкладку получения
- Выбрать данные, которые хотите скопировать в свой буфер обмена
- Нажать кнопку получения
## Формат данных
&emsp;Данные могут быть представлены как в текстовом формате, так и в виде картинок. При копировании текста на ctrl + c буфер обновляется автоматически, при копировании картинок нужно обновлять вручную нажатием кнопки "Обновить".
## Нюансы
&emsp; Рекомендуется отключение антивируса, так как в проекте содержится .exe файл, написанный на C#, который антивирус может считать вредоносным.
## Использованные технологии
- PyQt5 - фреймворк для работы с оконными приложениями
- FastAPI - фреймворк для передачи данных по сети
- pywin32 - библиотека для работы с буфером обмена
- Pillow - библиотека для работы с изображениями

# NetClip (en)
## Local clipboard

NetClip is a local clipboard project. To start the project you need:
- Python 3.11+
- Windows 10+
## Installation
- Clone the project:
```
git clone https://github.com/Folonder/NetClip.git
```
- Installing dependencies:
```
pip install -r requirements.txt
```
## Launch
- The project must be run as administrator
- Computers must be connected to the same network
- Run the startup.py file
```
python startup.py
```
## How to use the application
### Send data
- Send tab is open by default
- Add to IP-Manager the IP address to which you want to send
- Select data from the clipboard to send
- Press the send button
### Get data
- Open the receiving tab
- Select the data you want to copy to your clipboard
- Press the receive button
## Data format
&emsp;Data can be presented both in text format and in the form of pictures. When copying text using ctrl + c, the buffer is updated automatically; when copying pictures, you need to update it manually by clicking the "Refresh" button.
## Nuances
&emsp; It is recommended to disable the antivirus, since the project contains an .exe file written in C#, which the antivirus may consider malicious.
## Technologies used
- PyQt5 - a framework for working with window applications
- FastAPI - framework for transmitting data over the network
- pywin32 - library for working with the clipboard
- Pillow - a library for working with images

