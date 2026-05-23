import { siteConfig } from "../config";

let cachedStarCount: string | null = null;

export async function getGithubStars(): Promise<string> {
	if (cachedStarCount) return cachedStarCount;

	const res = await fetch(siteConfig.githubApiUrl, {
		headers: { "User-Agent": "Astro-Build-Client" },
	});

	if (!res.ok) {
		throw new Error(
			`GitHub API returned ${res.status} for ${siteConfig.githubApiUrl}`,
		);
	}

	const data = await res.json();
	const count: number = data.stargazers_count;
	cachedStarCount =
		count > 999 ? (count / 1000).toFixed(1) + "k" : String(count);
	return cachedStarCount;
}
