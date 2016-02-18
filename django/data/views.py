from operator import __or__
from cStringIO import StringIO
import csv

from django.db.models import Q
from django.http import JsonResponse, HttpResponse

from .models import Variant, Word


def index(request):
    order_by = request.GET.get('order_by')
    direction = request.GET.get('direction')
    page_size = int(request.GET.get('page_size','0'))
    page_num = int(request.GET.get('page_num','0'))
    search_term = request.GET.get('search_term')
    format = request.GET.get('format')
    source = request.GET.getlist('source')
    filters = request.GET.getlist('filter')
    filterValues = request.GET.getlist('filterValue')

    query = Variant.objects

    # if there are multiple filters given then AND them:
    # the row must match all the filters
    if filters:
        query = query.filter(**dict(zip(filters, filterValues)))

    # search using the tsvector column which represents our document made of all the columns
    if search_term:
        query = query.extra(
            where=["variant.fts_document @@ plainto_tsquery('simple', %s)"],
            params=[search_term]
        )

    # if there are multiple sources given then OR them:
    # the row must match in at least one column
    if source:
        query_list = (Q(**{column: True}) for column in source)
        query = query.filter(reduce(__or__, query_list))

    if order_by:
        if direction == 'descending':
            order_by = '-' + order_by
        query = query.order_by(order_by)

    # count the number of rows now before paginating
    count = query.count()

    if page_size:
        start = page_size * page_num
        end = start + page_size
        query = query[start:end]

    if format == 'tsv':
        header = [field.name for field in Variant._meta.fields]
        rows =  query.values_list()

        tsv_string = StringIO()
        writer = csv.writer(tsv_string, dialect='excel', delimiter='\t')
        writer.writerow(header)
        writer.writerows(rows)
        tsv = tsv_string.getvalue()

        response = HttpResponse(tsv)
        response['Content-Type'] = 'application/vnd.ms-excel'
        response['Content-Disposition'] = 'attachment;filename="variants.tsv"'

    elif format == 'json':
        # call list() now to evaluate the query
        response = JsonResponse({'count': count, 'data': list(query.values())})
        
    response['Access-Control-Allow-Origin'] = '*'
    return response


def autocomplete(request):
    term = request.GET.get('term')
    limit = request.GET.get('limit', 10)

    query = Word.objects.raw("""
        SELECT word FROM words
        WHERE word like '%%s%'
        ORDER BY similarity(word, '%S') DESC, word
    """, [term])

    response = JsonResponse(list(query)[:limit])
    return response
