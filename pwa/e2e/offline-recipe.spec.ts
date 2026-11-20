import { expect, test } from '@playwright/test'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

const __dirname = path.dirname(fileURLToPath(import.meta.url))
const screenshotDir = path.resolve(__dirname, '../../docs/demo')

test.describe('Fluffy Spoon PWA offline viewing', () => {
  test('manifest is installable and recipes work offline', async ({ page, context }) => {
    await page.goto('/')
    await expect(page.getByRole('heading', { name: 'Fluffy Spoon' })).toBeVisible()
    await expect(page.getByTestId('recipes-panel')).toBeVisible({ timeout: 15_000 })

    const manifestRes = await page.request.get('/manifest.webmanifest')
    expect(manifestRes.ok()).toBeTruthy()
    const manifest = await manifestRes.json()
    expect(manifest.name).toBe('Fluffy Spoon')
    expect(manifest.display).toBe('standalone')
    expect(manifest.start_url).toBe('/')
    expect(manifest.theme_color).toBe('#c45c2a')

    // Wait for service worker registration (vite-plugin-pwa)
    await page.waitForFunction(async () => {
      const regs = await navigator.serviceWorker.getRegistrations()
      return regs.length > 0
    })

    // Open a recipe while online so detail path is exercised
    await page.getByTestId('recipe-row').first().click()
    await expect(page.getByTestId('recipe-detail')).toBeVisible()
    await expect(page.getByTestId('ingredients')).toBeVisible()
    await expect(page.getByTestId('instructions')).toBeVisible()

    await page.getByRole('button', { name: 'Recipes', exact: true }).click()
    await expect(page.getByTestId('recipes-panel')).toBeVisible()

    // Go offline and reload — shell + IndexedDB seed should still render
    await context.setOffline(true)
    await page.reload()
    await expect(page.getByRole('heading', { name: 'Fluffy Spoon' })).toBeVisible()
    await expect(page.getByTestId('online-status')).toHaveText('Offline')
    await expect(page.getByTestId('recipes-panel')).toBeVisible({ timeout: 15_000 })
    await expect(page.getByTestId('recipe-row').first()).toBeVisible()

    await page.getByTestId('recipe-row').first().click()
    await expect(page.getByTestId('recipe-detail')).toBeVisible()
    await expect(page.getByTestId('ingredients').locator('li').first()).toBeVisible()

    await page.getByRole('button', { name: 'This week', exact: true }).click()
    await expect(page.getByTestId('week-panel')).toBeVisible()
    await expect(page.getByTestId('week-panel')).toContainText('Week')

    await page.getByRole('button', { name: 'BBQ prep', exact: true }).click()
    await expect(page.getByTestId('bbq-panel')).toBeVisible()

    await page.screenshot({
      path: path.join(screenshotDir, 'offline-recipe-view.png'),
      fullPage: true,
    })
  })
})
