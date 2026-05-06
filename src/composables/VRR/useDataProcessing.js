import * as d3 from 'd3'

function loadData(rawData) {
    const allData = Array.isArray(rawData) ? rawData : [];

    const getCategory = (d) => d.category ?? d.Category ?? '';
    const getChartNumber = (d) => {
        const val = d.chart_number ?? d['Chart Number'] ?? d['chart number'] ?? 0;
        return +val || 0;
    };

    const firstChartCategories = [...new Set(allData.filter(d => getChartNumber(d) === 1).map(d => getCategory(d)).filter(Boolean))];
    const secondChartCategories = [...new Set(allData.filter(d => getChartNumber(d) === 2).map(d => getCategory(d)).filter(Boolean))];

    const statsByCat = {};
    firstChartCategories.forEach(cat => {
        const rows = allData.filter(d => getCategory(d) === cat);
        statsByCat[cat] = {
            totalYear1: d3.sum(rows, d => +d['year1'] || 0),
            totalYear2: d3.sum(rows, d => +d['year2'] || 0),
            totalYear3: d3.sum(rows, d => +d['year3'] || 0),
        };
    });

    const secondChartData = allData.filter(d => getChartNumber(d) === 2).flatMap(d => [
        { year: 'year1', category: getCategory(d), value: +d['year1'] || 0 },
        { year: 'year2', category: getCategory(d), value: +d['year2'] || 0 },
        { year: 'year3', category: getCategory(d), value: +d['year3'] || 0 },
    ]);

    const pieData = allData.filter(d => getChartNumber(d) === 3).map(d => ({
        Percentage: +d.percentage ?? +d.Percentage ?? 0,
        Category: getCategory(d)
    }));

    const stats = {
        statsByCat,
        totalRecords: {
            totalYear1: d3.sum(Object.values(statsByCat), d => d.totalYear1),
            totalYear2: d3.sum(Object.values(statsByCat), d => d.totalYear2),
            totalYear3: d3.sum(Object.values(statsByCat), d => d.totalYear3),
        }
    };

    const categoryNames = {};
    allData.forEach(d => {
        const cat = getCategory(d);
        if (cat && !categoryNames[cat]) categoryNames[cat] = cat;
    });

    return { statsByCat, secondChartData, pieData, stats, firstChartCategories, secondChartCategories, categoryNames };
}

export { loadData };
