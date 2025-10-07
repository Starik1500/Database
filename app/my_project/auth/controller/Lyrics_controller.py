from flask import jsonify, request
from ..dao.Lyrics_dao import (
    insert_lyrics_in_dao,
    create_lyrics,
    get_lyrics_by_id,
    get_all_lyrics as dao_get_all_lyrics,
    update_lyrics as dao_update_lyrics,
    delete_lyrics as dao_delete_lyrics
)
from flasgger import swag_from

def serialize_lyrics(lyrics):
    """Helper function to serialize a lyrics entry."""
    return {
        'id': lyrics.id,
        'lyric': lyrics.lyric,
        'songwriter': lyrics.songwriter,
        'song_id': lyrics.song_id
    }

@swag_from({
    'tags': ['Lyrics'],
    'responses': {
        200: {
            'description': 'List of lyrics entries',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'lyric': {'type': 'string'},
                        'songwriter': {'type': 'string'},
                        'song_id': {'type': 'integer'}
                    }
                }
            }
        }
    }
})

def get_all_lyrics():
    """Retrieve all lyrics entries."""
    lyrics_entries = dao_get_all_lyrics()
    lyrics_data = [
        {'id': lyrics.id, 'lyric': lyrics.lyric, 'songwriter': lyrics.songwriter, 'song_id': lyrics.song_id}
        for lyrics in lyrics_entries
    ]
    return jsonify(lyrics_data)

@swag_from({
    'tags': ['Lyrics'],
    'parameters': [
        {'name': 'lyrics_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {
            'description': 'Single lyrics entry',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'lyric': {'type': 'string'},
                    'songwriter': {'type': 'string'},
                    'song_id': {'type': 'integer'}
                }
            }
        },
        404: {'description': 'Lyrics entry not found'}
    }
})

def get_lyrics(lyrics_id):
    """Retrieve a lyrics entry by its ID."""
    lyrics = get_lyrics_by_id(lyrics_id)
    if lyrics:
        lyrics_data = {
            'id': lyrics.id,
            'lyric': lyrics.lyric,
            'songwriter': lyrics.songwriter,
            'song_id': lyrics.song_id
        }
        return jsonify(lyrics_data)
    return jsonify({'error': 'Lyrics entry not found'}), 404

@swag_from({
    'tags': ['Lyrics'],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'lyric': {'type': 'string'},
                    'songwriter': {'type': 'string'},
                    'song_id': {'type': 'integer'}
                },
                'required': ['lyric', 'songwriter', 'song_id']
            }
        }
    ],
    'responses': {
        201: {'description': 'Lyrics entry created successfully'},
        400: {'description': 'Missing parameters'},
        500: {'description': 'Internal server error'}
    }
})

def add_lyrics():
    """Add a new lyrics entry."""
    data = request.get_json()
    lyric = data.get('lyric')
    songwriter = data.get('songwriter')
    song_id = data.get('song_id')

    if not all([lyric, songwriter, song_id]):
        return jsonify({'error': 'lyric, songwriter, and song_id are required'}), 400

    result = insert_lyrics_in_dao(lyric, songwriter, song_id)
    if "error" in result:
        return jsonify(result), 500
    else:
        return jsonify(result), 201

@swag_from({
    'tags': ['Lyrics'],
    'parameters': [
        {'name': 'lyrics_id', 'in': 'path', 'type': 'integer', 'required': True},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'lyric': {'type': 'string'},
                    'songwriter': {'type': 'string'},
                    'song_id': {'type': 'integer'}
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Lyrics entry updated successfully'},
        404: {'description': 'Lyrics entry not found'}
    }
})

def update_lyrics(lyrics_id):
    """Update an existing lyrics entry."""
    data = request.get_json()
    lyric = data.get('lyric')
    songwriter = data.get('songwriter')
    song_id = data.get('song_id')

    updated_lyrics = dao_update_lyrics(lyrics_id, lyric, songwriter, song_id)
    if updated_lyrics:
        return jsonify({'message': 'Lyrics entry updated successfully', 'id': updated_lyrics.id})
    return jsonify({'error': 'Lyrics entry not found'}), 404

@swag_from({
    'tags': ['Lyrics'],
    'parameters': [
        {'name': 'lyrics_id', 'in': 'path', 'type': 'integer', 'required': True}
    ],
    'responses': {
        200: {'description': 'Lyrics entry deleted successfully'},
        404: {'description': 'Lyrics entry not found'}
    }
})

def delete_lyrics(lyrics_id):
    """Delete a lyrics entry by its ID."""
    success = dao_delete_lyrics(lyrics_id)
    if success:
        return jsonify({'message': 'Lyrics entry deleted successfully'})
    return jsonify({'error': 'Lyrics entry not found'}), 404
