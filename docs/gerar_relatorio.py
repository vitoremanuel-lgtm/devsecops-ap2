# -*- coding: utf-8 -*-
from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

doc = Document()

# ---------- CAPA ----------
for _ in range(3):
    doc.add_paragraph()
t = doc.add_paragraph()
t.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = t.add_run('AP II — DevSecOps')
r.bold = True
r.font.size = Pt(26)

s = doc.add_paragraph()
s.alignment = WD_ALIGN_PARAGRAPH.CENTER
rs = s.add_run('Projeto Prático — Construção de uma Esteira CI/CD Segura')
rs.font.size = Pt(15)

st = doc.add_paragraph()
st.alignment = WD_ALIGN_PARAGRAPH.CENTER
rst = st.add_run('Empresa fictícia: TechSecure Solutions')
rst.italic = True
rst.font.size = Pt(13)

for _ in range(6):
    doc.add_paragraph()

info = doc.add_paragraph()
info.alignment = WD_ALIGN_PARAGRAPH.CENTER
info.add_run('Disciplina: DevSecOps\n').bold = True
info.add_run('Modalidade: Trabalho em grupo (até 5 alunos)\n')
info.add_run('Data de entrega: 19/10/2026\n')

# Integrantes
for _ in range(4):
    doc.add_paragraph()
integ = doc.add_paragraph()
integ.alignment = WD_ALIGN_PARAGRAPH.CENTER
integ.add_run('Integrantes do grupo:\n').bold = True
integ.add_run('Vitor Emanuel Santiago — RA 2501093\n')
integ.add_run('Rafael Neves — RA 2503380\n')
integ.add_run('Guilherme Lopes — RA 2502595\n')
integ.add_run('Viniccius Cezario — RA 2504060\n')

doc.add_page_break()

def h(txt):
    doc.add_heading(txt, level=1)

def p(txt):
    doc.add_paragraph(txt)

def bullet(txt):
    doc.add_paragraph(txt, style='List Bullet')

def code(txt):
    par = doc.add_paragraph()
    run = par.add_run(txt)
    run.font.name = 'Consolas'
    run.font.size = Pt(9)

# ---------- 1. OBJETIVO ----------
h('1. Objetivo')
p('Desenvolver uma esteira básica de CI/CD aplicando práticas de DevSecOps. '
  'O grupo implementou uma aplicação simples em container, automatizou o processo '
  'de integração e deploy e incluiu etapas de verificação de segurança integradas '
  'ao pipeline.')
p('Fluxo implementado:')
code('Código -> Build -> Teste -> Análise de Segurança -> Build da Imagem -> Deploy Automático -> Container')

# ---------- 2. ARQUITETURA ----------
h('2. Arquitetura da Solução')
p('A arquitetura é composta por quatro blocos: repositório Git (código-fonte), '
  'servidor de CI/CD (GitHub Actions), análise de segurança (Trivy e npm audit) e '
  'ambiente de execução em container (Docker).')
code(
'Desenvolvedor\n'
'     | git push\n'
'     v\n'
'[ Repositorio GitHub ] --(gatilho automatico)--> [ GitHub Actions ]\n'
'                                                         |\n'
'   +-----------------------------------------------------+\n'
'   |                |                 |                   |\n'
'   v                v                 v                   v\n'
'  Build          Testes        Security Scan       Build da Imagem\n'
' (npm install)   (Jest)      (npm audit + Trivy)     (Docker)\n'
'                                                         |\n'
'                                                         v\n'
'                                              Deploy -> Container (porta 3000)\n'
)

# ---------- 3. APLICACAO ESCOLHIDA ----------
h('3. Aplicação Escolhida')
p('API REST de gestão de tarefas desenvolvida em Node.js com Express. A aplicação '
  'é propositalmente simples (dados em memória, sem banco de dados), pois o foco da '
  'atividade é a esteira CI/CD segura e não a complexidade da aplicação.')
p('Rotas disponíveis:')
bullet('GET /          — status da aplicação')
bullet('GET /health    — healthcheck usado pelo Docker e pelo deploy')
bullet('GET /tarefas   — lista as tarefas')
bullet('POST /tarefas  — cria uma tarefa (valida o payload de entrada)')

# ---------- 4. TECNOLOGIAS ----------
h('4. Tecnologias Utilizadas')
bullet('Versionamento: Git e GitHub')
bullet('CI/CD: GitHub Actions')
bullet('Container: Docker (imagem base node:20-alpine)')
bullet('Testes: Jest + Supertest')
bullet('Segurança: Trivy (filesystem e imagem) e npm audit (SCA de dependências)')

# ---------- 5. DESCRICAO DA PIPELINE ----------
h('5. Descrição da Pipeline')
p('A pipeline (.github/workflows/ci-cd.yml) é disparada automaticamente a cada push '
  'ou pull request na branch main, e está dividida em três jobs encadeados:')
