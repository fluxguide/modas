export const accessibilityHappinessStory = {
  sectionId: 'accessibility-happiness',
  categoryIndex: 1,
  titleKey: 'accessibility_happiness_question',
  aggregates: {
    negative_pair: ['slot_3', 'slot_4'],
  },
  bubble: [
    {
      id: 'positive',
      segments: [
        { type: 'metric', key: 'slot_0' },
        { type: 'text', key: 'accessibility_happiness_bullet_1_text_1' },
        { type: 'highlight', key: 'accessibility_happiness_bullet_1_highlight_1', tone: 'blue' },
        { type: 'text', key: 'accessibility_happiness_bullet_1_text_2' },
        { type: 'metric', key: 'slot_1' },
        { type: 'text', key: 'accessibility_happiness_bullet_1_text_3' },
        { type: 'highlight', key: 'accessibility_happiness_bullet_1_highlight_2', tone: 'mint' },
      ],
    },
    {
      id: 'neutral',
      segments: [
        { type: 'metric', key: 'slot_2' },
        { type: 'text', key: 'accessibility_happiness_bullet_2_text_1' },
        { type: 'highlight', key: 'accessibility_happiness_bullet_2_highlight_1', tone: 'yellow' },
      ],
    },
    {
      id: 'negative',
      segments: [
        { type: 'text', key: 'accessibility_happiness_bullet_3_text_1' },
        { type: 'metric', key: 'negative_pair' },
        { type: 'text', key: 'accessibility_happiness_bullet_3_text_2' },
        { type: 'highlight', key: 'accessibility_happiness_bullet_3_highlight_1', tone: 'orange-soft' },
        { type: 'text', key: 'accessibility_happiness_bullet_3_text_3' },
        { type: 'highlight', key: 'accessibility_happiness_bullet_3_highlight_2', tone: 'orange-light' },
        { type: 'text', key: 'accessibility_happiness_bullet_3_text_4' },
      ],
    },
    {
      id: 'no-answer',
      segments: [
        { type: 'metric', key: 'slot_5' },
        { type: 'text', key: 'accessibility_happiness_bullet_4_text_1' },
        { type: 'highlight', key: 'accessibility_happiness_bullet_4_highlight_1', tone: 'taupe-light' },
        { type: 'text', key: 'accessibility_happiness_bullet_4_text_2' },
      ],
    },
  ],
}

