# Vue 3 입문 — 치트시트

> 41p 슬라이드 · Composition API + `<script setup>` 기반.
> **TL;DR** → **Quick Reference** → **Mind Map** 3 섹션.

---

# 1. TL;DR (5분 요약)

## 핵심 6줄
1. **반응성**: `ref` / `reactive` 가 Proxy 로 감싸져 값 변경 시 DOM 자동 갱신
2. **스크립트는 `count.value`**, 템플릿은 `{{ count }}` (자동 unwrap)
3. **`computed`** (캐싱) vs **`watch`** (사이드 이펙트) - 새 값=computed, fetch=watch
4. **Props down, events up**: 부모→자식 `:board="b"`, 자식→부모 `@delete="..."` + `$emit('delete', id)`
5. **`v-for` 에 `:key` 필수**, `v-model` 양방향, `v-if/else` 조건
6. **onMounted** 에서 초기 fetch, **onUnmounted** 에서 자원 정리

## 가장 중요한 코드 3개

```vue
<!-- (1) 기본 컴포넌트 (Composition API) -->
<template>
  <div>
    <input v-model="keyword" @keyup.enter="search"/>
    <p v-if="loading">로딩...</p>
    <ul v-else>
      <li v-for="b in boards" :key="b.id">
        {{ b.title }} (총 {{ total }}개)
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';

const keyword = ref('');
const boards = ref([]);
const loading = ref(false);
const total = computed(() => boards.value.length);

async function search() {
  loading.value = true;
  try {
    const res = await fetch(`/api/boards?keyword=${encodeURIComponent(keyword.value)}`);
    boards.value = await res.json();
  } finally {
    loading.value = false;
  }
}

onMounted(search);
</script>
```

```vue
<!-- (2) Props + Emit (부모 / 자식) -->
<!-- BoardItem.vue (자식) -->
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

<!-- 부모 -->
<BoardItem v-for="b in boards" :key="b.id" :board="b" @delete="onDelete"/>
```

```vue
<!-- (3) computed + watch -->
<script setup>
import { ref, computed, watch } from 'vue';

const items = ref([{ price: 1000 }, { price: 2000 }]);
const total = computed(() => items.value.reduce((s, i) => s + i.price, 0));

const userId = ref(1);
watch(userId, async (newId) => {
  const res = await fetch(`/api/users/${newId}`);
  user.value = await res.json();
});
</script>
```

## 면접 한 줄 답변
- **Vue 의 반응성?** → Proxy 로 `ref/reactive` 변수를 감싸 변경 감지 → DOM 자동 갱신. 선언형 UI.
- **`ref` vs `reactive`?** → 단일 값 ref (`.value`), 객체 reactive. 일관성 위해 ref 통일도 OK.
- **`v-for :key` 안 주면?** → 위치 기반 매칭 → 정렬 시 input 값이 다른 행으로 옮겨짐.
- **Vue vs React?** → Vue: Proxy 반응성 (자연스러움), React: 명시적 setState. SSAFY 는 Vue (한국 인기 + Spring 조합).

---

# 2. Quick Reference (실무 복붙)

## 반응성 (Reactivity)

```js
import { ref, reactive } from 'vue';

// ref - 단일 값 (모든 타입)
const count = ref(0);
count.value++;                    // 스크립트
// 템플릿: {{ count }}             자동 unwrap

// reactive - 객체만
const state = reactive({ name: 'lee', age: 20 });
state.age++;                      // .value 없음
// destructure 시 반응성 깨짐 -> toRefs(state)
```

## 디렉티브

