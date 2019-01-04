import React, { Component } from 'react';
import './App.css';
import SongList from './components/SongList';
import { Song } from './Song';
import Loading from './components/Loading';
import { fetchSongs, getStreamUrl } from './Service';
import { CssBaseline } from '@material-ui/core';
import Playback from './components/Playback';

interface AppState {
  songs: Song[]
  playingSong: Song|null
  playingStreamUrl: string|null
}

class App extends Component<{}, AppState> {

  constructor(props: {}) {
    super(props)
    this.state = {songs: [], playingSong: null, playingStreamUrl: null}
  }

  async componentDidMount() {
    const songs = await fetchSongs()
    this.setState({songs})
  }

  async playSong(song: Song) {
    const streamUrl = await getStreamUrl(song)
    this.setState({playingSong: song, playingStreamUrl: streamUrl})
  }

  render() {
    return <React.Fragment>
      <CssBaseline />
      <Playback song={this.state.playingSong} streamUrl={this.state.playingStreamUrl} />
      <div style={{ padding: '2em' }}>
        {this.state.songs.length > 0 ? <SongList songs={this.state.songs} onClickPlay={this.playSong.bind(this)} /> : <Loading />}
      </div>
    </React.Fragment>
  }
}

export default App;
