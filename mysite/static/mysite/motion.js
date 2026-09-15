// Site-wide motion. Everything here is skipped for visitors who have asked their
// device to reduce motion. Page-specific motion (the resume timeline) lives with
// its page.
(function () {
    const root = document.documentElement;
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
    const EASE_OUT = 'cubic-bezier(0.2, 0.8, 0.2, 1)';

    /* Page settles in: every time a page loads, elements marked data-enter rise
       and fade in one after another. The head script in layout.html hides them
       before the page paints, so they never flash in and back out. */
    if (root.classList.contains('will-enter')) {
        document.querySelectorAll('[data-enter]').forEach(function (el, i) {
            el.animate(
                [{ opacity: 0, transform: 'translateY(12px)' }, { opacity: 1, transform: 'none' }],
                { duration: 550, easing: EASE_OUT, delay: i * 60, fill: 'backwards' }
            );
        });
        root.classList.remove('will-enter');
    }

    /* Dark mode spreads from the button. A view transition snapshots the page,
       switches the theme, and reveals the new theme in a circle growing from the
       button, while the icon spins into its new shape. */
    const toggle = document.getElementById('theme-toggle');
    let revealStyle = null;

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

        // The circle is written in percentages of the page snapshot, not pixels.
        // Some browsers size the snapshot in device pixels, which put a pixel-based
        // circle halfway toward the top left on high-density screens and left it too
        // small to cover the page before the transition ended.
        const box = toggle.getBoundingClientRect();
        const width = window.innerWidth;
        const height = window.innerHeight;
        const x = box.left + box.width / 2;
        const y = box.top + box.height / 2;
        const center = (x / width * 100).toFixed(3) + '% ' + (y / height * 100).toFixed(3) + '%';
        // Reach the farthest corner. A percentage radius is measured against the
        // snapshot's diagonal divided by the square root of 2.
        const farthest = Math.hypot(Math.max(x, width - x), Math.max(y, height - y));
        const radius = (farthest / (Math.hypot(width, height) / Math.SQRT2) * 100 + 1).toFixed(3) + '%';

        if (!revealStyle) {
            revealStyle = document.createElement('style');
            document.head.appendChild(revealStyle);
        }
        revealStyle.textContent =
            '@keyframes theme-reveal {' +
            ' from { clip-path: circle(0% at ' + center + '); }' +
            ' to { clip-path: circle(' + radius + ' at ' + center + '); } }';

        // While switching, color transitions pause so the new theme is already
        // settled inside the circle; the icon keeps its spin.
        root.classList.add('theme-switching');
        const transition = document.startViewTransition(function () { applyTheme(next); });
        transition.finished.finally(function () { root.classList.remove('theme-switching'); });
    });
    updateLabel();

    /* Nav highlight slides between pages: arriving from another link in the nav,
       the highlight slides over from that link. It runs in the page itself rather
       than as a browser page transition, because some Chromium browsers (Arc, for
       one) report a page transition without showing it. */
    const navLinks = Array.from(document.querySelectorAll('.site-links a'));
    const pill = document.querySelector('.nav-pill');
    const here = navLinks.findIndex(link => link.hasAttribute('aria-current'));

    navLinks.forEach(function (link) {
        link.addEventListener('click', function () {
            try { sessionStorage.setItem('nav-from', String(here)); } catch (e) {}
        });
    });

    let cameFrom = -1;
    try {
        cameFrom = Number(sessionStorage.getItem('nav-from') ?? -1);
        sessionStorage.removeItem('nav-from');
    } catch (e) {}

    if (pill && cameFrom >= 0 && cameFrom !== here && navLinks[cameFrom] && !reduceMotion.matches) {
        const from = navLinks[cameFrom].getBoundingClientRect();
        const to = pill.parentElement.getBoundingClientRect();
        pill.animate(
            [
                { left: (from.left - to.left) + 'px', right: (to.right - from.right) + 'px' },
                { left: '0px', right: '0px' }
            ],
            { duration: 420, easing: 'cubic-bezier(0.3, 1.3, 0.5, 1)', fill: 'backwards' }
        );
    }

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
