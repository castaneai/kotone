import React, { SFC } from "react";
import { Song } from "../Song";
import { Card, CardMedia, CardContent, Typography, Theme, createStyles, WithStyles, withStyles, CardActions, Button, CardActionArea } from "@material-ui/core";
import { CloudDownload } from "@material-ui/icons";

interface SongProps extends WithStyles<typeof styles> {
    onClickDownload: (song: Song) => void
    onClickPlay: (song: Song) => void
    song: Song
}

const styles = (theme: Theme) => createStyles({
    card: {
        width: 200,
    },
    cover: {
        height: 200 * 3/4,
    },
    downloadIcon: {
        marginRight: theme.spacing.unit,
    }
})

const SongItem: SFC<SongProps> = ({ song, classes, onClickDownload, onClickPlay }) =>
    <Card className={classes.card}>
        <CardActionArea onClick={() => onClickPlay(song)}>
            <CardMedia className={classes.cover} image={song.albumArtRef && song.albumArtRef.length > 0 ? song.albumArtRef[0].url : ''} />
            <CardContent>
                <Typography noWrap variant="subtitle2">{song.title}</Typography>
                <Typography noWrap variant="caption" color="textSecondary">{song.artist}</Typography>
            </CardContent>
        </CardActionArea>
        <CardActions disableActionSpacing>
            <Button size="small" color="primary" onClick={() => onClickDownload(song)}><CloudDownload className={classes.downloadIcon} fontSize="small" />Download</Button>
        </CardActions>
    </Card>

export default withStyles(styles)(SongItem)