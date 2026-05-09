/**
 * Wires up a search input to the /search?q= endpoint.
 * Keyboard navigable, closes on outside click.
 * @param {string} inputId
 * @param {string} listId
 * @returns {void}
 */
function initAutocomplete(inputId, listId) {
    const input = document.getElementById(inputId);
    const list = document.getElementById(listId);

    if (!input || !list) return;

    let results = [];
    let activeIdx = -1;
    let debounce = null;

    async function fetchResults(q) {
        if (q.length < 2) { close(); return; }
        try {
            const res = await fetch(`/search?q=${encodeURIComponent(q)}`);
            results = await res.json();
            activeIdx = -1;
            render();
        } catch {
            close();
        }
    }

    function render() {
        if (!results.length) { close(); return; }

        list.innerHTML = results.map((p, i) => `
      <li
        class="autocomplete-list__item"
        role="option"
        data-idx="${i}"
        data-name="${escHtml(p.name)}"
      >
        <span>${escHtml(p.name)}</span>
        <span class="autocomplete-list__year">${p.birthYear ?? '—'}</span>
      </li>
    `).join('');

        list.classList.add('is-open');

        list.querySelectorAll('.autocomplete-list__item').forEach(el => {
            el.addEventListener('mousedown', e => {
                e.preventDefault(); // prevent blur firing
                select(parseInt(el.dataset.idx));
            });
        });
    }

    function select(idx) {
        if (!results[idx]) return;
        input.value = results[idx].name;
        close();
    }

    function close() {
        list.classList.remove('is-open');
        list.innerHTML = '';
        results = [];
        activeIdx = -1;
    }

    function setActive(idx) {
        const items = list.querySelectorAll('.autocomplete-list__item');
        items.forEach(el => el.classList.remove('is-active'));
        if (idx >= 0 && idx < items.length) {
            items[idx].classList.add('is-active');
            activeIdx = idx;
        }
    }

    input.addEventListener('input', () => {
        clearTimeout(debounce);
        debounce = setTimeout(() => fetchResults(input.value.trim()), 220);
    });

    input.addEventListener('keydown', e => {
        const items = list.querySelectorAll('.autocomplete-list__item');
        if (!items.length) return;

        if (e.key === 'ArrowDown') {
            e.preventDefault();
            setActive(Math.min(activeIdx + 1, items.length - 1));
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            setActive(Math.max(activeIdx - 1, 0));
        } else if (e.key === 'Enter' && activeIdx >= 0) {
            e.preventDefault();
            select(activeIdx);
        } else if (e.key === 'Escape') {
            close();
        }
    });

    input.addEventListener('blur', () => {
        setTimeout(close, 150);
    });

    document.addEventListener('click', e => {
        if (!input.contains(e.target) && !list.contains(e.target)) close();
    });

    function escHtml(str) {
        return String(str)
            .replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }
}