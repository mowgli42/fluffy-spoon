import { openDB, type DBSchema, type IDBPDatabase } from 'idb'
import type { PendingMutation, Recipe, Seed, WeekPlan } from './types'

type WeekRow = WeekPlan & { id: string }

interface FluffyDB extends DBSchema {
  meta: {
    key: string
    value: { key: string; value: unknown }
  }
  recipes: {
    key: string
    value: Recipe
  }
  weeks: {
    key: string
    value: WeekRow
    indexes: { 'by-year-week': [number, number] }
  }
  mutations: {
    key: string
    value: PendingMutation
    indexes: { 'by-status': string }
  }
}

const DB_NAME = 'fluffy-spoon'
const DB_VERSION = 1

let dbPromise: Promise<IDBPDatabase<FluffyDB>> | null = null

function weekId(year: number, week: number) {
  return `${year}-W${String(week).padStart(2, '0')}`
}

export function getDb() {
  if (!dbPromise) {
    dbPromise = openDB<FluffyDB>(DB_NAME, DB_VERSION, {
      upgrade(db) {
        if (!db.objectStoreNames.contains('meta')) {
          db.createObjectStore('meta', { keyPath: 'key' })
        }
        if (!db.objectStoreNames.contains('recipes')) {
          db.createObjectStore('recipes', { keyPath: 'id' })
        }
        if (!db.objectStoreNames.contains('weeks')) {
          const weeks = db.createObjectStore('weeks', { keyPath: 'id' })
          weeks.createIndex('by-year-week', ['year', 'week'])
        }
        if (!db.objectStoreNames.contains('mutations')) {
          const mutations = db.createObjectStore('mutations', { keyPath: 'id' })
          mutations.createIndex('by-status', 'status')
        }
      },
    })
  }
  return dbPromise
}

export async function hydrateFromSeed(seed: Seed): Promise<void> {
  const db = await getDb()
  const tx = db.transaction(['meta', 'recipes', 'weeks'], 'readwrite')
  await tx.objectStore('meta').put({ key: 'seedVersion', value: seed.version })
  await tx.objectStore('meta').put({
    key: 'generatedForYear',
    value: seed.generatedForYear,
  })
  await tx.objectStore('meta').put({ key: 'hydratedAt', value: new Date().toISOString() })

  for (const recipe of seed.recipes) {
    await tx.objectStore('recipes').put(recipe)
  }
  for (const week of seed.weeks) {
    await tx.objectStore('weeks').put({ ...week, id: weekId(week.year, week.week) })
  }
  await tx.done
}

export async function listRecipes(): Promise<Recipe[]> {
  const db = await getDb()
  const all = await db.getAll('recipes')
  return all.sort((a, b) => a.title.localeCompare(b.title))
}

export async function getRecipe(id: string): Promise<Recipe | undefined> {
  const db = await getDb()
  return db.get('recipes', id)
}

export async function getWeek(year: number, week: number): Promise<WeekPlan | undefined> {
  const db = await getDb()
  const row = await db.get('weeks', weekId(year, week))
  if (!row) return undefined
  const { id: _id, ...weekPlan } = row
  void _id
  return weekPlan
}

export async function isHydrated(): Promise<boolean> {
  const db = await getDb()
  const meta = await db.get('meta', 'hydratedAt')
  return Boolean(meta)
}

export async function enqueueMutation(
  mutation: Omit<PendingMutation, 'id' | 'createdAt' | 'status'>,
): Promise<PendingMutation> {
  const db = await getDb()
  const full: PendingMutation = {
    ...mutation,
    id: crypto.randomUUID(),
    createdAt: new Date().toISOString(),
    status: 'pending',
  }
  await db.put('mutations', full)
  return full
}

export async function listPendingMutations(): Promise<PendingMutation[]> {
  const db = await getDb()
  return db.getAllFromIndex('mutations', 'by-status', 'pending')
}

/** Demo sync: no backend — mark pending as synced when online. */
export async function flushMutationQueue(): Promise<number> {
  if (!navigator.onLine) return 0
  const db = await getDb()
  const pending = await db.getAllFromIndex('mutations', 'by-status', 'pending')
  const tx = db.transaction('mutations', 'readwrite')
  for (const m of pending) {
    await tx.store.put({ ...m, status: 'synced' })
  }
  await tx.done
  return pending.length
}
