from apps.logger.services import MemoryLoggerService


def scheduled_task():
    MemoryLoggerService.create_log()


if __name__ == '__main__':
    scheduled_task()
    print("Success")
