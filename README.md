# TechSecure Solutions — Esteira CI/CD Segura (AP II DevSecOps)

Prova de conceito de uma esteira **CI/CD com práticas de DevSecOps**: uma aplicação
simples em container, com integração e deploy automatizados e etapa de análise de
segurança integrada ao pipeline.

## Fluxo da esteira

```
Código → Build → Teste → Análise de Segurança → Build da Imagem → Deploy Automático → Container
```

## Aplicação

API REST de gestão de tarefas em **Node.js + Express** (sem banco, dados em memória —
foco é a esteira, não a aplicação).

| Rota | Método | Descrição |
|------|--------|-----------|
| `/` | GET | Status da aplicação |
| `/health` | GET | Healthcheck (usado pelo Docker/deploy) |
| `/tarefas` | GET | Lista tarefas |
| `/tarefas` | POST | Cria tarefa (`{ "titulo": "..." }`) |

## Tecnologias

- **Versionamento:** Git / GitHub
- **CI/CD:** GitHub Actions
- **Container:** Docker (imagem `node:20-alpine`, usuário não-root)
- **Testes:** Jest + Supertest
- **Segurança:** Trivy (filesystem + imagem) e `npm audit` (SCA de dependências)

## Como rodar localmente

```bash
npm install
npm test          # testes automatizados
npm start         # sobe em http://localhost:3000

# Via Docker
docker build -t techsecure-app:latest .
docker run -d -p 3000:3000 --name techsecure-app techsecure-app:latest
curl http://localhost:3000/health
```

## Pipeline (`.github/workflows/ci-cd.yml`)

A esteira é disparada **automaticamente** a cada `push`/`pull_request` na branch `main`:

1. **build-test** — instala dependências e roda os testes (Jest).
2. **security-scan** — `npm audit` + Trivy (scan do filesystem), publica relatório como artefato.
3. **build-deploy** — build da imagem Docker, Trivy na imagem, deploy do container e smoke test no `/health`.

## Análise de segurança

Ver [`docs/analise-seguranca.md`](docs/analise-seguranca.md) para o achado detalhado
(vulnerabilidade, componente, severidade e correção).

## Estrutura

```
.
├── src/            # aplicação (app.js, server.js)
├── test/           # testes automatizados
├── .github/workflows/ci-cd.yml
├── Dockerfile
├── docs/           # relatório e análise de segurança
└── README.md
```
