from environs import Env

__all__ = (
    'APP_HOST',
    'APP_PORT',
    'SECRET_KEY',
)

env = Env()
env.read_env()

APP_HOST: str = env.str('APP_HOST')
APP_PORT: int = env.int('APP_PORT')
SECRET_KEY: str = env.str('SECRET_KEY')
