import React, { Component, RefObject } from "react";
import { AppBar, Toolbar, Grid, Typography, Theme, createStyles, WithStyles, withStyles } from "@material-ui/core";
import { Song } from "../Song";

interface PlaybackProps extends WithStyles<typeof styles> {
    song: Song|null
    streamUrl: string|null
}

interface PlaybackState {
}

const styles = (theme: Theme) => createStyles({
    container: {
        padding: theme.spacing.unit,
    },
    coverImage: {
        margin: 'auto',
        display: 'block',
        width: 60,
        height: 60,
    }
})

class Playback extends Component<PlaybackProps, PlaybackState> {

    private audioRef: RefObject<HTMLAudioElement>

    constructor(props: PlaybackProps) {
        super(props)
        this.audioRef = React.createRef<HTMLAudioElement>()
        this.state = {}
    }

    componentDidUpdate() {
        console.log('did update!')
        if (this.props.streamUrl && this.audioRef.current) {
            const audio = this.audioRef.current;
            audio.currentTime = 0;
            audio.play()
        }
    }

    render() {
        const classes = this.props.classes
        const song = this.props.song
        const streamUrl = this.props.streamUrl
        return <AppBar position="sticky" color="default">
            <Toolbar>
                <Grid container justify="center" className={classes.container}>
                    <Grid item container xs={4} spacing={16}>
                        <Grid item xs={2}>
                            <img className={classes.coverImage} src={song && song.albumArtRef.length > 0 ? song.albumArtRef[0].url : 'https://dummyimage.com/4x4/eee/fff&text=+'} />
                        </Grid>
                        <Grid item xs={10} container direction="column">
                            <Grid item>
                                <Typography variant="h6">{song ? song.title : '---'}</Typography>
                                <Typography variant="caption" color="textSecondary">{song ? song.artist : '---'}</Typography>
                            </Grid>
                            <Grid item>
                                <audio src={streamUrl || ''} controls ref={this.audioRef} />
                            </Grid>
                        </Grid>
                    </Grid>
                </Grid>
            </Toolbar>
        </AppBar>
    }
}

export default withStyles(styles)(Playback)