# -*- coding: utf-8 -*-
"""Screencast animado estilo gravacao de tela: um dev digitando no terminal.
Gera frames + lista para ffmpeg (concat com duracoes variaveis)."""
import os, shutil
from PIL import Image, ImageDraw, ImageFont

FRAMES = r'C:\dev\devsecops-ap2\docs\sc_frames2'
if os.path.exists(FRAMES):
    shutil.rmtree(FRAMES)
os.makedirs(FRAMES)

W, H = 1920, 1080
# paleta do GNOME Terminal do Ubuntu (tema aubergine)
TERM_BG = (48, 10, 36)      # #300A24 - fundo classico do terminal Ubuntu
DESK = (30, 6, 22)          # borda
TITLE_BG = (47, 47, 47)     # headerbar Yaru (cinza escuro)
WHITE = (235, 235, 235)     # texto padrao
GREY = (178, 178, 178)      # texto secundario
GREEN = (115, 210, 90)      # sucesso / verde bash
CYAN = (52, 226, 226)
BLUE = (114, 159, 207)      # azul de diretorio do bash
RED = (239, 85, 85)         # erro
YELLOW = (233, 205, 90)     # aviso
MAGENTA = (173, 127, 168)
UB_GREEN = (138, 226, 52)   # user@host (verde bold do PS1 Ubuntu)
UB_BLUE = (114, 159, 207)   # diretorio (azul bold do PS1 Ubuntu)
PROMPT_C = WHITE

def mono(size):
    for p in [r'C:\Windows\Fonts\consola.ttf', r'C:\Windows\Fonts\cour.ttf']:
        if os.path.exists(p):
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()

def ui(size, bold=False):
    p = r'C:\Windows\Fonts\segoeui.ttf'
    if bold: p = r'C:\Windows\Fonts\segoeuib.ttf'
    if os.path.exists(p): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

FONT = mono(26)
LH = 36
MARGIN_X = 48
_tmp = Image.new('RGB', (10, 10))
CW = ImageDraw.Draw(_tmp).textlength('M', font=FONT)  # largura de caractere (monoespacada)

def draw_mono(d, x, y, text, color):
    """desenha texto monoespacado; '✓' e desenhado a mao (fontes nao tem o glifo)."""
    for ch in text:
        if ch in '✓✓':
            d.line([(x+CW*0.18, y+LH*0.52), (x+CW*0.42, y+LH*0.74), (x+CW*0.86, y+LH*0.26)],
                   fill=color, width=3, joint='curve')
        else:
            d.text((x, y), ch, font=FONT, fill=color)
        x += CW
    return x
TOP = 150          # inicio da area de texto
TITLEBAR = 64
CAP_TOP = 902      # inicio da faixa de legenda (narracao escrita)
MAXLINES = (CAP_TOP - TOP - 10) // LH

# estado do terminal: lista de (texto, cor)
buf = []
frames = []   # (filename, dur_segundos)
_counter = [0]
CAP = {'text': ''}

def set_caption(text):
    CAP['text'] = text

def _wrap(d, text, f, maxw):
    words = text.split(' ')
    lines, cur = [], ''
    for w in words:
        test = (cur + ' ' + w).strip()
        if d.textlength(test, font=f) <= maxw:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def visible_lines():
    return buf[-MAXLINES:] if len(buf) > MAXLINES else buf

