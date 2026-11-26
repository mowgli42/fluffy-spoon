import { hydrateFromSeed, isHydrated } from './db'
import type { Seed } from './types'

export async function loadSeedJson(): Promise<Seed> {
  const res = await fetch('/data/seed.json')
  if (!res.ok) {
    throw new Error(`Failed to load seed.json (${res.status})`)
  }
  return (await res.json()) as Seed
}

/** Hydrate IndexedDB from the baked seed when empty or forced. */
export async function ensureLocalData(force = false): Promise<Seed> {
  const seed = await loadSeedJson()
  if (force || !(await isHydrated())) {
    await hydrateFromSeed(seed)
  }
  return seed
}

export function currentIsoWeek(d = new Date()): { year: number; week: number } {
  // Copy Date so we do not mutate caller
  const date = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()))
  const dayNum = date.getUTCDay() || 7
  date.setUTCDate(date.getUTCDate() + 4 - dayNum)
  const yearStart = new Date(Date.UTC(date.getUTCFullYear(), 0, 1))
  const week = Math.ceil(((date.getTime() - yearStart.getTime()) / 86400000 + 1) / 7)
  return { year: date.getUTCFullYear(), week }
}
