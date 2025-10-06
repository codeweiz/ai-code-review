from contextlib import contextmanager
from typing import Dict, Generator

from common.config import appConfig
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


class DatabaseSessionFactory:
    """数据库会话工厂"""

    def __init__(self):
        self._engines: Dict[str, Engine] = {}
        self._session_factories: Dict[str, sessionmaker] = {}
        self.register_datasource()

    def register_datasource(self) -> None:
        """注册所有数据源"""
        for name, datasource_config in appConfig.datasource.list_datasource().items():
            engine = create_engine(
                url=datasource_config.database_url,
                pool_size=datasource_config.pool_size,
                max_overflow=datasource_config.max_overflow,
                pool_timeout=datasource_config.pool_timeout,
                pool_recycle=datasource_config.pool_recycle,
                echo=datasource_config.echo,
                future=True,
            )

            self._engines[name] = engine
            self._session_factories[name] = sessionmaker(
                bind=engine, autoflush=False, expire_on_commit=False, class_=Session
            )

    def get_engine(self, datasource: str = "default") -> Engine:
        """获取数据库引擎"""

        if datasource not in self._engines:
            raise ValueError(f"数据源 '{datasource}' 未注册")
        return self._engines[datasource]

    @contextmanager
    def get_session(
        self, datasource: str = "default"
    ) -> Generator[Session, None, None]:
        """获取数据库会话上下文管理器"""

        if datasource not in self._session_factories:
            raise ValueError(f"数据源 '{datasource}' 未注册")

        session_factory = self._session_factories[datasource]
        session = session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def get_session_sync(self, datasource: str = "default") -> Session:
        """获取同步数据库会话"""

        if datasource not in self._session_factories:
            raise ValueError(f"数据源 '{datasource}' 未注册")
        return self._session_factories[datasource]()
