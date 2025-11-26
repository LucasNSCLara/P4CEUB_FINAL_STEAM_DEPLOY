# Documentação - GameSphere (SteamExplorer)

## 📋 Visão Geral

**SteamExplorer** é uma aplicação web moderna para análise de jogos de PC, permitindo que usuários pesquisem informações detalhadas sobre jogos, verifiquem requisitos de sistema, e gerenciem seus favoritos. A aplicação integra dados da API RAWG para fornecer informações completas e atualizadas sobre jogos.

---

## 🎯 Objetivo

Fornecer uma plataforma intuitiva e visualmente atraente para gamers de PC que desejam:
- Pesquisar informações detalhadas sobre jogos
- Verificar se seus computadores podem rodar determinados jogos
- Descobrir jogos similares
- Gerenciar uma lista de jogos favoritos
- Analisar requisitos de sistema de forma clara e estruturada

---

## 🏗️ Arquitetura

### Stack Tecnológico

#### Frontend
- **Framework**: React 18.2 com TypeScript
- **Build Tool**: Vite 5.0
- **Estilização**: TailwindCSS 3.4
- **Gerenciamento de Estado**: Zustand 4.5
- **Gráficos**: Chart.js 4.4 + React-ChartJS-2
- **HTTP Client**: Axios 1.7
- **Ícones**: React Icons 5.0

#### Backend
- **Framework**: FastAPI (Python)
- **Servidor**: Uvicorn
- **Cache**: Redis (opcional)
- **HTTP Client**: Requests + HTTPX
- **Validação**: Pydantic
- **Configuração**: Python-dotenv

#### APIs Externas
- **RAWG API**: Fonte principal de dados sobre jogos

### Estrutura de Diretórios

```
GameSphere/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── GameDashboard.tsx    # Componente principal
│   │   │   ├── SearchBar.tsx        # Barra de pesquisa com autocomplete
│   │   │   ├── RequirementsCard.tsx # Exibição de requisitos
│   │   │   ├── LoginModal.tsx       # Modal de autenticação
│   │   │   └── FavoritesModal.tsx   # Modal de favoritos
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.ts
│
└── backend/
    ├── app/
    │   ├── api/
    │   │   └── endpoints.py         # Rotas da API
    │   ├── core/
    │   │   ├── config.py            # Configurações
    │   │   └── parser.py            # Parser de requisitos
    │   ├── models/
    │   │   └── schemas.py           # Modelos Pydantic
    │   ├── services/
    │   │   └── rawg_service.py      # Serviço RAWG
    │   └── main.py                  # Aplicação FastAPI
    └── requirements.txt
```

---

## ✨ Funcionalidades

### 1. Pesquisa de Jogos
- **Autocomplete inteligente**: Sugestões em tempo real enquanto o usuário digita
- **Busca por nome**: Encontra jogos usando a API RAWG
- **Resultados instantâneos**: Exibição rápida de informações do jogo

### 2. Detalhes do Jogo
- **Informações gerais**:
  - Nome, desenvolvedora, data de lançamento
  - Imagem de capa em alta resolução
  - Avaliação (rating) e pontuação Metacritic
  - Tempo médio de jogo
  - Tamanho estimado do arquivo

- **Visualizações gráficas**:
  - Gráfico de rosca (doughnut) para avaliação
  - Cards com métricas visuais

### 3. Requisitos de Sistema
- **Parsing inteligente**: Extração automática de requisitos mínimos e recomendados
- **Componentes analisados**:
  - CPU (processador)
  - GPU (placa de vídeo)
  - RAM (memória)
  - Storage (armazenamento)
  - OS (sistema operacional)

- **Verificação de compatibilidade**: 
  - Usuário pode inserir suas especificações
  - Sistema verifica se atende aos requisitos mínimos/recomendados

### 4. Jogos Similares
- **Recomendações automáticas**: 
  - Usa endpoint `/suggested` da RAWG
  - Fallback para busca por gênero
- **Exibição visual**: Cards clicáveis com imagem, nome, gênero e rating
- **Navegação rápida**: Clique para carregar detalhes do jogo similar

