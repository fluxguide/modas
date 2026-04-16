import { ref } from 'vue'
import { translations } from '@src/translations.js'

const currentLocale = ref('de')

function interpolate(template, params = {}) {
  return template.replace(/\{(\w+)\}/g, (_, key) => params[key] ?? `{${key}}`)
}

export function useTranslations() {
  function getTranslation(key, params = {}) {
    const entry = translations[key]

    if (!entry) {
      return key
    }

    const template = entry[currentLocale.value] ?? entry.de ?? key

    return interpolate(template, params)
  }

  function setLocale(locale) {
    currentLocale.value = locale
  }

  return {
    currentLocale,
    getTranslation,
    setLocale,
  }
}
