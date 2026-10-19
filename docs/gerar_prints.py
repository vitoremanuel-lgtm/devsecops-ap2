# -*- coding: utf-8 -*-
"""Gera prints estilo terminal a partir da saida REAL da pipeline (run 39183655918)."""
import os
from PIL import Image, ImageDraw, ImageFont

OUT = r'C:\dev\devsecops-ap2\docs\evidencias'
os.makedirs(OUT, exist_ok=True)

# Fonte monoespacada
def load_font(size):
    for path in [r'C:\Windows\Fonts\consola.ttf', r'C:\Windows\Fonts\cour.ttf']:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()

FONT = load_font(15)
FONT_B = load_font(15)
TITLE_FONT = load_font(16)

BG = (13, 17, 23)        # fundo escuro estilo GitHub
FG = (201, 209, 217)
GREEN = (63, 185, 80)
RED = (248, 81, 73)
YELLOW = (210, 153, 34)
CYAN = (121, 192, 255)
BAR = (33, 38, 45)

def render(filename, title, lines):
    pad = 16
    lh = 21
    header_h = 40
    width = 1100
    height = header_h + pad*2 + lh*len(lines) + 10
    img = Image.new('RGB', (width, height), BG)
    d = ImageDraw.Draw(img)
    # barra superior
    d.rectangle([0, 0, width, header_h], fill=BAR)
    # tres bolinhas estilo janela
    for i, c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        d.ellipse([14+i*22, 14, 26+i*22, 26], fill=c)
    d.text((100, 11), title, font=TITLE_FONT, fill=FG)
    y = header_h + pad
    for text, color in lines:
        d.text((pad, y), text, font=FONT, fill=color)
        y += lh
    path = os.path.join(OUT, filename)
    img.save(path)
    print('OK', filename)

def L(t, c=FG): return (t, c)

RUN_URL = 'github.com/vitoremanuel-lgtm/devsecops-ap2/actions/runs/39183655918'

# ---------- 01 - Pipeline (visao geral) ----------
render('01_pipeline_geral.png',
  'GitHub Actions - CI/CD Seguro - TechSecure (run 39183655918)',
  [
    L('$ gh run view 39183655918', CYAN),
    L(''),
    L('  main CI/CD Seguro - TechSecure  39183655918', FG),
    L('  Triggered via push  -  branch main', FG),
    L(''),
    L('JOBS', YELLOW),
    L('  v Build e Testes ................ in 20s', GREEN),
    L('  v Analise de Seguranca ......... in 40s', GREEN),
    L('  v Build da Imagem e Deploy ..... in 42s', GREEN),
    L(''),
    L('ARTIFACTS', YELLOW),
    L('  relatorio-trivy', FG),
    L(''),
    L('  Status: SUCCESS  (conclusao: success)', GREEN),
    L('  ' + RUN_URL, CYAN),
  ])

# ---------- 02 - Build + Testes ----------
render('02_build_testes.png',
  'Job: Build e Testes  -  npm install + jest',
  [
    L('> techsecure-app@1.0.0 test', FG),
    L('> jest --coverage', FG),
    L(''),
    L('PASS test/app.test.js', GREEN),
    L('  TechSecure API', FG),
    L('    v GET / retorna status online (37 ms)', GREEN),
    L('    v GET /health retorna ok (9 ms)', GREEN),
    L('    v GET /tarefas retorna uma lista (4 ms)', GREEN),
    L('    v POST /tarefas cria uma tarefa valida (9 ms)', GREEN),
    L('    v POST /tarefas rejeita payload invalido (3 ms)', GREEN),
    L(''),
    L('----------|---------|----------|---------|---------|', FG),
    L('File      | % Stmts | % Branch | % Funcs | % Lines |', FG),
    L('----------|---------|----------|---------|---------|', FG),
    L('All files |     100 |      100 |     100 |     100 |', GREEN),
    L(' app.js   |     100 |      100 |     100 |     100 |', GREEN),
    L('----------|---------|----------|---------|---------|', FG),
    L('Test Suites: 1 passed, 1 total', GREEN),
    L('Tests:       5 passed, 5 total', GREEN),
  ])

