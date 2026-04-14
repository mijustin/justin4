/* tweets.js — search, filter, and tab logic for /tweets/ index pages */
(function () {
  "use strict";

  // ── DOM refs ─────────────────────────────────────────────────────────────
  const searchInput   = document.getElementById("tw-search");
  const searchResults = document.getElementById("tw-search-results");
  const tweetList     = document.getElementById("tw-list");
  const tabs          = document.querySelectorAll(".tw-tab:not(.tw-tab-view)");
  const showRadios    = document.querySelectorAll('input[name="show"]');

  if (!searchInput) return;

  // ── State ─────────────────────────────────────────────────────────────────
  let searchIndex  = null;   // loaded lazily
  let loading      = false;
  let activeFilter = "all";  // tab filter
  let activeShow   = "all";  // show filter
  let searchActive = false;

  // ── Card filtering (tab + show, works on static HTML cards) ──────────────
  function applyFilters() {
    if (searchActive) return; // search mode overrides
    const cards = tweetList.querySelectorAll(".tw-card");
    cards.forEach(function (card) {
      const type     = card.dataset.type;
      const hasMedia = card.dataset.media === "1";
      const tabOk    = activeFilter === "all" || type === activeFilter;
      const showOk   = activeShow === "all" ||
                       (activeShow === "media" && hasMedia) ||
                       (activeShow === "text"  && !hasMedia);
      card.hidden = !(tabOk && showOk);
    });
  }

  // ── Tab clicks ────────────────────────────────────────────────────────────
  tabs.forEach(function (tab) {
    tab.addEventListener("click", function (e) {
      e.preventDefault();
      tabs.forEach(function (t) { t.classList.remove("active"); });
      tab.classList.add("active");
      activeFilter = tab.dataset.filter;
      if (!searchActive) applyFilters();
    });
  });

  // ── Show filter (radio buttons) ───────────────────────────────────────────
  showRadios.forEach(function (radio) {
    radio.addEventListener("change", function () {
      activeShow = radio.value;
      if (!searchActive) applyFilters();
    });
  });

  // ── Search index loader ───────────────────────────────────────────────────
  function loadIndex(callback) {
    if (searchIndex) { callback(); return; }
    if (loading)     { return; }
    loading = true;
    fetch("/tweets/search-index.json")
      .then(function (r) { return r.json(); })
      .then(function (data) {
        searchIndex = data;
        loading = false;
        callback();
      })
      .catch(function () { loading = false; });
  }

  // ── Render search results ─────────────────────────────────────────────────
  // Each entry in searchIndex: [id, text, date, type, has_media]
  function renderResults(query) {
    const q = query.trim().toLowerCase();

    if (!q) {
      searchResults.hidden = true;
      tweetList.hidden     = false;
      searchActive         = false;
      applyFilters();
      return;
    }

    searchActive         = true;
    tweetList.hidden     = true;
    searchResults.hidden = false;

    const words   = q.split(/\s+/);
    const matches = searchIndex.filter(function (entry) {
      const text = entry[1].toLowerCase();
      return words.every(function (w) { return text.includes(w); });
    });

    // Apply tab / show filters to results too
    const filtered = matches.filter(function (entry) {
      const type     = entry[3];
      const hasMedia = entry[4] === 1;
      const tabOk    = activeFilter === "all" || type === activeFilter;
      const showOk   = activeShow === "all" ||
                       (activeShow === "media" && hasMedia) ||
                       (activeShow === "text"  && !hasMedia);
      return tabOk && showOk;
    });

    if (!filtered.length) {
      searchResults.innerHTML =
        '<p class="tw-search-no-results">No tweets found for that search.</p>';
      return;
    }

    // Show top 200 results
    const top = filtered.slice(0, 200);
    const html = top.map(function (entry) {
      const id      = entry[0];
      const text    = entry[1].replace(/</g, "&lt;").replace(/>/g, "&gt;");
      const date    = entry[2];
      const type    = entry[3];
      const badge   = type !== "tweet"
        ? '<span class="tw-badge tw-rt" style="font-size:0.7rem;margin-right:0.3rem">'
          + type.toUpperCase() + "</span> "
        : "";
      return (
        '<div class="tw-search-result">' +
        '<p>' + badge + text + "</p>" +
        '<a href="/tweets/' + id + '/">' + date + " &rarr;</a>" +
        "</div>"
      );
    }).join("");

    searchResults.innerHTML =
      '<p class="tw-search-no-results" style="margin-bottom:0.75rem;color:#73808c">' +
      filtered.length.toLocaleString() + " tweet" + (filtered.length === 1 ? "" : "s") +
      " found" +
      (filtered.length > 200 ? " (showing first 200)" : "") +
      "</p>" + html;
  }

  // ── Search input handler ──────────────────────────────────────────────────
  let debounceTimer = null;
  searchInput.addEventListener("input", function () {
    clearTimeout(debounceTimer);
    const query = searchInput.value;
    debounceTimer = setTimeout(function () {
      if (!query.trim()) {
        renderResults("");
        return;
      }
      loadIndex(function () { renderResults(query); });
    }, 280);
  });

  // Clear on Escape
  searchInput.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      searchInput.value = "";
      renderResults("");
    }
  });

})();
