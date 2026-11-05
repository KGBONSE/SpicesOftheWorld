// Stripe -> Supabase. Sets profiles.membership_status. Deploy with --no-verify-jwt (Stripe has no JWT);
// authenticity comes from the Stripe signature check below.
import Stripe from 'npm:stripe@18'
import { admin, stripe } from '../_shared/common.ts'

const cryptoProvider = Stripe.createSubtleCryptoProvider()

// deno-lint-ignore no-explicit-any
function periodEnd(sub: any): string | null {
  // Newer Stripe API versions put the period on the subscription item; older ones on the subscription.
  const ts = sub.items?.data?.[0]?.current_period_end ?? sub.current_period_end
  return ts ? new Date(ts * 1000).toISOString() : null
}

async function applySubscription(sub: Stripe.Subscription) {
  const active = sub.status === 'active' || sub.status === 'trialing'
  const customerId = typeof sub.customer === 'string' ? sub.customer : sub.customer.id
  const update = {
    membership_status: active ? 'member' : 'free',
    stripe_subscription_id: sub.id,
    stripe_customer_id: customerId,
    current_period_end: periodEnd(sub),
  }
  // Prefer the user id we stamped on the subscription; fall back to the customer id.
  const userId = sub.metadata?.supabase_user_id
  const q = admin.from('profiles').update(update)
  const { error } = userId ? await q.eq('id', userId) : await q.eq('stripe_customer_id', customerId)
  if (error) throw new Error(error.message)
}

Deno.serve(async (req) => {
  const signature = req.headers.get('stripe-signature')
  const secret = Deno.env.get('STRIPE_WEBHOOK_SECRET')
  if (!signature || !secret) return new Response('Missing signature', { status: 400 })

  let event: Stripe.Event
  try {
    event = await stripe.webhooks.constructEventAsync(await req.text(), signature, secret, undefined, cryptoProvider)
  } catch (e) {
    return new Response(`Bad signature: ${(e as Error).message}`, { status: 400 })
  }

  try {
    switch (event.type) {
      case 'checkout.session.completed': {
        const s = event.data.object as Stripe.Checkout.Session
        if (s.mode === 'subscription' && s.subscription) {
          const subId = typeof s.subscription === 'string' ? s.subscription : s.subscription.id
          const sub = await stripe.subscriptions.retrieve(subId)
          // Make sure the profile can be found even if metadata is missing.
          if (s.client_reference_id) sub.metadata = { ...sub.metadata, supabase_user_id: s.client_reference_id }
          await applySubscription(sub)
        }
        break
      }
      case 'customer.subscription.created':
      case 'customer.subscription.updated':
      case 'customer.subscription.deleted':
        await applySubscription(event.data.object as Stripe.Subscription)
        break
    }
  } catch (e) {
    console.error(e)
    return new Response('Handler error', { status: 500 }) // Stripe will retry
  }
  return new Response(JSON.stringify({ received: true }), { headers: { 'Content-Type': 'application/json' } })
})
