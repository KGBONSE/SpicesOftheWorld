<?php
/**
 * Custom <title> and <meta name="description"> for the key pages (from the
 * 2026-09 SEO & AI Visibility Audit). No SEO plugin is active, so this sets
 * them directly; every other page keeps WordPress's default title.
 *
 * "Order online" wording switches itself: while snippet "Disable purchasing
 * (browse-only)" is active it says order by WhatsApp instead.
 *
 * Live copy: Code Snippets snippet "SEO titles and meta descriptions",
 * front-end scope. Kept in sync with this file by hand. ASCII only - en/em
 * dashes are written as \u{2013} / \u{2014}.
 */

function fudi_seo_meta() {
	$open = ! has_filter( 'woocommerce_is_purchasable', '__return_false' );
	$n    = "\u{2013}"; // en dash
	$m    = "\u{2014}"; // em dash

	if ( is_front_page() ) {
		return array(
			"Fudi People $n African & Asian Spice Blends and Chilli Oil, London",
			'Small-batch chilli oil and spice blends inspired by Africa, South Asia, East Asia and the Middle East. Grown and hand-blended on our farm in Sidcup, London.',
		);
	}
	if ( is_product_category( 'africa' ) ) {
		return array(
			'African Spice Blends & Chilli Oil | Fudi People, London',
			"Durban curry masala, harissa, yaji, pilau masala and more $m hand-blended African spice blends and chilli oil, made in Sidcup, London. "
				. ( $open ? 'Order online or visit us.' : 'Order by WhatsApp or visit us.' ),
		);
	}
	if ( is_product_category( 'middle-east' ) ) {
		return array(
			"Middle Eastern Spice Blends | Za'atar, Dukkah & Baharat $n Fudi People",
			"Za'atar, dukkah, baharat, hawaij and more $m Middle Eastern spice blends hand-blended in small batches in London. "
				. ( $open ? 'Order online, ready to ship.' : 'Order by WhatsApp or visit us.' ),
		);
	}
	if ( is_page( 'about-us' ) ) {
		return array(
			'Our Story ' . $n . ' From Mokola Market to a Farm in Sidcup | Fudi People',
			'Fudi People started at Mokola Market in Accra, Ghana. Today we grow chillies and okra on our own farm in Sidcup, London, and hand-blend every spice mix ourselves.',
		);
	}
	if ( is_page( 'where-to-buy' ) ) {
		return array(
			'Visit or Order | Fudi People, Sidcup, London',
			'Order Fudi People spice blends and chilli oil ' . ( $open ? 'online' : 'by WhatsApp' )
				. ", or visit our kitchen in Sidcup, London (DA14 5LX). Open Monday$n" . "Saturday, 10am$n" . '6pm.',
		);
	}
	if ( is_page( 'contact-us' ) ) {
		return array(
			'Contact Us | Fudi People, Sidcup, London',
			"Call or WhatsApp Fudi People on +44 7952 983201, email fudipeople@gmail.com, or visit our kitchen in Sidcup, London (DA14 5LX). Monday$n" . "Saturday, 10am$n" . '6pm.',
		);
	}
	return null;
}

add_filter( 'pre_get_document_title', function ( $title ) {
	$meta = fudi_seo_meta();
	return $meta ? esc_html( $meta[0] ) : $title;
}, 20 );

add_action( 'wp_head', function () {
	$meta = fudi_seo_meta();
	if ( $meta ) {
		echo '<meta name="description" content="' . esc_attr( $meta[1] ) . '" />' . "\n";
	}
}, 1 );
