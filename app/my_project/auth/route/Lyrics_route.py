from my_project.auth.controller.Lyrics_controller import (
    get_all_lyrics,
    get_lyrics,
    add_lyrics,
    update_lyrics,
    delete_lyrics
)

def lyrics_add_routes(app):
    app.add_url_rule('/api/lyrics', 'get_all_lyrics', get_all_lyrics, methods=['GET'])
    app.add_url_rule('/api/lyrics/<int:lyrics_id>', 'get_lyrics', get_lyrics, methods=['GET'])
    app.add_url_rule('/api/lyrics', 'add_lyrics', add_lyrics, methods=['POST'])
    app.add_url_rule('/api/lyrics/<int:lyrics_id>', 'update_lyrics', update_lyrics, methods=['PUT'])
    app.add_url_rule('/api/lyrics/<int:lyrics_id>', 'delete_lyrics', delete_lyrics, methods=['DELETE'])
