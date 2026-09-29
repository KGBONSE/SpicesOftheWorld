<?php
/**
 * Adds one real, page-specific <h1> plus a one-line intro above the product
 * grid on the region category pages (from the 2026-09 SEO & AI Visibility
 * Audit). The Qi theme hides WooCommerce's own archive title, so without
 * this the only headings on those pages were the footer's "Visit our
 * store" / "Want to say Hi?" / "Social media".
 *
 * Prints inside WooCommerce's (otherwise empty) products header via the
 * woocommerce_archive_description hook.
 *
 * Live copy: Code Snippets snippet "Category page headings", front-end
 * scope. Kept in sync with this file by hand. ASCII only - the em dash is
 * written as \u{2014}.
 */

add_action( 'woocommerce_archive_description', function () {
	$m = "\u{2014}";
	$headings = array(
		'africa'      => array( 'African Spice Blends & Chilli Oil', "Hand-blended in Sidcup, London $m from Durban curry masala to yassa and pilau masala." ),
		'middle-east' => array( 'Middle Eastern Spice Blends', "Za'atar, dukkah, baharat and more, hand-blended in small batches in London." ),
		'south-asia'  => array( 'South Asian Spice Blends & Chilli Oil', "Hand-blended in Sidcup, London $m from garam masala to panch phoran and chaat masala." ),
		'east-asia'   => array( 'East Asian Spice Blends & Chilli Oil', 'Five-spice, shichimi togarashi, Sichuan chilli bean and more, hand-blended in small batches in London.' ),
		'americas'    => array( 'Spice Blends of the Americas', "Hand-blended in Sidcup, London $m from Jamaican jerk rub to chimichurri and mole mix." ),
		'_shop'       => array( 'Spice Blends & Chilli Oil from Around the World', 'Small-batch blends from Africa, the Middle East, South Asia, East Asia and the Americas, hand-blended on our farm in Sidcup, London.' ),
	);
	foreach ( $headings as $slug => $h ) {
		if ( '_shop' === $slug ? is_shop() : is_product_category( $slug ) ) {
			echo '<div class="fudi-category-intro" style="margin:0 0 2em;">'
				. '<h1 class="page-title" style="margin:0 0 .3em;">' . esc_html( $h[0] ) . '</h1>'
				. '<p style="margin:0;">' . esc_html( $h[1] ) . '</p>'
				. '</div>';
			return;
		}
	}
}, 5 );
