"""
Query subclasses which provide extra functionality beyond simple data retrieval.
"""

from djangocg.core.exceptions import FieldError
from djangocg.db.models.fields import DateField, FieldDoesNotExist
from djangocg.db.models.sql.constants import *
from djangocg.db.models.sql.datastructures import Date
from djangocg.db.models.sql.query import Query
from djangocg.db.models.sql.where import AND, Constraint
from djangocg.utils.datastructures import SortedDict
from djangocg.utils.functional import Promise
from djangocg.utils.encoding import force_text
from djangocg.utils import six


__all__ = ['DeleteQuery', 'UpdateQuery', 'InsertQuery', 'DateQuery',
        'AggregateQuery']

class DeleteQuery(Query):
    """
    Delete queries are done through this class, since they are more constrained
    than general queries.
    """

    compiler = 'SQLDeleteCompiler'

    def do_query(self, table, where, using):
        self.tables = [table]
        self.where = where
        self.get_compiler(using).execute_sql(None)

    def delete_batch(self, pk_list, using, field=None):
        """
        Set up and execute delete queries for all the objects in pk_list.

        More than one physical query may be executed if there are a
        lot of values in pk_list.
        """
        if not field:
            field = self.model._meta.pk
        for offset in range(0, len(pk_list), GET_ITERATOR_CHUNK_SIZE):
            where = self.where_class()
            where.add((Constraint(None, field.column, field), 'in',
                    pk_list[offset:offset + GET_ITERATOR_CHUNK_SIZE]), AND)
            self.do_query(self.model._meta.db_table, where, using=using)

class UpdateQuery(Query):
    """
    Represents an "update" SQL query.
    """

    compiler = 'SQLUpdateCompiler'

    def __init__(self, *args, **kwargs):
        super(UpdateQuery, self).__init__(*args, **kwargs)
        self._setup_query()

    def _setup_query(self):
        """
        Runs on initialization and after cloning. Any attributes that would
        normally be set in __init__ should go in here, instead, so that they
        are also set up after a clone() call.
        """
        self.values = []
        self.related_ids = None
        if not hasattr(self, 'related_updates'):
            self.related_updates = {}

    def clone(self, klass=None, **kwargs):
        return super(UpdateQuery, self).clone(klass,
                related_updates=self.related_updates.copy(), **kwargs)

    def update_batch(self, pk_list, values, using):
        pk_field = self.model._meta.pk
        self.add_update_values(values)
        for offset in range(0, len(pk_list), GET_ITERATOR_CHUNK_SIZE):
            self.where = self.where_class()
            self.where.add((Constraint(None, pk_field.column, pk_field), 'in',
                    pk_list[offset:offset + GET_ITERATOR_CHUNK_SIZE]),
                    AND)
            self.get_compiler(using).execute_sql(None)

    def add_update_values(self, values):
        """
        Convert a dictionary of field name to value mappings into an update
        query. This is the entry point for the public update() method on
        querysets.
        """
        values_seq = []
        for name, val in six.iteritems(values):
            field, model, direct, m2m = self.model._meta.get_field_by_name(name)
            if not direct or m2m:
                raise FieldError('Cannot update model field %r (only non-relations and foreign keys permitted).' % field)
            if model:
                self.add_related_update(model, field, val)
                continue
            values_seq.append((field, model, val))
        return self.add_update_fields(values_seq)

    def add_update_fields(self, values_seq):
        """
        Turn a sequence of (field, model, value) triples into an update query.
        Used by add_update_values() as well as the "fast" update path when
        saving models.
        """
        # Check that no Promise object passes to the query. Refs #10498.
        values_seq = [(value[0], value[1], force_text(value[2]))
                      if isinstance(value[2], Promise) else value
                      for value in values_seq]
        self.values.extend(values_seq)

    def add_related_update(self, model, field, value):
        """
        Adds (name, value) to an update query for an ancestor model.

        Updates are coalesced so that we only run one update query per ancestor.
        """
        try:
            self.related_updates[model].append((field, None, value))
        except KeyError:
            self.related_updates[model] = [(field, None, value)]

    def get_related_updates(self):
        """
        Returns a list of query objects: one for each update required to an
        ancestor model. Each query will have the same filtering conditions as
        the current query but will only update a single table.
        """
        if not self.related_updates:
            return []
        result = []
        for model, values in six.iteritems(self.related_updates):
            query = UpdateQuery(model)
            query.values = values
            if self.related_ids is not None:
                query.add_filter(('pk__in', self.related_ids))
            result.append(query)
        return result

class InsertQuery(Query):
    compiler = 'SQLInsertCompiler'

    def __init__(self, *args, **kwargs):
        super(InsertQuery, self).__init__(*args, **kwargs)
        self.fields = []
        self.objs = []

    def clone(self, klass=None, **kwargs):
        extras = {
            'fields': self.fields[:],
            'objs': self.objs[:],
            'raw': self.raw,
        }
        extras.update(kwargs)
        return super(InsertQuery, self).clone(klass, **extras)

    def insert_values(self, fields, objs, raw=False):
        """
        Set up the insert query from the 'insert_values' dictionary. The
        dictionary gives the model field names and their target values.

        If 'raw_values' is True, the values in the 'insert_values' dictionary
        are inserted directly into the query, rather than passed as SQL
        parameters. This provides a way to insert NULL and DEFAULT keywords
        into the query, for example.
        """
        self.fields = fields
        # Check that no Promise object reaches the DB. Refs #10498.
        for field in fields:
            for obj in objs:
                value = getattr(obj, field.attname)
                if isinstance(value, Promise):
                    setattr(obj, field.attname, force_text(value))
        self.objs = objs
        self.raw = raw

class DateQuery(Query):
    """
    A DateQuery is a normal query, except that it specifically selects a single
    date field. This requires some special handling when converting the results
    back to Python objects, so we put it in a separate class.
    """

    compiler = 'SQLDateCompiler'

    def add_date_select(self, field_name, lookup_type, order='ASC'):
        """
        Converts the query into a date extraction query.
        """
        try:
            result = self.setup_joins(
                field_name.split(LOOKUP_SEP),
                self.get_meta(),
                self.get_initial_alias(),
                False
            )
        except FieldError:
            raise FieldDoesNotExist("%s has no field named '%s'" % (
                self.model._meta.object_name, field_name
            ))
        field = result[0]
        assert isinstance(field, DateField), "%r isn't a DateField." \
                % field.name
        alias = result[3][-1]
        select = Date((alias, field.column), lookup_type)
        self.select = [select]
        self.select_fields = [None]
        self.select_related = False # See #7097.
        self.aggregates = SortedDict() # See 18056.
        self.set_extra_mask([])
        self.distinct = True
        self.order_by = order == 'ASC' and [1] or [-1]

        if field.null:
            self.add_filter(("%s__isnull" % field_name, False))

class AggregateQuery(Query):
    """
    An AggregateQuery takes another query as a parameter to the FROM
    clause and only selects the elements in the provided list.
    """

    compiler = 'SQLAggregateCompiler'

    def add_subquery(self, query, using):
        self.subquery, self.sub_params = query.get_compiler(using).as_sql(with_col_aliases=True)