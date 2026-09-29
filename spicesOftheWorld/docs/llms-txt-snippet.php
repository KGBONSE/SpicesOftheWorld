<?php
/**
 * Serves https://fudipeople.com/llms.txt - a plain-language fact sheet for
 * AI assistants (from the 2026-09 SEO & AI Visibility Audit). The site root
 * isn't writable through WordPress, so the file is answered from PHP.
 *
 * "Where to buy" switches itself: while snippet "Disable purchasing
 * (browse-only)" is active it says order by WhatsApp; once that snippet is
 * switched off it says order online.
 *
 * Live copy: Code Snippets snippet "llms.txt", global scope.
 * Kept in sync with this file by hand. ASCII only (dashes are plain "-").
 */

add_action( 'init', function () {
	$path = strtok( $_SERVER['REQUEST_URI'] ?? '', '?' );
	if ( '/llms.txt' !== $path ) {
		return;
	}

	$txt = <<<'TXT'
# Fudi People

> Small-batch chilli oil and spice blends, hand-grown and hand-blended in Sidcup, London.

## About
Fudi People started at Mokola Market in Accra, Ghana, and is now run from a working farm in Sidcup, London, where chillies and okra are grown by hand using traditional family methods. Every spice blend and chilli oil is blended in small batches, not made in a factory.

## What we sell
- African spice blends and chilli oil - Durban curry masala, harissa, mbongo mix, niter kibbeh, pepper soup spice, pilau masala, yaji, yassa, and chilli oil infused with African spices
- South Asian spice blends
- East Asian spice blends
- Middle Eastern spice blends - advieh, Arabic baharat, dukkah, hawaij, taklia, Turkish baharat, za'atar, zhug-style blend

Southeast Asian, American and European lines are in development.

## Where to buy
{{WHERE_TO_BUY}}

## Hours
Monday-Saturday, 10am-6pm. Closed Sunday.

## Contact
Email: fudipeople@gmail.com
Phone / WhatsApp: +44 7952 983201
Location: Arcadia, Honeyden Road, Sidcup, DA14 5LX

## Links
- Shop: https://fudipeople.com/shop/
- About: https://fudipeople.com/about-us/
- Where to buy: https://fudipeople.com/where-to-buy/
- Contact: https://fudipeople.com/contact-us/

## Social media
- Instagram: https://www.instagram.com/fudi.people/
- TikTok: https://www.tiktok.com/@fudi.people
- YouTube: https://www.youtube.com/@fudi.people
- X: https://x.com/fudipeople
- Facebook: https://www.facebook.com/profile.php?id=100086517852695
TXT;

	// Browse-only snippet active -> it has hooked __return_false here.
	$orders_closed = has_filter( 'woocommerce_is_purchasable', '__return_false' );
	$where = $orders_closed
		? 'The full range can be browsed at https://fudipeople.com/shop/. Online checkout is opening soon; until then, order by WhatsApp on +44 7952 983201 (https://wa.me/447952983201), or visit the kitchen in person in Sidcup, London (by arrangement - see Contact).'
		: 'Order online at https://fudipeople.com/shop/, or visit the kitchen in person in Sidcup, London (by arrangement - see Contact).';
	$txt = str_replace( '{{WHERE_TO_BUY}}', $where, $txt );

	status_header( 200 );
	header( 'Content-Type: text/plain; charset=utf-8' );
	echo $txt . "\n";
	exit;
}, 0 );
