import time
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil

def organize_desktop():
    desktop_path = os.path.expanduser("~/Desktop")
    files = os.listdir(desktop_path)

    for file in files:
        if file.startswith('.') or os.path.isdir(os.path.join(desktop_path, file)):
            continue
        if file.endswith(('.lnk', '.ini', '.url')):
            continue

        _, ext = os.path.splitext(file)
        destination_dir = os.path.join(desktop_path, ext[1:].upper() + "_Files")
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
        move_success = False
        while not move_success:
            try:
                shutil.move(os.path.join(desktop_path, file), os.path.join(destination_dir, file))
                move_success = True
            except PermissionError:
                print(f"Erro ao mover {file}: O arquivo está sendo usado por outro processo. Tentando novamente em 5 segundos...")
                time.sleep(5)

class DesktopHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        organize_desktop()

def monitor_desktop():
    observer = Observer()
    observer.schedule(DesktopHandler(), path=os.path.expanduser("~/Desktop"), recursive=False)
    observer.start()
    return observer

def main():
    organize_desktop()
    observer = monitor_desktop()

    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()

if __name__ == "__main__":
    main()
