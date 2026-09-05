<?php
/**
 * Live copy: Code Snippets snippet #8 ("Retired product redirects"),
 * front-end scope. Kept in sync with this file by hand.
 */
/**
 * 301-redirects the retired region-named "___ Spice Mix" product URLs to
 * their kept dish-name product. The old products are set to draft; without
 * this they'd 404. Added 2026-09-05 when the duplicate product line was
 * consolidated onto the dish-name products.
 */
add_action( 'template_redirect', function () {
	$map = array(
		'amazon-spice-mix' => 'tucupi-amazon-basin',
		'andes-spice-mix' => 'chimichurri-the-andes',
		'arabian-peninsula-spice-mix' => 'hawaij-arabian-peninsula',
		'bangladesh-spice-mix' => 'panch-phoran-east-india-bangladesh',
		'caribbean-spice-mix' => 'jamaican-jerk-rub-the-caribbean',
		'central-africa-spice-mix' => 'mbongo-mix-central-africa',
		'central-india-spice-mix' => 'chaat-masala-central-india',
		'east-africa-spice-mix' => 'pilau-masala-zanzibar-east-africa',
		'east-china-spice-mix' => 'nanjing-spice-bag-east-china',
		'east-india-spice-mix' => 'panch-phoran-east-india-bangladesh',
		'egypt-spice-mix' => 'dukkah-egypt',
		'himalayan-belt-spice-mix' => 'timur-ko-chhop-himalayan-belt',
		'horn-of-africa-spice-mix' => 'niter-kibbeh-ethiopian-spiced-butter',
		'iraq-spice-mix' => 'arabic-baharat-iraq',
		'israel-spice-mix' => 'zhug-israel',
		'japan-spice-mix' => 'shichimi-togarashi-japan',
		'lebanon-spice-mix' => 'taklia-lebanon',
		'maghreb-spice-mix' => 'harissa-maghreb-chilli-paste',
		'mexico-central-america-spice-mix' => 'mole-mix-mexico-central-america',
		'north-america-spice-mix' => 'bbq-rub-north-america',
		'north-china-spice-mix' => 'shandong-spice-bag-north-china',
		'north-india-spice-mix' => 'garam-masala-north-india',
		'south-america-spice-mix' => 'leche-de-tigre-pacific-south-america',
		'south-china-spice-mix' => 'five-spice-powder-south-china',
		'south-india-spice-mix' => 'gunpowder-podi-south-india-sri-lanka',
		'south-korea-spice-mix' => 'yangnyeomjang-south-korea',
		'southern-africa-spice-mix' => 'durban-curry-masala-southern-africa',
		'sri-lanka-spice-mix' => 'gunpowder-podi-south-india-sri-lanka',
		'syria-spice-mix' => 'zaatar-syria',
		'turkey-spice-mix' => 'turkish-baharat-turkey',
		'west-africa-spice-mix' => 'yaji-west-african-suya-spice-rub',
		'west-china-spice-mix' => 'chilli-black-bean-sauce-west-china',
		'west-india-spice-mix' => 'vindaloo-paste-west-india',
	);

	$path = trim( parse_url( $_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH ) ?: '', '/' );
	if ( strpos( $path, 'product/' ) !== 0 ) {
		return;
	}
	$slug = trim( substr( $path, strlen( 'product/' ) ), '/' );
	if ( isset( $map[ $slug ] ) ) {
		wp_safe_redirect( home_url( '/product/' . $map[ $slug ] . '/' ), 301 );
		exit;
	}
} );
