# -*- coding: utf-8 -*-
"""Gera os quadros (1080p) do video demonstrativo do projeto AP II DevSecOps.
Sem audio - legendas na tela. Encoda depois com ffmpeg (concat)."""
import os
from PIL import Image, ImageDraw, ImageFont

EVID = r'C:\dev\devsecops-ap2\docs\evidencias'
FRAMES = r'C:\dev\devsecops-ap2\docs\video_frames'
os.makedirs(FRAMES, exist_ok=True)

W, H = 1920, 1080
DARK = (13, 17, 23)
PANEL = (22, 27, 34)
WHITE = (240, 246, 252)
GREY = (176, 186, 197)
GREEN = (63, 185, 80)
CYAN = (88, 166, 255)
RED = (248, 81, 73)
YELLOW = (210, 153, 34)

def font(size, bold=False):
    paths = [r'C:\Windows\Fonts\segoeuib.ttf'] if bold else [r'C:\Windows\Fonts\segoeui.ttf']
    paths += [r'C:\Windows\Fonts\arial.ttf']
    for p in paths:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def mono(size):
    for p in [r'C:\Windows\Fonts\consola.ttf', r'C:\Windows\Fonts\cour.ttf']:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def center_text(d, cx, y, text, f, fill):
    bb = d.textbbox((0, 0), text, font=f)
    w = bb[2]-bb[0]
    d.text((cx - w/2, y), text, font=f, fill=fill)

def base():
    img = Image.new('RGB', (W, H), DARK)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 10], fill=GREEN)
    d.rectangle([0, H-10, W, H], fill=GREEN)
    return img, d

def topbar(d, step_label, step_num, total=9):
    # barra de progresso das etapas
    d.rectangle([0, 0, W, 70], fill=PANEL)
    d.text((40, 18), 'AP II — DevSecOps  •  Esteira CI/CD Segura  •  TechSecure Solutions',
           font=font(24, True), fill=WHITE)
    if step_num:
        d.text((W-360, 20), f'Etapa {step_num}/{total}', font=font(22, True), fill=CYAN)
    if step_label:
        d.text((40, 90), step_label, font=font(40, True), fill=WHITE)
        d.rectangle([44, 150, 300, 157], fill=GREEN)

frames = []  # (filename, seconds)

DUR_MULT = 2.3  # alonga as cenas para atingir ~5 min
def save(name, img, secs):
    path = os.path.join(FRAMES, name)
    img.save(path)
    frames.append((name, round(secs*DUR_MULT, 1)))

def legend_box(d, lines, x=40, y=185, w=1840):
    # caixa de legenda explicativa
    bh = 40 + len(lines)*52
    d.rounded_rectangle([x, y, x+w, y+bh], radius=16, fill=PANEL)
    yy = y+22
    for text, color in lines:
        d.text((x+28, yy), text, font=font(28), fill=color)
        yy += 52
    return y+bh

def add_evidence(img, d, img_file, top):
    ev = Image.open(os.path.join(EVID, img_file)).convert('RGB')
    maxw = 1500
    scale = maxw / ev.width
    nw, nh = maxw, int(ev.height*scale)
    maxh = H - top - 60
    if nh > maxh:
        scale = maxh / ev.height
        nw, nh = int(ev.width*scale), maxh
    ev = ev.resize((nw, nh))
    x = (W-nw)//2
    # moldura
    d.rounded_rectangle([x-8, top-8, x+nw+8, top+nh+8], radius=12, outline=(48,54,61), width=3)
    img.paste(ev, (x, top))

# ===================== CENA 1: CAPA =====================
img, d = base()
center_text(d, W/2, 300, 'AP II — DevSecOps', font(96, True), WHITE)
center_text(d, W/2, 440, 'Construção de uma Esteira CI/CD Segura', font(48), CYAN)
center_text(d, W/2, 540, 'Empresa fictícia: TechSecure Solutions', font(34), GREY)
center_text(d, W/2, 700, 'Vídeo demonstrativo da esteira (sem áudio — legendas na tela)', font(28), GREY)
center_text(d, W/2, 760, 'O apresentador está sem microfone; segue a demonstração legendada.', font(24), GREY)
save('s01_capa.png', img, 6)

