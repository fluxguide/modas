export const sectionOne = {
  sectionId: 'section-one',
  bubble: [
    {
      id: 'firstMetric',
      segments: [
        { type: 'metric', key: 'slot_0' },
        { type: 'highlight', key: 'slot_0', tone: 'blue' },
      ],
    },
    {
      id: 'secondMetric',
      segments: [
        { type: 'metric', key: 'slot_1' },
        { type: 'highlight', key: 'slot_1', tone: 'mint' },
      ],
    },
    {
      id: 'thirdMetric',
      segments: [
        { type: 'metric', key: 'slot_2' },
        { type: 'highlight', key: 'slot_2', tone: 'yellow' },
      ],
    },
    {
      id: 'fourthMetric',
      segments: [
        { type: 'metric', key: 'slot_3' },
        { type: 'highlight', key: 'slot_3', tone: 'orange-soft' },
      ],
    },
    {
      id: 'fifthMetric',
      segments: [
        { type: 'metric', key: 'slot_4' },
        { type: 'highlight', key: 'slot_4', tone: 'orange-light' },
      ],
    },
    {
      id: 'sixthMetric',
      segments: [
        { type: 'metric', key: 'slot_5' },
        { type: 'highlight', key: 'slot_5', tone: 'taupe-light' },
      ],
    },
  ],
}

export const sectionTwo = {
  sectionId: 'section-two',
  bubble: [
    {
      id: 'positive',
      segments: [
        { type: 'metric', key: 'slot_0' },
        { type: 'highlight', key: 'slot_0', tone: 'blue' },
      ],
    },
    {
      id: 'positive-less',
      segments: [
        { type: 'metric', key: 'slot_1' },
        { type: 'highlight', key: 'slot_1', tone: 'mint' },
      ],
    },
    {
      id: 'neutral',
      segments: [
        { type: 'metric', key: 'slot_2' },
        { type: 'highlight', key: 'slot_2', tone: 'yellow' },
      ],
    },
    {
      id: 'negative-less',
      segments: [
        { type: 'metric', key: 'slot_3' },
        { type: 'highlight', key: 'slot_3', tone: 'orange-soft' },
      ],
    },
    {
      id: 'negative',
      segments: [
        { type: 'metric', key: 'slot_4' },
        { type: 'highlight', key: 'slot_4', tone: 'orange-light' },
      ],
    },
    {
      id: 'no-answer',
      segments: [
        { type: 'metric', key: 'slot_5' },
        { type: 'highlight', key: 'slot_5', tone: 'taupe-light' },
      ],
    },
  ],
}

export const safetyStory = {
  sectionId: 'safety',
  titleKey: 'safety_intro_question',
  bubble: [],
}

export const safetyDetailsStory = {
  bubble: [
    {
      id: 'firstMetric',
      segments: [
        { type: 'metric', key: 'slot_0' },
        { type: 'highlight', key: 'slot_0', tone: 'blue' },
      ],
    },
    {
      id: 'secondMetric',
      segments: [
        { type: 'metric', key: 'slot_1' },
        { type: 'highlight', key: 'slot_1', tone: 'mint' },
      ],
    },
    {
      id: 'thirdMetric',
      segments: [
        { type: 'metric', key: 'slot_2' },
        { type: 'highlight', key: 'slot_2', tone: 'yellow' },
      ],
    },
    {
      id: 'fourthMetric',
      segments: [
        { type: 'metric', key: 'slot_3' },
        { type: 'highlight', key: 'slot_3', tone: 'orange-soft' },
      ],
    },
    {
      id: 'fifthMetric',
      segments: [
        { type: 'metric', key: 'slot_4' },
        { type: 'highlight', key: 'slot_4', tone: 'orange-light' },
      ],
    },
    {
      id: 'sixthMetric',
      segments: [
        { type: 'metric', key: 'slot_5' },
        { type: 'highlight', key: 'slot_5', tone: 'taupe-light' },
      ],
    },
  ],
  treeItems: [
    { id: 'no-answer', metricKey: 'slot_5', imageKey: 'tree1', tone: 'taupe-light' },
    { id: 'very-safe', metricKey: 'slot_0', imageKey: 'tree4', tone: 'blue' },
    { id: 'rather-safe', metricKey: 'slot_1', imageKey: 'tree5', tone: 'mint' },
    { id: 'rather-unsafe', metricKey: 'slot_3', imageKey: 'tree5', tone: 'orange-soft' },
    { id: 'very-unsafe', metricKey: 'slot_4', imageKey: 'tree2', tone: 'orange-light' },
    { id: 'neutral', metricKey: 'slot_2', imageKey: 'tree3', tone: 'yellow' },
  ],
}

