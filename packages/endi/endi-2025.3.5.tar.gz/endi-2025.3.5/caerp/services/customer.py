"""
- Construire la query 
    - Quels éléments on requiert
    (- Restreindre les champs que l'on requiert)
    - Ajouter les jointures
    - Ajouter les filtres
-----> Compter les résultats
    - Trier les résultats
    - Paginer les résultats

- Constuire la réponse


customer_list_tool = CustomerListTool(request, options)


class CustomerListTool:
    def __init__(self, request, options):
        self.request = request
        self.options = options
        self.query_builder = CustomerQueryBuilder(options)

    def count_results(self, query=None):
        if query is None:
            query = self.query_builder.count_query()
        return self.request.dbsession.execute(query).scalar()

    def get_results(self):
        query = self.query_builder.build_main_query()
        number_items = self.count_results(query)
        query = self.sort_query(query)
        query = self.paginate_query(query)
        return {
            "entries": self.request.dbsession.execute(query).scalars().all(), 
            "count": number_items
        }
"""
import inspect
import typing
from sqlalchemy import select, asc, desc

from sqlalchemy.sql.expression import Select
from caerp_base.models.base import DBBASE


class BaseListQueryBuilder:
    """
    Base class used to build list queries
    """
    factory = None
    sort_columns = {}
    default_sort = None
    default_sort_direction = "asc"

    def __init__(self, request, options):
        self.request = request
        self.options = options

    def query(self):
        return select(self.factory)
    
    def _get_filters(self):
        """
        collect the filter_... methods attached to the current object
        """
        for key in dir(self):
            if key.startswith("filter_"):
                func = getattr(self, key)
                if inspect.ismethod(func):
                    yield func

    def _filter(self, query, appstruct):
        """
        filter the query with the configured filters
        """
        for method in self._get_filters():
            query = method(query, appstruct)
        return query
    
    def build_main_query(self, appstruct) -> Select:
        query = self.query()
        query = self._filter(query, appstruct)
        return query
    
    def _sort(self, query, key: typing.Optional[str], direction: typing.Optional[str]) -> Select:
        """
        Sort the results regarding the default values and
        the sort_columns dict, maybe overriden to provide a custom sort
        method
        """
        if key:
            custom_sort_method = getattr(self, f"sort_by_{key}", None)
            if custom_sort_method is not None:
                query = custom_sort_method(query, key, direction)
            else:
                sort_column = self.sort_columns.get(key)
                if sort_column:
                    sort_direction = self._get_sort_direction(appstruct)

                    if sort_direction == "asc":
                        func = asc
                        query = query.order_by(func(sort_column))
                    elif sort_direction == "desc":
                        func = desc
                        query = query.order_by(func(sort_column))
        return query

    def _paginate(self, query, items_per_page, page):
        """
        Add limit and offset to the query regarding the pagination query
        parameters

        :param obj query: The query to paginate
        :param dict appstruct: The filter datas that were provided
        :returns: The paginated query
        """
        query = query.offset(page * items_per_page)
        query = query.limit(items_per_page)
        return query


class CustomerListQueryBuilder(BaseListQueryBuilder):

