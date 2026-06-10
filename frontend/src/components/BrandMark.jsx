const variantSources = {
  lavender: '/brand/jarvis-symbol-lavender.svg',
  paper: '/brand/jarvis-symbol-paper.svg',
  micro: '/brand/jarvis-symbol-micro.svg',
  outline: '/brand/jarvis-symbol-outline.svg',
};

export default function BrandMark({
  variant = 'lavender',
  size = 38,
  title = 'JARVIS Acadêmico',
  decorative = true,
  className = '',
}) {
  const src = variantSources[variant] || variantSources.lavender;
  const classes = ['brand-mark', className].filter(Boolean).join(' ');

  return (
    <img
      className={classes}
      src={src}
      width={size}
      height={size}
      alt={decorative ? '' : title}
      title={decorative ? undefined : title}
      aria-hidden={decorative ? 'true' : undefined}
      loading="eager"
      decoding="async"
    />
  );
}