def draw_frame(active=None, cursor=True):
    img = Image.new('RGB', (W, H), DESK)
    d = ImageDraw.Draw(img)
    # headerbar estilo GNOME Terminal (Yaru)
    d.rectangle([0, 0, W, TITLEBAR], fill=TITLE_BG)
    titulo = 'vitor@ubuntu: ~/devsecops-ap2'
    tf = ui(26)
    tw = d.textlength(titulo, font=tf)
    d.text(((W-tw)/2, 16), titulo, font=tf, fill=(220, 220, 220))
    # botoes GNOME (minimizar, maximizar, fechar) como circulos Yaru
    cy = TITLEBAR//2
    for i, cx in enumerate([W-170, W-115, W-60]):
        col = (60, 60, 60)
        d.ellipse([cx-18, cy-18, cx+18, cy+18], fill=col)
    # simbolos
    d.line([W-179, cy, W-161, cy], fill=(210,210,210), width=2)                 # _
    d.rectangle([W-124, cy-8, W-106, cy+8], outline=(210,210,210), width=2)     # []
    d.line([W-69, cy-7, W-51, cy+7], fill=(230,230,230), width=2)               # x
    d.line([W-69, cy+7, W-51, cy-7], fill=(230,230,230), width=2)
    d.rectangle([0, TITLEBAR, W, H], fill=TERM_BG)
    # texto (suporta linha de cor unica (texto,cor) ou lista de segmentos [(t,c),...])
    y = TOP
    for entry in visible_lines():
        if isinstance(entry[0], list):
            x = MARGIN_X
            for t, c in entry[0]:
                x = draw_mono(d, x, y, t, c)
        else:
            text, color = entry
            draw_mono(d, MARGIN_X, y, text, color)
        y += LH
    # linha ativa (digitacao)
    if active is not None:
        segs, partial = active
        x = MARGIN_X
        for t, c in segs:
            x = draw_mono(d, x, y, t, c)
        x = draw_mono(d, x, y, partial, WHITE)
        if cursor:
            d.rectangle([x+2, y+4, x+16, y+LH-6], fill=WHITE)
    # faixa de legenda (narracao escrita)
    d.rectangle([0, CAP_TOP, W, H], fill=(18, 20, 32))
    d.rectangle([0, CAP_TOP, W, CAP_TOP+5], fill=GREEN)
    if CAP['text']:
        capf = ui(32, True)
        lines = _wrap(d, CAP['text'], capf, W-260)
        # marcador triangular desenhado
        tx, ty = 52, CAP_TOP+44
        d.polygon([(tx, ty-14), (tx, ty+14), (tx+22, ty)], fill=GREEN)
        yy = CAP_TOP + 30 if len(lines) > 1 else CAP_TOP + 48
        for ln in lines[:2]:
            d.text((120, yy), ln, font=capf, fill=WHITE)
            yy += 46
    return img

def emit(dur, active=None, cursor=True):
    img = draw_frame(active=active, cursor=cursor)
    name = f'f{_counter[0]:05d}.png'
    img.save(os.path.join(FRAMES, name))
    frames.append((name, round(dur, 3)))
    _counter[0] += 1

PROMPT = [('vitor@ubuntu', UB_GREEN), (':', WHITE), ('~/devsecops-ap2', UB_BLUE), ('$ ', WHITE)]

def type_cmd(cmd, cps=0.07):
    """digita um comando char a char apos o prompt bash."""
    partial = ''
    # breve pausa com prompt vazio + cursor piscando
    emit(0.4, active=(PROMPT, ''), cursor=True)
    emit(0.3, active=(PROMPT, ''), cursor=False)
    for ch in cmd:
        partial += ch
        emit(cps, active=(PROMPT, partial), cursor=True)
    # enter: fixa a linha no buffer como segmentos coloridos (prompt + comando)
    buf.append((PROMPT + [(cmd, WHITE)],))
    emit(0.25)

def out(lines, per=0.14, read=0.0):
    """escreve linhas de saida progressivamente."""
    for item in lines:
        if isinstance(item, tuple):
            text, color = item
        else:
            text, color = item, WHITE
        buf.append((text, color))
        emit(per)
    if read:
        emit(read)

def pause(dur):
    emit(dur)

def blank(n=1):
    for _ in range(n):
        buf.append(('', WHITE))
    emit(0.05)

# ============================================================
# ROTEIRO (fluxo de um desenvolvedor)
# ============================================================
buf.append(('Welcome to Ubuntu 24.04.4 LTS (GNU/Linux 6.8.0 x86_64)', GREY))
buf.append(('', WHITE))
buf.append((' * Documentation:  https://help.ubuntu.com', GREY))
buf.append(('Last login: Sun Oct 19 01:03:58 2026 from 127.0.0.1', GREY))
buf.append(('', WHITE))
buf.append(('# AP II DevSecOps - Cenario: empresa ficticia TechSecure Solutions', GREEN))
buf.append(('# Demonstracao da esteira CI/CD segura (video sem audio)', GREY))
buf.append(('', WHITE))
set_caption('AP II DevSecOps: demonstracao da esteira CI/CD segura, do codigo ao container.')
pause(2.6)

