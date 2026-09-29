<?php
/**
 * Makes the product name on single product pages a real <h1> (the Qi theme
 * prints it as an <h2>, leaving product pages with no H1 at all). Adds the
 * theme's own "qodef-h2" class so it keeps exactly the same look.
 *
 * The theme prints the title at woocommerce_single_product_summary
 * priority 5; this buffers priorities 4-6 and swaps only that one tag. If
 * the theme ever moves the title, nothing matches and nothing changes.
 *
 * Live copy: Code Snippets snippet "Product title as H1", front-end scope.
 * Kept in sync with this file by hand. ASCII only.
 */

add_action( 'woocommerce_single_product_summary', function () {
	ob_start();
}, 4 );

add_action( 'woocommerce_single_product_summary', function () {
	$out = ob_get_clean();
	echo preg_replace(
		'#<h2 class="([^"]*\bproduct_title\b[^"]*)">(.*?)</h2>#s',
		'<h1 class="qodef-h2 $1">$2</h1>',
		$out,
		1
	);
}, 6 );
