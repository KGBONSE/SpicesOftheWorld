<?php
/**
 * Serves https://fudipeople.com/links - the link-in-bio page every social
 * profile points to (Instagram, TikTok, YouTube, X, Facebook). A standalone,
 * fast, phone-first page rather than a theme page, so there's no header,
 * menu or footer between a visitor and the buttons.
 *
 * The top button switches itself: while snippet "Disable purchasing
 * (browse-only)" is active it's "Order on WhatsApp"; once that's off it
 * becomes "Shop now".
 *
 * Live copy: Code Snippets snippet "Link-in-bio page (/links)", global scope.
 * Kept in sync with this file by hand. ASCII only - emoji and dashes are
 * HTML entities.
 */

add_action( 'init', function () {
	$path = rtrim( strtok( $_SERVER['REQUEST_URI'] ?? '', '?' ), '/' );
	if ( '/links' !== $path ) {
		return;
	}

	$open = ! has_filter( 'woocommerce_is_purchasable', '__return_false' );
	$logo = 'https://fudipeople.com/wp-content/uploads/2026/02/WhatsApp_Image_2025-07-20_at_23.42.53-removebg-preview-300x300.webp';
	$wa   = 'https://wa.me/447952983201?text=' . rawurlencode( 'Hi Fudi People, I found you on social media and would like to order' );

	$buttons = $open
		? array( array( 'Shop now', 'https://fudipeople.com/shop/', true ) )
		: array(
			array( 'Order on WhatsApp', $wa, true ),
			array( 'Browse the range', 'https://fudipeople.com/shop/', false ),
		);
	$buttons[] = array( 'Watch us on YouTube', 'https://www.youtube.com/@fudi.people', false );
	$buttons[] = array( 'Visit the kitchen in Sidcup', 'https://fudipeople.com/where-to-buy/', false );
	$buttons[] = array( 'Wholesale enquiries', 'mailto:fudipeople@gmail.com?subject=' . rawurlencode( 'Wholesale enquiry' ), false );
	$buttons[] = array( 'Our story', 'https://fudipeople.com/about-us/', false );

	$social = array(
		'Instagram' => 'https://www.instagram.com/fudi.people/',
		'TikTok'    => 'https://www.tiktok.com/@fudi.people',
		'YouTube'   => 'https://www.youtube.com/@fudi.people',
		'X'         => 'https://x.com/fudipeople',
		'Facebook'  => 'https://www.facebook.com/profile.php?id=100086517852695',
	);

	status_header( 200 );
	header( 'Content-Type: text/html; charset=utf-8' );
	?><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Fudi People &#8211; Links</title>
<meta name="description" content="Chilli oil and spice blends grown, smoked and hand-blended on our farm in Sidcup, London. Shop, watch, visit or order wholesale.">
<meta name="robots" content="noindex, follow">
<meta property="og:title" content="Fudi People">
<meta property="og:description" content="Chilli oil and spice blends grown, smoked and hand-blended in Sidcup, London.">
<meta property="og:image" content="<?php echo esc_url( $logo ); ?>">
<link rel="icon" href="<?php echo esc_url( $logo ); ?>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Lora:wght@700&family=Poppins:wght@400;600&display=swap" rel="stylesheet">
<style>
  :root { --bg:#FFF3E2; --ink:#3A1408; --muted:#7A4A36; --accent:#E8741C; --btn:#FFFFFF; --line:#EED9C2; }
  @media (prefers-color-scheme: dark) { :root { --bg:#1E0D06; --ink:#FFF3E2; --muted:#D9B79C; --accent:#F4A53A; --btn:#2B140A; --line:#4A2A1A; } }
  * { box-sizing:border-box; }
  body { margin:0; min-height:100vh; background:var(--bg); color:var(--ink); font:16px/1.5 Poppins, system-ui, sans-serif; }
  main { max-width:460px; margin:0 auto; padding:36px 16px 40px; text-align:center; }
  img.logo { width:108px; height:108px; border-radius:50%; object-fit:contain; background:#fff; border:3px solid var(--accent); }
  h1 { font:700 26px/1.2 Lora, Georgia, serif; margin:14px 0 6px; }
  p.tag { margin:0 auto 24px; color:var(--muted); font-size:15px; max-width:340px; }
  a.btn { display:block; margin:0 0 12px; padding:15px 18px; border-radius:14px; background:var(--btn); color:var(--ink); border:1.5px solid var(--line); text-decoration:none; font-weight:600; transition:transform .15s; }
  a.btn:hover, a.btn:focus-visible { transform:translateY(-2px); border-color:var(--accent); }
  a.btn.main { background:var(--accent); border-color:var(--accent); color:#2B140A; }
  .social { display:flex; justify-content:center; flex-wrap:wrap; gap:8px 16px; margin:26px 0 18px; }
  .social a { color:var(--ink); font-size:14px; font-weight:600; text-decoration:none; border-bottom:2px solid var(--accent); }
  small { display:block; color:var(--muted); font-size:13px; }
</style>
</head>
<body>
<main>
  <img class="logo" src="<?php echo esc_url( $logo ); ?>" alt="Fudi People logo" width="108" height="108">
  <h1>Fudi People</h1>
  <p class="tag">Chillies grown and smoked by hand on our farm in Sidcup, London, then turned into chilli oil and spice blends from around the world&nbsp;&#127798;&#65039;</p>
<?php foreach ( $buttons as $b ) : ?>
  <a class="btn<?php echo $b[2] ? ' main' : ''; ?>" href="<?php echo esc_url( $b[1], array( 'https', 'mailto' ) ); ?>"<?php echo 0 === strpos( $b[1], 'mailto:' ) ? '' : ' target="_blank" rel="noopener"'; ?>><?php echo esc_html( $b[0] ); ?></a>
<?php endforeach; ?>
  <div class="social">
<?php foreach ( $social as $name => $url ) : ?>
    <a href="<?php echo esc_url( $url ); ?>" target="_blank" rel="noopener"><?php echo esc_html( $name ); ?></a>
<?php endforeach; ?>
  </div>
  <small>Kitchen open Monday&#8211;Saturday, 10am&#8211;6pm, by arrangement &middot; Arcadia, Honeyden Road, Sidcup, DA14 5LX</small>
</main>
</body>
</html>
<?php
	exit;
}, 0 );