# ===================== CENA 2: INTEGRANTES =====================
img, d = base()
center_text(d, W/2, 220, 'Integrantes do grupo', font(60, True), WHITE)
d.rectangle([W/2-130, 310, W/2+130, 318], fill=GREEN)
nomes = [
    'Vitor Emanuel Santiago — RA 2501093',
    'Rafael Neves — RA 2503380',
    'Guilherme Lopes — RA 2502595',
    'Viniccius Cezario — RA 2504060',
]
y = 420
for n in nomes:
    center_text(d, W/2, y, n, font(38), WHITE)
    y += 90
save('s02_integrantes.png', img, 6)

# ===================== CENA 3: ARQUITETURA =====================
img, d = base(); topbar(d, 'Arquitetura da Solução', 1)
legend_box(d, [
    ('Fluxo: Código → Build → Teste → Security Scan → Imagem → Deploy → Container.', WHITE),
    ('Git aciona a pipeline no GitHub Actions a cada push; o deploy só ocorre se tudo passar.', GREY),
], y=185)
# diagrama simples
etapas = ['Código', 'Build', 'Teste', 'Security\nScan', 'Imagem\nDocker', 'Deploy', 'Container']
bw, bh, gap = 220, 150, 40
total = len(etapas)*bw + (len(etapas)-1)*gap
sx = (W-total)//2; y = 560
for i, e in enumerate(etapas):
    x = sx + i*(bw+gap)
    c = GREEN if 'Security' in e else PANEL
    d.rounded_rectangle([x, y, x+bw, y+bh], radius=14, fill=c)
    lines = e.split('\n')
    yy = y + bh/2 - len(lines)*22
    for ln in lines:
        center_text(d, x+bw/2, yy, ln, font(30, True), WHITE if c==GREEN else WHITE)
        yy += 44
    if i < len(etapas)-1:
        d.text((x+bw+6, y+bh/2-28), '›', font=font(56), fill=CYAN)
save('s03_arquitetura.png', img, 9)

# ===================== CENA 4: APLICACAO =====================
img, d = base(); topbar(d, 'Aplicação Escolhida', 2)
legend_box(d, [
    ('API REST de tarefas em Node.js + Express (dados em memória).', WHITE),
    ('App simples de propósito: o foco é a esteira CI/CD segura.', GREY),
], y=185)
rotas = [
    ('GET  /',         'status da aplicação'),
    ('GET  /health',   'healthcheck (usado pelo Docker/deploy)'),
    ('GET  /tarefas',  'lista as tarefas'),
    ('POST /tarefas',  'cria tarefa (valida o payload)'),
]
y = 470
d.rounded_rectangle([360, y-30, W-360, y+360], radius=16, fill=PANEL)
yy = y+10
for r, desc in rotas:
    d.text((420, yy), r, font=mono(34), fill=GREEN)
    d.text((820, yy), '—  '+desc, font=font(30), fill=WHITE)
    yy += 85
save('s04_aplicacao.png', img, 9)

# ===================== CENA 5: REPOSITORIO =====================
img, d = base(); topbar(d, 'Repositório (Git / GitHub)', 3)
legend_box(d, [
    ('Código-fonte versionado no GitHub; o push dispara a pipeline automaticamente.', WHITE),
    ('github.com/vitoremanuel-lgtm/devsecops-ap2', CYAN),
], y=185)
estrut = [
    'devsecops-ap2/',
    '├── src/                 # app.js, server.js',
    '├── test/                # testes automatizados (Jest)',
    '├── .github/workflows/',
    '│      └── ci-cd.yml      # a esteira CI/CD',
    '├── Dockerfile            # imagem segura (não-root)',
    '├── docs/                 # relatório, prints, apresentação',
    '└── README.md',
]
y = 460
d.rounded_rectangle([360, y-30, W-360, y+30+len(estrut)*48], radius=16, fill=PANEL)
yy = y
for ln in estrut:
    d.text((420, yy), ln, font=mono(30), fill=WHITE)
    yy += 48
save('s05_repositorio.png', img, 8)

# ===================== CENAS DE EVIDENCIA =====================
def evid_scene(name, step_label, step_num, legend_lines, img_file, secs):
    img, d = base(); topbar(d, step_label, step_num)
    bottom = legend_box(d, legend_lines, y=185)
    add_evidence(img, d, img_file, bottom+30)
    save(name, img, secs)

evid_scene('s06_pipeline.png', 'Pipeline no GitHub Actions', 4,
    [('A cada push, os 3 jobs rodam encadeados — todos concluíram com sucesso.', WHITE),
     ('Build e Testes → Análise de Segurança → Build da Imagem e Deploy.', GREY)],
    '01_pipeline_geral.png', 11)

