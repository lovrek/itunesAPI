import itunes, json, datetime, random, MySQLdb


def SQLRequest(sql):
    list = []

    # Connect on mysql database
    db = MySQLdb.connect(host="192.168.1.50",  # your host, usually localhost
                         user="root",  # your username
                         passwd="vIbE2ol6",  # your password
                         db="viberate")  # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()

    # Use all the SQL you like
    cur.execute(sql)

    # Get all result in one arrray
    for row in cur.fetchall():
        list.append(row[0])

    db.close()

    return list


def setTrackInJSON(track, data, counter):
    data['data']['tracks'][counter] = {}
    data['data']['tracks'][counter]['track_id'] = track.track_id
    data['data']['tracks'][counter]['artist_id_itunes'] = track.artist_id
    data['data']['tracks'][counter]['artwork_url'] = track.artwork_url_100
    data['data']['tracks'][counter]['track_title'] = track.track_name
    data['data']['tracks'][counter]['artist_name'] = track.artist_name
    data['data']['tracks'][counter]['description'] = ""
    data['data']['tracks'][counter]['url'] = track.artist_view_url
    data['data']['tracks'][counter]['duration'] = track.track_time
    data['data']['tracks'][counter]['release_date'] = datetime.datetime.strptime(track.release_date[0:10],
                                                                                 "%Y-%m-%d").timestamp()
    data['data']['tracks'][counter]['updated'] = datetime.datetime.strptime(track.release_date[0:10],
                                                                            "%Y-%m-%d").timestamp()
    data['data']['tracks'][counter]['collection_name'] = track.collection_name
    data['data']['tracks'][counter]['collection_id'] = track.collection_id
    data['data']['tracks'][counter]['collection_view_url'] = track.collection_view_url
    data['data']['tracks'][counter]['country'] = track.country
    data['data']['tracks'][counter]['genre_name'] = track.primary_genre_name

    return data


def getTrackByTrackID(artistID):
    filename = str(artistID) + '.json'
    counter = 0
    first = True
    data = {}
    channelID = 'itunes_artist'

    sql = "SELECT itunes_connection_artist_track.track_id FROM itunes_connection_artist_track LEFT JOIN itunes_tracks ON itunes_connection_artist_track.track_id = itunes_tracks.track_id WHERE itunes_tracks.track_id IS NULL AND itunes_connection_artist_track.artist_id = " + str(artistID) + ""
    tracksID = SQLRequest(sql)

    if (len(tracksID) > 0):
        data['artist_id'] = artistID
        data['channel_id'] = channelID
        data['created'] = int(datetime.datetime.now().timestamp())
        data['updated'] = int(datetime.datetime.now().timestamp())
        data['status_id'] = 'ok'
        data['filename'] = str(int(datetime.datetime.now().timestamp())) + '_' + str(
            random.randint(1000, 9999)) + channelID + '.json'
        data['data'] = {}

        for track_id in tracksID:
            track = itunes.lookup(id=track_id, entity='song', proxy=1)

            if first:
                data['data']['created'] = str(int(datetime.datetime.now().timestamp()))
                data['data']['updated'] = str(int(datetime.datetime.now().timestamp()))
                data['data']['tracks'] = {}
                first = False
            data = setTrackInJSON(track[0], data, counter)
            counter += 1

        data['data']['track_gauge'] = counter

    if counter > 0:
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)


def getTop200Tracks(artistID):
    artist = artistID
    filename = str(artistID) + '.json'
    counter = 0
    data = {}
    first = True
    channelID = 'itunes_artist'

    sql = "SELECT itunes_connection_artist_track.track_id FROM itunes_connection_artist_track LEFT JOIN itunes_tracks ON itunes_connection_artist_track.track_id = itunes_tracks.track_id WHERE itunes_tracks.track_id IS NULL AND itunes_connection_artist_track.artist_id = " + str(artistID) + ""
    tracksID = SQLRequest(sql)

    if len(tracksID) > 0:

        sql = "SELECT track_id FROM itunes_connection_artist_track WHERE artist_id=" + str(artistID) + " LIMIT 0,1"

        trackID = SQLRequest(sql)[0]

        artistID = itunes.lookup(id=trackID, entity='song', proxy=1)[0].artist_id
        tracks = itunes.lookup(id=artistID, entity='song', limit=200, proxy=1)

        data['artist_id'] = artist
        data['channel_id'] = channelID
        data['created'] = int(datetime.datetime.now().timestamp())
        data['updated'] = int(datetime.datetime.now().timestamp())
        data['status_id'] = 'ok'
        data['filename'] = str(int(datetime.datetime.now().timestamp())) + '_' + str(
            random.randint(1000, 9999)) + channelID + '.json'
        data['data'] = {}

        for track in tracks[1:]:
            if int(track.track_id) in tracksID:
                if first:
                    data['data']['created'] = str(int(datetime.datetime.now().timestamp()))
                    data['data']['updated'] = str(int(datetime.datetime.now().timestamp()))
                    data['data']['tracks'] = {}
                    first = False
                data = setTrackInJSON(track, data, counter)
                counter += 1
        data['data']['track_gauge'] = counter

    if counter > 0:
        with open(filename, 'w') as outfile:
            json.dump(data, outfile)


def getAllArtists():
    sql = "SELECT DISTINCT(artist_id) FROM itunes_connection_artist_track"
    return SQLRequest(sql)



#Start script
for artist in getAllArtists():
    getTop200Tracks(artist)
    # getTrackByTrackID(artist)
