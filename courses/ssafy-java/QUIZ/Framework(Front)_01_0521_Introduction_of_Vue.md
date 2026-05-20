# Vue 3 입문 - 퀴즈

> 14문항. 개념·적용·디버그·면접. Composition API + `<script setup>` 기준.

---

### Q1. (개념) Vue 의 "반응성 (Reactivity)" 이란? 일반 자바스크립트 변수와 어떻게 다른가?

<details><summary>정답</summary>

**반응성**: 값이 바뀌면 그 값을 사용하는 화면도 **자동으로** 다시 그려지는 것.

**일반 JS (반응성 없음)**:
```js
let count = 0;
document.querySelector('#cnt').innerText = count;
count++;     // 값은 1 이지만 화면은 0 그대로 (innerText 다시 안 함)
```

**Vue (반응성 있음)**:
```vue
<template>
  <button @click="count++">{{ count }}</button>
</template>
<script setup>
import { ref } from 'vue';
const count = ref(0);    // 반응형 변수
// count.value++ 시 Vue 가 자동으로 DOM 갱신
</script>
```

**Vue 의 마법**:
1. `ref()` / `reactive()` 로 만든 변수는 Proxy 로 감싸짐
2. 템플릿이 그 변수를 읽으면 **의존성 추적**
3. 값이 바뀌면 → 의존하는 부분만 **선택적으로 DOM 재렌더**

→ "어떻게 DOM 을 업데이트 할지" 가 아니라 "무엇이 표시되어야 하는지" 만 선언 = **선언형 UI**.

</details>

### Q2. (개념) `ref` vs `reactive` 차이와 선택 기준?

<details><summary>정답</summary>

```js
import { ref, reactive } from 'vue';

// ref - 단일 값
const count = ref(0);
const name = ref('lee');
count.value++;              // 스크립트에선 .value
console.log(name.value);

// reactive - 객체
const state = reactive({ name: 'lee', age: 20 });
state.age++;                // .value 없음
console.log(state.name);
```

| | `ref` | `reactive` |
|--|--|--|
| 대상 | 모든 값 (원시·객체) | 객체만 |
| 접근 | `count.value` (스크립트) | `state.name` |
| 템플릿 | 자동 unwrap (`{{ count }}`) | 그대로 (`{{ state.name }}`) |
| 재할당 | `count.value = newValue` | `state = newObj` 안 됨 (참조 깨짐) |
| destructure | OK | **반응성 깨짐** (`toRefs` 필요) |

**선택 가이드**:
- 단일 값 (숫자, 문자열, boolean) → **`ref`**
- 관련된 여러 값 묶음 → **`reactive`** 또는 객체 ref
- **단순화**: 다 `ref` 만 써도 OK (Vue 공식 권장)

```js
// 일관성을 위해 ref 통일
const user = ref({ name: 'lee', age: 20 });
user.value.age++;
```

</details>

### Q3. (디버그) 스크립트에서 `console.log(count)` 하면 출력이 이상함. 왜?

<details><summary>정답</summary>

```js
const count = ref(0);
console.log(count);
// 출력: RefImpl { __v_isShallow: false, dep: ..., __v_isRef: true, _rawValue: 0, _value: 0 }
// 0 이 아님!

count++;     // TypeError 또는 NaN
```

**이유**: `ref()` 가 반환하는 것은 **객체 (RefImpl)**. 실제 값은 `.value` 안에.

**올바른 접근**:
```js
// 스크립트
console.log(count.value);   // 0
count.value++;              // 1
count.value = 100;

// 템플릿 - 자동 unwrap
<template>
  <p>{{ count }}</p>        <!-- 100, .value 자동 -->
</template>
```

**왜 이렇게 설계?**:
- 자바스크립트는 원시값 (`number`, `string`) 을 참조로 전달 못 함
- 함수에 `ref` 를 넘기면 객체로 넘어가서 양쪽이 같은 반응성 공유
- Vue 2 의 `data() { return { count: 0 } }` 의 한계 극복 (Composition API 의 핵심)

