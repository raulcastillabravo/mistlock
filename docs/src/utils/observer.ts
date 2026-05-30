export function observeEntrance(selector: string, threshold = 0.1) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold }
  );
  document.querySelectorAll(selector).forEach((el) => observer.observe(el));
}