# 1) rodar os testes localmente
set_caption('1. Primeiro rodamos os testes automatizados localmente com o Jest.')
type_cmd('npm test')
out([
    ('', WHITE),
    ('> techsecure-app@1.0.0 test', WHITE),
    ('> jest --coverage', WHITE),
    ('', WHITE),
    ('PASS test/app.test.js', GREEN),
    ('  TechSecure API', WHITE),
    ('    ✓ GET / retorna status online (37 ms)', GREEN),
    ('    ✓ GET /health retorna ok (9 ms)', GREEN),
    ('    ✓ GET /tarefas retorna uma lista (4 ms)', GREEN),
    ('    ✓ POST /tarefas cria uma tarefa valida (9 ms)', GREEN),
    ('    ✓ POST /tarefas rejeita payload invalido (3 ms)', GREEN),
    ('', WHITE),
    ('----------|---------|----------|---------|---------|', GREY),
    ('All files |     100 |      100 |     100 |     100 |', GREEN),
    ('----------|---------|----------|---------|---------|', GREY),
    ('Test Suites: 1 passed, 1 total', GREEN),
    ('Tests:       5 passed, 5 total', GREEN),
], per=0.16)
set_caption('Resultado: 5 testes aprovados e 100% de cobertura. Tudo verde.')
pause(3.0)
blank()

# 2) alterar o codigo
set_caption('2. Fizemos uma alteracao no codigo. O git mostra o arquivo modificado.')
type_cmd('git status --short')
out([('M  src/app.js', YELLOW)], per=0.2)
pause(2.2)
blank()

# 3) commit
set_caption('3. Registramos a alteracao: git add para preparar e git commit para salvar.')
type_cmd('git add -A')
pause(0.6)
type_cmd('git commit -m "Atualiza versao da aplicacao"')
out([
    ('[main 7b9b105] Atualiza versao da aplicacao', WHITE),
    (' 1 file changed, 1 insertion(+), 1 deletion(-)', GREY),
], per=0.2)
pause(2.4)
blank()

# 4) push -> dispara a pipeline
set_caption('4. git push envia o codigo ao GitHub - e isso dispara a pipeline automaticamente.')
type_cmd('git push')
out([
    ('Enumerating objects: 7, done.', GREY),
    ('Counting objects: 100% (7/7), done.', GREY),
    ('Compressing objects: 100% (4/4), done.', GREY),
    ('Writing objects: 100% (4/4), 480 bytes, done.', GREY),
    ('To https://github.com/vitoremanuel-lgtm/devsecops-ap2.git', WHITE),
    ('   650b90f..7b9b105  main -> main', GREEN),
], per=0.18)
pause(2.4)
blank()

# 5) acompanhar a pipeline (gh run watch) - simula atualizacao in-place
set_caption('5. Acompanhamos a pipeline no GitHub Actions executando em tempo real.')
type_cmd('gh run watch')
out([
    ('Refreshing run status every 3 seconds. Press Ctrl+C to quit.', GREY),
    ('', WHITE),
    ('* main CI/CD Seguro - TechSecure  39183655918', WHITE),
    ('', WHITE),
    ('JOBS', YELLOW),
], per=0.15)

# linhas dos jobs que vao mudando de estado
job_idx_base = len(buf)
buf.append(('  * Build e Testes', YELLOW))
buf.append(('  * Analise de Seguranca', GREY))
buf.append(('  * Build da Imagem e Deploy', GREY))
i1, i2, i3 = job_idx_base, job_idx_base+1, job_idx_base+2
emit(0.6)
# spinner frames
spin = ['|', '/', '-', '\\']
for k in range(8):
    buf[i1] = (f'  {spin[k%4]} Build e Testes   (executando...)', YELLOW)
    emit(0.35)
