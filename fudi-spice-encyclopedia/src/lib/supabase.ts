import { createClient } from '@supabase/supabase-js'

const url = import.meta.env.VITE_SUPABASE_URL as string | undefined
const anonKey = import.meta.env.VITE_SUPABASE_ANON_KEY as string | undefined

/** False until .env.local has real Supabase values. The app then runs on placeholder demo data. */
export const isConfigured = Boolean(url && anonKey && !url.includes('YOUR-PROJECT'))

export const supabase = isConfigured ? createClient(url!, anonKey!) : null

export const SITE_URL = (import.meta.env.VITE_SITE_URL as string | undefined) ?? window.location.origin
