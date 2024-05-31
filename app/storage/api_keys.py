import os
from dotenv import load_dotenv

class APIKeys:
    """
    환경 변수에서 API 키를 로드하는 클래스.
    """
    @staticmethod
    def load_key(key_name):
        """
        주어진 키 이름에 해당하는 API 키를 로드합니다.
        
        Args:
            key_name (str): 로드할 API 키의 이름.
        
        Returns:
            str: 로드된 API 키 값.
        """
        load_dotenv()
        return os.getenv(key_name)