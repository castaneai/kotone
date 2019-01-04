import React, { SFC } from "react";
import { Song } from "../Song";
import { Card, CardMedia, CardContent, Typography, Theme, createStyles, WithStyles, withStyles, CardActions, Button } from "@material-ui/core";
import { CloudDownload } from "@material-ui/icons";

interface SongProps extends WithStyles<typeof styles> {
    onClickDownload: (song: Song) => void
    song: Song
}

const styles = (theme: Theme) => createStyles({
    card: {
        width: 200,
    },
    cover: {
        height: 0,
        paddingTop: '100%',
    },
    downloadIcon: {
        marginRight: theme.spacing.unit,
    }
})

const SongItem: SFC<SongProps> = ({ song, classes, onClickDownload }) =>
    <Card className={classes.card}>
        <CardMedia className={classes.cover} image={song.albumArtRef.length > 0 ? song.albumArtRef[0].url : ''} />
        <CardContent>
            <Typography noWrap component="h5" variant="h5">{song.title}</Typography>
            <Typography noWrap variant="subtitle1" color="textSecondary">{song.artist}</Typography>
        </CardContent>
        <CardActions disableActionSpacing={true}>
            <Button size="small" color="primary" onClick={() => onClickDownload(song)}><CloudDownload className={classes.downloadIcon} fontSize="small" />Download</Button>
        </CardActions>
    </Card>

export default withStyles(styles)(SongItem)