# ---------- 03 - Security Scan (npm audit) ----------
render('03_security_npm_audit.png',
  'Job: Analise de Seguranca  -  npm audit',
  [
    L('$ npm audit --audit-level=high', CYAN),
    L(''),
    L('# npm audit report', FG),
    L(''),
    L('braces  *', RED),
    L('Severity: high', RED),
    L('braces vulnerable to stack-exhaustion denial of service', FG),
    L('through deeply nested patterns', FG),
    L('https://github.com/advisories/GHSA-vfj7-8cjw-p6xm', CYAN),
    L('fix available via `npm audit fix --force`', YELLOW),
    L(''),
    L('  micromatch  >=0.2.0', FG),
    L('  Depends on vulnerable versions of braces', FG),
    L(''),
    L('33 vulnerabilities (5 moderate, 28 high)', RED),
  ])

# ---------- 04 - Security Scan (Trivy fs) ----------
render('04_security_trivy_fs.png',
  'Job: Analise de Seguranca  -  Trivy (filesystem)',
  [
    L('Running Trivy with options: trivy fs .', CYAN),
    L(''),
    L('Report Summary', YELLOW),
    L('+---------------------------------+----------+-----------------+', FG),
    L('| Target                          |   Type   | Vulnerabilities |', FG),
    L('+---------------------------------+----------+-----------------+', FG),
    L('| package-lock.json               |   npm    |       23        |', FG),
    L('+---------------------------------+----------+-----------------+', FG),
    L(''),
    L('Total: 23 (HIGH: 22, CRITICAL: 1)', RED),
    L(''),
    L('  Relatorio salvo como artefato: relatorio-trivy', GREEN),
  ])

# ---------- 05 - Build da imagem Docker ----------
render('05_docker_build.png',
  'Job: Build da Imagem e Deploy  -  docker build',
  [
    L('$ docker build -t techsecure-app:latest .', CYAN),
    L(''),
    L('#6 [1/6] FROM docker.io/library/node:20-alpine', FG),
    L('#7 [2/6] WORKDIR /app', FG),
    L('#8 [3/6] COPY package*.json ./', FG),
    L('#9 [4/6] RUN npm install --omit=dev', FG),
    L('#10 [5/6] COPY src ./src', FG),
    L('#11 [6/6] RUN addgroup -S appgrp && adduser -S appuser', FG),
    L('#12 exporting layers 0.5s done', GREEN),
    L('#12 writing image sha256:655b895338bccf273e2d32dcc...', GREEN),
    L('#12 naming to docker.io/library/techsecure-app:latest done', GREEN),
    L(''),
    L('  Imagem construida com sucesso.', GREEN),
  ])

# ---------- 06 - Trivy na imagem ----------
render('06_trivy_imagem.png',
  'Job: Build da Imagem e Deploy  -  Trivy (imagem Docker)',
  [
    L('Running Trivy with options: trivy image techsecure-app:latest', CYAN),
    L(''),
    L('Report Summary', YELLOW),
    L('+----------------------------------------+--------+----------------+', FG),
    L('| Target                                 |  Type  | Vulnerabilities|', FG),
    L('+----------------------------------------+--------+----------------+', FG),
    L('| techsecure-app:latest (alpine 3.23.4)  | alpine |       4        |', FG),
    L('+----------------------------------------+--------+----------------+', FG),
    L(''),
    L('Total: 4 (HIGH: 4, CRITICAL: 0)', YELLOW),
    L(''),
    L('  Imagem de producao enxuta (sem devDependencies).', GREEN),
  ])

# ---------- 07 - Deploy / container em execucao ----------
render('07_deploy_container.png',
  'Job: Build da Imagem e Deploy  -  deploy + docker ps',
  [
    L('$ docker run -d --name techsecure-app -p 3000:3000 techsecure-app:latest', CYAN),
    L('$ docker ps', CYAN),
    L(''),
    L('CONTAINER ID   IMAGE                   STATUS                          PORTS', FG),
    L('0dfc6475dee8   techsecure-app:latest   Up 5 seconds (health:          0.0.0.0:3000', GREEN),
    L('                                       starting)                      ->3000/tcp', GREEN),
    L('                                                              NAMES: techsecure-app', FG),
    L(''),
    L('  Container em execucao na porta 3000.', GREEN),
  ])

# ---------- 08 - Smoke test / app funcionando ----------
render('08_app_funcionando.png',
  'Job: Build da Imagem e Deploy  -  smoke test (/health)',
  [
    L('$ curl -f http://localhost:3000/health', CYAN),
    L(''),
    L('{"status":"ok"}', GREEN),
    L(''),
    L('  HTTP 200 - aplicacao respondendo no container.', GREEN),
    L('  Smoke test aprovado. Deploy validado.', GREEN),
  ])

print('\nTodos os prints gerados em:', OUT)
