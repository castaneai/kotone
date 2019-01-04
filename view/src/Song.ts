interface AlbumArtRef {
    url: string
}

export interface Song {
    id: string
    albumArtRef: AlbumArtRef[]
    title: string
    artist: string
}