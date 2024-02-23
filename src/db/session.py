from settings import database_settings
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

engine = create_async_engine(
    database_settings.url,
    pool_size=20,
    pool_pre_ping=True,
    pool_use_lifo=True,
    echo=database_settings.echo,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)
