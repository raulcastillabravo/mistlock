// @ts-check
import { defineConfig } from 'astro/config';
import starlight from '@astrojs/starlight';
import sitemap from '@astrojs/sitemap';
import icon from 'astro-icon';

import tailwindcss from '@tailwindcss/vite';

// https://astro.build/config
export default defineConfig({
    site: 'https://raulcastillabravo.github.io',
    base: '/mve-collection/',
    integrations: [
        icon(),
        sitemap(),
        starlight({
            title: 'MistLock',
            logo: {
                src: './src/assets/mistlock.svg',
                alt: 'MistLock',
            },
            customCss: ['./src/styles/global.css'],
            social: [
                { icon: 'linkedin', label: 'LinkedIn', href: 'https://www.linkedin.com/in/raulcastillabravo/' },

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
                Hero: './src/components/Hero.astro',
                TableOfContents: './src/components/CustomTableOfContents.astro',
                MobileTableOfContents: './src/components/CustomMobileTableOfContents.astro',
                ThemeSelect: './src/components/ThemeSelect.astro',
                Header: './src/components/Header.astro',
                SocialIcons: './src/components/SocialIcons.astro',
                MobileMenuFooter: './src/components/MobileMenuFooter.astro',
            },
            sidebar: [
                {
                    label: 'Start Here',
                    translations: {
                        es: 'Empieza aquí',
                    },
                    items: [
                        {
                            label: 'Getting Started',
                            translations: {
                                es: 'Empezando',
                            },
                            link: '/start-here/getting-started/',
                        },
                        {
                            label: 'Catalog',
                            translations: {
                                es: 'Catálogo de ejemplos',
                            },
                            link: '/start-here/catalog/',
                        },
                    ],
                },
                {
                    label: 'AWS',
                    collapsed: true,
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
                    collapsed: true,
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
                    collapsed: true,
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
                    collapsed: true,
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
    vite: { plugins: [tailwindcss()] },
});