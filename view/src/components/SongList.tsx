import React, { SFC } from "react";
import { Song } from "../Song";
import SongItem from "./SongItem";
import { Grid } from "@material-ui/core";
import { downloadSong } from "../Service";

interface SongListProps {
    songs: Song[]
    onClickPlay: (song: Song) => void
}

const SongList: SFC<SongListProps> = ({ songs, onClickPlay }) =>
    <Grid container justify="center" spacing={32}>
        {songs.map(song => <Grid item zeroMinWidth key={song.id}>
            <SongItem song={song} onClickDownload={downloadSong} onClickPlay={onClickPlay} />
        </Grid>)}
    </Grid>

export default SongList