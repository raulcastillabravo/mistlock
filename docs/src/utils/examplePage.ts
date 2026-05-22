import { siteConfig } from '../config';

export function getExamplePageData(
  id: string,
  entry: { data: { isExample?: boolean } }
) {
  const isEs = id.startsWith('es/');
  const cleanId = id.replace(/^es\//, '');
  const pathParts = cleanId.split('/');
  const isExamplePage = !!entry.data.isExample;

  let zipUrl = '';
  let githubUrl = '';
  if (isExamplePage) {
    zipUrl = `/${siteConfig.repositoryName}/downloads/${pathParts.join('-')}.zip`;
    githubUrl = `${siteConfig.githubUrl}/tree/main/src/${cleanId}`;
  }

  const btnDownloadText = isEs ? 'Descargar código' : 'Download code';
  const btnGithubText = isEs ? 'Ver en GitHub' : 'View on GitHub';

  return { isExamplePage, zipUrl, githubUrl, btnDownloadText, btnGithubText };
}