export const accessibilityRoadStory = {
  sectionId: 'accessibility-road',
  categoryIndex: 2,
  titleKey: 'accessibility_road_question',
  aggregates: {
    negative_pair: ['slot_3', 'slot_4'],
  },
  bubble: [
    {
      id: 'positive',
      segments: [
        { type: 'metric', key: 'slot_0' },
        { type: 'text', key: 'accessibility_road_bullet_1_text_1' },
        { type: 'highlight', key: 'accessibility_road_bullet_1_highlight_1', tone: 'blue' },
        { type: 'text', key: 'accessibility_road_bullet_1_text_2' },
        { type: 'metric', key: 'slot_1' },
        { type: 'text', key: 'accessibility_road_bullet_1_text_3' },
        { type: 'highlight', key: 'accessibility_road_bullet_1_highlight_2', tone: 'mint' },
      ],
    },
    {
      id: 'neutral',
      segments: [
        { type: 'metric', key: 'slot_2' },
        { type: 'text', key: 'accessibility_road_bullet_2_text_1' },
        { type: 'highlight', key: 'accessibility_road_bullet_2_highlight_1', tone: 'yellow' },
      ],
    },
    {
      id: 'negative',
      segments: [
        { type: 'text', key: 'accessibility_road_bullet_3_text_1' },
        { type: 'metric', key: 'negative_pair' },
        { type: 'text', key: 'accessibility_road_bullet_3_text_2' },
        { type: 'highlight', key: 'accessibility_road_bullet_3_highlight_1', tone: 'orange-soft' },
        { type: 'text', key: 'accessibility_road_bullet_3_text_3' },
        { type: 'highlight', key: 'accessibility_road_bullet_3_highlight_2', tone: 'orange-light' },
        { type: 'text', key: 'accessibility_road_bullet_3_text_4' },
      ],
    },
    {
      id: 'no-answer',
      segments: [
        { type: 'metric', key: 'slot_5' },
        { type: 'text', key: 'accessibility_road_bullet_4_text_1' },
        { type: 'highlight', key: 'accessibility_road_bullet_4_highlight_1', tone: 'taupe-light' },
        { type: 'text', key: 'accessibility_road_bullet_4_text_2' },
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
  categoryIndex: 3,
  titleKey: 'safety_detail_question',
  aggregates: {
    negative_pair: ['slot_3', 'slot_4'],
  },
  bubble: [
    {
      id: 'positive',
      segments: [
        { type: 'text', key: 'safety_detail_bullet_1_text_1' },
        { type: 'metric', key: 'slot_0' },
        { type: 'text', key: 'safety_detail_bullet_1_text_2' },
        { type: 'highlight', key: 'safety_detail_bullet_1_highlight_1', tone: 'blue' },
        { type: 'text', key: 'safety_detail_bullet_1_text_3' },
        { type: 'metric', key: 'slot_1' },
        { type: 'text', key: 'safety_detail_bullet_1_text_4' },
        { type: 'highlight', key: 'safety_detail_bullet_1_highlight_2', tone: 'mint' },
      ],
    },
    {
      id: 'neutral',
      segments: [
        { type: 'metric', key: 'slot_2' },
        { type: 'text', key: 'safety_detail_bullet_2_text_1' },
        { type: 'highlight', key: 'safety_detail_bullet_2_highlight_1', tone: 'yellow' },
      ],
    },
    {
      id: 'negative',
      segments: [
        { type: 'text', key: 'safety_detail_bullet_3_text_1' },
        { type: 'metric', key: 'negative_pair' },
        { type: 'text', key: 'safety_detail_bullet_3_text_2' },
        { type: 'metric', key: 'slot_3' },
        { type: 'text', key: 'safety_detail_bullet_3_text_3' },
        { type: 'highlight', key: 'safety_detail_bullet_3_highlight_1', tone: 'orange-soft' },
        { type: 'text', key: 'safety_detail_bullet_3_text_4' },
        { type: 'metric', key: 'slot_4' },
        { type: 'text', key: 'safety_detail_bullet_3_text_5' },
        { type: 'highlight', key: 'safety_detail_bullet_3_highlight_2', tone: 'orange-light' },
      ],
    },
    {
      id: 'no-answer',
      segments: [
        { type: 'metric', key: 'slot_5' },
        { type: 'text', key: 'safety_detail_bullet_4_text_1' },
        { type: 'highlight', key: 'safety_detail_bullet_4_highlight_1', tone: 'taupe-light' },
        { type: 'text', key: 'safety_detail_bullet_4_text_2' },
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

export const othersAnswersStory = {
  sectionId: 'others-answers',
  titleKey: 'others_answers_reflection',
  bubble: [],
}

export const othersAcceptanceInfo = {
  categoryIndex: 4,
  titleKey: null,
  aggregates: {
    negative_pair: ['slot_3'],
  },
  bubble: [
    {
      id: 'positive',
      segments: [
        { type: 'text', key: 'others_acceptance_bullet_1_text_1' },
        { type: 'metric', key: 'slot_0' },
        { type: 'text', key: 'others_acceptance_bullet_1_text_2' },
        { type: 'highlight', key: 'others_acceptance_bullet_1_highlight_1', tone: 'blue' },
        { type: 'text', key: 'others_acceptance_bullet_1_text_3' },
        { type: 'metric', key: 'slot_1' },
        { type: 'text', key: 'others_acceptance_bullet_1_text_4' },
        { type: 'highlight', key: 'others_acceptance_bullet_1_highlight_2', tone: 'mint' },
      ],
    },
    {
      id: 'mixed',
      segments: [
        { type: 'metric', key: 'slot_2' },
        { type: 'text', key: 'others_acceptance_bullet_2_text_1' },
        { type: 'highlight', key: 'others_acceptance_bullet_2_highlight_1', tone: 'yellow' },
        { type: 'text', key: 'others_acceptance_bullet_2_text_2' },
        { type: 'metric', key: 'negative_pair' },
        { type: 'text', key: 'others_acceptance_bullet_2_text_3' },
        { type: 'highlight', key: 'others_acceptance_bullet_2_highlight_2', tone: 'orange-soft' },
        { type: 'text', key: 'others_acceptance_bullet_2_text_4' },
      ],
    },
    {
      id: 'no-answer',
      segments: [
        { type: 'metric', key: 'slot_4' },
        { type: 'text', key: 'others_acceptance_bullet_3_text_1' },
        { type: 'highlight', key: 'others_acceptance_bullet_3_highlight_1', tone: 'taupe-light' },
        { type: 'text', key: 'others_acceptance_bullet_3_text_2' },
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

export const conclusionTransportUsage = [
  { id: 'tram', imageKey: 'tram', labelKey: 'transportation_bus', value: 26 },
  { id: 'car', assetKey: 'end-car', labelKey: 'transportation_car', value: 21 },
  { id: 'bike', assetKey: 'rider', labelKey: 'transportation_bike', value: 22 },
  { id: 'walkers', imageKey: 'people-walking', labelKey: 'transportation_walk', value: 48 },
]

export const othersEbikesInfo = {
  categoryIndex: 5,
  blocks: [
    {
      id: 'intro',
      type: 'paragraph',
      segments: [
        { type: 'metric', key: 'total' },
        { type: 'text', key: 'others_ebike_intro_text_1' },
        { type: 'highlight', key: 'others_ebike_intro_highlight_1' },
        { type: 'text', key: 'others_ebike_intro_text_2' },
      ],
    },
    {
      id: 'one-ebike',
      type: 'bullet',
      segments: [
        { type: 'metric', key: 'slot_0' },
        { type: 'text', key: 'others_ebike_bullet_1_text_1' },
      ],
    },
    {
      id: 'more-ebikes',
      type: 'bullet',
      segments: [
        { type: 'metric', key: 'slot_1' },
        { type: 'text', key: 'others_ebike_bullet_2_text_1' },
      ],
    },
  ],
}

export const othersBikeSharingInfo = {
  categoryIndex: 6,
  aggregates: {
    negative_pair: ['slot_2', 'slot_3'],
  },
  blocks: [
    {
      id: 'intro',
      type: 'paragraph',
      segments: [
        { type: 'text', key: 'others_bikesharing_intro_text_1' },
        { type: 'highlight', key: 'others_bikesharing_intro_highlight_1' },
        { type: 'text', key: 'others_bikesharing_intro_text_2' },
      ],
    },
    {
      id: 'positive',
      type: 'bullet',
      segments: [
        { type: 'metric', key: 'slot_0' },
        { type: 'text', key: 'others_bikesharing_bullet_1_text_1' },
        { type: 'metric', key: 'slot_1' },
        { type: 'text', key: 'others_bikesharing_bullet_1_text_2' },
      ],
    },
    {
      id: 'negative',
      type: 'bullet',
      segments: [
        { type: 'text', key: 'others_bikesharing_bullet_2_text_1' },
        { type: 'metric', key: 'negative_pair' },
        { type: 'text', key: 'others_bikesharing_bullet_2_text_2' },
      ],
    },
    {
      id: 'no-opinion',
      type: 'bullet',
      segments: [
        { type: 'metric', key: 'slot_4' },
        { type: 'text', key: 'others_bikesharing_bullet_3_text_1' },
      ],
    },
  ],
}

export const storyScenes = {
  [accessibilityHappinessStory.sectionId]: accessibilityHappinessStory,
  [accessibilityRoadStory.sectionId]: accessibilityRoadStory,
  [safetyStory.sectionId]: safetyStory,
  [othersQuestionStory.sectionId]: othersQuestionStory,
  [othersAnswersStory.sectionId]: othersAnswersStory,
  [conclusionStory.sectionId]: conclusionStory,
  [endStory.sectionId]: endStory,
}