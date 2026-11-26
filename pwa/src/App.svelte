<script lang="ts">
  import { onMount } from 'svelte'
  import {
    enqueueMutation,
    flushMutationQueue,
    getRecipe,
    getWeek,
    listPendingMutations,
    listRecipes,
  } from './lib/db'
  import { currentIsoWeek, ensureLocalData } from './lib/seed'
  import type { PendingMutation, Recipe, WeekPlan } from './lib/types'

  type View = 'recipes' | 'recipe' | 'week' | 'bbq'

  let ready = $state(false)
  let error = $state('')
  let online = $state(typeof navigator !== 'undefined' ? navigator.onLine : true)
  let view = $state<View>('recipes')
  let recipes = $state<Recipe[]>([])
  let query = $state('')
  let selected = $state<Recipe | null>(null)
  let weekPlan = $state<WeekPlan | null>(null)
  let pending = $state<PendingMutation[]>([])
  let syncNote = $state('')
  let year = $state(2026)
  let week = $state(1)

  const filtered = $derived(
    recipes.filter((r) => {
      const q = query.trim().toLowerCase()
      if (!q) return true
      return (
        r.title.toLowerCase().includes(q) ||
        r.summary.toLowerCase().includes(q) ||
        r.tags.some((t) => t.toLowerCase().includes(q))
      )
    }),
  )

  async function refreshPending() {
    pending = await listPendingMutations()
  }

  async function loadWeek(y: number, w: number) {
    year = y
    week = w
    weekPlan = (await getWeek(y, w)) ?? null
  }

  async function openRecipe(id: string) {
    selected = (await getRecipe(id)) ?? null
    view = 'recipe'
  }

  async function markCooked(day: string) {
    if (!weekPlan || !selected && !weekPlan) return
    const dayEntry = weekPlan.days.find((d) => d.day === day)
    const recipeId = dayEntry?.recipeId
    if (!recipeId) return
    await enqueueMutation({
      type: 'mark-cooked',
      recipeId,
      week: weekPlan.week,
      year: weekPlan.year,
      day,
    })
    await refreshPending()
    syncNote = online
      ? 'Queued locally — will demo-sync while online.'
      : 'Queued offline — will sync when connectivity returns (demo).'
    if (online) {
      const n = await flushMutationQueue()
      if (n) syncNote = `Demo-synced ${n} change(s) (no remote backend).`
      await refreshPending()
    }
  }

  async function tryFlush() {
    const n = await flushMutationQueue()
    syncNote = n
      ? `Demo-synced ${n} change(s) (no remote backend).`
      : online
        ? 'Nothing pending to sync.'
        : 'Still offline — queue kept.'
    await refreshPending()
  }

  onMount(() => {
    const onOnline = () => {
      online = true
      void tryFlush()
    }
    const onOffline = () => {
      online = false
    }
    window.addEventListener('online', onOnline)
    window.addEventListener('offline', onOffline)

    ;(async () => {
      try {
        await ensureLocalData()
        recipes = await listRecipes()
        const now = currentIsoWeek()
        // Prefer seed year 2026 for demo consistency when current year has no seed.
        const seedYear = 2026
        const w = Math.min(Math.max(now.week, 1), 52)
        await loadWeek(seedYear, w)
        await refreshPending()
        ready = true
      } catch (e) {
        error = e instanceof Error ? e.message : String(e)
      }
    })()

    return () => {
      window.removeEventListener('online', onOnline)
      window.removeEventListener('offline', onOffline)
    }
  })
</script>

<svelte:head>
  <title>Fluffy Spoon</title>
  <meta name="theme-color" content="#c45c2a" />
  <link rel="apple-touch-icon" href="/icons/apple-touch-icon.png" />
</svelte:head>