**자주 하는 실수**:
- `if (count) { ... }` → 항상 truthy (객체임)
- `count + 1` → 의도와 다른 결과
- `count.value` 누락 → 가장 흔한 신입 버그

</details>

### Q4. (개념) `computed` 와 `watch` 의 차이와 각각 언제 사용?

<details><summary>정답</summary>

| | `computed` | `watch` |
|--|--|--|
| **목적** | 의존성으로 **새 값 계산** | 변화 감지 후 **사이드 이펙트** |
| **반환** | 값 (다른 ref 처럼 사용) | undefined (콜백 안에서 작업) |
| **캐싱** | 의존성 안 바뀌면 안 다시 계산 | 매 변화마다 콜백 실행 |
| **사용 예** | 합계, 필터링, 포맷팅 | API 호출, localStorage 저장, 라우팅 |

**computed**:
```js
const items = ref([{ price: 1000 }, { price: 2000 }]);
const total = computed(() => items.value.reduce((s, i) => s + i.price, 0));

// 사용
console.log(total.value);   // 3000
// 템플릿: {{ total }}
// items 가 안 바뀌면 total 도 안 다시 계산 (캐싱)
```

**watch**:
```js
const userId = ref(1);

// userId 가 바뀌면 새 사용자 fetch
watch(userId, async (newId, oldId) => {
    const res = await fetch(`/api/users/${newId}`);
    user.value = await res.json();
});

// 즉시 실행 + 초기값도 처리
watch(userId, fetchUser, { immediate: true });

// 여러 소스 동시 감지
watch([userId, filter], ([newId, newFilter]) => { ... });
```

**선택 가이드**:
- "이 값에서 다른 값을 도출" → `computed` (filter, sort, total)
- "이 값이 바뀌면 무언가 해야" → `watch` (fetch, save, navigate)

⚠️ **함정**: watch 안에서 watch 대상 값을 또 바꾸면 → 무한 루프.

</details>

### Q5. (개념) Vue 의 주요 디렉티브 (`v-if`, `v-for`, `v-bind`, `v-on`, `v-model`) 정리.

<details><summary>정답</summary>

| 디렉티브 | 단축 | 의미 |
|--|--|--|
| `v-bind:href="url"` | `:href` | 속성 바인딩 |
| `v-on:click="fn"` | `@click` | 이벤트 리스너 |
| `v-model="name"` | - | 양방향 바인딩 (input) |
| `v-if` / `v-else-if` / `v-else` | - | 조건부 렌더 (DOM 자체) |
| `v-show` | - | 조건부 표시 (`display: none`) |
| `v-for="item in items"` | - | 반복 렌더 |

**예제**:
```vue
<template>
  <!-- 보간 -->
  <h1>{{ title }}</h1>

  <!-- bind -->
  <a :href="url" :class="{ active: isActive }">링크</a>

  <!-- on -->
  <button @click="onClick" @keyup.enter="search">클릭</button>

  <!-- model -->
  <input v-model="name" placeholder="이름"/>

  <!-- if / else -->
  <p v-if="loggedIn">환영합니다</p>
  <p v-else-if="loading">로딩 중...</p>
  <p v-else>로그인 필요</p>

  <!-- for -->
  <ul>
    <li v-for="item in items" :key="item.id">
      {{ item.name }}
    </li>
  </ul>

  <!-- class / style binding -->
  <div :class="['box', { active: isActive }]"
       :style="{ color: textColor, fontSize: size + 'px' }">
  </div>
</template>
```

**v-if vs v-show**:
- `v-if` - DOM 추가/제거 (조건 자주 안 바뀜)
- `v-show` - `display:none` 토글 (자주 토글)

**이벤트 수정자**: `.prevent` (preventDefault), `.stop` (stopPropagation), `.once`, `.enter`.

</details>

### Q6. (디버그) `v-for` 에 `:key` 를 안 주면 어떤 문제가 발생?

<details><summary>정답</summary>

```vue
<!-- 안 좋은 예 - :key 누락 -->
<li v-for="item in items">
    <input v-model="item.draft"/>
    {{ item.name }}
</li>
```

