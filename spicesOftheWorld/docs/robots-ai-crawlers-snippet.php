<?php
/**
 * Adds an explicit "AI assistants and crawlers allowed" group to the virtual
 * robots.txt WordPress + WooCommerce already generate (from the 2026-09
 * SEO & AI Visibility Audit).
 *
 * A crawler that matches a named User-agent group ignores the `*` group
 * entirely, so the AI group repeats the same Disallow lines - otherwise
 * naming GPTBot etc. would let them into /wp-admin/, wc-logs and
 * add-to-cart URLs.
 *
 * Live copy: Code Snippets snippet "robots.txt - allow AI crawlers",
 * global scope. Kept in sync with this file by hand. ASCII only.
 */

add_filter( 'robots_txt', function ( $output, $public ) {
	if ( ! $public ) {
		return $output; // "Discourage search engines" is on - leave it alone.
	}

	$rules = "Disallow: /wp-content/uploads/wc-logs/\n"
		. "Disallow: /wp-content/uploads/woocommerce_transient_files/\n"
		. "Disallow: /wp-content/uploads/woocommerce_uploads/\n"
		. "Disallow: /*?add-to-cart=\n"
		. "Disallow: /*?*add-to-cart=\n"
		. "Disallow: /wp-admin/\n"
		. "Allow: /wp-admin/admin-ajax.php\n"
		. "Allow: /\n";

	$ai = "\n# AI assistants and crawlers - explicitly allowed\n"
		. "User-agent: ClaudeBot\n"
		. "User-agent: Claude-SearchBot\n"
		. "User-agent: Claude-User\n"
		. "User-agent: GPTBot\n"
		. "User-agent: OAI-SearchBot\n"
		. "User-agent: ChatGPT-User\n"
		. "User-agent: PerplexityBot\n"
		. "User-agent: Google-Extended\n"
		. $rules;

	// Keep the Sitemap line last, after the new group.
	if ( preg_match( '/^Sitemap:.*$/mi', $output, $m ) ) {
		$output = trim( str_replace( $m[0], '', $output ) ) . "\n" . $ai . "\n" . $m[0] . "\n";
	} else {
		$output = rtrim( $output ) . "\n" . $ai;
	}
	return $output;
}, 99, 2 );
