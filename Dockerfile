# Imagem base enxuta e com correcoes de seguranca
FROM node:20-alpine

# Cria diretorio de trabalho
WORKDIR /app

# Copia manifestos e instala apenas dependencias de producao
COPY package*.json ./
RUN npm install --omit=dev

# Copia o codigo da aplicacao
COPY src ./src

# Boa pratica de seguranca: nao rodar como root
RUN addgroup -S appgrp && adduser -S appuser -G appgrp
USER appuser

EXPOSE 3000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD wget -qO- http://localhost:3000/health || exit 1

CMD ["node", "src/server.js"]
