from common.orm.base import Base
from sqlalchemy import Column, DateTime, Integer, String, Text


class Content(Base):
    """内容实体"""

    __tablename__ = "EPG_CONTENT"

    # 内容编码，唯一键
    content_code = Column(
        String(50), name="CONTENT_CODE", primary_key=True, nullable=False
    )
    # 标题
    title = Column(Text, name="TITLE", nullable=True)
    # 副标题
    sub_title = Column(Text, name="SUB_TITLE", nullable=True)
    # 类型
    base_type = Column(String(50), name="BASE_TYPE", nullable=False)
    # 基础标签
    base_tags = Column(Text, name="BASE_TAGS", nullable=True)
    # 运营标签
    op_tags = Column(Text, name="OP_TAGS", nullable=True)
    # 国家/地区
    country = Column(String(50), name="COUNTRY", nullable=True)
    # 年份
    year = Column(Integer, name="YEAR", nullable=True)
    # 演员
    actors = Column(Text, name="ACTORS", nullable=True)
    # 导演
    director = Column(Text, name="DIRECTOR", nullable=True)
    # 编剧
    compere = Column(Text, name="COMPERE", nullable=True)
    # 评分
    rating = Column(String(50), name="SCORE", nullable=True)
    # 是否高清
    hd_type = Column(Integer, name="HD_TYPE", nullable=True)
    # 一句话看点
    summary = Column(Text, name="SUMMARY_SHORT", nullable=True)

    # 内容 ID
    content_id = Column(Integer, name="CONTENT_ID", nullable=False)
    # 外部编码
    external_code = Column(String(128), name="EXTERNAL_CODE", nullable=True)
    # 内容类型
    content_type = Column(String(256), name="CONTENT_TYPE", nullable=True)
    # 查询名称
    search_name = Column(String(256), name="SEARCH_NAME", nullable=True)
    # 海报
    poster = Column(String(512), name="POSTER", nullable=True)
    # 剧照
    still = Column(String(512), name="STILL", nullable=True)
    # 图标
    icon = Column(String(512), name="ICON", nullable=True)
    # 运营图片1
    op_img1 = Column(String(512), name="OPIMG1", nullable=True)
    # 运营图片2
    op_img2 = Column(String(512), name="OPIMG2", nullable=True)
    # 基础角标
    base_mark = Column(String(512), name="BASE_MARK", nullable=True)
    # 运营角标
    op_mark = Column(String(512), name="OP_MARK", nullable=True)
    # 启用状态
    enable_status = Column(Integer, name="ENABLE_STATUS", nullable=True)
    # 服务编码
    service_code = Column(String(128), name="SERVICE_CODE", nullable=True)
    # 上传时间
    update_time = Column(DateTime, name="UPDATE_TIME", nullable=True)
    # 演员编码
    actor_codes = Column(Text, name="ACTOR_CODES", nullable=True)
    # 播放指数
    play_rate = Column(Integer, name="PLAY_RATE", nullable=True)
    # 连续剧总集数
    episode_number = Column(Integer, name="EPISODE_NUMBER", nullable=True)
    # 最大问题数
    max_issue_no = Column(Integer, name="MAX_ISSUE_NO", nullable=True)
    # 最大剧集数
    max_episode_index = Column(Integer, name="MAX_EPISODE_INDEX", nullable=True)

    def __repr__(self):
        return (
            f"<Content(content_code={self.content_code}, title='{self.title}', sub_title='{self.sub_title}',"
            f" base_type='{self.base_type}', base_tags='{self.base_tags}', op_tags={self.op_tags},"
            f" country='{self.country}', year='{self.year}', actors='{self.actors}',"
            f" director='{self.director}', compere='{self.compere}', rating={self.rating},"
            f" hd_type='{self.hd_type}', summary='{self.summary}')>"
        )

    def to_dict(self) -> dict:
        """转换为字典"""
        return {
            "content_code": self.content_code,
            "title": self.title,
            "sub_title": self.sub_title,
            "base_type": self.base_type,
            "base_tags": self.base_tags,
            "op_tags": self.op_tags,
            "country": self.country,
            "year": self.year,
            "actors": self.actors,
            "director": self.director,
            "compere": self.compere,
            "rating": float(self.rating) if self.rating else None,
            "hd_type": self.hd_type,
            "summary": self.summary,
            "poster": self.poster,
            "still": self.still,
        }