**문제**: Vue 는 DOM 재사용을 위해 각 요소를 **식별** 해야 함. `:key` 가 없으면 **위치 (인덱스) 만** 보고 매칭.

**증상**:
- `items` 배열을 정렬·필터링·앞에 삽입 → 행의 위치가 바뀜
- Vue 는 "1번 자리의 DOM" 을 그대로 두고 데이터만 교체
- 사용자가 1번 행 input 에 친 글자가 → 정렬 후엔 **3번 행에 표시**
- 폼·input·focus 상태가 잘못된 행으로 옮겨감

**해결**:
```vue
<li v-for="item in items" :key="item.id">     <!-- 고유 id -->
    <input v-model="item.draft"/>
    {{ item.name }}
</li>
```

**`:key` 가 되어야 할 것**:
- 데이터의 **고유한 식별자** (보통 DB id)
- **안정적** - 같은 데이터는 항상 같은 key
- **유일** - 같은 v-for 안에서 중복 X

**`:key="index"` 가 안 좋은 이유**:
- 정렬·삽입·삭제 시 인덱스가 바뀜 → 결국 위치 기반
- "고유 식별자가 없을 때 어쩔 수 없이" 만 사용

**성능**: key 가 있어야 Vue 가 **최소 변경 DOM** 적용 가능.

</details>

### Q7. (적용) computed 로 장바구니 합계 계산 + 캐싱 이점.

<details><summary>정답</summary>

```vue
<template>
  <div>
    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.name }} - {{ item.price }}원 x {{ item.qty }}개
      </li>
    </ul>
    <p>합계: {{ total }}원</p>
    <p>할인 적용가: {{ discounted }}원</p>
    <p>아이템 수: {{ itemCount }}</p>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const items = ref([
    { id: 1, name: '책', price: 15000, qty: 2 },
    { id: 2, name: '펜', price: 3000,  qty: 5 }
]);

// 합계 - 의존성 = items
const total = computed(() =>
    items.value.reduce((s, i) => s + i.price * i.qty, 0)
);

// 할인 - 의존성 = total
const discounted = computed(() =>
    total.value > 30000 ? total.value * 0.9 : total.value
);

// 아이템 수 - 의존성 = items
const itemCount = computed(() =>
    items.value.reduce((s, i) => s + i.qty, 0)
);
</script>
```

**캐싱 이점**:
```js
// 안 좋은 예 - 함수 (매번 실행)
function total() {
    console.log('total 계산!');  // 템플릿에서 3번 사용 = 3번 호출
    return items.value.reduce(...);
}

// 좋은 예 - computed (한 번만)
const total = computed(() => {
    console.log('total 계산!');  // items 가 바뀔 때만 1번
    return items.value.reduce(...);
});
```

**언제 차이가 큰가**:
- 무거운 계산 (sort, filter, reduce 큰 배열)
- 템플릿에서 여러 번 참조하는 값
- 다른 computed 가 또 의존하는 값

</details>

### Q8. (적용) `v-model` 의 내부 동작 + 폼 처리.

<details><summary>정답</summary>

**`v-model` 은 설탕 문법**:
```vue
<input v-model="name"/>

<!-- 위는 아래와 동일 -->
<input :value="name" @input="name = $event.target.value"/>
```

**다양한 input 타입**:
```vue
<template>
  <!-- 텍스트 -->
  <input v-model="name"/>

  <!-- 체크박스 (boolean) -->
  <input type="checkbox" v-model="agreed"/>

  <!-- 체크박스 다중 (배열) -->
  <input type="checkbox" value="A" v-model="selected"/>
  <input type="checkbox" value="B" v-model="selected"/>

  <!-- 라디오 -->
  <input type="radio" value="M" v-model="gender"/>
  <input type="radio" value="F" v-model="gender"/>

  <!-- select -->
  <select v-model="country">
    <option value="KR">한국</option>
    <option value="US">미국</option>
  </select>

  <!-- textarea -->
  <textarea v-model="bio"/>
</template>

<script setup>
import { ref } from 'vue';
const name = ref('');
const agreed = ref(false);
const selected = ref([]);
const gender = ref('');
const country = ref('KR');
const bio = ref('');
</script>
```

