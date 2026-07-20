function assetUrl(name) {
    return new URL(`../src/assets/Hotspots/${name}`, import.meta.url).href;
}

export const hotspots = [
    {
        id: '01',
        key: 'verwaltung',
        label: 'Verwaltung',
        property: 'Verwaltungsgebühr',
        image: assetUrl('VerwaltungImg.svg'),
        color: '#11ff00',
        description: 'Jeder Anwohner, der hier parkt, benötigt eine Parkgenehmigung. Die Bearbeitung und Ausstellung dieser Genehmigung kostet die Gemeinde 30 € pro Stellplatz und Jahr. Bei insgesamt 350 Stellplätzen sind das 10.500 €.',
        card1: {
            headerNumber: '30€',
            description: 'admin fee / year'
        },
        card2: {
            headerNumber: '750€',
            description: 'over 25 years'
        },
        position: {
            bottom: '15vh',
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
        label: 'Personal',
        property: 'Personalkosten',
        image: assetUrl('PersonalImg.svg'),
        color: '#7b00ff',
        description: 'Der größte Einzelposten bei den Betriebskosten ist derjenige, der am wenigsten ins Auge fällt: das Personal. Pro 350 Stellplätze wird ein Vollzeitmitarbeiter für die Verwaltung dieses Parkplatzes benötigt, was 170 € pro Stellplatz und Jahr entspricht. Das macht 76 % aller jährlichen Betriebskosten aus und übersteigt über einen Zeitraum von 25 Jahren die ursprünglichen Baukosten.',
        card1: {
            headerNumber: '170€',
            description: 'personnel / year'
        },
        card2: {
            headerNumber: '4250€',
            description: 'over 25 years'
        },
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
        label: 'Unterhalt',
        property: 'Unterhaltskosten',
        image: assetUrl('UnterhaltImg.svg'),
        color: '#00eaff',
        description: 'Die Instandhaltung der Oberfläche – Ausbessern, Markieren und Sicherstellen der Nutzbarkeit – kostet 25 € pro Stellplatz und Jahr, ohne Personalkosten. Für sich genommen ist das ein bescheidener Betrag, aber über 25 Jahre summiert sich das auf 625 € pro Stellplatz, was das Instandhaltungsbudget still und leise belastet.',
        card1: {
            headerNumber: '25€',
            description: 'per space / year'
        },
        card2: {
            headerNumber: '625€',
            description: 'over 25 years'
        },
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
        label: 'Baustelle',
        property: 'Herstellungskosten für einen Parkplatz',
        image: assetUrl('BaustelleImg.svg'),
        color: '#ffbb00',
        description: 'Noch bevor dort auch nur ein einziges Auto parkt, zahlt die Stadt 270 € pro m² für die Errichtung der Fahrbahn, wobei die Nebenkosten für die Bauarbeiten noch nicht enthalten sind. Damit belaufen sich die Vorlaufkosten für einen Standardparkplatz auf 3.375 €. Und das noch bevor auch nur ein Jahr an Betriebskosten anfällt.',
        card1: {
            headerNumber: '270€',
            description: 'per m² (construction)'
        },
        card2: {
            headerNumber: '3375€',
            description: 'per parking space'
        },
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
        label: 'Parkplatz',
        property: 'Größe und Nutzungsdauer des Parkplatzes',
        color: '#c80000',
        description: 'Jeder Parkplatz nimmt 12,5 m² (5,0 × 2,5 Meter) ein, was in etwa der Fläche eines kleinen Badezimmers entspricht. Nach der Errichtung ist die Gemeinde für 25 Jahre an diese Fläche gebunden. Das ist eine ganze Generation, in der dieses Grundstück nicht als Sitzbank, Baumpflanzfläche oder Fahrradweg genutzt werden kann.',
        card1: {
            headerNumber: '12.5 m²',
            description: 'per space'
        },
        card2: {
            headerNumber: '25 years',
            description: 'committed lifespan'
        },
        position: {
            top: '30vh',
            right: '20vw',
        },
        labelMargin: '0 0 10px',
    },
];