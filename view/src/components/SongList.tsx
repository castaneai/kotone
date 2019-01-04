import React, { PureComponent } from "react";
import { Song } from "../Song";
import SongItem from "./SongItem";
import { Grid } from "@material-ui/core";
import { downloadSong } from "../Service";

interface SongListProps {
    songs: Song[]
}

class SongList extends PureComponent<SongListProps> {
    handleClickDownloadSong(song: Song) {
        downloadSong(song)
    }

    render() {
        return <Grid container justify="center" spacing={32}>
            {this.props.songs.map(song => <Grid item zeroMinWidth key={song.id}>
                <SongItem song={song} onClickDownload={this.handleClickDownloadSong.bind(this)} />
            </Grid>)}
        </Grid>
    }
}

export default SongList