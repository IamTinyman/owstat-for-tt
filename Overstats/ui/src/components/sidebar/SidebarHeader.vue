<template>
  <div class="sidebar-head">
    <div class="brand">
      <svg class="brand-icon" width="28" height="28" viewBox="0 0 28 28" fill="none">
        <rect x="2" y="2" width="24" height="24" rx="6" stroke="var(--accent)" stroke-width="1.5" opacity="0.5"/>
        <rect x="7" y="7" width="14" height="14" rx="3" stroke="var(--accent)" stroke-width="1.5"/>
        <circle cx="14" cy="14" r="3" fill="var(--accent)" opacity="0.7"/>
      </svg>
      <div>
        <p class="brand-sub">Overwatch Data</p>
        <h1>数据查询</h1>
      </div>
    </div>
    <p class="sidebar-copy">这是Tinyman（小笨蛋）给潼潼宝宝（小坏蛋）做的独享查询网站</p>
  </div>
</template>

<style scoped>
.sidebar-head { padding-bottom: 4px; }

.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.brand-icon { flex-shrink: 0; }

.brand-sub {
  margin: 0;
  font-size: 0.68rem;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: var(--text-muted);
  font-weight: 500;
}

.brand h1 {
  margin: 2px 0 0;
  font-size: 1.5rem;
  line-height: 1.15;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.01em;
}

.sidebar-copy {
  margin: 0;
  color: var(--text-muted);
  line-height: 1.6;
  font-size: 0.82rem;
}
</style>
