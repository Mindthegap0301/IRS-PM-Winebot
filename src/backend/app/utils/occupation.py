from app.utils.common import row2dict


def map_occupation(occupation):
    return row2dict(occupation, snake_to_camel=True) | {
        'createdAt': occupation.created_at.strftime('%Y-%m-%dT%H:%M:%S%z'),
        'updatedAt': occupation.updated_at.strftime('%Y-%m-%dT%H:%M:%S%z')
    }