### 5. Sistema de Autenticação
- **Login e Cadastro**: Modal com abas separadas
- **Armazenamento local**: Dados salvos no localStorage
- **Interface PT-BR**: Totalmente localizada em português

### 6. Favoritos
- **Gerenciamento de favoritos**:
  - Adicionar/remover jogos da lista
  - Persistência por usuário (localStorage)
  - Visualização em modal dedicado
- **Acesso rápido**: Menu dropdown do usuário
- **Contador visual**: Exibe quantidade de jogos favoritos

### 7. Design Responsivo
- **Mobile-first**: Funciona perfeitamente em dispositivos móveis
- **Glassmorphism**: Efeitos de vidro fosco modernos
- **Animações suaves**: Transições e hover effects
- **Tema escuro**: Design otimizado para baixa luminosidade

---

## 🔌 API Endpoints

### Backend (FastAPI)

#### `GET /`
Endpoint raiz de boas-vindas.

**Resposta**:
```json
{
  "message": "Welcome to GameSphere Analytics API"
}
```

#### `GET /api/search?query={termo}`
Busca jogos com autocomplete.

**Parâmetros**:
- `query` (string, obrigatório): Termo de busca

**Resposta**:
```json
{
  "results": [
    {
      "id": 3498,
      "name": "Grand Theft Auto V",
      "slug": "grand-theft-auto-v",
      "background_image": "https://...",
      "rating": 4.47,
      "released": "2013-09-17"
    }
  ]
}
```

#### `GET /api/game/{game_name}`
Obtém detalhes completos de um jogo.

**Parâmetros**:
- `game_name` (string): Nome ou slug do jogo

**Resposta**:
```json
{
  "id": 3498,
  "name": "Grand Theft Auto V",
  "description_raw": "...",
  "released": "2013-09-17",
  "background_image": "https://...",
  "website": "https://...",
  "rating": 4.47,
  "metacritic": 96,
  "playtime": 74,
  "platforms": [...],
  "genres": [...],
  "developers": [...],
  "publishers": [...],
  "parsed_requirements_min": {
    "cpu": "Intel Core 2 Quad CPU Q6600",
    "gpu": "NVIDIA 9800 GT 1GB",
    "ram": "4 GB",
    "storage": "72 GB",
    "os": "Windows 10 64 Bit"
  },
  "parsed_requirements_rec": {
    "cpu": "Intel Core i5 3470",
    "gpu": "NVIDIA GTX 660 2GB",
    "ram": "8 GB",
    "storage": "72 GB",
    "os": "Windows 10 64 Bit"
  },
  "file_size": "72 GB",
  "similar_games": [
    {
      "id": 5286,
      "name": "Tomb Raider",
      "background_image": "https://...",
      "rating": 4.05,
      "genres": [{"name": "Action"}]
    }
  ]
}
```

---

## 🔧 Requisitos do Sistema

### Para Desenvolvimento

#### Frontend
- Node.js 16+ e npm
- Navegador moderno (Chrome, Firefox, Edge)

#### Backend
- Python 3.8+
- Redis (opcional, para cache)

### Para Produção

#### Frontend (Vercel)
- Conta Vercel (gratuita)
- Repositório GitHub

#### Backend (Render)
- Conta Render (gratuita)
- Repositório GitHub

---

## 🚀 Configuração e Instalação

### Variáveis de Ambiente

#### Backend (.env)
```env
RAWG_API_KEY=sua_chave_rawg_aqui
REDIS_URL=redis://localhost:6379
ALLOWED_ORIGINS=http://localhost:5173,https://seu-frontend.vercel.app
```

#### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
```

### Instalação Local

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

A aplicação estará disponível em:
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 🎨 Design e UX

### Princípios de Design
1. **Minimalismo Premium**: Interface limpa com elementos visuais impactantes
2. **Hierarquia Visual**: Informações importantes em destaque
3. **Feedback Imediato**: Animações e estados visuais claros
4. **Acessibilidade**: Contraste adequado e navegação intuitiva

### Paleta de Cores
- **Primária (Accent)**: `#00ff9d` (Verde neon)
- **Secundária**: `#7c3aed` (Roxo vibrante)
- **Background**: Gradientes escuros com glassmorphism
- **Texto**: Branco e tons de cinza para contraste