evid_scene('s07_build.png', 'Build e Testes Automatizados', 5,
    [('npm install (build) + Jest: 5 testes, 5 aprovados, 100% de cobertura.', WHITE)],
    '02_build_testes.png', 11)

evid_scene('s08_audit.png', 'Security Scan — npm audit', 6,
    [('Análise de dependências detectou automaticamente uma vulnerabilidade HIGH.', WHITE),
     ('Achado: braces — Denial of Service (GHSA-vfj7-8cjw-p6xm).', RED)],
    '03_security_npm_audit.png', 11)

evid_scene('s09_trivy.png', 'Security Scan — Trivy na imagem', 6,
    [('O Trivy também escaneia a imagem Docker gerada antes do deploy.', WHITE)],
    '06_trivy_imagem.png', 9)

evid_scene('s10_docker.png', 'Build da Imagem Docker', 7,
    [('Imagem construída a partir de node:20-alpine, usuário não-root, só deps de produção.', WHITE)],
    '05_docker_build.png', 10)

evid_scene('s11_deploy.png', 'Deploy Automático — Container no ar', 8,
    [('Deploy sobe o container; docker ps confirma a aplicação em execução na porta 3000.', WHITE)],
    '07_deploy_container.png', 10)

evid_scene('s12_app.png', 'Aplicação Funcionando', 9,
    [('Smoke test no endpoint /health retorna HTTP 200 — deploy validado.', WHITE),
     ('{"status":"ok"}', GREEN)],
    '08_app_funcionando.png', 9)

# ===================== CENA: ACHADO DE SEGURANCA =====================
img, d = base(); topbar(d, 'Análise de Segurança — Achado', 0)
y = 230
linhas = [
    ('Vulnerabilidade', 'braces — stack-exhaustion Denial of Service', RED),
    ('Advisory', 'GHSA-vfj7-8cjw-p6xm', CYAN),
    ('Componente', 'pacote braces (transitivo: micromatch → jest)', WHITE),
    ('Severidade', 'HIGH (Alta)', RED),
    ('Correção', 'npm audit fix --force  /  fixar braces >= 3.0.3', GREEN),
    ('Mitigação', 'é devDependency; Dockerfile usa --omit=dev (fora da produção)', GREEN),
]
d.rounded_rectangle([200, y, W-200, y+620], radius=18, fill=PANEL)
yy = y+40
for k, v, c in linhas:
    d.text((260, yy), k, font=font(32, True), fill=CYAN)
    d.text((720, yy), v, font=font(32), fill=c)
    yy += 95
save('s13_achado.png', img, 11)

# ===================== CENA: CONCLUSAO =====================
img, d = base()
center_text(d, W/2, 240, 'Conclusão', font(70, True), WHITE)
d.rectangle([W/2-120, 340, W/2+120, 348], fill=GREEN)
txt_lines = [
    'Construímos uma esteira CI/CD com segurança integrada (DevSecOps).',
    'Todo código passa por build, testes e análise de segurança antes do deploy.',
    'Segurança deslocada para o início do ciclo — shift-left.',
    'A vulnerabilidade foi identificada automaticamente pela pipeline.',
]
y = 430
for ln in txt_lines:
    center_text(d, W/2, y, ln, font(32), WHITE)
    y += 75
center_text(d, W/2, 820, 'github.com/vitoremanuel-lgtm/devsecops-ap2', font(30, True), CYAN)
save('s14_conclusao.png', img, 9)

# ===================== CENA: FIM =====================
img, d = base()
center_text(d, W/2, 420, 'Obrigado!', font(100, True), WHITE)
center_text(d, W/2, 580, 'TechSecure Solutions — AP II DevSecOps', font(34), CYAN)
save('s15_fim.png', img, 5)

# ===================== gerar lista para ffmpeg =====================
listpath = os.path.join(FRAMES, 'lista.txt')
with open(listpath, 'w', encoding='utf-8') as f:
    for name, secs in frames:
        f.write(f"file '{name}'\n")
        f.write(f"duration {secs}\n")
    # ultima imagem repetida (exigencia do concat demuxer)
    f.write(f"file '{frames[-1][0]}'\n")

total = sum(s for _, s in frames)
print(f'{len(frames)} cenas geradas. Duracao total: {total}s (~{total//60}min {total%60}s)')
print('Lista:', listpath)
