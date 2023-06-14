# -shell_3

Техническое задание на разработку системы

Постановка задачи

Условия работы системы Имеется база (видеопоток) примеров людей с оружием.

Требуется разработать модуль распознавания в видеопотоке человека, держащего в руках оружие: пистолет или автомат (далее обьект - O ) со следующими критериями точности: ложноположительное распознание - не более 5% ложноотрицательное распознание - не более 3% Система должна распознать данный объект на сцене, аналогичной следующей:

Распознавание оружия должно работать на камерах с разрешением от 2mp (2mp maximal resolution - 1600 x 1200 (Width * Height) )

Высота объекта от 250 пикселей

Скорость распознавания от 2х секунд с момента появления человека с оружием в кадре

Требования к интеграционной части Облачный сервер заказчика

Ссылки на датасеты заказчика:
https://drive.google.com/file/d/1pPOePt6SHrM_xNVGWuBLOjwBTYwXX9N2/view?usp=drive_link  (test dataset)

https://drive.google.com/file/d/1l2Kuor1DsOPPeViwd1mQLL6zE578SJLe/view?usp=sharing  (train dataset)

https://drive.google.com/file/d/1jInsh5FiQabLsfGWldzdC7ChqDTimdCs/view?usp=drive_link  (test dataset)

Ссылка на ТЗ по раскадровке - https://docs.google.com/document/d/11SbjcFItnXCkLv0nqjfmA6D8bHNGYtp1OTRhbvdqrlA/edit?usp=sharing


Ссылка на таблицу с результатами экспериментов - https://docs.google.com/spreadsheets/d/1mkLEyEIA9nmPby4vUsFGXcbFgXwK8FxeHVyxBl4PKCM/edit?usp=sharing
