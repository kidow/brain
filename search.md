---
layout: search
permalink: /search/
title: 문서 검색
---

<script id="document-sources" type="application/json">[
{% assign first_source = true %}{% for group in site.data.notes_order %}{% for item in group.items %}{% unless first_source %},{% endunless %}{"type":"note","title":{{ item.title | jsonify }},"url":{{ item.path | prepend: '/' | jsonify }}}{% assign first_source = false %}{% endfor %}{% endfor %}{% for item in site.static_files %}{% if item.path contains '/sheets/' or item.path contains '/drills/' %}{% assign extension = item.extname | downcase %}{% if extension == '.html' or extension == '.json' %}{% unless first_source %},{% endunless %}{% assign source_title = item.name | remove: extension | replace: '_', ' ' %}{% if item.path contains '/sheets/' %}{% assign source_type = 'sheet' %}{% elsif extension == '.json' %}{% assign source_type = 'drill-data' %}{% else %}{% assign source_type = 'drill' %}{% endif %}{"type":{{ source_type | jsonify }},"title":{{ source_title | jsonify }},"url":{{ item.path | jsonify }}}{% assign first_source = false %}{% endif %}{% endif %}{% endfor %}
]</script>

<main class="search-page" aria-labelledby="search-title">
  <p class="eyebrow">brain</p>
  <h1 id="search-title">문서 검색</h1>
  <p class="description">노트, 치트시트, 드릴을 제목과 본문에서 찾습니다.</p>

  <form id="search-form" class="search-form" role="search">
    <label class="sr-only" for="search-input">검색어</label>
    <input id="search-input" name="q" type="search" autocomplete="off" placeholder="검색어 입력" spellcheck="false">
    <button type="submit">검색</button>
  </form>

  <div class="search-controls">
    <div class="filters" aria-label="문서 유형 필터">
      <button type="button" class="filter is-active" data-filter="all" aria-pressed="true">전체</button>
      <button type="button" class="filter" data-filter="note" aria-pressed="false">노트</button>
      <button type="button" class="filter" data-filter="sheet" aria-pressed="false">치트시트</button>
      <button type="button" class="filter" data-filter="drill" aria-pressed="false">드릴</button>
    </div>
    <p id="search-status" class="status" role="status">검색 인덱스를 준비하고 있습니다.</p>
  </div>

  <ol id="search-results" class="results" aria-live="polite"></ol>
</main>

<script src="{{ '/assets/js/search.js' | relative_url }}" defer></script>
