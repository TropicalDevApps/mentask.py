import time
from typing import Any


class ReadFileConstraint:
    MAX_LINES = 1000

    @staticmethod
    def check_request(total_lines: int, existing_line_offset: int = 1, max_lines: int = None, chunk_size: int = 500) -> dict[str, Any]:
        """
        Evalúa el tamaño del archivo en líneas y determina la estrategia de lectura.
        """
        limit = max_lines or ReadFileConstraint.MAX_LINES

        if total_lines > limit:
            return {
                "strategy": "chunked",
                "chunk_size": chunk_size,
                "current_offset": existing_line_offset,
                "next_offset": existing_line_offset + chunk_size,
                "total_size": total_lines
            }

        return {
            "strategy": "full",
            "size": total_lines
        }

class FileReadingSession:
    """Mantiene el estado de una lectura progresiva de un archivo basado en líneas."""

    def __init__(self, path: str, total_lines: int):
        self.path = path
        self.total_size = total_lines
        self.chunks_read = []
        self.current_offset = 1  # 1-indexed lines
        self.read_attempts = 0
        self.metrics = {
            "total_chunks_read": 0,
            "total_bytes": 0,
            "time_started": time.time(),
            "chunk_timing": []
        }

    def add_chunk(self, start_line: int, end_line: int, content: str) -> None:
        """Registra un nuevo chunk leído."""
        self.chunks_read.append((start_line, end_line, content))
        self.current_offset = end_line + 1
        self.read_attempts = 0

        # Metrics update
        chunk_len = len(content.encode('utf-8')) if content else 0
        self.metrics["total_chunks_read"] += 1
        self.metrics["total_bytes"] += chunk_len
        elapsed = time.time() - self.metrics["time_started"]
        self.metrics["chunk_timing"].append((start_line, end_line, elapsed))

    def should_retry(self) -> bool:
        """Determina si se debe seguir intentando leer."""
        return self.read_attempts < 3

    def mark_attempt(self) -> None:
        """Registra un intento fallido o redundante."""
        self.read_attempts += 1

    def is_complete(self) -> bool:
        """Verifica si se ha leído todo el archivo."""
        return self.current_offset > self.total_size

    def last_chunk_content(self) -> str:
        """Retorna el contenido del último chunk leído."""
        if not self.chunks_read:
            return ""
        return self.chunks_read[-1][2]
