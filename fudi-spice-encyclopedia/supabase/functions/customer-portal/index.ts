// Returns a Stripe Customer Portal link so members can manage or cancel.
import { admin, corsHeaders, getUser, json, stripe } from '../_shared/common.ts'

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: corsHeaders })

  const user = await getUser(req)
  if (!user) return json({ error: 'Sign in first.' }, 401)

  const { data: profile } = await admin.from('profiles').select('stripe_customer_id').eq('id', user.id).maybeSingle()
  if (!profile?.stripe_customer_id) return json({ error: 'No membership found for this account.' }, 404)

  const session = await stripe.billingPortal.sessions.create({
    customer: profile.stripe_customer_id,
    return_url: `${Deno.env.get('SITE_URL') ?? ''}/account`,
  })
  return json({ url: session.url })
})
