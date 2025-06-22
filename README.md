# Обработка CSV файлов.

Скрипт для обработки CSV-файла с поддержкой:

- фильтрации по условиям `>`, `<`, `=`
- агрегации (`avg`, `min`, `max`) по числовой колонке
---
## Структура проекта:

- `app/main.py` — основной файл с запуском и логикой
- `assets/` — скриншоты для `README.md`
- `products.csv` — csv файл
- `pyproject.toml` — конфигурационный файл проекта (зависимости, настройки)  
- `tests/` — тесты для проверки кода  


---

##  Установка

```bash
pip install -e .
````

---

##  Команды запуска и примеры результатов:

### 1. Вывод всех данных из файла:

```bash
python app/main.py --file products.csv
```

![](assets/all.png)

---

### 2. Фильтрация:

```bash
python app/main.py --file products.csv --where "rating>4.6"
```

![](assets/filter.png)

---

### 3. Агрегация:

```bash
python app/main.py --file products.csv --aggregate "price=avg"
```

![](assets/aggregate.png)

---

### 4. Фильтрация + агрегация:

```bash
python app/main.py --file products.csv --where "rating>4.5" --aggregate "price=max"
```

![](assets/filter_and_aggregate.png)

---

## % покрытия тестами:

```bash
pytest --cov=app
```
![](assets/coverage.png)


