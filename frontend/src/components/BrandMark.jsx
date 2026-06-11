export default function BrandMark({
  size = 38,
  title = 'JARVIS Acadêmico',
  decorative = true,
  className = '',
}) {
  const classes = ['brand-mark', className].filter(Boolean).join(' ');

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