export const othersQuestionStory = {
  sectionId: 'others-question',
  titleKey: 'others_question_intro',
  bubble: [],
}

export const othersAcceptanceInfo = {
  titleKey: null,
  bubble: [
    {
      id: 'firstMetric',
      segments: [
        { type: 'metric', key: 'slot_0' },
        { type: 'highlight', key: 'slot_0', tone: 'blue' },
      ],
    },
    {
      id: 'secondMetric',
      segments: [
        { type: 'metric', key: 'slot_1' },
        { type: 'highlight', key: 'slot_1', tone: 'mint' },
      ],
    },
    {
      id: 'thirdMetric',
      segments: [
        { type: 'metric', key: 'slot_2' },
        { type: 'highlight', key: 'slot_2', tone: 'yellow' },
      ],
    },
    {
      id: 'fourthMetric',
      segments: [
        { type: 'metric', key: 'slot_3' },
        { type: 'highlight', key: 'slot_3', tone: 'orange-soft' },
      ],
    },
    {
      id: 'fifthMetric',
      segments: [
        { type: 'metric', key: 'slot_4' },
        { type: 'highlight', key: 'slot_4', tone: 'orange-light' },
      ],
    },
    {
      id: 'sixthMetric',
      segments: [
        { type: 'metric', key: 'slot_5' },
        { type: 'highlight', key: 'slot_5', tone: 'taupe-light' },
      ],
    },
  ],
}

export const conclusionSummaryInfo = {
  blocks: [
    {
      id: 'paragraph-1',
      type: 'paragraph',
      segments: [
        { type: 'highlight', key: 'conclusion_summary_paragraph_1_highlight_1' },
        { type: 'text', key: 'conclusion_summary_paragraph_1_text_1' },
        { type: 'highlight', key: 'conclusion_summary_paragraph_1_highlight_2' },
        { type: 'text', key: 'conclusion_summary_paragraph_1_text_2' },
      ],
    },
    {
      id: 'paragraph-2',
      type: 'paragraph',
      segments: [
        { type: 'highlight', key: 'conclusion_summary_paragraph_2_highlight_1' },
        { type: 'text', key: 'conclusion_summary_paragraph_2_text_1' },
      ],
    },
    {
      id: 'paragraph-3',
      type: 'paragraph',
      segments: [
        { type: 'highlight', key: 'conclusion_summary_paragraph_3_highlight_1' },
        { type: 'text', key: 'conclusion_summary_paragraph_3_text_1' },
        { type: 'highlight', key: 'conclusion_summary_paragraph_3_highlight_2' },
        { type: 'text', key: 'conclusion_summary_paragraph_3_text_2' },
      ],
    },
  ],
}

export const conclusionStory = {
  sectionId: 'conclusion',
  titleKey: 'conclusion_intro_question',
  bubble: [],
}

export const endStory = {
  sectionId: 'end',
  titleKey: 'end_closing_message',
  bubble: [],
}

export const conclusionTransportUsage = [
  { id: 'tram', imageKey: 'tram', labelKey: 'transportation_bus', value: 26 },
  { id: 'car', assetKey: 'end-car', labelKey: 'transportation_car', value: 21 },
  { id: 'bike', assetKey: 'rider', labelKey: 'transportation_bike', value: 22 },
  { id: 'walkers', imageKey: 'people-walking', labelKey: 'transportation_walk', value: 48 },
]

export const storyScenes = {
  [sectionOne.sectionId]: sectionOne,
  [sectionTwo.sectionId]: sectionTwo,
  [safetyStory.sectionId]: safetyStory,
  [othersQuestionStory.sectionId]: othersQuestionStory,
  [conclusionStory.sectionId]: conclusionStory,
  [endStory.sectionId]: endStory,
}

export const orderedStoryScenes = [
  sectionOne,
  sectionTwo,
  safetyDetailsStory,
  othersAcceptanceInfo,
  conclusionStory,
  endStory,
];