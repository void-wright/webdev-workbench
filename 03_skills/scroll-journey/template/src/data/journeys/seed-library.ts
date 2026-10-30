import type { Journey } from './types';

/**
 * EXAMPLE (an invented site): a neighbourhood seed library's "How borrowing works" section, on the page's white paper.
 * Four stops, three passages. Words alternate sides so each wide passage carries a gentle sideways drift. The third
 * stop is the peak (the moment a borrowed seed comes home as a harvest), so it holds longest.
 * Paintings: src/assets/journeys/seed-library/s0-w.jpg ... s3-p.jpg. Clips: public/video/seed-library/.
 */
export const seedLibrary: Journey = {
  idPrefix: 'slj',
  theme: 'light',
  clips: '/video/seed-library/p{n}-{tier}-v1.mp4',
  fit: true,
  skipLabel: 'Skip the journey',
  railLabel: 'Journey stops',
  pause: { pause: 'Pause motion', play: 'Play motion' },
  stops: [
    {
      art: 'seed-library/s0',
      side: 'left',
      anchor: 'borrow',
      title: 'Borrow a packet',
      subhead: 'No card, no fee.',
      body: 'Pick up to five packets from the drawers by the front window. Write your name and the variety in the ledger so we know what is growing where.',
      hold: 1.1,
    },
    {
      art: 'seed-library/s1',
      side: 'right',
      anchor: 'grow',
      title: 'Grow it out',
      body: 'Plant as you would any seed. Let a few of your best plants flower and set seed at the end of the season, away from other varieties of the same crop.',
    },
    {
      art: 'seed-library/s2',
      side: 'left',
      anchor: 'save',
      title: 'Save the seed',
      subhead: 'The harvest that comes back.',
      body: [
        'Dry the pods or heads indoors for two weeks, then shake the seed loose and pick out the chaff.',
        'Our saving evenings run on the first Thursday of each month from September to November.',
      ],
      hold: 1.5,
    },
    {
      art: 'seed-library/s3',
      side: 'center',
      anchor: 'return',
      title: 'Bring some back',
      body: 'Return a packet of what you saved, labelled with the variety and the year. Next spring someone else borrows it.',
      more: { href: '#visit', label: 'Opening hours and address' },
    },
  ],
};