```vue
<!-- 보간 -->
<h1>{{ title }}</h1>

<!-- bind -->
<a :href="url" :class="{ active: isActive }">링크</a>

<!-- on -->
<button @click="onClick" @keyup.enter="search">클릭</button>

<!-- model (양방향) -->
<input v-model="name"/>
<input v-model.number="age"/>
<input v-model.trim="email"/>

<!-- if / else -->
<p v-if="loggedIn">환영</p>
<p v-else-if="loading">로딩</p>
<p v-else>로그인 필요</p>

<!-- show (display:none 토글) -->
<p v-show="visible">보임</p>

<!-- for -->
<li v-for="(item, index) in items" :key="item.id">
  {{ index }} : {{ item.name }}
</li>

<!-- 이벤트 수정자 -->
<form @submit.prevent="onSubmit">
<button @click.stop>      <!-- stopPropagation -->
<a @click.once>           <!-- 한 번만 -->
```

## computed vs watch

```js
import { computed, watch, watchEffect } from 'vue';

// computed - 의존성 캐싱
const total = computed(() => items.value.reduce((s, i) => s + i.price, 0));

// watch - 변경 감지 사이드 이펙트
watch(userId, async (newId, oldId) => {
  user.value = await fetch(`/api/users/${newId}`).then(r => r.json());
});

// 여러 소스
watch([userId, filter], ([id, f]) => { ... });

// 즉시 실행
watch(userId, fetchUser, { immediate: true });

// watchEffect (자동 의존성 추적)
watchEffect(async () => {
  user.value = await fetch(`/api/users/${userId.value}`).then(r => r.json());
});
```

## Composition API + `<script setup>`

```vue
<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue';

// 1. 반응형 상태
const count = ref(0);

// 2. 계산값
const double = computed(() => count.value * 2);

// 3. 함수
function increment() {
  count.value++;
}

// 4. 라이프사이클
onMounted(() => console.log('마운트'));
onUnmounted(() => console.log('언마운트'));

// 5. Props / Emits
const props = defineProps({ msg: String });
const emit = defineEmits(['update', 'delete']);
</script>
```

## Props + Emits

```vue
<!-- 자식 -->
<script setup>
const props = defineProps({
  board: { type: Object, required: true },
  count: { type: Number, default: 0 }
});

const emit = defineEmits(['delete', 'update:modelValue']);

function remove() {
  emit('delete', props.board.id);
}
</script>

<!-- 부모 -->
<BoardItem :board="b" :count="10" @delete="onDelete"/>
```

## v-model (양방향) 내부 동작

```vue
<!-- 설탕 문법 -->
<input v-model="name"/>

<!-- 동등 -->
<input :value="name" @input="name = $event.target.value"/>

<!-- 커스텀 컴포넌트 -->
<!-- MyInput.vue -->
<input :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"/>

<!-- 부모 -->
<MyInput v-model="text"/>
```

## 라이프사이클 훅

```js
onBeforeMount(() => {})       // 마운트 직전
onMounted(() => {})            // 마운트 후 (DOM 접근, 초기 fetch)
onBeforeUpdate(() => {})
onUpdated(() => {})            // 재렌더 후
onBeforeUnmount(() => {})      // 언마운트 직전 (이벤트 정리, 타이머 clearInterval)
onUnmounted(() => {})

// 자주 쓰는 패턴
let intervalId;
onMounted(() => {
  fetchData();
  intervalId = setInterval(fetchData, 30000);
});
onUnmounted(() => clearInterval(intervalId));
```

## fetch + 에러 처리

```vue
<script setup>
import { ref, onMounted } from 'vue';

const boards = ref([]);
const loading = ref(false);
const error = ref(null);

async function fetchBoards() {
  loading.value = true;
  error.value = null;
  try {
    const res = await fetch('/api/boards', { credentials: 'include' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    boards.value = await res.json();
  } catch (e) {
    error.value = e.message;
  } finally {
    loading.value = false;
  }
}

onMounted(fetchBoards);
</script>
```

## CORS 해결

```js
// vite.config.js (개발)
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      }
    }
  }
});

// 그러면 Vue 에서 /api/boards 호출 -> Vite 가 백엔드로 프록시
```

## reactive destructure 함정