buf[i1] = ('  ✓ Build e Testes   in 20s', GREEN)
set_caption('Etapa 1 concluida: build e testes passaram. Agora roda a analise de seguranca.')
buf[i2] = ('  * Analise de Seguranca   (executando...)', YELLOW)
emit(0.6)
for k in range(8):
    buf[i2] = (f'  {spin[k%4]} Analise de Seguranca   (npm audit + Trivy)', YELLOW)
    emit(0.35)
buf[i2] = ('  ✓ Analise de Seguranca   in 40s', GREEN)
set_caption('Etapa 2 concluida: npm audit e Trivy executados. Por fim, build da imagem e deploy.')
buf[i3] = ('  * Build da Imagem e Deploy   (executando...)', YELLOW)
emit(0.6)
for k in range(10):
    buf[i3] = (f'  {spin[k%4]} Build da Imagem e Deploy   (docker build + deploy)', YELLOW)
    emit(0.35)
buf[i3] = ('  ✓ Build da Imagem e Deploy   in 42s', GREEN)
emit(0.6)
set_caption('Pipeline concluida com sucesso: os 3 estagios passaram do commit ao deploy.')
out([
    ('', WHITE),
    ('✓ Run CI/CD Seguro - TechSecure completed with "success"', GREEN),
], per=0.3)
pause(3.2)
blank()

# 6) ver o achado de seguranca
set_caption('6. A analise de seguranca encontrou uma vulnerabilidade: braces, severidade HIGH.')
type_cmd('gh run view --log | grep braces')
out([
    ('security-scan  npm audit  # npm audit report', WHITE),
    ('security-scan  npm audit  braces  *', RED),
    ('security-scan  npm audit  Severity: high', RED),
    ('security-scan  npm audit  braces vulnerable to stack-exhaustion', WHITE),
    ('security-scan  npm audit  denial of service (GHSA-vfj7-8cjw-p6xm)', WHITE),
], per=0.2)
set_caption('Correcao: atualizar o pacote; e por ser dependencia de dev, nao vai para a imagem de producao.')
pause(3.4)
blank()

# 7) confirmar container no ar
set_caption('7. O deploy subiu a aplicacao em um container Docker, rodando na porta 3000.')
type_cmd('docker ps')
out([
    ('CONTAINER ID   IMAGE                   STATUS          PORTS                    NAMES', GREY),
    ('0dfc6475dee8   techsecure-app:latest   Up 5 seconds    0.0.0.0:3000->3000/tcp   techsecure-app', GREEN),
], per=0.25)
pause(2.6)
blank()

# 8) testar a app
set_caption('8. Por fim, testamos a aplicacao no ar: ela responde normalmente as requisicoes.')
type_cmd('curl http://localhost:3000/health')
out([('{"status":"ok"}', GREEN)], per=0.3)
pause(1.8)
type_cmd('curl http://localhost:3000/')
out([
    ('{', WHITE),
    ('  "app": "TechSecure Solutions - Gestor de Tarefas",', WHITE),
    ('  "status": "online",', GREEN),
    ('  "versao": "1.0.0"', WHITE),
    ('}', WHITE),
], per=0.18)
set_caption('Esteira CI/CD segura funcionando de ponta a ponta: codigo, testes, seguranca, imagem, deploy e container.')
pause(3.0)
blank()

set_caption('Obrigado!  |  Vitor, Rafael, Guilherme e Viniccius  |  github.com/vitoremanuel-lgtm/devsecops-ap2')
type_cmd('# Esteira CI/CD segura funcionando de ponta a ponta. Obrigado!')
pause(4.0)

# ============================================================
# lista para ffmpeg
# ============================================================
listpath = os.path.join(FRAMES, 'lista.txt')
with open(listpath, 'w', encoding='utf-8') as f:
    for name, dur in frames:
        f.write(f"file '{name}'\n")
        f.write(f"duration {dur}\n")
    f.write(f"file '{frames[-1][0]}'\n")

total = sum(d for _, d in frames)
print(f'{len(frames)} frames. Duracao ~{int(total//60)}min {int(total%60)}s')
print('Lista:', listpath)
