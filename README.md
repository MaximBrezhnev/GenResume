# GenResume
# Описание проекта
Данный проект разработан с использованием Django REST
Framework и представляет собой API
для конструктора резюме.

Идея проекта заключается в следующем: пользователь
вводит в форме название позиции, которую он
хочет включить в свое резюме. Далее, согласно определенному алгоритму, пользователь через форму, выбирая
необходимые данные, формирует содержание своего резюме (например,
опыт в рамках указанной позиции), которое затем он может
получить в формате PDF
на указанный адрес электронной почты. Причем таких позиций в резюме
может быть несколько.


# Принцип работы

API предполагает возможность реализовать для него фронтэнд, работа которого должна
четко соответствовать указанному ниже алгоритму для корректного функционирования бэкенда
1. Пользователь в форме вводит название позиции на
эндпоинт api/v1/resumes/check-position/.
2. Если позиции не существует, то пользователь должен увидеть форму, в которой
уже заполнено название позиции, которую вернул эндпоинт в п.1, а также
присутствует поле, которое позволяет выбрать тип позиции из тех, что
вернул эндпоинт в п.1.
Данные, введенные в форму, должны быть отправлены
на эндпоинт api/v1/resumes/create-position/, где будет создана новая позиция
в базе данных и возвращен список отраслей для выбора
3. Если позиция существует, то пользователь должен увидеть форму с
заполненным полем, содержащим возвращенную бэкендом позицию, а также поле,
содержащее список отраслей, из которого надо выбрать одну и отправить
на эндпоинт api/v1/resumes/list-of-competencies/ (Форма описанная в этом
пункте также должна быть
отображена в случае удачной работы эндпоинта из пункта 2)
4. Затем пользователь видит резюме, которое он сформировал и получает выбор:
отправить эти данные ему в формате PDF (эндпоинт
api/v1/resumes/get-resume/) на почту или вернуться в начало
и дополнить резюме новыми позициями (причем теперь все ответы API и запросы
к нему будут содержать id документа для этого пользователя).

Примечание: если при использовании эндпоинта api/v1/resumes/list-of-competencies/
оказывается, что такая позиция и отрасль
уже есть в документе, то пользователю дается выбор: вернуться к п.1 и
ввести новую позицию или вернуться к выбору отрасли (с той же позицией).

# Установка

1. Клонируйте репозиторий
```
git clone https://github.com/MaximBrezhnev/GenResume.git
```

2. Установите на свое устройство docker и docker compose

3. Перейдите в папку проекта
4. Создайте файл .env в данной папке по аналогии с файлом .env.example

5. Запустите контейнеры с приложением, background worker'ом celery, redis, nginx, postgres командой
```
docker compose up -d
```

# Документация

По следующей ссылке доступна документация проекта:

http://localhost/api/schema/docs/

При тестировании работы фронтэнда в связке с API необходимо использовать
данные, полученные на предыдущем шаге описанного алгоритма. В качестве примера
позиции, существующей в базе данных, для эндпоинта /api/v1/resumes/check-position/
можете использовать "Менеджер по продажам".
