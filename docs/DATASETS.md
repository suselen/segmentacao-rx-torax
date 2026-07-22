# Bases públicas de radiografias de tórax

Este documento registra as bases previstas para o projeto, o objetivo de cada uma e os links oficiais de acesso.

> As imagens não devem ser copiadas para o GitHub. Faça o download localmente ou no ambiente temporário do Google Colab e respeite os termos de cada base.

## Ordem recomendada

1. **Montgomery County CXR Set** — primeira base do projeto.
2. **Shenzhen Hospital CXR Set** — teste de generalização.
3. **CheXpert** — classificação exploratória de achados.
4. **MIMIC-CXR-JPG** — fase avançada e estudos em larga escala.

---

## 1. Montgomery County CXR Set

### Uso no projeto

Será a base inicial para:

- carregar radiografias PA;
- ler máscaras do pulmão esquerdo e direito;
- compor a máscara pulmonar completa;
- testar CLAHE, filtros, Otsu, morfologia e componentes conexos;
- avaliar segmentação com Dice e IoU;
- produzir visualizações comparativas.

### Conteúdo relevante

- 138 radiografias PA;
- 80 classificadas como normais;
- 58 com manifestações compatíveis com tuberculose;
- imagens desidentificadas;
- máscaras pulmonares esquerda e direita em PNG;
- leituras radiológicas;
- anotações de consenso.

### Links oficiais

- Página da NLM com descrição das bases:
  https://lhncbc.nlm.nih.gov/CHRB/CHRB-resources.html

- Diretório oficial para download:
  https://data.lhncbc.nlm.nih.gov/public/Tuberculosis-Chest-X-ray-Datasets/Montgomery-County-CXR-Set/MontgomerySet/

### Estrutura esperada

```text
data/
└── montgomery/
    ├── CXR_png/
    ├── ClinicalReadings/
    ├── ManualMask/
    │   ├── leftMask/
    │   └── rightMask/
    ├── montgomery_consensus_roi.csv
    └── NLM-MontgomeryCXRSet-ReadMe.pdf
```

### Prioridade

**Alta.** É a primeira base que será integrada ao notebook.

---

## 2. Shenzhen Hospital CXR Set

### Uso no projeto

Será utilizada após a Montgomery para:

- testar o pipeline em imagens de outra instituição;
- analisar generalização;
- comparar histogramas e contraste;
- verificar se parâmetros fixos funcionam em outra distribuição de imagens;
- explorar anotações de regiões em um subconjunto.

### Conteúdo relevante

- 662 radiografias em PNG;
- 326 normais;
- 336 com manifestações compatíveis com tuberculose;
- leituras clínicas;
- anotações de consenso em um subconjunto.

### Links oficiais

- Página da NLM com descrição:
  https://lhncbc.nlm.nih.gov/CHRB/CHRB-resources.html

- Diretório oficial para download:
  https://data.lhncbc.nlm.nih.gov/public/Tuberculosis-Chest-X-ray-Datasets/Shenzhen-Hospital-CXR-Set/

### Estrutura esperada

```text
data/
└── shenzhen/
    ├── CXR_png/
    ├── ClinicalReadings/
    ├── Annotations/
    ├── Annotations-2/
    ├── shenzhen_consensus_roi.csv
    └── NLM-ChinaCXRSet-ReadMe.docx
```

### Prioridade

**Média.** Será usada para validar a generalização da v0.2.

---

## 3. CheXpert

### Uso no projeto

A CheXpert não será a primeira base de segmentação. Ela será usada posteriormente para:

- classificação multi-rótulo;
- exploração de cardiomegalia, atelectasia, consolidação, edema e derrame;
- estudo de rótulos positivos, negativos e incertos;
- mapas de atenção;
- comparação entre medições quantitativas e rótulos;
- futura geração de tabela de probabilidades.

### Conteúdo relevante

- 224.316 radiografias;
- 65.240 pacientes;
- 14 observações;
- rótulos positivos, negativos e incertos;
- relatórios associados;
- conjuntos de avaliação com anotação de radiologistas.

### Links oficiais

- Página do projeto:
  https://stanfordmlgroup.github.io/competitions/chexpert/

- Página atual de acesso ao conjunto:
  https://stanford.redivis.com/datasets/5yyj-1a9f6ap0x

### Atenção

- pode exigir conta e aceite de termos;
- não redistribua as imagens;
- registre a versão utilizada;
- mantenha separação por paciente entre treino, validação e teste.

### Prioridade

**Futura.** Entrará depois da segmentação anatômica básica.

---

## 4. MIMIC-CXR-JPG

### Uso no projeto

Será considerada em uma fase avançada para:

- análise em larga escala;
- metadados de posição AP, PA e lateral;
- rótulos estruturados;
- estudos longitudinais;
- dispositivos médicos;
- comparação entre exames;
- futura geração ou avaliação de texto estruturado.

### Conteúdo relevante

- 377.110 imagens JPG;
- rótulos derivados de relatórios;
- metadados de orientação e dimensões;
- divisões oficiais de treino, validação e teste;
- dados desidentificados.

### Link oficial

- Página do PhysioNet:
  https://physionet.org/content/mimic-cxr-jpg/2.1.0/

### Requisitos de acesso

A base possui acesso controlado. O pesquisador deve seguir as exigências vigentes no PhysioNet, que podem incluir:

- criação de conta;
- verificação de identidade;
- treinamento de pesquisa;
- aceite de acordo de uso de dados;
- compromisso de não reidentificação e não redistribuição.

### Prioridade

**Avançada.** Não é necessária para a primeira entrega da disciplina.

---

## Matriz de utilização

| Base | Segmentação pulmonar | Máscaras de referência | Classificação | Relatórios/rótulos | Acesso |
|---|---:|---:|---:|---:|---|
| Montgomery | Sim | Sim | Limitada | Leituras | Direto |
| Shenzhen | Parcial/experimental | Anotações em subconjunto | Limitada | Leituras | Direto |
| CheXpert | Não é o foco inicial | Não para pulmão | Sim | Sim | Cadastro/termos |
| MIMIC-CXR-JPG | Não é o foco inicial | Não para pulmão | Sim | Sim | Controlado |

## Regras do repositório

- Não adicionar as bases ao Git.
- Não realizar commit de DICOM, PNG ou JPG clínico.
- Não publicar chaves, credenciais ou cookies.
- Não redistribuir dados de acesso controlado.
- Registrar fonte, versão, data de download e licença.
- Separar pacientes entre treino, validação e teste.
- Conferir se o uso acadêmico desejado é permitido pelos termos da base.

## Primeira tarefa de implementação

```text
Montgomery
    ↓
radiografia PNG
    ↓
máscara esquerda + máscara direita
    ↓
máscara pulmonar completa
    ↓
pipeline clássico
    ↓
Dice e IoU
    ↓
visualização e tabela
```
