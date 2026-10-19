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
# paleta CLASSICA do Windows PowerShell (console azul-marinho)
TERM_BG = (1, 36, 86)       # #012456 - azul classico do PowerShell
DESK = (1, 24, 56)          # borda levemente mais escura
TITLE_BG = (16, 32, 64)     # barra de titulo
WHITE = (238, 237, 240)     # texto padrao (cinza claro classico)
GREY = (170, 180, 200)      # texto secundario (legivel no azul)
GREEN = (102, 224, 140)     # sucesso
CYAN = (108, 214, 230)
BLUE = (140, 190, 255)
RED = (255, 120, 120)       # erro (vermelho legivel no azul)
YELLOW = (240, 215, 120)    # aviso
MAGENTA = (210, 170, 250)
PROMPT_C = WHITE            # no PowerShell classico o prompt usa a cor padrao

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
    # janela do terminal
    d.rectangle([0, 0, W, TITLEBAR], fill=TITLE_BG)
    # traffic lights / icone
    d.text((24, 16), 'Windows PowerShell', font=ui(26, True), fill=WHITE)
    d.text((W-460, 18), 'devsecops-ap2  —  C:\\dev', font=ui(22), fill=GREY)
    # botoes janela (desenhados)
    bx = W-150; by = 32
    d.line([bx, by, bx+18, by], fill=GREY, width=2)                       # minimizar
    d.rectangle([bx+40, by-9, bx+58, by+9], outline=GREY, width=2)        # maximizar
    d.line([bx+82, by-9, bx+100, by+9], fill=(220,120,120), width=2)      # fechar X
    d.line([bx+82, by+9, bx+100, by-9], fill=(220,120,120), width=2)
    d.rectangle([0, TITLEBAR, W, H], fill=TERM_BG)
    # texto
    y = TOP
    for text, color in visible_lines():
        d.text((MARGIN_X, y), text, font=FONT, fill=color)
        y += LH
    # linha ativa (digitacao)
    if active is not None:
        segs, partial = active
        x = MARGIN_X
        for t, c in segs:
            d.text((x, y), t, font=FONT, fill=c)
            x += d.textlength(t, font=FONT)
        d.text((x, y), partial, font=FONT, fill=WHITE)
        x += d.textlength(partial, font=FONT)
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

PROMPT = [('PS C:\\dev\\devsecops-ap2> ', WHITE)]

def type_cmd(cmd, cps=0.07):
    """digita um comando char a char apos o prompt."""
    partial = ''
    # breve pausa com prompt vazio + cursor piscando
    emit(0.4, active=(PROMPT, ''), cursor=True)
    emit(0.3, active=(PROMPT, ''), cursor=False)
    for ch in cmd:
        partial += ch
        emit(cps, active=(PROMPT, partial), cursor=True)
    # enter: fixa a linha no buffer
    line_segs = PROMPT + [(cmd, WHITE)]
    buf.append((''.join(t for t, _ in line_segs), WHITE))  # placeholder removido abaixo
    buf.pop()
    # armazena a linha composta como texto unico colorido (simplificacao: prompt+cmd)
    buf.append(('PS C:\\dev\\devsecops-ap2> ' + cmd, WHITE))
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
buf.append(('Windows PowerShell', GREY))
buf.append(('Copyright (C) Microsoft Corporation. Todos os direitos reservados.', GREY))
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
    ('    √ GET / retorna status online (37 ms)', GREEN),
    ('    √ GET /health retorna ok (9 ms)', GREEN),
    ('    √ GET /tarefas retorna uma lista (4 ms)', GREEN),
    ('    √ POST /tarefas cria uma tarefa valida (9 ms)', GREEN),
    ('    √ POST /tarefas rejeita payload invalido (3 ms)', GREEN),
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
buf[i1] = ('  √ Build e Testes   in 20s', GREEN)
set_caption('Etapa 1 concluida: build e testes passaram. Agora roda a analise de seguranca.')
buf[i2] = ('  * Analise de Seguranca   (executando...)', YELLOW)
emit(0.6)
for k in range(8):
    buf[i2] = (f'  {spin[k%4]} Analise de Seguranca   (npm audit + Trivy)', YELLOW)
    emit(0.35)
buf[i2] = ('  √ Analise de Seguranca   in 40s', GREEN)
set_caption('Etapa 2 concluida: npm audit e Trivy executados. Por fim, build da imagem e deploy.')
buf[i3] = ('  * Build da Imagem e Deploy   (executando...)', YELLOW)
emit(0.6)
for k in range(10):
    buf[i3] = (f'  {spin[k%4]} Build da Imagem e Deploy   (docker build + deploy)', YELLOW)
    emit(0.35)
buf[i3] = ('  √ Build da Imagem e Deploy   in 42s', GREEN)
emit(0.6)
set_caption('Pipeline concluida com sucesso: os 3 estagios passaram do commit ao deploy.')
out([
    ('', WHITE),
    ('√ Run CI/CD Seguro - TechSecure completed with "success"', GREEN),
], per=0.3)
pause(3.2)
blank()

# 6) ver o achado de seguranca
set_caption('6. A analise de seguranca encontrou uma vulnerabilidade: braces, severidade HIGH.')
type_cmd('gh run view --log | Select-String braces')
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
