from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from common.orm.session_factory import DatabaseSessionFactory
from sqlalchemy import or_
from sqlalchemy.orm import DeclarativeBase

# 定义泛型类型
ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseRepository(Generic[ModelType]):
    """数据库仓库基类"""

    def __init__(
        self,
        model: Type[ModelType],
        db_factory: DatabaseSessionFactory,
        datasource: str = "default",
    ):
        self.model = model
        self.datasource = datasource
        self.db_factory = db_factory

    def _session(self):
        return self.db_factory.get_session(self.datasource)

    def create(self, obj_data: Dict[str, Any]) -> ModelType:
        with self._session() as session:
            db_obj = self.model(**obj_data)
            session.add(db_obj)
            session.flush()
            session.refresh(db_obj)
            session.expunge(db_obj)
            return db_obj

    def get_by_id(self, obj_id: int) -> Optional[ModelType]:
        """根据 ID 获取记录"""

        with self._session() as session:
            result = session.query(self.model).filter(self.model.id == obj_id).first()
            if result:
                session.expunge(result)
            return result

    def get_by_field(self, field_name: str, field_value: Any) -> Optional[ModelType]:
        """根据指定字段获取记录"""

        with self._session() as session:
            field = getattr(self.model, field_name)
            result = session.query(self.model).filter(field == field_value).first()
            if result:
                session.expunge(result)
            return result

    def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """获取所有记录"""

        with self._session() as session:
            results = session.query(self.model).offset(skip).limit(limit).all()
            # 触发所有属性的加载，避免 DetachedInstanceError
            for result in results:
                session.expunge(result)
            return results

    def get_by_filters(
        self,
        filters: Dict[str, Any],
        skip: int = 0,
        limit: int = 100,
        paged: bool = True,
    ) -> List[ModelType]:
        """根据过滤条件获取记录，支持时间范围查询操作符"""

        with self._session() as session:
            query = session.query(self.model)
            for field_name, field_value in filters.items():
                # 解析操作符（如 field__gte, field__lte 等）
                if "__" in field_name:
                    field_name_base, operator = field_name.split("__", 1)
                    if hasattr(self.model, field_name_base):
                        field = getattr(self.model, field_name_base)
                        if operator == "gte":
                            query = query.filter(field >= field_value)
                        elif operator == "lte":
                            query = query.filter(field <= field_value)
                        elif operator == "gt":
                            query = query.filter(field > field_value)
                        elif operator == "lt":
                            query = query.filter(field < field_value)
                        elif operator == "ne":
                            query = query.filter(field != field_value)
                        elif operator == "in":
                            query = query.filter(field.in_(field_value))
                        elif operator == "not_in":
                            query = query.filter(field.notin_(field_value))
                        elif operator == "like":
                            query = query.filter(field.like(f"%{field_value}%"))
                elif hasattr(self.model, field_name):
                    field = getattr(self.model, field_name)
                    if isinstance(field_value, list):
                        query = query.filter(field.in_(field_value))
                    else:
                        query = query.filter(field == field_value)
            if paged:
                results = query.offset(skip).limit(limit).all()
            else:
                results = query.all()
            # 触发所有属性的加载，避免 DetachedInstanceError
            for result in results:
                session.expunge(result)
            return results

    def search(
        self,
        search_fields: List[str],
        search_term: str,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ModelType]:
        """模糊搜索"""

        with self._session() as session:
            query = session.query(self.model)
            if search_term:
                conditions = []
                for field_name in search_fields:
                    if hasattr(self.model, field_name):
                        field = getattr(self.model, field_name)
                        conditions.append(field.like(f"%{search_term}%"))
                if conditions:
                    query = query.filter(or_(*conditions))
            results = query.offset(skip).limit(limit).all()
            # 触发所有属性的加载，避免 DetachedInstanceError
            for result in results:
                session.expunge(result)
            return results

    def update(self, obj_id: int, update_data: Dict[str, Any]) -> Optional[ModelType]:
        """更新记录"""

        with self._session() as session:
            db_obj = session.query(self.model).filter(self.model.id == obj_id).first()
            if db_obj:
                for field, value in update_data.items():
                    if hasattr(db_obj, field):
                        setattr(db_obj, field, value)
                session.flush()
                session.refresh(db_obj)
                return db_obj
            return None

    def update_by_field(
        self, field_name: str, field_value: Any, update_data: Dict[str, Any]
    ) -> Optional[ModelType]:
        """根据指定字段更新记录"""

        with self._session() as session:
            field = getattr(self.model, field_name)
            db_obj = session.query(self.model).filter(field == field_value).first()
            if db_obj:
                for field_name, value in update_data.items():
                    if hasattr(db_obj, field_name):
                        setattr(db_obj, field_name, value)
                session.flush()
                session.refresh(db_obj)
                return db_obj
            return None

    def delete(self, obj_id: int) -> bool:
        """删除记录"""

        with self._session() as session:
            db_obj = session.query(self.model).filter(self.model.id == obj_id).first()
            if db_obj:
                session.delete(db_obj)
                return True
            return False

    def delete_by_field(self, field_name: str, field_value: Any) -> bool:
        """根据指定字段删除记录"""

        with self._session() as session:
            field = getattr(self.model, field_name)
            db_obj = session.query(self.model).filter(field == field_value).first()
            if db_obj:
                session.delete(db_obj)
                return True
            return False

    def count(self, filters: Optional[Dict[str, Any]] = None) -> int:
        """统计记录数量，支持时间范围查询操作符"""

        with self._session() as session:
            query = session.query(self.model)
            if filters:
                for field_name, field_value in filters.items():
                    # 解析操作符（如 field__gte, field__lte 等）
                    if "__" in field_name:
                        field_name_base, operator = field_name.split("__", 1)
                        if hasattr(self.model, field_name_base):
                            field = getattr(self.model, field_name_base)
                            if operator == "gte":
                                query = query.filter(field >= field_value)
                            elif operator == "lte":
                                query = query.filter(field <= field_value)
                            elif operator == "gt":
                                query = query.filter(field > field_value)
                            elif operator == "lt":
                                query = query.filter(field < field_value)
                            elif operator == "ne":
                                query = query.filter(field != field_value)
                            elif operator == "in":
                                query = query.filter(field.in_(field_value))
                            elif operator == "like":
                                query = query.filter(field.like(f"%{field_value}%"))
                    elif hasattr(self.model, field_name):
                        field = getattr(self.model, field_name)
                        if isinstance(field_value, list):
                            query = query.filter(field.in_(field_value))
                        else:
                            query = query.filter(field == field_value)
            return query.count()

    def exists(self, obj_id: int) -> bool:
        """检查记录是否存在"""

        with self._session() as session:
            return (
                session.query(self.model).filter(self.model.id == obj_id).first()
                is not None
            )

    def exists_by_field(self, field_name: str, field_value: Any) -> bool:
        """根据指定字段检查记录是否存在"""

        with self._session() as session:
            field = getattr(self.model, field_name)
            return (
                session.query(self.model).filter(field == field_value).first()
                is not None
            )

    def bulk_create(self, obj_data_list: List[Dict[str, Any]]) -> List[ModelType]:
        """批量创建记录"""

        with self._session() as session:
            db_objs = [self.model(**obj_data) for obj_data in obj_data_list]
            session.add_all(db_objs)
            session.flush()
            for db_obj in db_objs:
                session.refresh(db_obj)
            return db_objs

    def bulk_update(self, updates: List[Dict[str, Any]]) -> List[ModelType]:
        """批量更新记录"""

        with self._session() as session:
            updated_objs = []
            for update_data in updates:
                if "id" not in update_data:
                    continue
                obj_id = update_data.pop("id")
                db_obj = (
                    session.query(self.model).filter(self.model.id == obj_id).first()
                )
                if db_obj:
                    for field, value in update_data.items():
                        if hasattr(db_obj, field):
                            setattr(db_obj, field, value)
                    updated_objs.append(db_obj)
            session.flush()
            for db_obj in updated_objs:
                session.refresh(db_obj)
            return updated_objs

    def bulk_delete(self, obj_ids: List[int]) -> int:
        """批量删除记录，返回删除的数量"""

        with self._session() as session:
            deleted_count = (
                session.query(self.model)
                .filter(self.model.id.in_(obj_ids))
                .delete(synchronize_session=False)
            )
            return deleted_count
