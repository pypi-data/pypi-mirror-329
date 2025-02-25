import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      collapsed: false,
      items: [
        'getting-started/overview',
        'getting-started/quickstart',
        'getting-started/installation',
        'getting-started/concepts',
      ],
    },
    {
      type: 'category',
      label: 'About', 
      collapsed: false,
      items: [
        'about/community',
        'about/contributing',
      ],
    },
  ],
};

export default sidebars;