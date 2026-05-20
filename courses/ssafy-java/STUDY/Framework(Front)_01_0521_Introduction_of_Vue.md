# Vue 3 입문 — 선언형 UI 와 반응성

> **이 강의는 무엇인가**: Vue.js 3 의 핵심 — 반응형 데이터(`ref`/`reactive`), 컴포넌트, 디렉티브(`v-if`/`v-for`/`v-bind`/`v-model`), computed/watch, Composition API.
> **왜 배우는가**: REST API 를 직접 호출해 SPA 만드는 경험. 백엔드만으론 현대 웹의 절반.

---

## 들어가기 전에

- **선수**: HTML/CSS/JS ES6+.
- **환경**: Node 18+, `npm create vue@latest`.

---

## 핵심 개념

### 1. 반응성 — 왜 Vue

```vue
<template>
  <button @click="count++">{{ count }}</button>
</template>
<script setup>
import { ref } from 'vue';
const count = ref(0);
</script>
```

`count.value` 가 바뀌면 화면 자동 갱신. Vue 가 의존성 추적해서 DOM 최소 변경만.

### 2. `ref` vs `reactive`

```js
import { ref, reactive } from 'vue';
const count = ref(0);                    // 단일 값 (.value)
const state = reactive({ name: 'lee' });  // 객체 (그대로 접근)
```

**가이드**: 단일=ref, 객체=reactive. 단순함을 위해 ref 만 써도 OK.

### 3. 디렉티브

```vue
<p>{{ message }}</p>                              <!-- 보간 -->
<a :href="url">링크</a>                            <!-- v-bind 단축 -->
<button @click="onClick">클릭</button>             <!-- v-on 단축 -->
<input v-model="name"/>                            <!-- 양방향 -->

<p v-if="loggedIn">환영</p>
<p v-else-if="loading">로딩</p>
<p v-else>로그인 필요</p>

<li v-for="item in items" :key="item.id">{{ item.name }}</li>

<div :class="{ active: isActive, disabled: !enabled }"></div>
```

> 💡 `v-for` 에 `:key` 필수.

### 4. Computed

```js
const items = ref([{price:1000}, {price:2000}]);
const total = computed(() => items.value.reduce((s, i) => s + i.price, 0));
```

의존성 변경 시만 재계산, 캐싱.

### 5. Watch

```js
watch(count, (newVal, oldVal) => console.log(`${oldVal} → ${newVal}`));
```

vs computed: 새 값 만들기=computed, 외부 호출(fetch, localStorage)=watch.

### 6. 컴포넌트

```vue
<!-- BoardItem.vue -->
<template>
  <article>
    <h3>{{ board.title }}</h3>
    <button @click="$emit('delete', board.id)">삭제</button>
  </article>
</template>
<script setup>
defineProps({ board: { type: Object, required: true } });
defineEmits(['delete']);
</script>
```

```vue
<!-- 부모 -->
<BoardItem v-for="b in boards" :key="b.id" :board="b" @delete="onDelete"/>
```

**Props down, events up** — 부모→자식 props, 자식→부모 emit. 단방향 데이터 흐름.

### 7. 라이프사이클

```js
import { onMounted, onUnmounted } from 'vue';
onMounted(() => fetchData());
onUnmounted(() => { /* 정리 */ });
```

### 8. 백엔드 호출

```js
const boards = ref([]);
onMounted(async () => {
    const res = await fetch('/api/boards');
    boards.value = await res.json();
});
```

또는 `axios`. CORS 는 백엔드(Spring) 에서.

---

## 코드 깊게 들여다보기

게시판 목록 + 검색 + 삭제:

```vue
<template>
  <div>
    <input v-model="keyword" @keyup.enter="search" placeholder="검색"/>
    <button @click="search">검색</button>

    <p v-if="loading">로딩…</p>
    <p v-else-if="boards.length === 0">결과 없음</p>

    <ul v-else>
      <li v-for="b in boards" :key="b.id">
        <span>{{ b.title }}</span>
        <small>by {{ b.writer }} · {{ formatDate(b.createdAt) }}</small>
        <button @click="remove(b.id)">삭제</button>
      </li>
    </ul>

    <p>총 {{ totalCount }}건</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const keyword = ref('');
const boards = ref([]);
const loading = ref(false);
const totalCount = computed(() => boards.value.length);

async function search() {
  loading.value = true;
  try {
    const res = await fetch(`/api/boards?keyword=${encodeURIComponent(keyword.value)}`);
    boards.value = await res.json();
  } finally {
    loading.value = false;
  }
}

async function remove(id) {
  if (!confirm('삭제할까요?')) return;
  await fetch(`/api/boards/${id}`, { method: 'DELETE' });
  boards.value = boards.value.filter(b => b.id !== id);
}

function formatDate(iso) {
  return new Date(iso).toLocaleString('ko-KR', { dateStyle: 'short', timeStyle: 'short' });
}

onMounted(search);
</script>
```

핵심: `ref` 상태, `computed` 파생, `onMounted` 초기 로드, `v-model` 양방향, `v-if/else`, `v-for + :key`, `@click`/`@keyup.enter`.

---

## 실전 패턴 / 자주 빠지는 함정

- ❌ `v-for` 에 `:key` 빠뜨림 → 성능 + 상태 꼬임.
- ❌ 스크립트에서 `count` 직접 접근 (`count.value` 필요).
- ❌ `reactive` 객체 destructure → 반응성 깨짐.
  ✅ `toRefs`.
- ❌ 자식이 props 직접 수정 → 단방향 위반.
  ✅ emit.
- ❌ fetch 한 데이터를 watch 로 다시 fetch → 무한 루프.
- ❌ 일반 `let x = 0` → 화면 안 바뀜.

---

## 다음 강의로 가기 전 자가점검

1. `ref` vs `reactive` 사용 기준?
2. `computed` vs `watch` 차이?
3. `v-for` 에 `:key` 안 주면?
4. 부모→자식 데이터, 자식→부모 알림 방법?

<details><summary>풀이</summary>

1. 단일 값=ref, 객체 묶음=reactive.
2. computed=의존성으로 새 값+캐싱, watch=변화 감지 사이드 이펙트.
3. Vue 가 DOM 재사용 키 못 정함 → 위치만 보고 매칭 → 인풋 입력값이 다른 행으로 옮겨가는 등 상태 꼬임.
4. props(부모→자식), emit(자식→부모).

</details>

---

## 슬라이드 ↔ 노트 매핑

| 슬라이드 | 노트 섹션 |
|--|--|
| p.1~5 표지·왜 Vue | §1 |
| p.6~12 ref/reactive | §2 |
| p.13~22 디렉티브 | §3 |
| p.23~30 computed/watch | §4, §5 |
| p.31~38 컴포넌트·라이프 | §6, §7 |
| p.39~41 백엔드 호출 | §8, 코드 |

_단독 학습 가능 노트._
