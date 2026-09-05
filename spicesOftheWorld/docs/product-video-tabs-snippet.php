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
 * Live copy: Code Snippets snippet #5 ("Product Video Tabs"), global scope.
 * Kept in sync with this file by hand.
 *
 * Each tab shows the WRITTEN RECIPE first, then the VIDEO below it once one
 * exists (or a "video coming soon" line until then). Both come from product
 * custom fields:
 *
 *   spice_blend_recipe    - HTML: the blend ingredients + method
 *   spice_blend_video_url - a YouTube/Vimeo link, or a Media Library file URL
 *   cooking_recipe        - HTML: how to cook the paired dish
 *   cooking_video_url     - a YouTube/Vimeo link, or a Media Library file URL
 *
 * To edit a field in wp-admin: edit the product -> Custom Fields panel
 * (three-dot menu -> Preferences -> Panels -> "Custom fields" if hidden) ->
 * enter the field Name and Value -> Add Custom Field -> Update. Underscore-
 * prefixed names are hidden from that panel by design, so these have none.
 *
 * A video Value can be either:
 *  - A YouTube/Vimeo link, e.g. https://www.youtube.com/watch?v=XXXXXXXXXXX
 *  - A direct link to a video file in the Media Library (ends .mp4/.mov/etc)
 *
 * If both the recipe and the video field for a tab are empty, the tab shows
 * a plain "Coming soon" placeholder.
 */
add_filter( 'woocommerce_product_tabs', function ( $tabs ) {
	global $product;

	if ( ! $product ) {
		return $tabs;
	}

	$id = $product->get_id();

	$render_section = function ( $recipe, $video_url, $no_video_note, $empty_note ) {
		$recipe    = trim( (string) $recipe );
		$video_url = trim( (string) $video_url );

		if ( '' === $recipe && '' === $video_url ) {
			echo '<p><em>Coming soon</em> — ' . esc_html( $empty_note ) . '</p>';
			return;
		}

		if ( '' !== $recipe ) {
			echo '<div class="fp-recipe">' . wp_kses_post( wpautop( $recipe ) ) . '</div>';
		}

		if ( '' === $video_url ) {
			echo '<p class="fp-video-soon"><em>' . esc_html( $no_video_note ) . '</em></p>';
			return;
		}

		$is_file = (bool) preg_match( '/\.(mp4|m4v|mov|webm|ogv)(\?.*)?$/i', $video_url );
		echo '<div class="fp-recipe-video">';
		if ( $is_file ) {
			echo wp_video_shortcode( array( 'src' => esc_url( $video_url ) ) );
		} else {
			echo wp_oembed_get( esc_url( $video_url ) );
		}
		echo '</div>';
	};

	$blend_recipe = get_post_meta( $id, 'spice_blend_recipe', true );
	$blend_url    = get_post_meta( $id, 'spice_blend_video_url', true );
	$cook_recipe  = get_post_meta( $id, 'cooking_recipe', true );
	$cook_url     = get_post_meta( $id, 'cooking_video_url', true );

	$tabs['spice_blend_video'] = array(
		'title'    => __( 'Spice Blend', 'fudi-people' ),
		'priority' => 25,
		'callback' => function () use ( $blend_recipe, $blend_url, $render_section ) {
			$render_section(
				$blend_recipe,
				$blend_url,
				'Blend video coming soon.',
				'the recipe and video for this blend are on their way.'
			);
		},
	);

	$tabs['cooking_video'] = array(
		'title'    => __( 'Cooking', 'fudi-people' ),
		'priority' => 26,
		'callback' => function () use ( $cook_recipe, $cook_url, $render_section ) {
			$render_section(
				$cook_recipe,
				$cook_url,
				'Cooking video coming soon.',
				'the recipe and video for cooking with this blend are on their way.'
			);
		},
	);

	return $tabs;
} );
