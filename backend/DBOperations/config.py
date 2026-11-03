"""Чтение .env"""

class Config:
    def __init__(self):
        self.mode = "test"
    def set_mode(self, mode="test"):
        """Установка режима базы данных: тестировочный или продакшн"""
        
        if mode in ["test", "prod"]:
            self.mode = mode
        else:
            raise ValueError("Type 'test' mode or 'prod' mode in config!")
        
        return True
