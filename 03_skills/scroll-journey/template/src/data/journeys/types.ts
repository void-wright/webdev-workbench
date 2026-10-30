/**
 * A scroll journey's data, read by src/components/ScrollJourney.astro.
 *
 * Every word the reader sees is a plain string here; the component carries none of its own. Paintings are found by
 * name: `art: 'seed-library/s0'` means src/assets/journeys/seed-library/s0-w.jpg (wide, 16:9) and s0-p.jpg (phone,
 * 9:16). .jpg, .jpeg, .png and .webp all work.
 */

/** A real link laid over a painted form (for example a product, a room or a programme the reader can visit). */
export type JourneyDoor = {
  href: string;
  /** the link's visible name, set under the form */
  label: string;
  /** a one-line description shown beside the words on hover or focus (always shown on touch screens) */
  readout: string;
  /** the clickable region as fractions of the painting: [centre x, centre y, width, height], wide painting */
  w: [number, number, number, number];
  /** the same for the phone painting */
  p: [number, number, number, number];
  /** the glow colour on hover and focus (any CSS colour); default: the journey's accent */
  color?: string;
};

export type JourneyStop = {
  /** the painting's name, without the -w / -p suffix */
  art: string;
  /** the heading's id (default `${idPrefix}-s${i}-title`); keep an old section's id here so outside links still land */
  anchor?: string;
  /** where the words sit on wide screens; on portrait screens they always sit in the lower part */
  side: 'left' | 'right' | 'center';
  title: string;
  subhead?: string;
  /** one paragraph, or several */
  body?: string | string[];
  /** a closing line in the display face */
  line?: string;
  /** the heading level (default 2) */
  level?: 2 | 3;
  /** a larger title, for an opening statement */
  lead?: boolean;
  /** this stop's hold as a multiple of --sj-hold (the last stop: of --sj-end); default 1. Give the peak stop more. */
  hold?: number;
  /** the rail marker's accessible name (default: the title) */
  rail?: string;
  door?: JourneyDoor;
  /** a text link under the words */
  more?: { href: string; label: string };
};

export type Journey = {
  /** a short unique prefix for ids: `${idPrefix}-s${i}`; the last stop's words are `${idPrefix}-s${n-1}-words` */
  idPrefix: string;
  /** dark: a night ground; light: the page's own white paper */
  theme: 'dark' | 'light';
  /** the passages' URL pattern under public/: {n} is the passage (1-based), {tier} is 16x9 | 16x9-1080 | 9x16.
   *  Put a version in the name (-v1) and bump it whenever a clip changes, so long-lived caches never serve an old one. */
  clips: string;
  /** run the parse-time fit test: if any stop's words cannot sit whole in the pinned screen, the stops stack instead */
  fit?: boolean;
  /** the "skip the journey" link's text */
  skipLabel: string;
  /** the stop rail's accessible name */
  railLabel: string;
  /** the built-in motion pause button's two labels; false when the site already has its own control that sets
   *  <html data-motion="paused"> */
  pause: { pause: string; play: string } | false;
  /** hints for journeys with doors: how to preview a door with a pointer, and on touch */
  affordance?: { pointer: string; touch: string };
  /** the words' paper veil on a light journey (0..1), set from measured contrast; default 0.8 wide, 0.86 phone */
  veil?: { wide: number; phone: number };
  class?: string;
  stops: JourneyStop[];
};
