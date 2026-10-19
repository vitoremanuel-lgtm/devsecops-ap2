const request = require('supertest');
const app = require('../src/app');

describe('TechSecure API', () => {
  test('GET / retorna status online', async () => {
    const res = await request(app).get('/');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('online');
  });

  test('GET /health retorna ok', async () => {
    const res = await request(app).get('/health');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('ok');
  });

  test('GET /tarefas retorna uma lista', async () => {
    const res = await request(app).get('/tarefas');
    expect(res.statusCode).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
  });

  test('POST /tarefas cria uma tarefa valida', async () => {
    const res = await request(app)
      .post('/tarefas')
      .send({ titulo: 'Nova tarefa de teste' });
    expect(res.statusCode).toBe(201);
    expect(res.body.titulo).toBe('Nova tarefa de teste');
  });

  test('POST /tarefas rejeita payload invalido', async () => {
    const res = await request(app).post('/tarefas').send({});
    expect(res.statusCode).toBe(400);
  });
});
