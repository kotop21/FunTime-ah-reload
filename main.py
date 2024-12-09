import json
import pyautogui
import os
import pygetwindow as gw
from pynput import keyboard

CONFIG_FILE = 'config.json'
hotkey = None
click_position = None

def load_config():
    """Загрузить конфигурацию из файла."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return None

def save_config(config):
    """Сохранить конфигурацию в файл."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def on_activate():
    """Действие при активации горячей клавиши."""
    global click_position
    
    # Получаем текущее активное окно
    active_window = gw.getActiveWindow()
    
    if active_window is not None:
        active_window_title = active_window.title()  # Вызов метода title()
        print(f"Активное окно: {active_window_title}")  # Отладочная информация
        
        # Проверяем, что title окна - это строка
        if isinstance(active_window_title, str) and "java" in active_window_title.lower():
            # Запоминаем текущее положение курсора
            original_position = pyautogui.position()
            # Перемещаем курсор в заданное место и кликаем
            pyautogui.moveTo(click_position, duration=0)  # Устанавливаем длительность перемещения в 0
            pyautogui.click()
            # Возвращаем курсор на исходное место
            pyautogui.moveTo(original_position, duration=0)  # Устанавливаем длительность перемещения в 0
        else:
            print("Текущая программа не является Minecraft. Действие не выполнено.")
    else:
        print("Не удалось получить активное окно.")

def on_press(key):
    """Обрабатывает нажатия клавиш."""
    global hotkey
    try:
        if key.char == hotkey:
            on_activate()
    except AttributeError:
        # Игнорируем специальные клавиши
        pass

def main():
    global hotkey, click_position
    
    config = load_config()
    
    if config is None:
        # Этап 1: Настройка клавиши
        hotkey_input = input("Введите клавишу для выполнения действия (например, 'h'):\n").lower()
        
        if len(hotkey_input) != 1 or not hotkey_input.isalpha():
            print(f"Ошибка: горячая клавиша '{hotkey_input}' не распознана.")
            return

        hotkey = hotkey_input
        
        # Этап 2: Настройка места для клика
        print("Переместите курсор в желаемое место и нажмите Enter.")
        input("Нажмите Enter, чтобы сохранить место клика.")
        click_position = pyautogui.position()
        
        # Сохраняем конфигурацию
        config = {
            'hotkey': hotkey,
            'click_position': click_position
        }
        save_config(config)
    else:
        hotkey = config['hotkey']
        click_position = tuple(config['click_position'])

    # Запускаем слушателя
    with keyboard.Listener(on_press=on_press) as listener:
        print(f"Программа запущена. Нажмите '{hotkey}' для клика на заданное место в Minecraft. Закройте программу, нажав Ctrl+C в терминале.")
        listener.join()

if __name__ == "__main__":
    main()


#by kotop21