### Componentes Visuais
- **Glass Panels**: Cards com efeito de vidro fosco
- **Gradientes**: Transições suaves de cor
- **Sombras**: Profundidade e elevação
- **Animações**: Fade-in, slide-up, hover effects

---

## 🔒 Segurança

### Implementações
1. **CORS**: Configurado para permitir apenas origens autorizadas
2. **Validação de Entrada**: Pydantic valida todos os dados de entrada
3. **Rate Limiting**: Implementado via cache Redis
4. **Sanitização**: Dados da API externa são validados antes do uso

### Boas Práticas
- Chaves de API armazenadas em variáveis de ambiente
- Não expor informações sensíveis no frontend
- Timeout em requisições HTTP para evitar travamentos

---

## 📊 Cache e Performance

### Redis Cache
- **TTL**: 1 hora (3600 segundos)
- **Chave**: `game:{game_name}`
- **Fallback**: Aplicação funciona sem Redis, apenas sem cache

### Otimizações
- **Lazy Loading**: Componentes carregados sob demanda
- **Debounce**: Pesquisa com autocomplete otimizada
- **Imagens**: Lazy loading e otimização de tamanho
- **Bundle Splitting**: Vite divide o código automaticamente

---

## 🧪 Testes e Validação

### Testes Manuais Recomendados
1. Pesquisar por jogos populares (ex: "Cyberpunk 2077")
2. Verificar exibição de requisitos de sistema
3. Testar funcionalidade de favoritos
4. Validar responsividade em diferentes dispositivos
5. Testar jogos similares

### Casos de Erro
- Jogo não encontrado: Exibe mensagem de erro
- API indisponível: Timeout e mensagem apropriada
- Sem conexão: Feedback visual claro

---

## 📈 Melhorias Futuras

### Funcionalidades Planejadas
- [ ] Comparação lado a lado de jogos
- [ ] Histórico de pesquisas
- [ ] Filtros avançados (gênero, ano, plataforma)
- [ ] Integração com Steam para preços
- [ ] Sistema de reviews de usuários
- [ ] Notificações de lançamentos
- [ ] Modo claro/escuro toggle
- [ ] Exportar lista de favoritos

### Melhorias Técnicas
- [ ] Testes automatizados (Jest, Pytest)
- [ ] CI/CD pipeline
- [ ] Monitoramento de erros (Sentry)
- [ ] Analytics (Google Analytics)
- [ ] PWA (Progressive Web App)
- [ ] SSR (Server-Side Rendering)

---

## 🐛 Troubleshooting

### Problemas Comuns

#### "Game not found"
- Verifique se o nome do jogo está correto
- Tente usar o nome em inglês
- Alguns jogos podem não estar na base RAWG

#### "RAWG API Key not configured"
- Verifique se a variável `RAWG_API_KEY` está definida
- Confirme que a chave é válida em [rawg.io](https://rawg.io/apidocs)

#### CORS Error
- Verifique `ALLOWED_ORIGINS` no backend
- Confirme que a URL do frontend está correta
- Não esqueça o protocolo (`https://` ou `http://`)

#### Redis Connection Failed
- Aplicação funciona sem Redis
- Para usar Redis, verifique se está rodando: `redis-cli ping`
- Confirme a URL de conexão em `REDIS_URL`

---

## 📝 Licença e Créditos

### APIs Utilizadas
- **RAWG API**: Dados de jogos - [rawg.io](https://rawg.io)

### Bibliotecas Open Source
- React, FastAPI, TailwindCSS, Chart.js e todas as dependências listadas

### Desenvolvido por
Lucas - P4CEUB Final Project

---

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique a seção de Troubleshooting
2. Consulte a documentação de deploy (`DEPLOYMENT.md`)
3. Revise os logs do backend e console do navegador

---

**Última atualização**: Novembro 2025
