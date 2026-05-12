// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	integrations: [
		starlight({
			title: 'My Docs',
			social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/withastro/starlight' }],
			sidebar: [
				{
					label: 'AWS',
					items: [{ autogenerate: { directory: 'aws' } }]
				},
				{
					label: 'Azure',
					items: [{ autogenerate: { directory: 'azure' } }]
				},
				{
					label: 'Google Cloud',
					items: [{ autogenerate: { directory: 'google-cloud' } }]
				},
				{
					label: 'Hybrid',
					items: [{ autogenerate: { directory: 'hybrid' } }]
				},
				{
					label: 'Guides',
					items: [
						// Each item here is one entry in the navigation menu.
						{ label: 'Example Guide', slug: 'guides/example' },
					],
				},
				{
					label: 'Reference',
					items: [{ autogenerate: { directory: 'reference' } }],
				},
			],
		}),
	],
});
