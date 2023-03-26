from environs import Env
import os

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
CHANNELS = env.list("CHANNELS") #majburiy kanallar ro'yxati
PGUSER = str(os.getenv("PGUSER"))
PGPASSWORD = str(os.getenv("PGPASSWORD"))
DATABASE = str(os.getenv("DATABASE"))
DB_HOST=env.str("DB_HOST")
DB_PORT=env.str("DB_PORT")
IP = env.str("ip")  # Xosting ip manzili
POSTGRES_URL=f"postgresql://postgres:V5KpU5QF3KHpLV9rYy0O@containers-us-west-45.railway.app:7613/railway"
BAZA_CHANNEL = env.list("BAZA_CHANNEL") #Baza kanal 
