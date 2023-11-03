import re


def convert_snake_to_camel(string: str):
    temp = re.split('_+', string)

    res = temp[0] + ''.join(map(lambda x: x.title(), temp[1:]))
    return res


def is_same_db_data(row, update_data):
    is_same = True
    for column in update_data.keys():
        if update_data[column] != getattr(row, column):
            is_same = False
            break
    return is_same


def row2dict(row, snake_to_camel=False):
    d = {}
    for column in row.__table__.columns:
        new_col_name = convert_snake_to_camel(
            column.name) if snake_to_camel else column.name
        d[new_col_name] = getattr(row, column.name)

    return d


def rows2dict(rows, key_by=None, snake_to_camel=False, row_callback=None):
    r = {} if key_by else [None] * len(rows)
    for i in range(len(rows)):
        row = rows[i]
        d = {}
        for column in row.__table__.columns:
            new_col_name = convert_snake_to_camel(
                column.name) if snake_to_camel else column.name
            d[new_col_name] = getattr(row, column.name)

        key = d[key_by] if key_by else i
        d = row_callback(d, row) if row_callback else d
        r[key] = d

    return r


def map_row(row):
    return row2dict(row, snake_to_camel=True) | {
        'createdAt': row.created_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'updatedAt': row.updated_at.strftime('%Y-%m-%dT%H:%M:%S%z')
    }
