import queue
import threading

import apprise


class NotificationHandler:
    def __init__(self, telegram_chat_ids, telegram_api_key, enabled=True):
        if enabled and telegram_chat_ids and telegram_api_key:
            self.apobj = apprise.Apprise()
            ids = ""
            for telegram_chat_id in telegram_chat_ids:
                ids += f"/{telegram_chat_id}"

            self.apobj.add(f"tgram://{telegram_api_key}{ids}")
            self.queue = queue.Queue()
            self.worker = threading.Thread(target=self.process_queue, daemon=False)
            self.worker.start()
            self.enabled = True
        else:
            self.enabled = False

    def process_queue(self):
        while True:
            item = self.queue.get()
            # Проверяем "сигнал завершения"
            if item is None:
                self.queue.task_done()
                break

            message, attachments = item
            if attachments:
                self.apobj.notify(body=message, attach=attachments)
            else:
                self.apobj.notify(body=message)
            self.queue.task_done()

    def send_notification(self, message, attachments=None):
        if self.enabled:
            self.queue.put((message, attachments or []))

    def shutdown(self):
        """
        Завершает обработчик: отправляет все уведомления и закрывает поток.
        """
        if self.enabled:
            # Сигнал завершения
            self.queue.put(None)
            self.worker.join()  # Дожидаемся завершения потока
            self.queue.join()  # Убеждаемся, что очередь пуста
            self.enabled = False
