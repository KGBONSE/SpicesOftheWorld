// Starts a Stripe Checkout subscription session (GBP prices are defined in your Stripe Dashboard).
import { admin, corsHeaders, getUser, json, stripe } from '../_shared/common.ts'

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: corsHeaders })

  const user = await getUser(req)
  if (!user) return json({ error: 'Sign in first.' }, 401)

  const { plan } = await req.json().catch(() => ({ plan: '' }))
  const price = plan === 'annual' ? Deno.env.get('STRIPE_PRICE_ANNUAL') : plan === 'monthly' ? Deno.env.get('STRIPE_PRICE_MONTHLY') : null
  if (!price) return json({ error: 'Unknown plan.' }, 400)

  const { data: profile } = await admin.from('profiles').select('stripe_customer_id').eq('id', user.id).maybeSingle()
  const site = Deno.env.get('SITE_URL') ?? ''

  const session = await stripe.checkout.sessions.create({
    mode: 'subscription',
    line_items: [{ price, quantity: 1 }],
    client_reference_id: user.id,
    ...(profile?.stripe_customer_id ? { customer: profile.stripe_customer_id } : { customer_email: user.email ?? undefined }),
    subscription_data: { metadata: { supabase_user_id: user.id } },
    allow_promotion_codes: true,
    success_url: `${site}/account?checkout=success`,
    cancel_url: `${site}/membership`,
  })
  return json({ url: session.url })
})
