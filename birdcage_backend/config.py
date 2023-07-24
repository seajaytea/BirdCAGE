import os

DATABASE_FILE = os.environ.get('DATABASE_FILE', 'birdcage.db')
API_SERVER_PORT = int(os.environ.get('API_SERVER_PORT', 7006))
TEMP_DIR_NAME = os.environ.get('TEMP_DIR_NAME', 'tmp')
DETECTION_DIR_NAME = os.environ.get('DETECTION_DIR_NAME', 'detections')
CONCURRENCY = os.environ.get('CONCURRENCY', 10)
JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'TheseAreTheTimesThatTryMensSouls')
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')
REDIS_SERVER = os.environ.get('REDIS_SERVER', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6380)
SCRIPT_NAME = os.environ.get('SCRIPT_NAME')
