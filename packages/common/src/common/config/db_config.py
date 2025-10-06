from typing import Dict, List

from pydantic import BaseModel, Field


class DataSourceConfig(BaseModel):
    """数据源配置类"""

    name: str = Field(description="数据源名称")

    host: str = Field(description="数据库主机地址")
    port: int = Field(default=3306, description="数据库端口")
    username: str = Field(description="数据库用户名")
    password: str = Field(description="数据库密码")
    database: str = Field(description="数据库名称")
    charset: str = Field(default="utf8mb4", description="数据库字符集")

    pool_size: int = Field(default=5, description="连接池大小")
    max_overflow: int = Field(default=10, description="连接池最大溢出数量")
    pool_timeout: int = Field(default=30, description="连接池超时时间（秒）")
    pool_recycle: int = Field(default=3600, description="连接池回收时间（秒）")

    echo: bool = Field(default=False, description="是否打印SQL语句")

    @property
    def database_url(self) -> str:
        """构建数据库连接URL"""
        return f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}?charset={self.charset}"


class DataSourceDictConfig(BaseModel):
    """数据源字典配置类"""

    datasource_dict: Dict[str, DataSourceConfig] = Field(
        default_factory=dict, description="数据源配置字典"
    )

    @classmethod
    def from_toml_list(cls, toml_list: List[Dict]) -> "DataSourceDictConfig":
        """从 TOML list 配置创建数据源配置"""
        datasource_dict = {}
        for config_dict in toml_list:
            config = DataSourceConfig(**config_dict)
            datasource_dict[config.name] = config
        return cls(datasource_dict=datasource_dict)

    def get_datasource(self, name: str) -> DataSourceConfig:
        """获取指定名称的数据源配置"""
        if name not in self.datasource_dict:
            raise ValueError(f"数据源配置 '{name}' 不存在")
        return self.datasource_dict[name]

    def list_datasource(self) -> Dict[str, DataSourceConfig]:
        """列出所有数据源配置"""
        return self.datasource_dict.copy()

    def add_datasource(self, config: DataSourceConfig):
        """添加数据源配置"""
        self.datasource_dict[config.name] = config
