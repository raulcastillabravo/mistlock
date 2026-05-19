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
			components: {
				TableOfContents: './src/components/CustomTableOfContents.astro',
				MobileTableOfContents: './src/components/CustomMobileTableOfContents.astro',
			},
			sidebar: [
				{
					label: 'AWS',
					items: [
						{
							label: 'Services',
							translations: {
								es: 'Servicios'
							},
							items: [
								{ autogenerate: { directory: 'aws/mves' } }
							]
						},
						{
							label: 'Projects',
							translations: {
								es: 'Proyectos'
							},
							items: [
								{ autogenerate: { directory: 'aws/projects' } }
							]
						}
					]
				},
				{
					label: 'Azure',
					items: [
						{
							label: 'Services',
							translations: {
								es: 'Servicios'
							},
							items: [
								{ autogenerate: { directory: 'azure/mves' } }
							]
						},
						{
							label: 'Projects',
							translations: {
								es: 'Proyectos'
							},
							items: [
								{ autogenerate: { directory: 'azure/projects' } }
							]
						}
					]
				},
				{
					label: 'Google Cloud',
					items: [
						{
							label: 'Services',
							translations: {
								es: 'Servicios'
							},
							items: [
								{ autogenerate: { directory: 'google-cloud/mves' } }
							]
						},
						{
							label: 'Projects',
							translations: {
								es: 'Proyectos'
							},
							items: [
								{ autogenerate: { directory: 'google-cloud/projects' } }
							]
						}
					]
				},
				{
					label: 'Hybrid',
					translations: {
						es: 'Híbrido'
					},
					items: [
						{
							label: 'Services',
							translations: {
								es: 'Servicios'
							},
							items: [
								{ autogenerate: { directory: 'hybrid/mves' } }
							]
						},
						{
							label: 'Projects',
							translations: {
								es: 'Proyectos'
							},
							items: [
								{ autogenerate: { directory: 'hybrid/projects' } }
							]
						}
					]
				},
			],
		}),
	],
});
