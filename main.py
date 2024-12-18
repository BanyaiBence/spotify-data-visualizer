from json import dumps, load
from spotify import Spotify
from yattag import Doc



def list_artists(artists: dict) -> str:
    doc, tag, text = Doc().tagtext()
    with tag("html"):
        with tag("head"):
            with tag("title"):
                text("Artists")
            with tag("link", rel="stylesheet", href="style.css"):
                pass
        with tag("body"):
            with tag("h1"):
                text("Artists")
            with tag("div", klass="artists-grid"):
                for artist in artists:
                    with tag("div", klass="artist-card"):
                        with tag("h2"):
                            text(artist["name"])
                        with tag("a", href=artist["external_urls"]["spotify"]):
                            text("Spotify")
                        with tag("div"):
                            with tag("img", src=artist["images"][0]["url"], alt=artist["name"]):
                                pass
                        with tag("p"):
                            text("Genres: " + ", ".join(artist["genres"]))
                        with tag("p"):
                            text("Followers: " + str(artist["followers"]["total"]))
                        with tag("h3"):
                            text("Albums")
                        with tag("ul"):
                            for album in artist["albums"]:
                                with tag("li", onclick=f"openModal('{album['name']}', '{album['images'][0]['url']}', '{album['external_urls']['spotify']}', {dumps(album['tracks'])})"):
                                    text(album["name"])

            # Modal structure (hidden by default)
            with tag("div", klass="modal", id="albumModal"):
                with tag("div", klass="modal-content"):
                    with tag("span", klass="close-btn"):
                        text("×")
                    with tag("div", klass="modal-body"):
                        # This content will be populated dynamically by JS
                        with tag("h2"):
                            text("Album Name")
                        with tag("img", src="", alt="Album Image", klass="album-image"):
                            pass
                        with tag("p"):
                            with tag("a", href="#"):
                                text("Listen on Spotify")
                        with tag("h3"):
                            text("Tracks")
                        with tag("ul"):
                            pass

            with tag("script", src="script.js"):
                pass
                
    return doc.getvalue()






if __name__ == "__main__":
    spotify = Spotify()
    with open("artists.json", "r", encoding="UTF-8") as f:
        artist_list = load(f)["artists"]
    result_artists = []
    for artist_name in artist_list:
        artists = spotify.search_artist(artist_name)
        artist = artists["artists"]["items"][0]["id"]
        artist = spotify.get_artist(artist)
        artist["albums"] = spotify.get_albums_of_artist(artist["id"])["items"]
        for album in artist["albums"]:
            tracks = spotify.get_album(album["id"])["tracks"]["items"]
            tracks = list(map(lambda track: track["name"], tracks))
            album["tracks"] = tracks
        result_artists.append(artist)

    with open("index.html", "w", encoding='UTF-8') as f:
        f.write(list_artists(result_artists))
