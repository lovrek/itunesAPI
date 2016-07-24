<?php
/**
 * Created by PhpStorm.
 * User: root
 * Date: 7/14/16
 * Time: 1:16 PM
 */

function parsingJSON($filename)
{
    $object = file_get_contents($filename);

    $tracksID = [];

    if ($object != "{}") {
        $json = json_decode($object, true);

        /* Connect to MySQLI */
        include 'connect_mysqli_kiki_viberate.php';
        /* SQL if  */
        $sql = "SELECT itunes_connection_artist_track.track_id FROM itunes_connection_artist_track LEFT JOIN itunes_tracks ON itunes_connection_artist_track.track_id = itunes_tracks.track_id WHERE itunes_tracks.track_id IS NULL";
        $result = $conn_kiki_viberate->query($sql);

        if ($result->num_rows > 0) {
            while ($row = $result->fetch_assoc()) {
                array_push($tracksID, $row['track_id']);
            }
        }

        if (sizeof($tracksID) > 0) {
            foreach ($json["data"]["tracks"] as $key => $event) {

                /* check if track is not in database and add it */
                if (in_array($event["track_id"], $tracksID)) {
                    $sql = 'INSERT INTO itunes_tracks (track_id,track_album_id,track_title,track_album,track_released, track_duration, track_artists, track_url, genre_name)';
                    $sql .= ' VALUES ';
                    $sql .= '(' . (int)$event["track_id"] . ',' . (int)$event["collection_id"] . ',"' . mysqli_real_escape_string($conn_kiki_viberate, $event["track_title"]) . '","' . mysqli_real_escape_string($conn_kiki_viberate, $event["collection_name"]) . '",' . (int)$event["release_date"] . ',' . (int)$event["duration"] . ',"' . mysqli_real_escape_string($conn_kiki_viberate, $event["artist_name"]) . '","' . mysqli_real_escape_string($conn_kiki_viberate, $event["url"]) . '","' . mysqli_real_escape_string($conn_kiki_viberate, $event["genre_name"]) . '")';

                    if ($conn_kiki_viberate->query($sql) != True) {
                        echo $sql;
                        echo "\nInsert was faild! \n";
                    }
                }
            }

            /* Close connection */
            $conn_kiki_viberate->close();

        } else {
            echo "No new tracks";
        }

    } else {
        echo "JSON is empty \n";
    }

    return 0;
}

function readFileName()
{
    /* Connect to MySQLI */
    include 'connect_mysqli_kiki_viberate.php';

    $sql = "SELECT DISTINCT artist_id FROM itunes_connection_artist_track";
    $result = $conn_kiki_viberate->query($sql);

    if ($result->num_rows > 0) {
        while ($row = $result->fetch_assoc()) {
            $filename = $row['artist_id'] . '.json';
            if (file_exists($filename)) {
                parsingJSON($filename);
            } else {
            }
        }
    }
}


readFileName();