```js
// 안 좋은 예
const state = reactive({ name: 'lee', age: 20 });
const { name, age } = state;     // 반응성 깨짐

state.age = 30;                   // state.age 만 30, age 는 그대로 20

// 좋은 예
import { toRefs } from 'vue';
const { name, age } = toRefs(state);
name.value;                       // 이제 ref
age.value;
```

## composable 패턴 (재사용)

```js
// composables/useUser.js
import { ref, onMounted } from 'vue';

export function useUser(id) {
  const user = ref(null);
  const loading = ref(false);

  async function load() {
    loading.value = true;
    user.value = await fetch(`/api/users/${id}`).then(r => r.json());
    loading.value = false;
  }

  onMounted(load);
  return { user, loading, reload: load };
}

// 컴포넌트에서
<script setup>
const { user, loading, reload } = useUser(1);
</script>
```

## 자주 빠지는 함정

| 함정 | 해결 |
|--|--|
| `console.log(count)` → `RefImpl` | `count.value` |
| `v-for :key` 누락 | 고유 id |
| `reactive` destructure | `toRefs` |
| props 직접 수정 | emit 으로 부모에게 |
| watch 안에서 watch 대상 수정 | 무한 루프 |
| fetch 한 데이터를 onMounted + watch 같이 | 한 곳만 |
| CORS 에러 | Vite proxy 또는 Spring CORS |
| `${...}` 대신 `{{...}}` | Vue 는 `{{ }}` |

---

# 3. Mind Map (전체 구조 + 체크리스트)

## 전체 토픽 트리

```
Vue 3 입문 (41p)
│
├── [A] 반응성
│   ├── ref (.value)
│   ├── reactive (객체)
│   ├── Proxy 기반
│   └── toRefs / toRef
│
├── [B] 디렉티브
│   ├── {{ }} 보간
│   ├── v-bind / :
│   ├── v-on / @
│   ├── v-model (양방향)
│   ├── v-if / v-else-if / v-else
│   ├── v-show
│   └── v-for + :key
│
├── [C] Composition API
│   ├── <script setup>
│   ├── ref / reactive / computed / watch
│   ├── defineProps / defineEmits
│   └── composable 함수
│
├── [D] 컴포넌트
│   ├── 정의 + import
│   ├── props (부모 -> 자식)
│   ├── emits (자식 -> 부모)
│   ├── slot
│   └── 단방향 데이터 흐름
│
├── [E] 라이프사이클
│   ├── onMounted
│   ├── onUnmounted
│   ├── onUpdated
│   └── DOM 접근·자원 정리
│
├── [F] 비동기
│   ├── fetch / axios
│   ├── loading / error 상태
│   ├── credentials: include
│   └── CORS
│
└── [G] 도구
    ├── Vite (빌드)
    ├── Vue Router
    ├── Pinia (상태 관리)
    └── DevTools 브라우저 확장
```

## 학습 진도 체크리스트

### A. 반응성
- [ ] ref vs reactive 차이
- [ ] .value 의 의미
- [ ] toRefs 사용

### B. 디렉티브
- [ ] v-bind / v-on 단축 (`:`, `@`)
- [ ] v-model 양방향
- [ ] v-if vs v-show
- [ ] v-for + :key

### C. Composition
- [ ] computed vs watch
- [ ] defineProps / defineEmits
- [ ] composable 패턴

### D. 컴포넌트
- [ ] Props down, events up
- [ ] slot
- [ ] 단방향 데이터 흐름의 이점

### E. 비동기
- [ ] onMounted 초기 fetch
- [ ] loading / error 상태
- [ ] CORS (Vite proxy 또는 Spring)

## 연관 강의

```
Framework Back 12강 REST API    -> API 서버
Framework Back 14강 CORS PJT    -> CORS 설정
Framework Front 1강 Vue          <- 현재 위치
```

→ 다음 (패턴 매칭) 에서 **알고리즘 PJT**.