<main class="shell">
  <header>
    <h1 class="brand">Fluffy Spoon</h1>
    <p class="tagline">
      Crockpot weekdays, weekend BBQ batch cooks, and meal prep — installable and offline-ready.
    </p>
  </header>

  <div class="status-bar" data-testid="status-bar">
    <span class="pill {online ? 'online' : 'offline'}" data-testid="online-status">
      {online ? 'Online' : 'Offline'}
    </span>
    <span class="pill" data-testid="pending-count">Queue: {pending.length}</span>
    {#if syncNote}
      <span class="muted">{syncNote}</span>
    {/if}
  </div>

  <nav class="nav" aria-label="Primary">
    <button class:active={view === 'recipes'} onclick={() => (view = 'recipes')}>Recipes</button>
    <button class:active={view === 'week'} onclick={() => (view = 'week')}>This week</button>
    <button class:active={view === 'bbq'} onclick={() => (view = 'bbq')}>BBQ prep</button>
  </nav>

  {#if error}
    <p class="error" role="alert">{error}</p>
  {:else if !ready}
    <p class="muted">Loading local recipe box…</p>
  {:else if view === 'recipes'}
    <section class="panel" data-testid="recipes-panel">
      <h2>Recipes</h2>
      <input
        class="search"
        type="search"
        placeholder="Search title, summary, or tag"
        bind:value={query}
        data-testid="recipe-search"
      />
      <ul class="list">
        {#each filtered as recipe (recipe.id)}
          <li>
            <button class="row" onclick={() => openRecipe(recipe.id)} data-testid="recipe-row">
              <div class="row-title">{recipe.title}</div>
              <div class="row-meta">{recipe.summary.slice(0, 140)}…</div>
              <div class="tags">
                {#each recipe.tags.slice(0, 5) as tag}
                  <span class="tag">{tag}</span>
                {/each}
              </div>
            </button>
          </li>
        {/each}
      </ul>
    </section>
  {:else if view === 'recipe' && selected}
    <section class="panel" data-testid="recipe-detail">
      <div class="actions">
        <button class="btn ghost" onclick={() => (view = 'recipes')}>← Recipes</button>
      </div>
      <h2>{selected.title}</h2>
      <p class="muted">{selected.summary}</p>
      <div class="tags">
        {#each selected.tags as tag}
          <span class="tag">{tag}</span>
        {/each}
      </div>
      {#if selected.metadata.difficulty || selected.metadata.totalTime}
        <p class="row-meta">
          {selected.metadata.difficulty}
          {#if selected.metadata.totalTime}
            · {selected.metadata.totalTime}
          {/if}
          {#if selected.metadata.servings}
            · serves {selected.metadata.servings}
          {/if}
        </p>
      {/if}

      <h3>Ingredients</h3>
      <ul class="ingredients" data-testid="ingredients">
        {#each selected.ingredients as ing}
          <li>
            {#if ing.quantity}{ing.quantity} {/if}{#if ing.unit}{ing.unit} {/if}{ing.text}
          </li>
        {/each}
      </ul>

      <h3>Instructions</h3>
      <ol class="steps" data-testid="instructions">
        {#each selected.steps as step}
          <li>{step.text}</li>
        {/each}
      </ol>

      {#if selected.image}
        <img src={selected.image} alt={selected.title} />
      {:else}
        <p class="muted" data-testid="no-image">
          No photo in seed — text and steps are cached for offline use.
        </p>
      {/if}
    </section>
  {:else if view === 'week'}
    <section class="panel" data-testid="week-panel">
      <h2>{weekPlan?.label ?? `Week ${week}`}</h2>
      <div class="actions">
        <button
          class="btn ghost"
          disabled={week <= 1}
          onclick={() => loadWeek(year, week - 1)}
        >
          Prev
        </button>
        <button
          class="btn ghost"
          disabled={week >= 52}
          onclick={() => loadWeek(year, week + 1)}
        >
          Next
        </button>
        <button class="btn ghost" onclick={() => tryFlush()}>Sync queue</button>
      </div>
      {#if weekPlan}
        <ul class="list">
          {#each weekPlan.days as day}
            <li class="day-row">
              <div class="row-title">{day.day} · {day.theme}</div>
              <div class="row-meta">
                {#if day.recipeId}
                  <button class="btn ghost" onclick={() => openRecipe(day.recipeId!)}>
                    {day.recipeTitle}
                  </button>
                {:else}
                  {day.recipeTitle}
                {/if}
              </div>
              {#if day.notes}
                <p class="muted">{day.notes}</p>
              {/if}
              <div class="actions">
                <button
                  class="btn"
                  data-testid="mark-cooked"
                  onclick={() => markCooked(day.day)}
                  disabled={!day.recipeId}
                >
                  Mark cooked
                </button>
              </div>
            </li>
          {/each}
        </ul>
      {:else}
        <p class="muted">No week plan in local store.</p>
      {/if}
    </section>
  {:else if view === 'bbq'}
    <section class="panel" data-testid="bbq-panel">
      <h2>BBQ / batch prep · {weekPlan?.label}</h2>
      {#if weekPlan?.bbqPrep?.length}
        <ul class="prep-list">
          {#each weekPlan.bbqPrep as prep}
            <li>
              <div class="row-title">{prep.day}: {prep.recipeTitle}</div>
              <ul>
                {#each prep.tasks as task}
                  <li>{task}</li>
                {/each}
              </ul>
              <div class="actions">
                <button class="btn ghost" onclick={() => openRecipe(prep.recipeId)}>
                  Open recipe
                </button>
              </div>
            </li>
          {/each}
        </ul>
      {:else}
        <p class="muted">No BBQ prep items for this week.</p>
      {/if}
    </section>
  {/if}

  <p class="muted" style="margin-top: 2rem; font-size: 0.85rem">
    Prototype PWA · data from build-time seed ·
    <a href="/classic/recipe-box.html">Classic static recipe box</a>
  </p>
</main>
