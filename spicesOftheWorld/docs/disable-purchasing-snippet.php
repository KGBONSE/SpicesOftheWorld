<?php
/**
 * Browse-only mode: the store stays live and every product stays visible,
 * but nothing can be bought. Removes all add-to-basket buttons, empties any
 * existing basket, sends /cart and /checkout back to the shop, and shows a
 * "order via WhatsApp" notice where the buy button used to be.
 *
 * To reopen the shop: Snippets -> deactivate this snippet. Nothing else
 * needs undoing (no product, stock or price data is touched).
 *
 * Live copy: Code Snippets snippet "Disable purchasing (browse-only)",
 * front-end scope. Kept in sync with this file by hand. ASCII only.
 */

// Nothing is purchasable -> WooCommerce hides add-to-basket everywhere and
// refuses add-to-cart requests (including ?add-to-cart= links).
add_filter( 'woocommerce_is_purchasable', '__return_false' );
add_filter( 'woocommerce_variation_is_purchasable', '__return_false' );

function fudi_browse_only_notice() {
	echo '<p class="fudi-orders-closed" style="margin:1em 0;padding:.8em 1em;border-left:3px solid #38524f;background:#f3f7f6;">'
		. 'Online orders open soon. WhatsApp us on '
		. '<a href="https://wa.me/447952983201" target="_blank" rel="noopener">+44 7952 983201</a>'
		. ' to order.</p>';
}
add_action( 'woocommerce_single_product_summary', 'fudi_browse_only_notice', 30 );

// Empty any basket filled before the switch, and keep people off
// the basket/checkout pages.
add_action( 'template_redirect', function () {
	if ( function_exists( 'WC' ) && WC()->cart && ! WC()->cart->is_empty() ) {
		WC()->cart->empty_cart();
	}
	if ( is_cart() || is_checkout() ) {
		wp_safe_redirect( wc_get_page_permalink( 'shop' ) );
		exit;
	}
} );

// Belt and braces: block any order that reaches classic checkout processing
// anyway (e.g. a direct POST).
add_action( 'woocommerce_checkout_process', function () {
	wc_add_notice( 'Online orders are not open yet.', 'error' );
} );
