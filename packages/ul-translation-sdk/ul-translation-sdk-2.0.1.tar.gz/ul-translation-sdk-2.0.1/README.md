# Translation

Сервис переводов

Для понимания это управление умной экселькой, в которой первая колонка это ключ перевода, а вторая и последующие колонки - перевод на разных языках (каждая колонка - это новый язык)

## Make New Enc Keys
```bash
ulapiutls enc_keys --algorithm RS256 --follower-services translation-web --service-name translation-auth --jwt-permissions-module src.conf.permissions --jwt-environment local --jwt-user-id 6ff8eaba-b5b4-49b2-9a83-f48fcdf6d361
```

## Services

- translation__balancer = nginx
- translation__public_api = flask+sqlalchemy
- translation__internal_api = flask+sqlalchemy
- translation__auth_api = COMMON SERVICE
- translation__management_view = flask+jingja2
- translation__db = pg14
- translation__db_ui = pgweb

## Структура хранимых данных
```yaml
lang:
    id: uuid, pk
    user_created: uuid, fk(api_user)
    user_modified: uuid, fk(api_user)
    date_created: date-time, utc
    date_modified: date-time, utc
    is_alive: bool

    name: str(255), uniq  # human readable text in ANY LANGUAGE
    abbr: str(10), uniq, ASCII symbols only, RESTRICT WHITE SPACES  # exaples - en, ru, en_EN, en_US, ...

key:
    id: uuid, pk
    user_created: uuid, fk(api_user)
    user_modified: uuid, fk(api_user)
    date_created: date-time, utc
    date_modified: date-time, utc
    is_alive: bool

    name: str(255), uniq, ASCII symbols only, RESTRICT WHITE SPACES !!!!   # examples - "account.something.0.else",   "user_profile.full_name", "name"  

translation:  # не может стать удаленным или помечен быть как удален
    id: uuid, pk
    user_created: uuid, fk(api_user)
    user_modified: uuid, fk(api_user)
    date_created: date-time, utc
    date_modified: date-time, utc

    lang_id: fk(lang)
    key_id: fk(key)
    content: text  #  ЛЮБАЯ СТРОКА. БЕЗ ВАЛИДАЦИИ. ПУСТАЯ СТРОКА ВАЛИДНА

translation_cache:  # material-view, trigger(translation, key, lang). ТОЛЬКО активные записи
    translation_id: uuid, fk(translation)
    lang_abbr: str(10)
    key_name: str(255)
    translation_content: text

    # constaint: uniq_together(lang_id, key_id, content)
```

### PUBLIC API service

#### GET `/lang/en_EN/translation-cache`
где `en_EN` - это существующая абривиатура языка

нет авторизации. ЛЮБОЙ может получить ответ

Кэш запроса на уровне `nginx` = 1 час

Строится ответ по таблице `translation-cache`

ключи сортируются согласно alpha-numeric

```json
{
    "key.name": "translation_content",
    "field.0.some": "translation_content 2",
    /*другие ключи этого языка и переводы к ним*/
}
```

если такого языка не найдено в `translation_cache` то возвращается пустой обьект со статусом 404

#### GET `/lang/en_EN/translation-cache-compiled`

тоже самое что и GET `/lang/en_EN/translation-cache` НО ключи разворачиваются согласно точкам в структуры обьектов

если точка вначале или в конце - игнорируются

Напрмер `key.name` - это вложенные обьекты. в первом есть атрибут `key` и его значение равен обьекту у которого есть ключ `name`. пустая строка = валидное проперти обьекта


```json
{
    "key": {
        "name": "translation_content",
    },

    "field": {
        "0": {
            "some": "translation_content 2"
        }
    },
    /*другие ключи этого языка и переводы к ним*/
}
```

Решением построения дерева предлагается как утилитарная функция
```python
def set_obj_attr_by_path(mut_obj: Dict[str, Any], path_key: str, value: Any) -> NDict[str, Any]:
    obj = mut_obj 
    segments = path_key.strip(".").split(".")
    for i, segment in enumerate(segments):
        if i == (len(segments) - 1):
            obj[segment] = value
        else:
            if segment not in obj:
                obj[segment] = dict()
            obj = obj[segment]
    return mut_obj
```

## INTERNAL API service
### Languages API
#### GET `/langs`
Получение списка всех (даже неактивных) языков 
(при создании нового, создаются записи для всех переводов `translation` по всем существующим ключам с пустым контентом)
```json
/* Response example */
[
    {
        "id": "...",
        "user_created": "...",
        "user_modified": "...",
        "date_created": "...",
        "date_modified": "...",
        "is_alive": "...",

        "name": "English",
        "abbr": "en_EN",
    },
    ...
]
```

