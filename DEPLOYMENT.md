# Guia de Deploy - SteamExplorer

Este guia fornece instruções passo a passo para fazer o deploy da aplicação SteamExplorer.

## Arquitetura

- **Frontend**: React + Vite (deploy no Vercel)
- **Backend**: FastAPI + Python (deploy no Render)
- **Banco de Dados**: Redis (opcional, pode usar Redis Cloud ou Upstash)

---

## 1. Deploy do Backend (Render)

### Passo 1: Criar conta no Render
1. Acesse [render.com](https://render.com) e crie uma conta gratuita
2. Faça login

### Passo 2: Criar Web Service
1. No dashboard, clique em **"New +"** → **"Web Service"**
2. Conecte seu repositório GitHub: `LucasNSCLara/P4CEUB_FINAL_STEAM_DEPLOY`
3. Configure o serviço:
   - **Name**: `steamexplorer-backend` (ou nome de sua preferência)
   - **Region**: escolha a mais próxima
   - **Branch**: `main`
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Passo 3: Configurar Variáveis de Ambiente
Na seção **Environment**, adicione:

```
RAWG_API_KEY=sua_chave_rawg_aqui
REDIS_URL=redis://localhost:6379
ALLOWED_ORIGINS=https://seu-frontend.vercel.app
```

> **Importante**: 
> - Obtenha sua chave RAWG em [rawg.io/apidocs](https://rawg.io/apidocs)
> - Substitua `https://seu-frontend.vercel.app` pela URL real do Vercel (você obterá isso no próximo passo)
> - Para Redis, você pode usar o padrão local ou configurar Redis Cloud (gratuito)

### Passo 4: Deploy
1. Clique em **"Create Web Service"**
2. Aguarde o deploy (pode levar alguns minutos)
3. Anote a URL gerada (ex: `https://steamexplorer-backend.onrender.com`)

---

## 2. Deploy do Frontend (Vercel)

### Passo 1: Criar conta no Vercel
1. Acesse [vercel.com](https://vercel.com) e crie uma conta gratuita
2. Conecte com sua conta GitHub

### Passo 2: Importar Projeto
1. No dashboard, clique em **"Add New..."** → **"Project"**
2. Selecione o repositório: `LucasNSCLara/P4CEUB_FINAL_STEAM_DEPLOY`
3. Configure o projeto:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build` (padrão)
   - **Output Directory**: `dist` (padrão)

### Passo 3: Configurar Variáveis de Ambiente
Na seção **Environment Variables**, adicione:

```
VITE_API_URL=https://steamexplorer-backend.onrender.com
```

> **Importante**: Use a URL do backend que você anotou no Passo 4 do deploy do backend

### Passo 4: Deploy
1. Clique em **"Deploy"**
2. Aguarde o build e deploy
3. Anote a URL gerada (ex: `https://steamexplorer.vercel.app`)

### Passo 5: Atualizar CORS no Backend
1. Volte ao Render
2. Acesse seu serviço backend
3. Vá em **Environment**
4. Atualize `ALLOWED_ORIGINS` com a URL do Vercel:
   ```
   ALLOWED_ORIGINS=https://steamexplorer.vercel.app
   ```
5. Salve e aguarde o redeploy automático

---

## 3. Configuração do Redis (Opcional)

### Opção 1: Redis Cloud (Recomendado)
1. Acesse [redis.com/try-free](https://redis.com/try-free/)
2. Crie uma conta e um banco gratuito
3. Copie a URL de conexão
4. No Render, atualize `REDIS_URL` com a URL do Redis Cloud

### Opção 2: Upstash
1. Acesse [upstash.com](https://upstash.com)
2. Crie um banco Redis gratuito
3. Copie a URL de conexão
4. No Render, atualize `REDIS_URL`

### Opção 3: Sem Redis
- O app funcionará sem Redis, mas sem cache
- Mantenha `REDIS_URL=redis://localhost:6379` (o código trata erros de conexão)

---

## 4. Verificação

### Testar Backend
1. Acesse: `https://steamexplorer-backend.onrender.com/`
2. Deve retornar: `{"message": "Welcome to GameSphere Analytics API"}`
3. Teste a API: `https://steamexplorer-backend.onrender.com/api/game/cyberpunk`

### Testar Frontend
1. Acesse sua URL do Vercel
2. Busque por um jogo (ex: "Cyberpunk 2077")
3. Verifique se os dados aparecem corretamente

---

## 5. Troubleshooting

### Erro de CORS
- Verifique se `ALLOWED_ORIGINS` no backend inclui a URL exata do Vercel
- Não esqueça o `https://` e não adicione `/` no final

### Backend não inicia
- Verifique os logs no Render
- Confirme que `RAWG_API_KEY` está configurada
- Verifique se o `Start Command` está correto

### Frontend não conecta ao backend
- Verifique se `VITE_API_URL` está configurada no Vercel
- Confirme que a URL do backend está correta
- Abra o console do navegador para ver erros

### Redis não conecta
- Verifique a URL de conexão
- Se não quiser usar Redis, ignore os avisos nos logs

---

## 6. Atualizações Futuras

Sempre que fizer alterações no código:

1. **Commit e Push**:
   ```bash
   git add .
   git commit -m "Descrição das alterações"
   git push origin main
   ```

2. **Deploy Automático**:
   - Vercel e Render farão redeploy automaticamente
   - Acompanhe o progresso nos dashboards

---

## Resumo das URLs

Após o deploy, você terá:

- **Frontend**: `https://steamexplorer.vercel.app`
- **Backend**: `https://steamexplorer-backend.onrender.com`
- **API Docs**: `https://steamexplorer-backend.onrender.com/docs`

---

## Variáveis de Ambiente - Resumo

### Backend (Render)
```env
RAWG_API_KEY=sua_chave_aqui
REDIS_URL=redis://localhost:6379
ALLOWED_ORIGINS=https://steamexplorer.vercel.app
```

### Frontend (Vercel)
```env
VITE_API_URL=https://steamexplorer-backend.onrender.com
```

---

## Custos

- **Render Free Tier**: 750 horas/mês (suficiente para 1 serviço 24/7)
- **Vercel Free Tier**: Ilimitado para projetos pessoais
- **Redis Cloud/Upstash**: Tier gratuito disponível

> **Nota**: O Render pode colocar o serviço em "sleep" após 15 minutos de inatividade no plano gratuito. O primeiro acesso após o sleep pode demorar ~30 segundos.
