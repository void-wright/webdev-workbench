import type { Journey } from './types';

/**
 * EXAMPLE (an invented site): an amateur astronomy club's "A first night out" section, on a dark ground. Four stops,
 * three passages; two stops carry a door (a link laid over a painted form) to a club page. The closing stop is centred.
 * Paintings: src/assets/journeys/night-sky/s0-w.jpg ... s3-p.jpg. Clips: public/video/night-sky/.
 */
export const nightSky: Journey = {
  idPrefix: 'nsj',
  theme: 'dark',
  clips: '/video/night-sky/p{n}-{tier}-v1.mp4',
  fit: true,
  skipLabel: 'Skip the journey',
  railLabel: 'Journey stops',
  pause: { pause: 'Pause motion', play: 'Play motion' },
  affordance: { pointer: 'Hover or focus a glowing shape to preview it. Esc clears it.', touch: 'Tap a glowing shape to visit it.' },
  stops: [
    {
      art: 'night-sky/s0',
      side: 'left',
      title: 'Your first night out',
      line: 'No telescope needed to start.',
      lead: true,
      rail: 'Start',
    },
    {
      art: 'night-sky/s1',
      side: 'right',
      title: 'Let your eyes adjust',
      body: 'Give it twenty minutes away from screens and street lights. A red torch keeps your night vision while you read a chart.',
      level: 3,
      door: {
        href: '/guides/dark-adaptation/',
        label: 'Dark adaptation',
        readout: 'Why twenty minutes, and how to keep it.',
        w: [0.3, 0.5, 0.3, 0.5],
        p: [0.5, 0.22, 0.7, 0.28],
      },
    },
    {
      art: 'night-sky/s2',
      side: 'left',
      title: 'Find one landmark',
      body: 'Start from one bright, easy pattern and hop from it to its neighbours. One landmark learned well beats ten half-remembered.',
      level: 3,
      hold: 1.3,
      door: {
        href: '/guides/star-hopping/',
        label: 'Star hopping',
        readout: 'A first route across the autumn sky.',
        w: [0.72, 0.5, 0.32, 0.5],
        p: [0.5, 0.22, 0.7, 0.28],
        color: '#f2a65a',
      },
    },
    {
      art: 'night-sky/s3',
      side: 'center',
      title: 'Come to an observing night',
      body: 'Members bring telescopes to the hill car park on clear Saturdays. Guests are always welcome.',
      rail: 'Join us',
      more: { href: '/observing-nights/', label: 'See the next dates' },
    },
  ],
};