#### GET `/langs/:id`
Получение списка конкретного языка

```json
/* Response example */
{
    "id": "...",
    "user_created": "...",
    "user_modified": "...",
    "date_created": "...",
    "date_modified": "...",
    "is_alive": "...",

    "name": "English",
    "abbr": "en_EN",
}
```

#### POST `/langs/`
Созданиен языка
```json
/* Request example */
{
    "name": "Russian",
    "abbr": "ru_RU",
}
```

#### PUT `/langs/:id`
Изменение конкретного языка
```json
/* Request example */
{
    "id": "...",
    "user_created": "...",
    "user_modified": "...",
    "date_created": "...",
    "date_modified": "...",
    "is_alive": "...",

    "name": "Russian",
    "abbr": "ru_RU",
}
```

#### DELETE `/langs/:id`
Удаление конкретного языка


### Keys API
#### GET `/keys`
Получение списка всех (даже неактивных) ключей 

```json
/* Response example */
[
    {
        "id": "...",
        "user_created": "...",
        "user_modified": "...",
        "date_created": "...",
        "date_modified": "...",
        "is_alive": "...",

        "name": "field.3.some",
    },
    ...
]
```

#### GET `/keys/:id`
Получение списка конкретного ключа

```json
/* Response example */
{
    "id": "...",
    "user_created": "...",
    "user_modified": "...",
    "date_created": "...",
    "date_modified": "...",
    "is_alive": "...",

    "name": "field.3.some",
}
```

#### POST `/keys/`
Созданиен ключа
```json
/* Request example */
{
    "name": "field.3.some",
}
```

#### PUT `/keys/:id`
Изменение конкретного ключа
```json
/* Request example */
{
    "id": "...",
    "user_created": "...",
    "user_modified": "...",
    "date_created": "...",
    "date_modified": "...",
    "is_alive": "...",

    "name": "field.3.some",
}
```

#### DELETE `/keys/:id`
Удаление конкретного языка


### Translation API
#### GET `/translations`
Получение списка всех переводов 

```json
/* Response example */
[
    {
        "translation_id": "fk(translation).id",
        "lang_abbr": "en_EN",
        "key_name": "field.3.some",
        "translation_content": "",
    },
    ...
]
```

#### GET `/translations/:id`
Получение списка конкретного переводов

```json
/* Response example */
{
    "translation_id": "fk(translation).id",
    "lang_abbr": "en_EN",
    "key_name": "fields.3.some",
    "translation_content": "some text",
}
```

#### POST `/translations`
Созданиен ключа
```json
/* Request example */
{
    "translation_id": "fk(translation).id",
    "content": "some text",
}
```

#### PUT `/translations`
Изменение конкретного ключа
```json
/* Request example */
[
    {
        "translation_id": "fk(translation).id",
        "content": "some text",
    }
]
```


### View service
Работает через логин в котором вставляется токен авторизации в поле при старте приложения

Токен генерируется в Auth Api

pages:
- Login
- Lang 
- Keys
- Translation 
- Import *
- Export *

#### Login Page

Одно поле - токен, который потом записывается в куку, если токен валиден

#### Lang Page
это таблица со всеми языками (даже с неактивными)

можно редактировать языки, добавлять, удалять - через модалку

модалка - поля, кнопка сохранить, кнопка отменить

#### Keys Page
это таблица со всеми ключами (даже с неактивными)

можно редактировать ключи, добавлять, удалять - через модалку

модалка - поля, кнопка сохранить, кнопка отменить

#### Translation Page
таблица строится по `translation_cache` и `key`

Выводятся Абсолютно все активные записи

колонки:
- ПЕРВАЯ КОЛОНКА = key_name  всех активных ключей
- остальные колонки это все доступные АКТИВНЫЕ языки и переводы к ним

Ячейки в которых нет текста должны подстветиться оранжевым (или другим ярким) цветом

строки отсортированы по имени ключа

Нажимая на строку (или только на ключ строки) открывается модалка с изменениями сразу всех возможных переводов для данного ключа. ключ менять нельзя. после применения страница перезагружается

модалка - поля, кнопка сохранить, кнопка отменить

#### Export Page *
Кнопка с генерацией файла на скачку

Формат файла - JSON

Экспортируются ТОЛЬКО активные записи !

```json
{
    "langs": [{/*... все поля языков*/}, /*...*/],
    "key": [{/*... все поля ключей*/}, /*...*/],
    "translation": [{/*... все поля переводов*/, /*...*/}],
}
```

#### Import Page *
На странице есть кнопка с загрузкой файла

Формат файла точно соответсвует формату файла экспорта. 

Любое несоотвествие, лишние поля итп - ошибка !

Если такой айди существует - контент заменяется

Применяется одной транзакцией
