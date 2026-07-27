function assetUrl(name) {
    return new URL(`../static/img/Story4/Hotspots/${name}`, import.meta.url).href;
}

export const hotspots = [
    {
        id: '01',
        key: 'verwaltung',
        image: assetUrl('VerwaltungImg.svg'),
        color: '#11ff00',
        position: {
            bottom: '8vh',
            left: '65vw',
        },
        imageStyle: {
            width: '16vw',
            scale: 0.85,
            rotate: '-5deg',
        },
        labelMargin: '0 0 -20px',
    },
    {
        id: '02',
        key: 'personal',
        image: assetUrl('PersonalImg.svg'),
        color: '#7b00ff',
        position: {
            top: '50vh',
            left: '20vw',
        },
        imageStyle: {
            width: '6vw',
        },
        labelMargin: '0 0 20px',
    },
    {
        id: '03',
        key: 'unterhalt',
        image: assetUrl('UnterhaltImg.svg'),
        color: '#00eaff',
        position: {
            top: '0',
            left: '0',
        },
        imageStyle: {
            width: '30vw',
        },
        labelMargin: '20px 0 -10px',
    },
    {
        id: '04',
        key: 'baustelle',
        image: assetUrl('BaustelleImg.svg'),
        color: '#ffbb00',
        position: {
            top: '10vh',
            right: '35vw',
        },
        imageStyle: {
            width: '14vw',
        },
        labelMargin: '0 0 10px',
    },
    {
        id: '05',
        key: 'parkplatz',
        color: '#c80000',
        position: {
            top: '36vh',
            right: '20vw',
        },
        labelMargin: '0 0 10px',
    },
];