**수정자**:
```vue
<input v-model.lazy="msg"/>      <!-- @change (focus 잃을 때) -->
<input v-model.number="age"/>     <!-- 자동 Number 변환 -->
<input v-model.trim="name"/>      <!-- 자동 trim -->
```

**커스텀 컴포넌트에 v-model**:
```vue
<!-- 부모 -->
<MyInput v-model="text"/>

<!-- MyInput.vue -->
<template>
  <input :value="modelValue" @input="$emit('update:modelValue', $event.target.value)"/>
</template>
<script setup>
defineProps(['modelValue']);
defineEmits(['update:modelValue']);
</script>
```

</details>

### Q9. (개념) "Props down, events up" - 단방향 데이터 흐름의 이점?

<details><summary>정답</summary>

**규칙**:
- 부모 → 자식: **props** (데이터 내려보냄)
- 자식 → 부모: **emit** (이벤트 올려보냄)
- 자식이 props 를 **직접 수정 금지**

**올바른 패턴**:
```vue
<!-- 부모 -->
<template>
  <BoardItem :board="b" @delete="onDelete"/>
</template>
<script setup>
function onDelete(id) {
    boards.value = boards.value.filter(b => b.id !== id);  // 부모가 변경
}
</script>

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
```

**안 좋은 예 (안티 패턴)**:
```vue
<!-- 자식이 props 직접 수정 -->
<script setup>
const props = defineProps(['board']);
function remove() {
    props.board.deleted = true;  // 안 좋은 예!
}
</script>
```
→ Vue 가 경고: `Avoid mutating a prop directly`.

**단방향 흐름의 이점**:

1. **추적 가능** - 데이터가 어디서 바뀌는지 한 방향만 따라가면 됨
2. **디버깅 쉬움** - "이 값이 왜 바뀌었지?" → 부모만 보면 됨
3. **테스트 용이** - 자식은 순수 함수 (props → 화면)
4. **재사용 가능** - 자식이 부모 모름 → 어디서든 쓸 수 있음

→ Redux, Vuex, Pinia 모두 같은 원칙 (state → view → action → state).

</details>

### Q10. (적용) 게시판 아이템 컴포넌트 + props + emit + 부모 사용.

<details><summary>정답</summary>

```vue
<!-- BoardItem.vue (자식) -->
<template>
  <article class="board-item">
    <h3>{{ board.title }}</h3>
    <small>by {{ board.writer }} | {{ formatDate(board.createdAt) }}</small>
    <p>{{ board.content }}</p>

    <div class="actions">
      <button @click="$emit('edit', board.id)">수정</button>
      <button @click="$emit('delete', board.id)">삭제</button>
    </div>
  </article>
</template>

<script setup>
defineProps({
    board: {
        type: Object,
        required: true,
        validator: (b) => b.id && b.title    // 검증
    }
});

defineEmits(['edit', 'delete']);

function formatDate(iso) {
    return new Date(iso).toLocaleString('ko-KR', {
        dateStyle: 'short', timeStyle: 'short'
    });
}
</script>
```

```vue
<!-- BoardList.vue (부모) -->
<template>
  <section>
    <input v-model="keyword" @keyup.enter="search" placeholder="검색"/>

    <p v-if="loading">로딩 중...</p>
    <p v-else-if="boards.length === 0">결과 없음</p>

    <BoardItem
      v-for="b in boards"
      :key="b.id"
      :board="b"
      @edit="onEdit"
      @delete="onDelete"
    />
  </section>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import BoardItem from './BoardItem.vue';

const keyword = ref('');
const boards = ref([]);
const loading = ref(false);

async function search() {
    loading.value = true;
    try {
        const res = await fetch(`/api/boards?keyword=${encodeURIComponent(keyword.value)}`);
        boards.value = await res.json();
    } finally {
        loading.value = false;
    }
}

async function onDelete(id) {
    if (!confirm('삭제할까요?')) return;
    await fetch(`/api/boards/${id}`, { method: 'DELETE' });
    boards.value = boards.value.filter(b => b.id !== id);
}

function onEdit(id) {
    // 라우터로 수정 페이지 이동
}

onMounted(search);
</script>
```

