const express = require('express');

const app = express();
app.use(express.json());

// Lista simples em memoria (PoC - sem banco de dados)
const tarefas = [
  { id: 1, titulo: 'Configurar pipeline CI/CD', concluida: false },
  { id: 2, titulo: 'Rodar scan de seguranca', concluida: false },
];

app.get('/', (req, res) => {
  res.json({
    app: 'TechSecure Solutions - Gestor de Tarefas',
    status: 'online',
    versao: '1.0.0',
  });
});

// Healthcheck usado pelo Docker e pelo deploy
app.get('/health', (req, res) => {
  res.status(200).json({ status: 'ok' });
});

app.get('/tarefas', (req, res) => {
  res.json(tarefas);
});

app.post('/tarefas', (req, res) => {
  const { titulo } = req.body;
  if (!titulo || typeof titulo !== 'string') {
    return res.status(400).json({ erro: 'titulo e obrigatorio' });
  }
  const nova = { id: tarefas.length + 1, titulo, concluida: false };
  tarefas.push(nova);
  res.status(201).json(nova);
});

module.exports = app;
