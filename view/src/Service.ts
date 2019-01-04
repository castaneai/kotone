import { Song } from "./Song";

const isLocal = () => window.location.hostname == 'localhost' && window.location.port === '3000'

const mockSongs: Song[] = [
    {
        id: '201e2de1-e072-3d4a-b546-f13f37c35f80',
        title: '夏音-フシギナイロ-',
        artist: 'Clover（CV:五十嵐　裕美・久野　美咲・木戸　衣吹・悠木　碧）',
        albumArtRef: [{url: 'https://dummyimage.com/400x400/000/fff'}],
    },
    {
        id: '5dc0ea7a-14f1-3ea7-973a-d3de964638d8',
        title: '一件落着ゴ用心',
        artist: 'イヤホンズ',
        albumArtRef: [{url: 'https://dummyimage.com/400x400/000/fff'}],
    }
]

export async function fetchSongs(): Promise<Song[]> {
    if (isLocal()) {
        return new Promise<Song[]>((resolve, reject) => {
            setTimeout(() => {
                const songs = mockSongs.concat(mockSongs).concat(mockSongs).concat(mockSongs)
                resolve(songs)
            }, 3000);
        })
    }
    const resp = await fetch('/api/songs')
    return await resp.json()
}

export function downloadSong(song: Song) {
    window.location.assign(`/api/download/${song.id}`)
}

export async function getStreamUrl(song: Song): Promise<string> {
    if (isLocal()) {
        return new Promise<string>((resolve, reject) => {
            setTimeout(() => {
                resolve('http://www.largesound.com/ashborytour/sound/brobob.mp3')
            }, 1000);
        })
    }
    const resp = await fetch(`/api/stream/${song.id}`)
    const data = await resp.json()
    return data.stream_url;
}