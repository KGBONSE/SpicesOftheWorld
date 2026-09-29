<?php
/**
 * Prints schema.org "Store" JSON-LD (name, contact, address, opening hours)
 * on the homepage and Contact page (from the 2026-09 SEO & AI Visibility
 * Audit). Product pages already get Product JSON-LD from WooCommerce.
 *
 * Live copy: Code Snippets snippet "Store schema (JSON-LD)", front-end scope.
 * Kept in sync with this file by hand. ASCII only.
 */

add_action( 'wp_head', function () {
	if ( ! is_front_page() && ! is_page( 'contact-us' ) ) {
		return;
	}

	$logo = 'https://fudipeople.com/wp-content/uploads/2026/02/WhatsApp_Image_2025-07-20_at_23.42.53-removebg-preview.webp';

	$schema = array(
		'@context'    => 'https://schema.org',
		'@type'       => 'Store',
		'@id'         => 'https://fudipeople.com/#store',
		'name'        => 'Fudi People',
		'description' => 'Small-batch chilli oil and spice blends, hand-grown and hand-blended on our farm in Sidcup, London.',
		'url'         => 'https://fudipeople.com',
		'logo'        => $logo,
		'image'       => $logo,
		'email'       => 'fudipeople@gmail.com',
		'telephone'   => '+44 7952 983201',
		'address'     => array(
			'@type'           => 'PostalAddress',
			'streetAddress'   => 'Arcadia, Honeyden Road',
			'addressLocality' => 'Sidcup',
			'postalCode'      => 'DA14 5LX',
			'addressCountry'  => 'GB',
		),
		'openingHoursSpecification' => array(
			'@type'     => 'OpeningHoursSpecification',
			'dayOfWeek' => array( 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' ),
			'opens'     => '10:00',
			'closes'    => '18:00',
		),
		'sameAs'      => array(
			'https://www.instagram.com/fudi.people/',
			'https://www.tiktok.com/@fudi.people',
			'https://www.youtube.com/@fudi.people',
			'https://x.com/fudipeople',
			'https://www.facebook.com/profile.php?id=100086517852695',
		),
	);

	echo '<script type="application/ld+json">'
		. wp_json_encode( $schema, JSON_UNESCAPED_SLASHES )
		. "</script>\n";
} );
