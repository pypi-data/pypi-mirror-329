from pychurros.base import BaseRepository, T
from pychurros.dynamic_query_mixin import DynamicQueryMixin

class ChurrosRepository(BaseRepository[T], DynamicQueryMixin[T]):
    pass
