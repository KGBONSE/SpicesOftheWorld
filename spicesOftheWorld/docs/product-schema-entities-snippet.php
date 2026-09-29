<?php
/**
 * Fixes WooCommerce's product JSON-LD printing "&" as "&amp;amp;" (e.g.
 * "Sierra Leone &amp;amp; Liberia"). WooCommerce runs its JSON through
 * wc_esc_json(), which HTML-escapes it - but a <script> block is never
 * HTML-decoded, so any "&" ends up in the schema as a literal entity.
 *
 * Uses only the documented woocommerce_structured_data_product filter:
 * decodes entities and writes "&" as "and" in the schema's name and
 * description, so there is nothing left for wc_esc_json() to mangle.
 * The visible product title on the page is unchanged.
 *
 * (A first attempt that replaced WooCommerce's whole wp_footer output took
 * the site down with a fatal error - don't go back to that approach.)
 *
 * Live copy: Code Snippets snippet "Product schema - fix &amp; in names",
 * front-end scope. Kept in sync with this file by hand. ASCII only.
 */

add_filter( 'woocommerce_structured_data_product', function ( $markup ) {
	foreach ( array( 'name', 'description' ) as $key ) {
		if ( isset( $markup[ $key ] ) && is_string( $markup[ $key ] ) ) {
			$v = html_entity_decode( html_entity_decode( $markup[ $key ], ENT_QUOTES, 'UTF-8' ), ENT_QUOTES, 'UTF-8' );
			$markup[ $key ] = str_replace( '&', 'and', $v );
		}
	}
	return $markup;
} );
