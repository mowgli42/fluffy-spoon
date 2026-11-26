export type Recipe = {
  id: string
  title: string
  summary: string
  tags: string[]
  metadata: Record<string, string>
  source: { name: string; url: string }
  ingredients: { text: string; quantity: string; unit: string }[]
  steps: { number: number; text: string }[]
  image: string | null
}

export type BbqPrep = {
  day: string
  recipeId: string
  recipeTitle: string
  tasks: string[]
}

export type WeekDay = {
  day: string
  date: string
  theme: string
  recipeId: string | null
  recipeTitle: string
  notes: string
}

export type WeekPlan = {
  week: number
  year: number
  label: string
  startDate: string
  days: WeekDay[]
  bbqPrep: BbqPrep[]
}

export type Seed = {
  version: number
  generatedForYear: number
  appName: string
  recipes: Recipe[]
  weeks: WeekPlan[]
}

export type PendingMutation = {
  id: string
  type: 'mark-cooked'
  recipeId: string
  week: number
  year: number
  day: string
  createdAt: string
  status: 'pending' | 'synced' | 'failed'
}
