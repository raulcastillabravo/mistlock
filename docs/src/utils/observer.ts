export function observeEntrance(
  selector: string,
  threshold = 0.1,
  container: Element | Document = document
) {
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
  container.querySelectorAll(selector).forEach((el) => observer.observe(el));
}
