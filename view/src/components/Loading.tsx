import React, { SFC } from "react"
import { CircularProgress, Grid } from "@material-ui/core"

const Loading: SFC = () =>
    <Grid container justify="center">
        <CircularProgress />
    </Grid>

export default Loading