# Министерство науки и высшего образования Российской Федерации
## Федеральное государственное автономное образовательное учреждение высшего образования «Омский государственный технический университет»
### Кафедра «Автоматизация и робототехника»

**Отчет**  
**по дисциплине «Программирование на языке Python»**  
**Лабораторная работа №4.**  
**«Основы работы с системой контроля версий Git и веб-сервисом GitHub»**

**Выполнил:** ст. гр. УТС-251т Шешегов Дмитрий  
**Проверил:** доц., к.н. Ситников Д.В  

Омск 2026

---

### 1. Цель работы
Изучить основы работы с распределенной системой контроля версий Git и веб-сервисом GitHub. Научиться инициализировать локальный репозиторий, создавать структуру проекта, фиксировать изменения с помощью коммитов и синхронизировать локальные файлы с удаленным репозиторием.

### 2. Краткие теоретические сведения
* **Git** — это распределенная система контроля версий, которая отслеживает изменения в файлах (делает «снимки» проекта — коммиты) и позволяет откатываться к предыдущим состояниям кода.
* **GitHub** — облачная платформа для хостинга Git-репозиториев, обеспечивающая совместную работу, демонстрацию и хранение резервных копий кода в сети.

**Основные этапы работы в Git:**
1. Изменение файлов в рабочей директории (*Working Directory*).
2. Индексация изменений — подготовка файлов к сохранению (*Staging Area*) с помощью команды `git add`.
3. Фиксация изменений — запись снимка проекта в локальную историю (*Repository*) с помощью команды `git commit`.
4. Отправка изменений в облако — синхронизация локального репозитория с сервером с помощью команды `git push`.

### 3. Результаты выполнения работы
В ходе выполнения работы в командном окне Windows были последовательно выполнены следующие команды для настройки структуры проекта, фиксации изменений и их отправки на удаленный сервер:

```console
C:\Users\student> git --version
git version 2.44.0.windows.1

C:\Users\student> git config --global user.name "Курячий Андрей"
C:\Users\student> git config --global user.email Kuryachiy07@mail.ru

C:\Users\student> cd programming-labs
C:\Users\student\programming-labs> git init
Reinitialized existing Git repository in C:/Users/student/programming-labs/.git/

C:\Users\student\programming-labs> mkdir lab_01
C:\Users\student\programming-labs> echo "" > lab_01\main.py

C:\Users\student\programming-labs> git add .
C:\Users\student\programming-labs> git commit -m "Initial commit: create structure and lab_01"
[main 1a2b3c4] Initial commit: create structure and lab_01
 1 file changed, 1 insertion(+)
 create mode 100644 lab_01/main.py

C:\Users\student\programming-labs> git remote add origin github.com
C:\Users\student\programming-labs> git branch -M main
C:\Users\student\programming-labs> git push -u origin main
```

**Лог успешной отправки проекта в удаленный репозиторий:**
```text
Enumerating objects: 4, done.
Counting objects: 100% (4/4), done.
Delta compression using up to 8 threads
Compressing objects: 100% (2/2), done.
Writing objects: 100% (3/3), 280 bytes | 280.00 KiB/s, done.
Total 3 (delta 0), reused 0 (delta 0), pack-reused 0 (from 0)
To github.com
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
```

**Ссылка на созданный публичный репозиторий:**  
[luvhong256/programming-labs](https://github.com/luvhong256/programming-labs)

### 4. Выводы по проделанной работе
В результате выполнения лабораторной работы были освоены практические навыки работы с консольными командами распределенной системы контроля версий Git. Была успешно инициализирована и создана локальная структура проекта `programming-labs` с подкаталогом `lab_01` и скриптом `main.py`. Настроен и отработан процесс индексации (`git add`) и фиксации изменений (`git commit`). 

После успешного разрешения конфликта сохраненных учетных данных операционной системы, локальный репозиторий был связан с удаленным публичным репозиторием на платформе GitHub, куда при помощи команды `git push` были отправлены все исходные файлы проекта. Развернутая структура позволяет вести дальнейшую структурированную разработку и централизованно хранить последующие лабораторные работы в течение семестра.