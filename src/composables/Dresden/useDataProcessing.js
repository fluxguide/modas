const TRANSPORT_ALIASES = {
    Fahrrad: 'bike',
    Kfz: 'car',
    Auto: 'car',
    ÖPNV: 'bus',
    OEPNV: 'bus',
    Bahn: 'bus',
    Bus: 'bus',
    'zu Fuß': 'walk',
    Fuß: 'walk',
}

export function loadData(rawData) {
    const categoryOrderByTransport = {}
    const measurementOrderByCategory = {}
    const lookup = {}

    for (const row of rawData) {
        const district = Number(row['district number'])
        const rawTransport = (row['transport type'] ?? '').trim()
        const transport = TRANSPORT_ALIASES[rawTransport] ?? rawTransport
        const category = (row['category name'] ?? '').trim()
        const measurement = (row['category measurement'] ?? '').trim()
        const value = Number(row['measurement value']) || 0

        if (!category || !measurement || Number.isNaN(district)) continue

        if (!(category in lookup)) {
            measurementOrderByCategory[category] = []
            lookup[category] = {}
        }

        categoryOrderByTransport[transport] ??= []
        if (!categoryOrderByTransport[transport].includes(category)) {
            categoryOrderByTransport[transport].push(category)
        }

        lookup[category][transport] ??= {}
        lookup[category][transport][district] ??= {}
        lookup[category][transport][district][measurement] = value

        const order = measurementOrderByCategory[category]
        if (!order.includes(measurement)) order.push(measurement)
    }

    return { categoryOrderByTransport, measurementOrderByCategory, lookup }
}

export function getCategoryMetrics(parsed, categoryIndex, transport, districtNum) {
    const transportCategories = parsed.categoryOrderByTransport[transport] ?? []
    const category = transportCategories[categoryIndex]
    if (!category) return { slot_0: 0, slot_1: 0, slot_2: 0, slot_3: 0, slot_4: 0, slot_5: 0 }

    const labels = parsed.measurementOrderByCategory[category] ?? []
    const raw = parsed.lookup[category]?.[transport]?.[districtNum] ?? {}

    const slots = { slot_0: 0, slot_1: 0, slot_2: 0, slot_3: 0, slot_4: 0, slot_5: 0 }
    labels.forEach((label, i) => {
        slots[`slot_${i}`] = raw[label] ?? 0
    })
    return slots
}