import * as d3 from 'd3'

function loadData(rawData) {
    const allData = Array.isArray(rawData) ? rawData : [];
    const telefonData = allData.filter(d => d.Category === 'telefon').map(d => {
        return {
            month: d.label || '',
            year2022: +d['2022'] || 0,
            year2023: +d['2023'] || 0,
            year2024: +d['2024'] || 0
        };
    });

    const smData = allData.filter(d => d.Category === 'sm').map(d => {
        return {
            interactionType: d.label,
            year2022: +d['2022'] || 0,
            year2023: +d['2023'] || 0,
            year2024: +d['2024'] || 0
        };
    });

    const bkeData = allData.filter(d => d.Category === 'bke').map(d => {
        return {
            month: d.label || '',
            year2022: +d['2022'] || 0,
            year2023: +d['2023'] || 0,
            year2024: +d['2024'] || 0
        };
    });

    const mehrwertData = allData.filter(d => d.Category === 'mehrwert').flatMap(d => [
        { year: 2022, category: d.label, value: +d['2022'] || 0 },
        { year: 2023, category: d.label, value: +d['2023'] || 0 },
        { year: 2024, category: d.label, value: +d['2024'] || 0 }
    ]);

    const pieData = allData.filter(d => d.Category === 'pie').map(d => ({
        Percentage: +d.Percentage || 0,
        Category: d.label
    }));

    const stats = {
        telefonRecords: {
            total2022: d3.sum(telefonData, d => d.year2022),
            total2023: d3.sum(telefonData, d => d.year2023),
            total2024: d3.sum(telefonData, d => d.year2024)
        },
        smRecords: {
            total2022: d3.sum(smData, d => d.year2022),
            total2023: d3.sum(smData, d => d.year2023),
            total2024: d3.sum(smData, d => d.year2024)
        },
        bkeRecords: {
            total2022: d3.sum(bkeData, d => d.year2022),
            total2023: d3.sum(bkeData, d => d.year2023),
            total2024: d3.sum(bkeData, d => d.year2024)
        },
        totalRecords: {
            total2022: d3.sum(telefonData, d => d.year2022) + d3.sum(smData, d => d.year2022) + d3.sum(bkeData, d => d.year2022),
            total2023: d3.sum(telefonData, d => d.year2023) + d3.sum(smData, d => d.year2023) + d3.sum(bkeData, d => d.year2023),
            total2024: d3.sum(telefonData, d => d.year2024) + d3.sum(smData, d => d.year2024) + d3.sum(bkeData, d => d.year2024)
        }
    };

    return { telefonData, smData, bkeData, mehrwertData, pieData, stats };
}

export { loadData };
