import { siteConfig } from "../config";

// Caching with a Promise prevents race conditions when Astro parallelizes page rendering:
// all callers await the same in-flight request instead of each firing their own fetch.
let pending: Promise<string> | null = null;

export function getGithubStars(): Promise<string> {
	if (pending) return pending;

	pending = (async () => {
		try {
			const res = await fetch(siteConfig.githubApiUrl, {
				headers: { "User-Agent": "Astro-Build-Client" },
			});
			if (!res.ok) throw new Error(`GitHub API ${res.status}`);
			const data = await res.json();
			const count: number = data.stargazers_count;
			return count > 999 ? (count / 1000).toFixed(1) + "k" : String(count);
		} catch {
			return "–";
		}
	})();

	return pending;
}
