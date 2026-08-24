<?php
/**
 * Adds "Spice Blend" and "Cooking" tabs to every WooCommerce product page,
 * alongside the default Description and Reviews tabs.
 *
 * Install: Plugins -> Add New -> install & activate "Code Snippets" (free) ->
 * Snippets -> Add New -> paste everything below this comment block (not
 * including the <?php tag - Code Snippets adds that automatically) ->
 * Save Changes and Activate.
 *
 * To add or edit a video on a product: edit the product in wp-admin ->
 * scroll down below the description editor -> if you don't see a "Custom
 * Fields" panel, click the three-dot menu (top right) -> Preferences ->
 * Panels -> turn on "Custom fields" (the page will reload) -> scroll back
 * down -> under "Add New Custom Field" enter the field Name
 * (spice_blend_video_url or cooking_video_url) and the Value -> click
 * "Add Custom Field" -> Update the product. To edit an existing one, just
 * change the Value and click "Update" next to that field.
 *
 * The Value can be either:
 *  - A YouTube/Vimeo link, e.g. https://www.youtube.com/watch?v=XXXXXXXXXXX
 *  - A direct link to a video file already in your Media Library
 *    (Media -> Add New -> upload the file -> click it -> copy the "File URL"
 *    field, which ends in .mp4/.mov/etc)
 *
 * Until a link is added, the tab shows a "Coming soon" placeholder instead.
 */
add_filter( 'woocommerce_product_tabs', function ( $tabs ) {
	global $product;

	if ( ! $product ) {
		return $tabs;
	}

	$blend_url   = get_post_meta( $product->get_id(), 'spice_blend_video_url', true );
	$cooking_url = get_post_meta( $product->get_id(), 'cooking_video_url', true );

	$render_video = function ( $url, $placeholder ) {
		if ( ! $url ) {
			echo $placeholder;
			return;
		}
		$is_file = (bool) preg_match( '/\.(mp4|m4v|mov|webm|ogv)(\?.*)?$/i', $url );
		if ( $is_file ) {
			echo wp_video_shortcode( array( 'src' => esc_url( $url ) ) );
		} else {
			echo wp_oembed_get( esc_url( $url ) );
		}
	};

	$tabs['spice_blend_video'] = array(
		'title'    => __( 'Spice Blend', 'fudi-people' ),
		'priority' => 25,
		'callback' => function () use ( $blend_url, $render_video ) {
			$render_video( $blend_url, '<p><em>Coming soon</em> — watch how this spice blend comes together.</p>' );
		},
	);

	$tabs['cooking_video'] = array(
		'title'    => __( 'Cooking', 'fudi-people' ),
		'priority' => 26,
		'callback' => function () use ( $cooking_url, $render_video ) {
			$render_video( $cooking_url, '<p><em>Coming soon</em> — watch this blend used in a real dish.</p>' );
		},
	);

	return $tabs;
} );
