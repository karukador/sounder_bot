# Бот озвучкер
бот-озвучкер для telegram на python с SpeechKit
# Как использовать
1) Клонируйте этот репозиторий:
```
git clone https://github.com/karukador/sounder_bot.git
```
2) Установите зависимости из `requirements.txt`
3) Установите DB Browser  
4) Получите токен через [BotFather](https://telegram.me/BotFather) в Telegram 
5) Откройте терминал и подключитесь к своей виртуальной машине:  
   Посмотрите [видео](https://code.s3.yandex.net/kids-ai/video/1710521524357368.mp4) от Яндекс Практикума  
   Зайдите на сервер, используя команду (укажите IP и место расположения ключа):  
```
ssh -i <путь_до_файла_с_ключом> student@<ip_адрес_сервера>  
```
6) Получите IAM-токен, который живет 12 часов  
   Посмотрите [видео](https://code.s3.yandex.net/kids-ai/video/1710080423616925.mp4) о получении IAM-токена  
   Введите на сервере команду ниже:  
```
curl -H Metadata-Flavor:Google 169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token
```
7) Создайте файл `.env`
8) В файле `.env` вставьте ваш TOKEN, iam_token, folder_id:
```
TOKEN = "ВАШ_ТОКЕН"
IAM_TOKEN = "ВАШ_IAM-ТОКЕН"
FOLDER_ID = "ВАШ_FOLDER_ID"
```
9) Измените данные в файле system_config.py (по желанию)  
10) Запустите файл bot.py  
