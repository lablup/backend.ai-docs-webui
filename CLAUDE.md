# Backend.AI Docs-WebUI — Claude Code 지침

이 저장소는 Backend.AI WebUI의 사용자 문서입니다.
Sphinx + reStructuredText 형식이며, ko/th 번역을 지원합니다.

## 문서 업데이트 작업 흐름

WebUI 릴리즈 시 자동으로 Draft PR이 생성됩니다.
PR 본문에 **변경된 React 소스 파일**과 **영향받는 RST 파일** 목록이 포함되어 있습니다.

### 작업 순서

1. PR 본문에서 영향받는 RST 파일 목록을 확인합니다.
2. webui repo의 변경된 React 소스를 읽고 UI 변경사항을 파악합니다.
3. 해당 RST 파일을 읽고, 변경된 UI에 맞게 문서를 수정합니다.
4. `STYLE_GUIDE.md`의 규칙을 반드시 따릅니다.
5. 스크린샷이 필요한 경우 `.. TODO:: Update screenshot` 코멘트를 삽입합니다.

## 핵심 규칙

### 스타일 가이드 (STYLE_GUIDE.md 요약)

- **절차 설명**: 2인칭 명령형 ("Click 'Create Folder' to create a new folder.")
- **기능 설명**: 2인칭 서술형 ("You can view the list of sessions.")
- **버튼**: 작은따옴표 ('Create Folder')
- **페이지/탭 이름**: 볼드 (**Dashboard**)
- **코드/상태값**: 백틱 (``RUNNING``)
- **제목**: 동명사 기반 ("Creating a Storage Folder")
- **이미지**: 반드시 `:alt:` 포함, 전체 페이지는 `width: 100%`

### 파일 구조

```
docs/
├── <section_name>/
│   ├── <section_name>.rst    ← 문서 본문
│   └── <section_name>.png    ← 스크린샷
├── locale/
│   ├── ko/LC_MESSAGES/*.po   ← 한국어 번역
│   └── th/LC_MESSAGES/*.po   ← 태국어 번역
└── conf.py                   ← Sphinx 설정
```

### 소스 매핑

`.github/docs-mapping.yml`에 webui React 소스 → RST 파일 매핑이 정의되어 있습니다.
어떤 React 파일이 어떤 문서에 대응하는지 확인할 때 참고하세요.

## 하지 말아야 할 것

- RST 파일의 기존 이미지 경로(.. image::)를 변경하지 마세요.
- 번역 PO 파일을 직접 수정하지 마세요 (번역은 별도 파이프라인이 처리합니다).
- 존재하지 않는 스크린샷을 참조하지 마세요.
- conf.py를 수정하지 마세요.