bullet('build-test: instala as dependências (build) e executa os testes automatizados com Jest.')
bullet('security-scan: executa npm audit (dependências) e Trivy (scan do filesystem), '
       'publicando o relatório do Trivy como artefato. Depende do job de testes.')
bullet('build-deploy: faz o build da imagem Docker, roda o Trivy sobre a imagem, '
       'sobe o container (deploy automático) e valida a aplicação com smoke test no /health.')

# ---------- 6. DOCKERFILE ----------
h('6. Dockerfile')
p('O Dockerfile aplica boas práticas de segurança: imagem enxuta, usuário não-root, '
  'apenas dependências de produção e healthcheck.')
code(
'FROM node:20-alpine\n'
'WORKDIR /app\n'
'COPY package*.json ./\n'
'RUN npm install --omit=dev\n'
'COPY src ./src\n'
'RUN addgroup -S appgrp && adduser -S appuser -G appgrp\n'
'USER appuser\n'
'EXPOSE 3000\n'
'HEALTHCHECK --interval=30s --timeout=3s \\\n'
'  CMD wget -qO- http://localhost:3000/health || exit 1\n'
'CMD ["node", "src/server.js"]\n'
)

# ---------- 7. FERRAMENTA DE SEGURANCA / ACHADO ----------
h('7. Ferramenta de Segurança e Achado')
p('Foram utilizadas duas ferramentas: npm audit (análise de dependências) e Trivy '
  '(análise de vulnerabilidades no filesystem e na imagem). Abaixo o achado selecionado, '
  'detectado automaticamente pela pipeline.')

tbl = doc.add_table(rows=5, cols=2)
tbl.style = 'Light Grid Accent 1'
dados = [
    ('Vulnerabilidade', 'braces vulnerável a Denial of Service por stack-exhaustion '
                        'com padrões profundamente aninhados (GHSA-vfj7-8cjw-p6xm).'),
    ('Componente afetado', 'Pacote braces, trazido transitivamente por micromatch -> jest.'),
    ('Severidade', 'HIGH (Alta)'),
    ('Correção', 'Atualizar braces (npm audit fix --force) ou fixar braces >= 3.0.3 '
                 'via overrides no package.json.'),
    ('Mitigação', 'É dependência apenas de desenvolvimento; o Dockerfile usa '
                  'npm install --omit=dev, então o pacote não vai para a imagem de produção.'),
]
for i, (k, v) in enumerate(dados):
    tbl.rows[i].cells[0].text = k
    tbl.rows[i].cells[1].text = v

# ---------- 8. RESULTADOS ----------
h('8. Resultados')
bullet('Testes automatizados: 5 testes executados, 5 aprovados, 100% de cobertura.')
bullet('Análise de segurança: achado HIGH identificado automaticamente (braces).')
bullet('Build da imagem Docker e deploy do container concluídos na pipeline.')
bullet('Aplicação respondendo no endpoint /health (smoke test aprovado).')
p('Saída resumida dos testes (jest):')
code(
'PASS test/app.test.js\n'
'  TechSecure API\n'
'    v GET / retorna status online\n'
'    v GET /health retorna ok\n'
'    v GET /tarefas retorna uma lista\n'
'    v POST /tarefas cria uma tarefa valida\n'
'    v POST /tarefas rejeita payload invalido\n'
'Tests: 5 passed, 5 total | Coverage: 100%\n'
)

# ---------- 9. EVIDENCIAS ----------
h('9. Evidências')
p('As evidências em imagem devem ser anexadas aqui (prints capturados durante a execução):')
bullet('[Print] Pipeline executando no GitHub Actions (jobs verdes)')
bullet('[Print] Resultado do build e dos testes')
bullet('[Print] Resultado do security scan (npm audit / Trivy)')
bullet('[Print] Build da imagem Docker')
bullet('[Print] Container em execução (docker ps)')
bullet('[Print] Aplicação funcionando no navegador / curl')

# ---------- 10. DIFICULDADES ----------
h('10. Dificuldades Encontradas')
bullet('Configurar o encadeamento correto dos jobs (needs) para que o deploy só ocorra '
       'após build, testes e scan de segurança passarem.')
bullet('Interpretar os resultados do npm audit e distinguir vulnerabilidades de produção '
       'das de desenvolvimento.')
bullet('Garantir boas práticas de segurança no Dockerfile (usuário não-root, imagem enxuta).')

# ---------- 11. CONCLUSAO ----------
h('11. Conclusão')
p('O projeto demonstrou, na prática, a construção de uma esteira CI/CD com segurança '
  'integrada (DevSecOps). A automação garante que todo código enviado ao repositório '
  'passe por build, testes e análise de segurança antes do deploy, deslocando a segurança '
  'para o início do ciclo (shift-left). O achado de vulnerabilidade identificado '
  'automaticamente comprova o valor de incorporar verificações de segurança ao pipeline, '
  'reduzindo riscos antes que a aplicação chegue ao ambiente de execução.')

doc.save(r'C:\dev\devsecops-ap2\docs\AP_II_DevSecOps_TechSecure.docx')
print('Relatorio gerado com sucesso.')
