# Documentação de Testes - GameSphere (SteamExplorer)

**Projeto**: GameSphere - Plataforma de Análise de Jogos de PC  
**Versão do Documento**: 1.0  
**Data**: 27/11/2025  
**Responsável**: Equipe de QA - P4CEUB

---

## 📑 Índice

1. [Plano de Testes](#1-plano-de-testes)
   - 1.1 [Introdução](#11-introdução)
   - 1.2 [Requisitos a Serem Testados](#12-requisitos-a-serem-testados)
   - 1.3 [Estratégia de Testes](#13-estratégia-de-testes)
   - 1.4 [Critérios de Aceitação](#14-critérios-de-aceitação)
   - 1.5 [Recursos](#15-recursos)
   - 1.6 [Cronograma](#16-cronograma)
   - 1.7 [Riscos e Mitigações](#17-riscos-e-mitigações)

2. [Casos de Teste](#2-casos-de-teste)
   - 2.1 [Pesquisa de Jogos (5 casos)](#21-pesquisa-de-jogos-rf01)
   - 2.2 [Detalhes do Jogo (4 casos)](#22-detalhes-do-jogo-rf02)
   - 2.3 [Requisitos de Sistema (4 casos)](#23-requisitos-de-sistema-rf03)
   - 2.4 [Jogos Similares (3 casos)](#24-jogos-similares-rf04)
   - 2.5 [Autenticação (4 casos)](#25-sistema-de-autenticação-rf05)
   - 2.6 [Favoritos (3 casos)](#26-gerenciamento-de-favoritos-rf06)
   - 2.7 [API Backend (2 casos)](#27-api-backend-rf07)

3. [Registros de Testes](#3-registros-de-testes)
   - 3.1 [Templates](#31-templates-de-registro)
   - 3.2 [Exemplos](#32-exemplos-de-registros-preenchidos)
   - 3.3 [Métricas](#33-métricas-de-execução)
   - 3.4 [Rastreabilidade](#34-rastreabilidade-de-defeitos)

---

# 1. PLANO DE TESTES

## 1.1 Introdução

### 1.1.1 Objetivo
Este documento define o plano de testes para o projeto GameSphere (SteamExplorer), uma aplicação web para análise de jogos de PC que integra dados da API RAWG. O objetivo é garantir que todas as funcionalidades atendam aos requisitos especificados e proporcionem uma experiência de usuário de alta qualidade.

### 1.1.2 Escopo
O plano de testes abrange:
- **Frontend**: Interface React com TypeScript
- **Backend**: API FastAPI em Python
- **Integração**: Comunicação entre frontend/backend e API RAWG
- **Funcionalidades**: Todas as 7 funcionalidades principais do sistema

### 1.1.3 Documentos de Referência
- `DOCUMENTACAO.md` - Documentação técnica completa
- `DEPLOYMENT.md` - Guia de deployment e configuração
- Especificação de Requisitos do Projeto Integrador

---

## 1.2 Requisitos a Serem Testados

### 1.2.1 Requisitos Funcionais

#### RF01 - Pesquisa de Jogos
- Autocomplete com sugestões em tempo real
- Busca por nome de jogo via API RAWG
- Exibição de resultados instantâneos

#### RF02 - Detalhes do Jogo
- Exibição de informações gerais (nome, desenvolvedora, data de lançamento)
- Visualização de imagem de capa em alta resolução
- Exibição de métricas (rating, Metacritic, tempo de jogo)
- Gráficos visuais (doughnut chart para avaliação)

#### RF03 - Requisitos de Sistema
- Parsing automático de requisitos mínimos e recomendados
- Extração de componentes (CPU, GPU, RAM, Storage, OS)
- Verificação de compatibilidade com especificações do usuário

#### RF04 - Jogos Similares
- Recomendações automáticas via endpoint `/suggested`
- Fallback para busca por gênero
- Exibição em cards clicáveis com navegação

#### RF05 - Sistema de Autenticação
- Login de usuários existentes
- Cadastro de novos usuários
- Armazenamento seguro no localStorage
- Interface totalmente em PT-BR

#### RF06 - Gerenciamento de Favoritos
- Adicionar jogos à lista de favoritos
- Remover jogos da lista
- Persistência por usuário
- Visualização em modal dedicado

#### RF07 - API Backend
- Endpoint `/api/search` para autocomplete
- Endpoint `/api/game/{game_name}` para detalhes
- Tratamento de erros e timeouts
- Cache com Redis (opcional)

### 1.2.2 Requisitos Não-Funcionais

#### RNF01 - Desempenho
- Tempo de resposta da pesquisa < 2 segundos
- Carregamento de detalhes do jogo < 3 segundos
- Cache efetivo reduzindo chamadas à API

#### RNF02 - Usabilidade
- Interface intuitiva e responsiva
- Design premium com glassmorphism
- Feedback visual imediato para ações do usuário
- Suporte a dispositivos móveis

#### RNF03 - Compatibilidade
- Funcionamento em Chrome, Firefox, Edge (versões recentes)
- Responsividade em resoluções 320px a 4K
- Suporte a touch em dispositivos móveis

#### RNF04 - Confiabilidade
- Tratamento adequado de erros de API
- Mensagens de erro claras e em PT-BR
- Graceful degradation quando Redis não disponível

#### RNF05 - Segurança
- CORS configurado corretamente
- Validação de entrada via Pydantic
- Proteção de chaves de API (variáveis de ambiente)
- Sanitização de dados da API externa

---

## 1.3 Estratégia de Testes

### 1.3.1 Níveis de Teste

#### Testes de Unidade
- **Escopo**: Funções individuais do parser de requisitos
- **Ferramenta**: Pytest (backend)
- **Responsável**: Desenvolvedores

#### Testes de Integração
- **Escopo**: Comunicação entre componentes (Frontend ↔ Backend ↔ RAWG API)
- **Ferramenta**: Testes manuais e automatizados
- **Responsável**: Equipe de QA

#### Testes de Sistema
- **Escopo**: Fluxos completos de usuário
- **Ferramenta**: Testes manuais exploratórios
- **Responsável**: Equipe de QA

#### Testes de Aceitação
- **Escopo**: Validação de requisitos com stakeholders
- **Ferramenta**: Demonstrações e validações manuais
- **Responsável**: Product Owner + QA

### 1.3.2 Tipos de Teste

| Tipo de Teste | Descrição | Prioridade |
|---------------|-----------|------------|
| **Funcional** | Verificação de requisitos funcionais | Alta |
| **Usabilidade** | Experiência do usuário e interface | Alta |
| **Desempenho** | Tempos de resposta e carregamento | Média |
| **Compatibilidade** | Browsers e dispositivos | Média |
| **Segurança** | CORS, validação, proteção de dados | Alta |
| **Regressão** | Garantir que novas mudanças não quebrem funcionalidades existentes | Alta |

### 1.3.3 Técnicas de Teste

- **Particionamento de Equivalência**: Agrupar entradas similares
- **Análise de Valor Limite**: Testar limites de campos
- **Teste de Fluxo**: Validar jornadas completas do usuário
- **Teste Exploratório**: Descobrir comportamentos inesperados
- **Teste de Erro**: Validar tratamento de exceções

---

## 1.4 Critérios de Aceitação

### 1.4.1 Critérios de Entrada
- Ambiente de desenvolvimento configurado
- Backend e Frontend deployados
- API RAWG acessível com chave válida
- Documentação técnica disponível

### 1.4.2 Critérios de Saída
- 100% dos casos de teste executados
- 0 defeitos críticos abertos
- ≤ 2 defeitos médios abertos
- Todos os requisitos funcionais validados
- Aprovação do Product Owner

### 1.4.3 Critérios de Suspensão
- Ambiente de teste indisponível por > 4 horas
- API RAWG fora do ar
- > 5 defeitos críticos identificados
- Bloqueadores que impedem execução de testes

---

## 1.5 Recursos

### 1.5.1 Recursos Humanos
| Papel | Responsabilidade | Quantidade |
|-------|------------------|------------|
| **QA Lead** | Coordenação e planejamento | 1 |
| **Testador** | Execução de casos de teste | 2-3 |
| **Desenvolvedor** | Correção de defeitos | 2 |

### 1.5.2 Recursos de Ambiente

#### Ambiente de Desenvolvimento
- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **Redis**: localhost:6379 (opcional)

#### Ambiente de Produção
- **Frontend**: Vercel (https://steamexplorer.vercel.app)
- **Backend**: Render (https://steamexplorer-backend.onrender.com)
- **Redis**: Redis Cloud ou Upstash (opcional)

### 1.5.3 Ferramentas
- **Navegadores**: Chrome, Firefox, Edge (últimas versões)
- **Dispositivos**: Desktop, Tablet, Mobile (emuladores)
- **Gerenciamento de Testes**: Planilhas Google Sheets / Excel
- **Rastreamento de Bugs**: GitHub Issues
- **API Testing**: Postman / Thunder Client
- **DevTools**: Chrome DevTools, React DevTools

---

## 1.6 Cronograma

| Fase | Atividade | Duração | Responsável |
|------|-----------|---------|-------------|
| **Fase 1** | Planejamento de Testes | 2 dias | QA Lead |
| **Fase 2** | Elaboração de Casos de Teste | 3 dias | Testadores |
| **Fase 3** | Preparação de Ambiente | 1 dia | DevOps/Dev |
| **Fase 4** | Execução de Testes Funcionais | 4 dias | Testadores |
| **Fase 5** | Execução de Testes Não-Funcionais | 2 dias | Testadores |
| **Fase 6** | Reporte e Correção de Defeitos | 3 dias | QA + Dev |
| **Fase 7** | Testes de Regressão | 2 dias | Testadores |
| **Fase 8** | Aprovação Final | 1 dia | Product Owner |
| **Total** | | **18 dias** | |

---

## 1.7 Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| API RAWG indisponível | Média | Alto | Usar dados mockados para testes |
| Ambiente de teste instável | Baixa | Médio | Manter ambiente local de backup |
| Atraso na correção de bugs | Média | Médio | Priorizar defeitos críticos |
| Mudanças de requisitos | Baixa | Alto | Processo de change request formal |
| Falta de cobertura de testes | Baixa | Alto | Revisão de casos de teste por pares |

---

# 2. CASOS DE TESTE

**Total de Casos de Teste**: 25

## Índice de Casos de Teste por Funcionalidade

| Funcionalidade | Casos de Teste | IDs |
|----------------|----------------|-----|
| Pesquisa de Jogos | 5 | CT-001 a CT-005 |
| Detalhes do Jogo | 4 | CT-006 a CT-009 |
| Requisitos de Sistema | 4 | CT-010 a CT-013 |
| Jogos Similares | 3 | CT-014 a CT-016 |
| Autenticação | 4 | CT-017 a CT-020 |
| Favoritos | 3 | CT-021 a CT-023 |
| API Backend | 2 | CT-024 a CT-025 |

---

## 2.1 Pesquisa de Jogos (RF01)

### CT-001: Pesquisa de jogo com autocomplete
**Prioridade**: Alta | **Tipo**: Funcional

**Pré-condições**: 
- Aplicação carregada
- Backend conectado à API RAWG

**Passos**:
1. Acessar a página principal
2. Clicar na barra de pesquisa
3. Digitar "Cyber" no campo de busca
4. Aguardar sugestões de autocomplete

**Resultado Esperado**:
- Lista de sugestões aparece em tempo real
- Sugestões incluem "Cyberpunk 2077" e jogos relacionados
- Cada sugestão mostra nome e imagem do jogo
- Tempo de resposta < 2 segundos

**Dados de Teste**: "Cyber"

---

### CT-002: Pesquisa de jogo inexistente
**Prioridade**: Média | **Tipo**: Funcional - Negativo

**Pré-condições**: Aplicação carregada

**Passos**:
1. Acessar a página principal
2. Digitar "XYZ123INEXISTENTE456" na barra de pesquisa
3. Pressionar Enter ou clicar em buscar

**Resultado Esperado**:
- Sistema exibe mensagem "Nenhum jogo encontrado"
- Mensagem em PT-BR
- Não ocorre erro de aplicação
- Interface permanece responsiva

**Dados de Teste**: "XYZ123INEXISTENTE456"

---

### CT-003: Pesquisa com caracteres especiais
**Prioridade**: Baixa | **Tipo**: Funcional

**Pré-condições**: Aplicação carregada

**Passos**:
1. Acessar a página principal
2. Digitar "Grand Theft Auto V" na barra de pesquisa
3. Selecionar o jogo da lista de sugestões

**Resultado Esperado**:
- Sistema processa corretamente espaços e caracteres especiais
- Jogo "Grand Theft Auto V" é encontrado
- Detalhes do jogo são exibidos corretamente

**Dados de Teste**: "Grand Theft Auto V"

---

### CT-004: Pesquisa com campo vazio
**Prioridade**: Média | **Tipo**: Funcional - Negativo

**Pré-condições**: Aplicação carregada

**Passos**:
1. Acessar a página principal
2. Deixar campo de pesquisa vazio
3. Pressionar Enter ou clicar em buscar

**Resultado Esperado**:
- Sistema não realiza busca
- Nenhuma mensagem de erro é exibida
- Campo de pesquisa permanece focado
- Autocomplete não é acionado

**Dados de Teste**: "" (vazio)

---

### CT-005: Autocomplete com menos de 3 caracteres
**Prioridade**: Baixa | **Tipo**: Funcional

**Pré-condições**: Aplicação carregada

**Passos**:
1. Acessar a página principal
2. Digitar "GTA" (3 caracteres)
3. Observar comportamento do autocomplete

**Resultado Esperado**:
- Autocomplete é acionado
- Sugestões relacionadas a "GTA" aparecem
- Performance adequada (< 2s)

**Dados de Teste**: "GTA"

---

## 2.2 Detalhes do Jogo (RF02)

### CT-006: Visualização de detalhes completos do jogo
**Prioridade**: Alta | **Tipo**: Funcional

**Pré-condições**: Jogo pesquisado com sucesso

**Passos**:
1. Pesquisar "The Witcher 3"
2. Selecionar o jogo da lista
3. Aguardar carregamento dos detalhes

**Resultado Esperado**:
- Imagem de capa em alta resolução exibida
- Nome, desenvolvedora e data de lançamento visíveis
- Rating e Metacritic score exibidos
- Tempo médio de jogo mostrado
- Gráfico doughnut de avaliação renderizado
- Tempo de carregamento < 3 segundos

**Dados de Teste**: "The Witcher 3"

---

### CT-007: Visualização de jogo sem Metacritic score
**Prioridade**: Média | **Tipo**: Funcional

**Pré-condições**: Aplicação carregada

**Passos**:
1. Pesquisar jogo indie sem Metacritic score
2. Selecionar o jogo
3. Verificar exibição de informações

**Resultado Esperado**:
- Jogo é exibido normalmente
- Campo Metacritic mostra "N/A" ou é omitido
- Demais informações são exibidas corretamente
- Sem erros de renderização

**Dados de Teste**: Jogo indie sem Metacritic

---

### CT-008: Visualização de imagem de capa em alta resolução
**Prioridade**: Média | **Tipo**: Funcional

**Pré-condições**: Detalhes do jogo carregados

**Passos**:
1. Pesquisar "Red Dead Redemption 2"
2. Selecionar o jogo
3. Verificar qualidade da imagem de capa

**Resultado Esperado**:
- Imagem carregada em alta resolução
- Imagem não pixelizada
- Lazy loading funcional
- Placeholder durante carregamento

**Dados de Teste**: "Red Dead Redemption 2"

---

### CT-009: Gráfico de avaliação (Doughnut Chart)
**Prioridade**: Média | **Tipo**: Funcional

**Pré-condições**: Detalhes do jogo carregados

**Passos**:
1. Pesquisar "Portal 2"
2. Selecionar o jogo
3. Localizar gráfico de avaliação
4. Verificar renderização

**Resultado Esperado**:
- Gráfico doughnut renderizado corretamente
- Cores vibrantes e legíveis
- Percentual de avaliação visível
- Animação suave ao carregar

**Dados de Teste**: "Portal 2"

---

## 2.3 Requisitos de Sistema (RF03)

### CT-010: Parsing de requisitos mínimos
**Prioridade**: Alta | **Tipo**: Funcional

**Pré-condições**: Jogo com requisitos de sistema disponíveis

**Passos**:
1. Pesquisar "Cyberpunk 2077"
2. Selecionar o jogo
3. Navegar até seção de requisitos
4. Verificar requisitos mínimos

**Resultado Esperado**:
- CPU, GPU, RAM, Storage e OS extraídos corretamente
- Informações formatadas e legíveis
- Valores numéricos parseados (ex: "8 GB RAM")
- Layout organizado em cards

**Dados de Teste**: "Cyberpunk 2077"

---

### CT-011: Parsing de requisitos recomendados
**Prioridade**: Alta | **Tipo**: Funcional

**Pré-condições**: Jogo com requisitos de sistema disponíveis

**Passos**:
1. Pesquisar "Elden Ring"
2. Selecionar o jogo
3. Verificar requisitos recomendados

**Resultado Esperado**:
- Requisitos recomendados exibidos separadamente dos mínimos
- Todos os componentes (CPU, GPU, RAM, Storage, OS) listados
- Diferenciação visual clara entre mínimo e recomendado
- Parsing correto de especificações

**Dados de Teste**: "Elden Ring"

---

### CT-012: Verificação de compatibilidade - Sistema compatível
**Prioridade**: Alta | **Tipo**: Funcional

**Pré-condições**: Requisitos do jogo carregados

**Passos**:
1. Pesquisar "Stardew Valley" (jogo leve)
2. Inserir especificações: Intel i5-8400, GTX 1060, 16GB RAM
3. Clicar em "Verificar Compatibilidade"

**Resultado Esperado**:
- Sistema indica compatibilidade total
- Mensagem positiva em PT-BR
- Indicação visual (ícone verde/check)
- Atende requisitos mínimos e recomendados

**Dados de Teste**: CPU: Intel i5-8400 | GPU: GTX 1060 | RAM: 16GB

---

### CT-013: Verificação de compatibilidade - Sistema incompatível
**Prioridade**: Média | **Tipo**: Funcional - Negativo

**Pré-condições**: Requisitos do jogo carregados

**Passos**:
1. Pesquisar "Microsoft Flight Simulator" (jogo pesado)
2. Inserir especificações baixas: Intel i3, GT 730, 4GB RAM
3. Clicar em "Verificar Compatibilidade"

**Resultado Esperado**:
- Sistema indica incompatibilidade
- Mensagem clara em PT-BR sobre componentes insuficientes
- Lista de componentes que não atendem requisitos
- Indicação visual (ícone vermelho/X)

**Dados de Teste**: CPU: Intel i3 | GPU: GT 730 | RAM: 4GB

---

## 2.4 Jogos Similares (RF04)

### CT-014: Exibição de jogos similares
**Prioridade**: Alta | **Tipo**: Funcional

**Pré-condições**: Detalhes do jogo carregados

**Passos**:
1. Pesquisar "Dark Souls 3"
2. Selecionar o jogo
3. Rolar até seção "Jogos Similares"

**Resultado Esperado**:
- Pelo menos 2 jogos similares exibidos
- Cada card mostra: imagem, nome, gênero, rating
- Cards clicáveis
- Layout responsivo

**Dados de Teste**: "Dark Souls 3"

---

### CT-015: Navegação para jogo similar
**Prioridade**: Média | **Tipo**: Funcional

**Pré-condições**: Jogos similares exibidos

**Passos**:
1. Pesquisar "Hollow Knight"
2. Visualizar jogos similares
3. Clicar em um dos jogos similares

**Resultado Esperado**:
- Página atualiza com detalhes do jogo similar
- Transição suave
- Novos jogos similares são carregados
- Histórico de navegação funcional

**Dados de Teste**: "Hollow Knight"

---

### CT-016: Fallback para busca por gênero
**Prioridade**: Baixa | **Tipo**: Funcional

**Pré-condições**: Endpoint `/suggested` indisponível ou sem resultados

**Passos**:
1. Pesquisar jogo obscuro sem sugestões diretas
2. Verificar seção de jogos similares

**Resultado Esperado**:
- Sistema utiliza busca por gênero como fallback
- Jogos do mesmo gênero são exibidos
- Sem erro visível para o usuário
- Pelo menos 1 jogo similar exibido

**Dados de Teste**: Jogo indie obscuro

---

## 2.5 Sistema de Autenticação (RF05)

### CT-017: Cadastro de novo usuário
**Prioridade**: Alta | **Tipo**: Funcional

**Pré-condições**: Aplicação carregada, usuário não logado

**Passos**:
1. Clicar no botão "Entrar" no canto superior direito
2. Selecionar aba "Cadastro"
3. Preencher: Nome "João Silva", Email "joao@test.com", Senha "Senha123!"
4. Clicar em "Cadastrar"

**Resultado Esperado**:
- Cadastro realizado com sucesso
- Modal fecha automaticamente
- Usuário logado (nome aparece no header)
- Dados salvos no localStorage
- Interface em PT-BR

**Dados de Teste**: Nome: João Silva | Email: joao@test.com | Senha: Senha123!

---

### CT-018: Login com credenciais válidas
**Prioridade**: Alta | **Tipo**: Funcional

**Pré-condições**: Usuário previamente cadastrado

**Passos**:
1. Clicar no botão "Entrar"
2. Selecionar aba "Login"
3. Preencher Email e Senha corretos
4. Clicar em "Entrar"

**Resultado Esperado**:
- Login realizado com sucesso
- Modal fecha
- Nome do usuário exibido no header
- Menu dropdown de usuário disponível

**Dados de Teste**: Email: joao@test.com | Senha: Senha123!

---

### CT-019: Login com credenciais inválidas
**Prioridade**: Média | **Tipo**: Funcional - Negativo

**Pré-condições**: Aplicação carregada

**Passos**:
1. Clicar no botão "Entrar"
2. Preencher Email: "invalido@test.com", Senha: "senhaerrada"
3. Clicar em "Entrar"

**Resultado Esperado**:
- Mensagem de erro "Credenciais inválidas" em PT-BR
- Modal permanece aberto
- Campos não são limpos
- Usuário não é logado

**Dados de Teste**: Email: invalido@test.com | Senha: senhaerrada

---

### CT-020: Logout de usuário
**Prioridade**: Média | **Tipo**: Funcional

**Pré-condições**: Usuário logado

**Passos**:
1. Clicar no nome do usuário no header
2. Selecionar "Sair" no menu dropdown
3. Confirmar logout

**Resultado Esperado**:
- Usuário deslogado
- Botão "Entrar" volta a aparecer
- Favoritos do usuário permanecem salvos
- Redirecionamento para página inicial

---

## 2.6 Gerenciamento de Favoritos (RF06)

### CT-021: Adicionar jogo aos favoritos
**Prioridade**: Alta | **Tipo**: Funcional

**Pré-condições**: Usuário logado, jogo selecionado

**Passos**:
1. Fazer login
2. Pesquisar "Hades"
3. Selecionar o jogo
4. Clicar no botão "Adicionar aos Favoritos" (ícone de coração)

**Resultado Esperado**:
- Ícone de coração muda para preenchido
- Mensagem de confirmação exibida
- Contador de favoritos incrementado
- Jogo salvo no localStorage

**Dados de Teste**: "Hades"

---

### CT-022: Remover jogo dos favoritos
**Prioridade**: Alta | **Tipo**: Funcional

**Pré-condições**: Usuário logado, jogo já está nos favoritos

**Passos**:
1. Acessar modal de favoritos
2. Localizar jogo "Hades"
3. Clicar no botão de remover (X ou ícone de lixeira)

**Resultado Esperado**:
- Jogo removido da lista
- Contador de favoritos decrementado
- Atualização imediata da interface
- Mudança persistida no localStorage

**Dados de Teste**: "Hades"

---

### CT-023: Visualizar lista de favoritos
**Prioridade**: Média | **Tipo**: Funcional

**Pré-condições**: Usuário logado, pelo menos 2 jogos favoritados

**Passos**:
1. Clicar no nome do usuário
2. Selecionar "Meus Favoritos" no dropdown
3. Verificar modal de favoritos

**Resultado Esperado**:
- Modal abre com lista de favoritos
- Cada jogo mostra: imagem, nome, rating
- Contador correto de favoritos
- Opção de remover disponível para cada jogo
- Cards clicáveis para ver detalhes

---

## 2.7 API Backend (RF07)

### CT-024: Endpoint /api/search com query válida
**Prioridade**: Alta | **Tipo**: Integração

**Pré-condições**: Backend rodando, API RAWG acessível

**Passos**:
1. Abrir Postman/Thunder Client
2. Fazer GET request para: `http://localhost:8000/api/search?query=zelda`
3. Verificar resposta

**Resultado Esperado**:
- Status Code: 200 OK
- JSON com array "results"
- Cada resultado contém: id, name, slug, background_image, rating, released
- Tempo de resposta < 2 segundos

**Dados de Teste**: `GET /api/search?query=zelda`

---

### CT-025: Endpoint /api/game/{game_name} com jogo válido
**Prioridade**: Alta | **Tipo**: Integração

**Pré-condições**: Backend rodando, API RAWG acessível

**Passos**:
1. Abrir Postman/Thunder Client
2. Fazer GET request para: `http://localhost:8000/api/game/minecraft`
3. Verificar resposta

**Resultado Esperado**:
- Status Code: 200 OK
- JSON completo com detalhes do jogo
- Campos incluem: id, name, description_raw, rating, metacritic, platforms, genres
- `parsed_requirements_min` e `parsed_requirements_rec` presentes
- `similar_games` array com pelo menos 1 jogo
- Tempo de resposta < 3 segundos

**Dados de Teste**: `GET /api/game/minecraft`

---

## Resumo de Cobertura de Casos de Teste

| Categoria | Casos de Teste | Cobertura |
|-----------|----------------|-----------|
| **Funcionais** | 23 | 92% |
| **Não-Funcionais** | 2 | 8% |
| **Positivos** | 20 | 80% |
| **Negativos** | 5 | 20% |
| **Prioridade Alta** | 15 | 60% |
| **Prioridade Média** | 9 | 36% |
| **Prioridade Baixa** | 1 | 4% |
| **TOTAL** | **25** | **100%** |

---

# 3. REGISTROS DE TESTES

## 3.1 Templates de Registro

### 3.1.1 Template de Registro Individual

| Campo | Descrição |
|-------|-----------|
| **ID do Caso de Teste** | Identificador único (ex: CT-001) |
| **Nome do Caso de Teste** | Título descritivo do teste |
| **Testador** | Nome do responsável pela execução |
| **Data de Execução** | DD/MM/AAAA |
| **Ambiente** | Desenvolvimento / Produção |
| **Versão da Aplicação** | Número da versão testada |
| **Navegador/Dispositivo** | Chrome 120 / Firefox 121 / Mobile Android |
| **Status** | ✅ Passou / ❌ Falhou / ⚠️ Bloqueado / ⏸️ Não Executado |
| **Resultado Obtido** | Descrição do que aconteceu durante o teste |
| **Evidências** | Links para screenshots, vídeos, logs |
| **Tempo de Execução** | Tempo gasto na execução (minutos) |
| **Observações** | Notas adicionais, comportamentos inesperados |

### 3.1.2 Planilha de Registro Consolidado

**Formato Sugerido (Excel/Google Sheets)**:

| ID | Nome do Teste | Prioridade | Testador | Data | Ambiente | Status | Defeito | Observações |
|----|---------------|------------|----------|------|----------|--------|---------|-------------|
| CT-001 | Pesquisa com autocomplete | Alta | | | | | | |
| CT-002 | Pesquisa de jogo inexistente | Média | | | | | | |
| CT-003 | Pesquisa com caracteres especiais | Baixa | | | | | | |
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

**Legenda de Status**:
- ✅ **Passou**: Teste executado com sucesso, resultado esperado obtido
- ❌ **Falhou**: Teste falhou, defeito identificado
- ⚠️ **Bloqueado**: Não pode ser executado devido a bloqueio
- ⏸️ **Não Executado**: Ainda não foi executado

---

## 3.2 Exemplos de Registros Preenchidos

### 3.2.1 Exemplo: Teste Bem-Sucedido

**CT-001: Pesquisa de jogo com autocomplete**

| Campo | Valor |
|-------|-------|
| **Testador** | Maria Santos |
| **Data de Execução** | 28/11/2025 |
| **Ambiente** | Desenvolvimento (localhost:5173) |
| **Versão** | 1.0.0 |
| **Navegador** | Chrome 120.0.6099.109 |
| **Status** | ✅ Passou |
| **Resultado Obtido** | Ao digitar "Cyber", o autocomplete exibiu 5 sugestões em 1.2s, incluindo "Cyberpunk 2077". Cada sugestão mostrou imagem e nome corretamente. |
| **Evidências** | `evidencias/ct001_autocomplete_success.png` |
| **Tempo de Execução** | 3 minutos |
| **Observações** | Performance excelente, interface responsiva e intuitiva. |

---

### 3.2.2 Exemplo: Teste com Falha

**CT-010: Parsing de requisitos mínimos**

| Campo | Valor |
|-------|-------|
| **Testador** | João Silva |
| **Data de Execução** | 28/11/2025 |
| **Ambiente** | Desenvolvimento |
| **Versão** | 1.0.0 |
| **Navegador** | Firefox 121.0 |
| **Status** | ❌ Falhou |
| **Resultado Obtido** | Ao pesquisar "Cyberpunk 2077", o campo "Storage" mostrou "undefined" ao invés de "70 GB". |
| **Evidências** | `evidencias/ct010_storage_undefined.png` |
| **Defeito** | [#123](https://github.com/user/repo/issues/123) - Severidade: Média |
| **Tempo de Execução** | 5 minutos |
| **Observações** | Demais campos (CPU, GPU, RAM, OS) parseados corretamente. |

---

### 3.2.3 Exemplo: Teste Bloqueado

**CT-024: Endpoint /api/search com query válida**

| Campo | Valor |
|-------|-------|
| **Testador** | Ana Costa |
| **Data de Execução** | 28/11/2025 |
| **Ambiente** | Desenvolvimento |
| **Status** | ⚠️ Bloqueado |
| **Resultado Obtido** | Backend não está respondendo. Erro: "Connection refused on port 8000". |
| **Evidências** | `evidencias/ct024_backend_down.png` |
| **Tempo de Execução** | 2 minutos |
| **Observações** | Verificar se backend está rodando: `uvicorn app.main:app --reload` |

---

## 3.3 Métricas de Execução

### 3.3.1 Resumo Geral

| Métrica | Valor | Percentual |
|---------|-------|------------|
| **Total de Casos de Teste** | 25 | 100% |
| **Executados** | 0 | 0% |
| **Passou** | 0 | 0% |
| **Falhou** | 0 | 0% |
| **Bloqueado** | 0 | 0% |
| **Não Executado** | 25 | 100% |

### 3.3.2 Defeitos Encontrados

| Severidade | Quantidade | Status |
|------------|------------|--------|
| **Crítica** | 0 | - |
| **Alta** | 0 | - |
| **Média** | 0 | - |
| **Baixa** | 0 | - |
| **Total** | 0 | - |

### 3.3.3 Cobertura por Funcionalidade

| Funcionalidade | Total | Executados | Passou | Falhou | % Sucesso |
|----------------|-------|------------|--------|--------|-----------|
| Pesquisa de Jogos | 5 | 0 | 0 | 0 | - |
| Detalhes do Jogo | 4 | 0 | 0 | 0 | - |
| Requisitos de Sistema | 4 | 0 | 0 | 0 | - |
| Jogos Similares | 3 | 0 | 0 | 0 | - |
| Autenticação | 4 | 0 | 0 | 0 | - |
| Favoritos | 3 | 0 | 0 | 0 | - |
| API Backend | 2 | 0 | 0 | 0 | - |

---

## 3.4 Rastreabilidade de Defeitos

### 3.4.1 Template de Defeito (GitHub Issue)

```markdown
# [BUG] Título Descritivo do Defeito

## Informações Básicas
- **ID**: #XXX
- **Severidade**: Crítica / Alta / Média / Baixa
- **Prioridade**: Alta / Média / Baixa
- **Status**: Aberto / Em Análise / Em Correção / Resolvido / Fechado
- **Caso de Teste**: CT-XXX
- **Encontrado por**: Nome do Testador
- **Data**: DD/MM/AAAA

## Descrição
Descrição clara e concisa do problema.

## Passos para Reproduzir
1. Passo 1
2. Passo 2
3. Passo 3

## Resultado Esperado
O que deveria acontecer.

## Resultado Obtido
O que realmente aconteceu.

## Evidências
- Screenshot: link
- Vídeo: link
- Logs: código do log

## Ambiente
- **Navegador**: Chrome 120
- **SO**: Windows 11
- **Versão**: 1.0.0
- **URL**: http://localhost:5173
```

---

## 3.5 Ciclos de Teste

### Ciclo 1 - Testes Funcionais Iniciais
- **Período**: DD/MM/AAAA a DD/MM/AAAA
- **Responsável**: QA Lead
- **Ambiente**: Desenvolvimento
- **Casos**: CT-001 a CT-023
- **Resultado**: 0/23 executados

### Ciclo 2 - Testes de Integração API
- **Período**: DD/MM/AAAA a DD/MM/AAAA
- **Responsável**: QA Lead
- **Ambiente**: Desenvolvimento
- **Casos**: CT-024 a CT-025
- **Resultado**: 0/2 executados

### Ciclo 3 - Testes de Regressão
- **Período**: DD/MM/AAAA a DD/MM/AAAA
- **Responsável**: QA Lead
- **Ambiente**: Produção
- **Casos**: CT-001 a CT-025 (todos)
- **Resultado**: 0/25 executados

---

## 3.6 Boas Práticas de Registro

### Durante a Execução
1. ✅ Registre imediatamente após executar o teste
2. ✅ Seja específico e objetivo nas descrições
3. ✅ Anexe evidências (screenshots, logs, vídeos)
4. ✅ Use linguagem clara e profissional
5. ✅ Registre tanto sucessos quanto falhas

### Evidências
1. **Screenshots**: Capture tela inteira ou área relevante
2. **Vídeos**: Grave fluxos complexos (max 2 minutos)
3. **Logs**: Copie mensagens de erro do console
4. **Network**: Capture requisições/respostas da API

### Nomenclatura de Arquivos
```
evidencias/
├── ct001_autocomplete_success.png
├── ct010_storage_undefined.png
├── ct024_backend_down.png
└── videos/
    └── ct015_similar_games_navigation.mp4
```

---

## 3.7 Ferramentas Recomendadas

| Ferramenta | Uso | Link |
|------------|-----|------|
| **Google Sheets** | Planilha de registros | sheets.google.com |
| **GitHub Issues** | Rastreamento de defeitos | github.com |
| **Lightshot** | Captura de screenshots | lightshot.com |
| **OBS Studio** | Gravação de vídeos | obsproject.com |
| **Postman** | Testes de API | postman.com |
| **Chrome DevTools** | Inspeção e debugging | Built-in |

---

## 3.8 Checklist de Execução

**Antes de iniciar os testes**:
- [ ] Ambiente configurado e funcional
- [ ] Casos de teste revisados
- [ ] Ferramentas de captura instaladas
- [ ] Pasta de evidências criada
- [ ] Planilha de registro preparada

**Durante os testes**:
- [ ] Seguir passos exatamente como descritos
- [ ] Registrar resultados imediatamente
- [ ] Capturar evidências de falhas
- [ ] Reportar bloqueios imediatamente
- [ ] Manter comunicação com a equipe

**Após os testes**:
- [ ] Atualizar métricas consolidadas
- [ ] Revisar registros para completude
- [ ] Organizar evidências
- [ ] Criar relatório de ciclo
- [ ] Comunicar resultados aos stakeholders

---

# ANEXOS

## Glossário
- **RAWG API**: API pública de dados de jogos
- **Glassmorphism**: Estilo de design com efeito de vidro fosco
- **Autocomplete**: Sugestões automáticas durante digitação
- **Cache**: Armazenamento temporário para melhorar performance
- **CORS**: Cross-Origin Resource Sharing
- **Parsing**: Análise e extração de dados estruturados

## Referências
- Documentação RAWG API: https://rawg.io/apidocs
- React Documentation: https://react.dev
- FastAPI Documentation: https://fastapi.tiangolo.com

## Aprovações

| Nome | Papel | Assinatura | Data |
|------|-------|------------|------|
| | QA Lead | | |
| | Desenvolvedor Lead | | |
| | Product Owner | | |

---

**Fim do Documento**  
**Última atualização**: 27/11/2025
