export default function BrandMark({
  variant = 'default',
  size = 38,
  title = 'JARVIS Acadêmico',
  decorative = true,
  className = '',
}) {
  const classes = ['brand-mark', `brand-mark-${variant}`, className].filter(Boolean).join(' ');

  return (
    <span
      className={classes}
      style={{ '--brand-mark-size': `${size}px` }}
      role={decorative ? undefined : 'img'}
      aria-label={decorative ? undefined : title}
      aria-hidden={decorative ? 'true' : undefined}
    />
  );
}
