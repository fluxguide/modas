const TRANSPORT_ALIASES = {
    Fahrrad: 'bike',
    Kfz: 'car',
    Auto: 'car',
    ÖPNV: 'bus',
    Bus: 'bus',
    'zu Fuß': 'walk',
    Fuß: 'walk',
}

export function loadData(rawData) {
    const categoryOrder = []
    const measurementOrderByCategory = {}
    const lookup = {}

    for (const row of rawData) {
        const district = Number(row['district number'])
        const districtName = (row['district name'] ?? '').trim()
        const rawTransport = (row['transport type'] ?? '').trim()
        const transport = TRANSPORT_ALIASES[rawTransport] ?? rawTransport.toLowerCase()
        const category = (row['category name'] ?? '').trim()
        const measurement = (row['category measurement'] ?? '').trim()
        const value = Number(row['measurement value']) || 0

        if (!category || !measurement || Number.isNaN(district)) continue

        if (!(category in lookup)) {
            categoryOrder.push(category)
            measurementOrderByCategory[category] = []
            lookup[category] = {}
        }

        lookup[category][transport] ??= {}
        lookup[category][transport][district] ??= {}
        lookup[category][transport][district][measurement] = value

        const order = measurementOrderByCategory[category]
        if (!order.includes(measurement)) order.push(measurement)
    }

    return { categoryOrder, measurementOrderByCategory, lookup }
}

export function getCategoryMetrics(parsed, categoryIndex, transport, districtNum) {
    const category = parsed.categoryOrder[categoryIndex]
    if (!category) return {}

    const labels = parsed.measurementOrderByCategory[category] ?? []
    const raw = parsed.lookup[category]?.[transport]?.[districtNum] ?? {}

    const slots = {}
    labels.forEach((label, i) => {
        slots[`slot_${i}`] = raw[label] ?? 0
    })
    return slots
}