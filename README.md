
В 13 строку вставить свой ID и в файл proxy.txt, добавить прокси.  
Сколько проксей, столько и потоков на 1 акк.  

Хотите несколько акков, тогда делайте отдельны папки и повторяйте для них 


## Получение ID
Откройте консоль (F12) и ввидите следующую команду в консоле: 
```
console.log(localStorage.getItem('userId'))
```
![292853742-31d0e16e-df2f-443a-a141-910d16052ed9](https://github.com/user-attachments/assets/68a184bf-f7a9-4318-b0f8-b3177738054b)


## Прокси такого вида
```
'http://user:password@ip:port',
'socks5://user:password@ip:port',
```

# Установка:
1. Установить python (Протестировано на 3.11)

2. Установить модули
   
   ```
   pip install -r requirements.txt
   ```
 
   или
   
   ```
   pip3 install -r requirements.txt
   ```



3. Запуск
   ```
   python gr.py
   ```

   или

   ```
   python3 gr.py
   ```
