# -*- coding: utf-8 -*-
"""Gera a apresentacao (.pptx) do projeto AP II DevSecOps - TechSecure."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

EVID = r'C:\dev\devsecops-ap2\docs\evidencias'
OUT = r'C:\dev\devsecops-ap2\docs\AP_II_DevSecOps_Apresentacao.pptx'

# Paleta
DARK = RGBColor(0x0D, 0x11, 0x17)
PANEL = RGBColor(0x16, 0x1B, 0x22)
WHITE = RGBColor(0xF0, 0xF6, 0xFC)
GREY = RGBColor(0xB0, 0xBA, 0xC5)
GREEN = RGBColor(0x3F, 0xB9, 0x50)
CYAN = RGBColor(0x58, 0xA6, 0xFF)
RED = RGBColor(0xF8, 0x51, 0x49)
YELLOW = RGBColor(0xD2, 0x99, 0x22)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
SW, SH = prs.slide_width, prs.slide_height
BLANK = prs.slide_layouts[6]

def bg(slide, color=DARK):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = color

def box(slide, l, t, w, h, color):
    from pptx.enum.shapes import MSO_SHAPE
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = color
    s.line.fill.background()
    s.shadow.inherit = False
    return s

def txt(slide, l, t, w, h, text, size=18, color=WHITE, bold=False,
        align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, font='Calibri'):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    tf.vertical_anchor = anchor
    lines = text.split('\n')
    for i, line in enumerate(lines):
        pr = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        pr.alignment = align
        run = pr.add_run(); run.text = line
        run.font.size = Pt(size); run.font.bold = bold
        run.font.color.rgb = color; run.font.name = font
    return tb

def bullets(slide, l, t, w, h, items, size=18, color=WHITE, gap=6):
    tb = slide.shapes.add_textbox(l, t, w, h)
    tf = tb.text_frame; tf.word_wrap = True
    for i, (it, c) in enumerate(items):
        pr = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        pr.space_after = Pt(gap)
        run = pr.add_run(); run.text = '•  ' + it
        run.font.size = Pt(size); run.font.color.rgb = c; run.font.name = 'Calibri'
    return tb

def accent(slide):
    box(slide, 0, 0, Inches(0.18), SH, GREEN)

def header(slide, title, num):
    accent(slide)
    txt(slide, Inches(0.5), Inches(0.35), Inches(11), Inches(0.9),
        title, size=30, color=WHITE, bold=True)
    box(slide, Inches(0.55), Inches(1.15), Inches(2.2), Inches(0.05), GREEN)
    txt(slide, Inches(12.3), Inches(6.9), Inches(0.9), Inches(0.4),
        str(num), size=12, color=GREY, align=PP_ALIGN.RIGHT)

# ---------- SLIDE 1 - CAPA ----------
s = prs.slides.add_slide(BLANK); bg(s)
box(s, 0, 0, SW, Inches(0.25), GREEN)
txt(s, Inches(1), Inches(2.1), Inches(11.3), Inches(1.2),
    'AP II — DevSecOps', size=52, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(1), Inches(3.3), Inches(11.3), Inches(0.8),
    'Construção de uma Esteira CI/CD Segura', size=26, color=CYAN, align=PP_ALIGN.CENTER)
txt(s, Inches(1), Inches(4.1), Inches(11.3), Inches(0.6),
    'Cenário proposto no enunciado: empresa fictícia TechSecure Solutions', size=18, color=GREY, align=PP_ALIGN.CENTER)
txt(s, Inches(1), Inches(5.5), Inches(11.3), Inches(1.3),
    'Vitor Emanuel Santiago (RA 2501093)   •   Rafael Neves (RA 2503380)\n'
    'Guilherme Lopes (RA 2502595)   •   Viniccius Cezario (RA 2504060)',
    size=15, color=WHITE, align=PP_ALIGN.CENTER)
box(s, 0, SH-Inches(0.25), SW, Inches(0.25), GREEN)

# ---------- SLIDE 2 - OBJETIVO + FLUXO ----------
s = prs.slides.add_slide(BLANK); bg(s); header(s, 'Objetivo', 2)
txt(s, Inches(0.6), Inches(1.5), Inches(12), Inches(1.2),
    'Desenvolver uma esteira de CI/CD aplicando práticas de DevSecOps: uma aplicação '
    'simples em container, com integração e deploy automatizados e segurança integrada '
    'ao pipeline (shift-left).', size=20, color=WHITE)
# Fluxo em caixas
etapas = ['Código', 'Build', 'Teste', 'Security\nScan', 'Imagem\nDocker', 'Deploy', 'Container']
n = len(etapas); bw = Inches(1.55); gap = Inches(0.15)
total = n*bw + (n-1)*gap
startx = (SW - total)//2
y = Inches(4.0)
for i, e in enumerate(etapas):
    x = startx + i*(bw+gap)
    c = GREEN if e in ('Security\nScan',) else PANEL
    box(s, x, y, bw, Inches(1.1), c)
    txt(s, x, y, bw, Inches(1.1), e, size=14, color=WHITE, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    if i < n-1:
        txt(s, x+bw-Inches(0.05), y, gap+Inches(0.1), Inches(1.1), '›',
            size=24, color=CYAN, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
txt(s, Inches(0.6), Inches(5.6), Inches(12), Inches(0.6),
    'A segurança é executada automaticamente a cada alteração, antes do deploy.',
    size=16, color=GREY, align=PP_ALIGN.CENTER)

# ---------- SLIDE 3 - CENARIO + APLICACAO ----------
s = prs.slides.add_slide(BLANK); bg(s); header(s, 'Cenário e Aplicação', 3)
box(s, Inches(0.6), Inches(1.5), Inches(5.9), Inches(4.8), PANEL)
txt(s, Inches(0.9), Inches(1.7), Inches(5.4), Inches(0.5), 'Cenário', size=20, color=CYAN, bold=True)
txt(s, Inches(0.9), Inches(2.3), Inches(5.4), Inches(3.8),
    'A TechSecure Solutions quer reduzir erros de implantação e incorporar segurança '
    'ao ciclo de desenvolvimento.\n\nCada grupo cria uma prova de conceito de esteira '
    'CI/CD automatizada, do commit ao container em execução.', size=17, color=WHITE)
box(s, Inches(6.8), Inches(1.5), Inches(5.9), Inches(4.8), PANEL)
txt(s, Inches(7.1), Inches(1.7), Inches(5.4), Inches(0.5), 'Aplicação (PoC)', size=20, color=CYAN, bold=True)
txt(s, Inches(7.1), Inches(2.3), Inches(5.4), Inches(0.6),
    'API REST de tarefas em Node.js + Express (dados em memória).', size=16, color=WHITE)
bullets(s, Inches(7.1), Inches(3.3), Inches(5.4), Inches(2.8), [
    ('GET /  — status da aplicação', GREY),
    ('GET /health  — healthcheck', GREY),
    ('GET /tarefas  — lista tarefas', GREY),
    ('POST /tarefas  — cria tarefa (valida payload)', GREY),
], size=15)

# ---------- SLIDE 4 - TECNOLOGIAS ----------
s = prs.slides.add_slide(BLANK); bg(s); header(s, 'Tecnologias', 4)
cols = [
    ('Versionamento', ['Git', 'GitHub'], CYAN),
    ('CI/CD', ['GitHub Actions'], GREEN),
    ('Container', ['Docker', 'node:20-alpine', 'usuário não-root'], YELLOW),
    ('Testes', ['Jest', 'Supertest'], CYAN),
    ('Segurança', ['Trivy (fs + imagem)', 'npm audit (SCA)'], RED),
]
cw = Inches(2.3); gap = Inches(0.15)
total = len(cols)*cw + (len(cols)-1)*gap
startx = (SW-total)//2
for i, (titulo, itens, c) in enumerate(cols):
    x = startx + i*(cw+gap)
    box(s, x, Inches(2.0), cw, Inches(3.6), PANEL)
    box(s, x, Inches(2.0), cw, Inches(0.7), c)
    txt(s, x, Inches(2.0), cw, Inches(0.7), titulo, size=15, color=DARK, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    txt(s, x+Inches(0.15), Inches(2.9), cw-Inches(0.3), Inches(2.5),
        '\n'.join(itens), size=15, color=WHITE, align=PP_ALIGN.CENTER)

# ---------- SLIDE 5 - PIPELINE ----------
s = prs.slides.add_slide(BLANK); bg(s); header(s, 'A Pipeline (GitHub Actions)', 5)
txt(s, Inches(0.6), Inches(1.45), Inches(12), Inches(0.5),
    'Disparada automaticamente a cada push / pull request na branch main — 3 jobs encadeados:',
    size=16, color=GREY)
jobs = [
    ('1 · build-test', ['Instala dependências (build)', 'Executa testes (Jest)', '5/5 • 100% cobertura'], GREEN),
    ('2 · security-scan', ['npm audit (dependências)', 'Trivy (filesystem)', 'Relatório como artefato'], YELLOW),
    ('3 · build-deploy', ['Build da imagem Docker', 'Trivy na imagem', 'Deploy + smoke test'], CYAN),
]
cw = Inches(3.9); gap = Inches(0.25)
total = len(jobs)*cw + (len(jobs)-1)*gap
startx = (SW-total)//2
for i, (titulo, itens, c) in enumerate(jobs):
    x = startx + i*(cw+gap)
    box(s, x, Inches(2.2), cw, Inches(3.6), PANEL)
    box(s, x, Inches(2.2), cw, Inches(0.8), c)
    txt(s, x, Inches(2.2), cw, Inches(0.8), titulo, size=18, color=DARK, bold=True,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    bullets(s, x+Inches(0.3), Inches(3.3), cw-Inches(0.5), Inches(2.3),
            [(it, WHITE) for it in itens], size=15, gap=10)
    if i < len(jobs)-1:
        txt(s, x+cw-Inches(0.05), Inches(2.2), gap+Inches(0.2), Inches(3.6), '→',
            size=28, color=GREEN, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)

# ---------- SLIDE 6 - ANALISE DE SEGURANCA ----------
s = prs.slides.add_slide(BLANK); bg(s); header(s, 'Análise de Segurança — Achado', 6)
box(s, Inches(0.6), Inches(1.6), Inches(12.1), Inches(4.6), PANEL)
linhas = [
    ('Vulnerabilidade', 'braces — stack-exhaustion Denial of Service (GHSA-vfj7-8cjw-p6xm)', RED),
    ('Componente', 'pacote braces (transitivo: micromatch → jest)', WHITE),
    ('Severidade', 'HIGH (Alta)', RED),
    ('Detecção', 'automática via npm audit na pipeline', WHITE),
    ('Correção', 'npm audit fix --force  /  fixar braces >= 3.0.3 em overrides', GREEN),
    ('Mitigação', 'é devDependency; Dockerfile usa --omit=dev → não vai p/ produção', GREEN),
]
y = Inches(1.9)
for k, v, c in linhas:
    txt(s, Inches(1.0), y, Inches(2.8), Inches(0.6), k, size=16, color=CYAN, bold=True)
    txt(s, Inches(3.9), y, Inches(8.5), Inches(0.6), v, size=16, color=c)
    y += Inches(0.68)

# ---------- SLIDES 7-9 - EVIDENCIAS (imagens) ----------
evid_slides = [
    ('Evidência — Pipeline e Testes', ['01_pipeline_geral.png', '02_build_testes.png']),
    ('Evidência — Security Scan', ['03_security_npm_audit.png', '06_trivy_imagem.png']),
    ('Evidência — Build, Deploy e App no ar', ['05_docker_build.png', '07_deploy_container.png']),
]
num = 7
for titulo, imgs in evid_slides:
    s = prs.slides.add_slide(BLANK); bg(s); header(s, titulo, num)
    iw = Inches(6.0)
    xs = [Inches(0.55), Inches(6.85)]
    for x, img in zip(xs, imgs):
        caminho = os.path.join(EVID, img)
        if os.path.exists(caminho):
            s.shapes.add_picture(caminho, x, Inches(2.0), width=iw)
    num += 1

# ---------- SLIDE 10 - DEMONSTRACAO ----------
s = prs.slides.add_slide(BLANK); bg(s); header(s, 'Demonstração ao Vivo', 10)
bullets(s, Inches(0.9), Inches(1.8), Inches(11.5), Inches(5), [
    ('Aplicação funcionando no container', WHITE),
    ('Alteração simples no código', WHITE),
    ('Commit e push para o GitHub', WHITE),
    ('Pipeline iniciando automaticamente', GREEN),
    ('Build → Teste → Security scan', GREEN),
    ('Build da imagem Docker → Deploy', GREEN),
    ('Aplicação atualizada e no ar', WHITE),
], size=22, gap=12)

# ---------- SLIDE 11 - CONCLUSAO ----------
s = prs.slides.add_slide(BLANK); bg(s); header(s, 'Conclusão', 11)
txt(s, Inches(0.8), Inches(1.9), Inches(11.7), Inches(3.5),
    'Construímos uma esteira CI/CD com segurança integrada (DevSecOps). Todo código '
    'enviado ao repositório passa por build, testes e análise de segurança antes do '
    'deploy — deslocando a segurança para o início do ciclo (shift-left).\n\n'
    'O achado de vulnerabilidade identificado automaticamente comprova o valor de '
    'integrar verificações de segurança ao pipeline, reduzindo riscos antes da '
    'aplicação chegar ao ambiente de execução.', size=20, color=WHITE)
txt(s, Inches(0.8), Inches(5.7), Inches(11.7), Inches(0.8),
    'github.com/vitoremanuel-lgtm/devsecops-ap2', size=16, color=CYAN, bold=True)

# ---------- SLIDE 12 - OBRIGADO ----------
s = prs.slides.add_slide(BLANK); bg(s)
box(s, 0, 0, SW, Inches(0.25), GREEN)
txt(s, Inches(1), Inches(2.8), Inches(11.3), Inches(1.2),
    'Obrigado!', size=54, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
txt(s, Inches(1), Inches(4.2), Inches(11.3), Inches(0.8),
    'Perguntas?', size=24, color=CYAN, align=PP_ALIGN.CENTER)
box(s, 0, SH-Inches(0.25), SW, Inches(0.25), GREEN)

prs.save(OUT)
print('Apresentacao gerada:', OUT)
print('Total de slides:', len(prs.slides._sldIdLst))