**구조**:
- 부모 (BoardList): 데이터 fetch, 상태 관리, API 호출
- 자식 (BoardItem): 표시, 이벤트 발사 (props 만 받음, 절대 수정 X)
- 단방향: props 로 데이터, emit 으로 액션

</details>

### Q11. (디버그) `reactive` 객체를 destructure 하면 반응성이 깨짐. 이유와 해결?

<details><summary>정답</summary>

**문제 코드**:
```js
const state = reactive({ name: 'lee', age: 20 });

// destructure
const { name, age } = state;

// 사용
console.log(name, age);    // 'lee', 20 - 첫 출력은 OK
state.age = 30;            // state.age 만 30
console.log(age);          // 20 - 안 바뀜!
```

**이유**: destructure 는 **현재 값을 복사**. `name` 과 `age` 는 더 이상 `state` 의 Proxy 와 연결 안 됨.

**해결 1: `toRefs`** (가장 흔함):
```js
import { reactive, toRefs } from 'vue';

const state = reactive({ name: 'lee', age: 20 });
const { name, age } = toRefs(state);

// 이제 name 과 age 는 ref 임
console.log(name.value, age.value);    // 'lee', 20
state.age = 30;
console.log(age.value);                 // 30 - 반응성 유지
```

**해결 2: `toRef`** (개별):
```js
const age = toRef(state, 'age');
```

**해결 3: composable 패턴** (재사용):
```js
function useUser() {
    const state = reactive({ name: 'lee', age: 20 });

    function celebrateBirthday() { state.age++; }

    return {
        ...toRefs(state),       // 자동 toRefs
        celebrateBirthday
    };
}

// 사용
const { name, age, celebrateBirthday } = useUser();
celebrateBirthday();
console.log(age.value);    // 21
```

→ Composition API 의 가장 흔한 패턴. composable 함수 안에서 reactive + toRefs.

</details>

### Q12. (적용) Composition API + onMounted 로 초기 데이터 fetch.

<details><summary>정답</summary>

```vue
<template>
  <div>
    <p v-if="loading">로딩 중...</p>
    <p v-else-if="error">에러: {{ error }}</p>
    <ul v-else>
      <li v-for="b in boards" :key="b.id">{{ b.title }}</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const boards = ref([]);
const loading = ref(false);
const error = ref(null);
let intervalId = null;

async function fetchBoards() {
    loading.value = true;
    error.value = null;
    try {
        const res = await fetch('/api/boards');
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        boards.value = await res.json();
    } catch (e) {
        error.value = e.message;
    } finally {
        loading.value = false;
    }
}

// 컴포넌트 마운트 후 초기 로드
onMounted(() => {
    fetchBoards();

    // 30초마다 갱신
    intervalId = setInterval(fetchBoards, 30000);
});

// 언마운트 시 인터벌 정리 (메모리 누수 방지)
onUnmounted(() => {
    if (intervalId) clearInterval(intervalId);
});
</script>
```

**라이프사이클 훅**:
- `onBeforeMount` - DOM 생성 직전
- `onMounted` - DOM 생성 후 (초기 fetch, focus 설정)
- `onBeforeUpdate` / `onUpdated` - 재렌더 전후
- `onBeforeUnmount` - 사라지기 직전 (이벤트 리스너 제거, 타이머 정리)
- `onUnmounted` - 사라진 후

**원칙**:
- DOM 접근 필요 (`querySelector`) → `onMounted`
- 외부 자원 정리 (타이머, 웹소켓) → `onUnmounted`
- 데이터 변경 감시는 → `watch` 또는 `watchEffect`

</details>

