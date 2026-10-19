# Análise de Segurança — Achado

A etapa de segurança da esteira executa **`npm audit`** (análise de dependências / SCA)
e **Trivy** (filesystem e imagem Docker). Abaixo o achado selecionado, detectado
automaticamente pelo `npm audit`.

## Achado selecionado

| Item | Descrição |
|------|-----------|
| **Vulnerabilidade** | `braces` vulnerável a *stack-exhaustion Denial of Service* através de padrões profundamente aninhados (ReDoS/DoS). Advisory **GHSA-vfj7-8cjw-p6xm**. |
| **Componente afetado** | Pacote **`braces`**, trazido transitivamente por `micromatch` → `jest` (dependência de desenvolvimento/testes). |
| **Severidade** | **HIGH (Alta)** |
| **Vetor** | Processamento de padrões (globs) com aninhamento muito profundo faz o parser consumir a pilha/CPU, causando negação de serviço. |

## Correção / Mitigação

- **Correção:** atualizar a dependência para versão corrigida de `braces` —
  `npm audit fix --force` (que atualiza o `jest` para a linha corrigida), ou fixar
  `braces >= 3.0.3` via `overrides` no `package.json`.
- **Mitigação:** por ser dependência **apenas de desenvolvimento** (`devDependencies`),
  ela **não é empacotada na imagem de produção** — o Dockerfile instala com
  `npm install --omit=dev`, removendo o pacote vulnerável do container final.
- **Controle contínuo:** o `npm audit` roda a cada execução da pipeline, bloqueando/
  alertando sobre novas vulnerabilidades HIGH/CRITICAL antes do deploy.

## Boas práticas de segurança já aplicadas no container

- Imagem base enxuta `node:20-alpine` (menor superfície de ataque).
- Container roda como **usuário não-root** (`appuser`).
- Apenas dependências de produção na imagem (`--omit=dev`).
- `HEALTHCHECK` configurado.
- Scan Trivy do filesystem **e** da imagem gerada dentro da pipeline.
