# Sea Voyage

Sea Voyage는 지구상의 두 지점 간 최단 해상 경로를 계산하는 Python 패키지입니다. 이 패키지는 [searoute](https://github.com/genthalili/searoute-py) 패키지를 기반으로 개선되었습니다.

## 원본 프로젝트
- 원본 패키지: [searoute](https://github.com/genthalili/searoute-py)
- 원작자: Gent Halili
- 라이선스: Apache License 2.0

## 주요 개선사항
1. 성능 최적화
   - 경로 계산 속도 향상
2. 코드 구조 개선
   - TODO: 코드 구조 개선
3. 기능 추가
   - 다양한 Graph 형태 지원
   - 다양하고 쉬운 방법으로 graph에 node 및 edge 추가 가능
   - 육지를 지나거나 육지 위의 node 및 edge 제거 가능
   - TODO: 새로운 해상 경로 옵션 추가

## 설치 방법
```bash
pip install seavoyage
```

## 사용 예시
```python
import seavoyage as sv

# 출발지와 목적지 좌표 설정
origin = [0.3515625, 50.064191736659104]
destination = [117.42187500000001, 39.36827914916014]

# 경로 계산
route = sv.searoute(origin, destination)

# 거리 및 단위 출력
print("{:.1f} {}".format(route.properties['length'], route.properties['units']))
```

## 라이선스
이 프로젝트는 Apache License 2.0 라이선스 하에 배포됩니다.

```
Copyright 2024 - Gent Halili (원작자)
Copyright 2025 - Byeonggong Hwang

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
```

## 기여
버그 리포트, 기능 제안, 풀 리퀘스트는 언제나 환영합니다.

## 연락처
- 이메일: bk22106@gmail.com
- GitHub: [a22106](https://github.com/a22106)
