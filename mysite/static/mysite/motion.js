// Site-wide motion. Everything here is skipped for visitors who have asked their
// device to reduce motion. Page-specific motion (the resume timeline) lives with
// its page.
(function () {
    const root = document.documentElement;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const EASE_OUT = 'cubic-bezier(0.2, 0.8, 0.2, 1)';

    /* Page settles in: on the first page of a visit, elements marked data-enter
       rise and fade in one after another. The head script in layout.html hides
       them before the page paints, so they never flash in and back out. */
    if (root.classList.contains('will-enter')) {
        document.querySelectorAll('[data-enter]').forEach(function (el, i) {
            el.animate(
                [{ opacity: 0, transform: 'translateY(12px)' }, { opacity: 1, transform: 'none' }],
                { duration: 550, easing: EASE_OUT, delay: i * 60, fill: 'backwards' }
            );
        });
        root.classList.remove('will-enter');
        try { sessionStorage.setItem('entered', '1'); } catch (e) {}
    }

    /* Dark mode spreads from the button. A view transition snapshots the page,
       switches the theme, and reveals the new theme in a growing circle centered
       on the button. The circle is a CSS animation (theme-reveal in styles.css),
       so it starts from the button on the first frame. */
    const toggle = document.getElementById('theme-toggle');

    function updateLabel() {
        const label = root.dataset.theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
        toggle.setAttribute('aria-label', label);
        toggle.title = label;
    }

    function applyTheme(theme) {
        root.dataset.theme = theme;
        try { localStorage.setItem('theme', theme); } catch (e) {}
        updateLabel();
    }

    toggle.addEventListener('click', function () {
        const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
        if (!document.startViewTransition || reduceMotion.matches) {
            applyTheme(next);
            return;
        }

        const box = toggle.getBoundingClientRect();
        const x = box.left + box.width / 2;
        const y = box.top + box.height / 2;
        // Far enough to cover the farthest corner of the window.
        const radius = Math.hypot(Math.max(x, window.innerWidth - x), Math.max(y, window.innerHeight - y));
        root.style.setProperty('--reveal-x', x + 'px');
        root.style.setProperty('--reveal-y', y + 'px');
        root.style.setProperty('--reveal-r', Math.ceil(radius) + 'px');

        // While switching, color transitions are paused so the new theme is
        // already settled inside the circle instead of fading as it spreads.
        root.classList.add('theme-switching');
        const transition = document.startViewTransition(function () { applyTheme(next); });
        transition.finished.finally(function () { root.classList.remove('theme-switching'); });
    });
    updateLabel();

    /* Cards glide into place when the homepage switches between one and two
       columns. Positions are measured relative to the grid, so scrolling or the
       header changing height between resizes doesn't throw them off. */
    const grid = document.querySelector('.home-grid');
    if (grid && 'ResizeObserver' in window) {
        const items = [grid.querySelector('.prose')].concat(Array.from(grid.querySelectorAll('.home-side > *')));
        const columnCount = () => getComputedStyle(grid).gridTemplateColumns.split(' ').length;
        const measure = function () {
            const origin = grid.getBoundingClientRect();
            return new Map(items.map(function (el) {
                const box = el.getBoundingClientRect();
                return [el, { left: box.left - origin.left, top: box.top - origin.top }];
            }));
        };

        let lastColumns = columnCount();
        let lastPositions = measure();

        new ResizeObserver(function () {
            const columns = columnCount();
            const positions = measure();
            if (columns !== lastColumns && !reduceMotion.matches) {
                items.forEach(function (el, i) {
                    const before = lastPositions.get(el);
                    const after = positions.get(el);
                    el.animate(
                        [{ transform: 'translate(' + (before.left - after.left) + 'px, ' + (before.top - after.top) + 'px)' }, { transform: 'none' }],
                        { duration: 460, easing: EASE_OUT, delay: i * 30, fill: 'backwards' }
                    );
                });
            }
            lastColumns = columns;
            lastPositions = positions;
        }).observe(grid);
    }
})();
