import { describe, expect, it } from 'vitest'
import { cleanText, isProductionVariant, slugFromFilename, titleFromFilename } from './importLib'

describe('importLib', () => {
  it('makes slug and title from the filename', () => {
    expect(slugFromFilename('episode-09-caribbean-jerk.md')).toBe('episode-09-caribbean-jerk')
    expect(slugFromFilename('Black Pepper (Kerala).txt')).toBe('black-pepper-kerala')
    expect(titleFromFilename('episode-09-caribbean-jerk.md')).toBe('Episode 09 Caribbean Jerk')
  })
  it('flags production variants', () => {
    expect(isProductionVariant('episode-01-filming-script.md')).toBe(true)
    expect(isProductionVariant('episode-01-read-aloud.md')).toBe(true)
    expect(isProductionVariant('episode-01-west-africa-yaji.md')).toBe(false)
  })
  it('only strips BOM and normalises newlines', () => {
    expect(cleanText('﻿a\r\nb\rc')).toBe('a\nb\nc')
  })
})