### Q13. (디버그) Vue 앱이 백엔드 API 를 호출할 때 CORS 에러. 해결 옵션 3가지?

<details><summary>정답</summary>

**증상**:
```
Access to fetch at 'http://localhost:8080/api/boards' from origin
'http://localhost:5173' has been blocked by CORS policy
```

**원인**: 브라우저가 다른 origin (포트·도메인) 으로의 요청을 보안상 차단. Vue dev server (`5173`) → Spring (`8080`) 은 다른 origin.

**해결 1: 백엔드에서 CORS 허용** (Spring):
```java
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
            .allowedOrigins("http://localhost:5173")
            .allowedMethods("GET", "POST", "PUT", "DELETE")
            .allowCredentials(true);
    }
}
```

또는 컨트롤러 어노테이션:
```java
@CrossOrigin(origins = "http://localhost:5173")
@RestController
public class BoardApi { ... }
```

**해결 2: Vite proxy (개발 환경)**:
```js
// vite.config.js
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
```
- Vue 가 `/api/boards` 호출 → Vite 가 서버 사이드로 `http://localhost:8080/api/boards` 로 프록시
- 브라우저는 같은 origin 으로 인식 → CORS 우회

**해결 3: 같은 도메인 배포 (운영)**:
- Vue 빌드 결과 (`dist/`) 를 Spring 의 정적 리소스로 (`src/main/resources/static`)
- Nginx 가 정적 파일 + `/api/**` 둘 다 같은 도메인으로 라우팅
- → 처음부터 같은 origin 이라 CORS 발생 X

**개발/운영 분리**:
- 개발: Vite proxy (가장 편함)
- 운영: 같은 도메인 (보안·CORS 부담 없음)

</details>

### Q14. (면접) "Vue vs React vs Svelte 의 반응성 모델 차이?"

<details><summary>정답</summary>

**Vue 3 - Proxy 기반 반응성**:
```js
const state = reactive({ count: 0 });
state.count++;    // Vue 가 자동 감지 (Proxy)
```
- **장점**: 코드 자연스러움, 깊은 객체 자동 추적
- **단점**: `ref.value` 가 어색, destructure 함정

**React - 명시적 setState**:
```jsx
const [count, setCount] = useState(0);
setCount(count + 1);    // 명시적으로 함수 호출
```
- **장점**: 명확함, 불변성 강제
- **단점**: 변경마다 함수 호출, 의존성 배열 (`useEffect`) 복잡

**Svelte - 컴파일 타임 반응성**:
```svelte
<script>
  let count = 0;
  function increment() { count++; }    // 일반 변수
</script>
<button on:click={increment}>{count}</button>
```
- **장점**: 코드 가장 자연스러움 (런타임 가상 DOM X)
- **단점**: 새로운 컴파일러 매직 학습

**비교표**:

| | Vue 3 | React | Svelte |
|--|--|--|--|
| 반응성 방식 | Proxy (런타임) | 명시적 (`setState`) | 컴파일러 |
| 가상 DOM | O | O | X (컴파일 결과가 직접 DOM) |
| 학습 곡선 | 중간 | 중간 (Hooks 어려움) | 낮음 |
| 생태계 | 중간 | 거대 | 작음 |
| 번들 크기 | 중간 | 큼 | 가장 작음 |
| 채용 시장 | 중간 (한국 인기 ↑) | 압도적 | 작음 |

**선택 가이드**:
- 큰 팀, 풍부한 라이브러리, 안정성 → **React**
- 학습 쉽고 빠른 개발, 한국 시장, 풀스택 (Spring + Vue) → **Vue**
- 성능 최우선, 작은 번들, 실험적 → **Svelte**

**SSAFY 커리큘럼**: Vue 선택 이유 - 한국 백엔드 (Spring) 와 자주 조합되고, 학습 곡선 낮으며, 공식 가이드가 한국어 잘 됨.

**공통**: 셋 다 **컴포넌트 + 단방향 데이터 + 선언형 UI** 패러다임. 하나 익히면 다른 것도 쉬워짐.

</details>
