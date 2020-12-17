#Numberlink - решатель головоломки

На вход не решённая головоломка шестиугольная или прямоугольная

##Запуск
```
        python -m solve - to solve 
                  puzzle [file] - puzzle file
                  type [hex/rect] - puzzle-type
                  --out_file [file] - output file| default = ./solved_puzzles/output.txt
                  --solve_count [count] - max soves ount, if -1 not limited| default = -1
                  --line_len [len] - max line len, if -1 not limited| default = -1
                  --saves_folder [folder] - folder for saves| default = ./saves
        
        python -m solve_saved - to continue solve from save
                  save [file.json] - .json file with save
                  --out_file [file] - output file| default = ./solved_puzzles/output.txt
                  --saves_folder [folder] - folder for saves| default = ./saves
```
##Входные данные
поле где 0 это пустая ячейка.
могут быть только парные не пустые яейки
```
rect: 
        1 0 0 0 
        2 0 0 0 
        0 0 0 0
        2 0 0 0
hex:
          1 0 0
         0 0 0 0
        0 0 0 2 0
         0 0 3 0
          2 3 1
```
##Выход
    Список путей решений