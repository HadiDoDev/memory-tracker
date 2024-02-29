__all__ = ['MemoryLoggerService']

from datetime import datetime

import psutil

from memory_tracker.databases import MemoryTrackerDatabase

mt_db = MemoryTrackerDatabase()


class MemoryLoggerService:
    @staticmethod
    def get_memory_info():
        mem = psutil.virtual_memory()
        total_mb = mem.total // (1024 * 1024)
        free_mb = mem.available // (1024 * 1024)
        used_mb = (mem.total - mem.available) // (1024 * 1024)
        return total_mb, free_mb, used_mb

    @staticmethod
    def create_log():
        total_mb, free_mb, used_mb = MemoryLoggerService.get_memory_info()
        current_time = int(datetime.now().timestamp())
        mt_db.insert_mem_log(
            timestamp=current_time,
            total=total_mb,
            free=free_mb,
            used=used_mb
        )
        mt_db.close()

    @staticmethod
    def logs_to_json(rows):
        json_data = []
        for row in rows:
            timestamp, total_mb, free_mb, used_mb = row
            json_data.append({
                "timestamp": timestamp,
                "total": total_mb,
                "free": free_mb,
                "used": used_mb
            })
        return json_data

    @staticmethod
    def get_logs(limit, skip):
        mem_logs = MemoryLoggerService.logs_to_json(
            mt_db.fetch_mem_logs(limit, skip)
        )
        return mem_logs
