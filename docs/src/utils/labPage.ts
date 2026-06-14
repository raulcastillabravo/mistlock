import { siteConfig } from '../config';

export function getLabPageData(
  id: string,
  entry: { data: { isLab?: boolean } }
) {
  const isEs = id.startsWith('es/');
  const cleanId = id.replace(/^es\//, '');
  const pathParts = cleanId.split('/');
  const isLabPage = !!entry.data.isLab;

  let zipUrl = '';
  let githubUrl = '';
  if (isLabPage) {
    zipUrl = `/downloads/${pathParts.join('-')}.zip`;
    githubUrl = `${siteConfig.githubUrl}/tree/main/src/${cleanId}`;
  }

  const btnDownloadText = isEs ? 'Descargar código' : 'Download code';
  const btnGithubText = isEs ? 'Ver en GitHub' : 'View on GitHub';

  return { isLabPage, labId: cleanId, zipUrl, githubUrl, btnDownloadText, btnGithubText };
}
