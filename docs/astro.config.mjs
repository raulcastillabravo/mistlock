// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';

// https://astro.build/config
export default defineConfig({
	site: 'https://raulcastillabravo.github.io',
	base: '/mve-collection/',
	integrations: [
		starlight({
			title: 'Cloud Local Lab',
			social: [
				{ icon: 'github', label: 'GitHub', href: 'https://github.com/raulcastillabravo/mve-collection' },
				{ icon: 'linkedin', label: 'LinkedIn', href: 'https://www.linkedin.com/in/raulcastillabravo/' }
			],
			locales: {
				root: {
					label: 'English',
					lang: 'en',
				},
				es: {
					label: 'Español',
					lang: 'es',
				},
			},
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
					translations: {
						es: 'Híbrido'
					},
					items: [{ autogenerate: { directory: 'hybrid' } }]
				},
				{
					label: 'Guides',
					translations: {
						es: 'Guías'
					},
					items: [
						{ 
							label: 'Example Guide', 
							translations: { es: 'Guía de ejemplo' },
							slug: 'guides/example' 
						},
					],
				},
				{
					label: 'Reference',
					translations: {
						es: 'Referencia'
					},
					items: [{ autogenerate: { directory: 'reference' } }],
				},
			],
		}),
	],
});
