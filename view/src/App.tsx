import React, { Component } from 'react';
import './App.css';
import SongList from './components/SongList';
import { Song } from './Song';
import Loading from './components/Loading';
import { fetchSongs } from './Service';
import { CssBaseline } from '@material-ui/core';

interface AppState {
  songs: Song[]
}

class App extends Component<{}, AppState> {

  constructor(props: {}) {
    super(props)
    this.state = {songs: []}
  }

  async componentDidMount() {
    const songs = await fetchSongs()
    this.setState({songs})
  }

  render() {
    return <React.Fragment>
      <CssBaseline />
      {this.state.songs.length > 0 ? <SongList songs={this.state.songs} /> : <Loading />}
    </React.Fragment>
  }
}

export default App;
