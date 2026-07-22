# Segmentação e Análise Quantitativa de Radiografias de Tórax

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/suselen/segmentacao-rx-torax/blob/main/notebooks/segmentacao_rx_torax.ipynb)

Pipeline acadêmico e reprodutível de **Processamento Digital de Imagens e Visão Computacional** aplicado a radiografias de tórax. O projeto começa com anonimização, realce, filtragem, histogramas, detecção de bordas e segmentação pulmonar, evoluindo para análise quantitativa da silhueta cardíaca, ângulos costofrênicos, dispositivos médicos e geração de um rascunho técnico estruturado.

> **Aviso:** este projeto é educacional e experimental. Não substitui laudo, diagnóstico ou avaliação médica.

## Objetivo geral

Desenvolver um pipeline executável no **Google Colab**, versionado no GitHub e organizado em módulos Python para:

1. carregar imagens PNG, JPG, TIFF e DICOM;
2. remover identificadores de metadados DICOM;
3. mascarar textos identificadores gravados nos pixels;
4. normalizar e analisar níveis de cinza;
5. aplicar CLAHE e filtros;
6. detectar bordas;
7. segmentar campos pulmonares;
8. segmentar a silhueta cardíaca;
9. calcular métricas quantitativas;
10. avaliar máscaras com Dice e IoU;
11. gerar tabelas, imagens comparativas e uma descrição técnica;
12. evoluir futuramente para detecção de dispositivos e integração com XNAT/OHIF.

## Escopo da primeira versão acadêmica

A primeira versão demonstrável deverá executar:

- carregamento e anonimização da radiografia;
- pré-processamento com CLAHE;
- filtros Gaussiano, mediana e bilateral;
- histograma e estatísticas dos tons de cinza;
- detecção de bordas por Sobel e Canny;
- segmentação dos campos pulmonares;
- comparação com máscaras de referência;
- cálculo de Dice e IoU;
- visualização da máscara sobre a radiografia;
- tabela de resultados;
- descrição técnica quantitativa.

A segmentação cardíaca, o índice cardiotorácico, os ângulos costofrênicos e a detecção de dispositivos serão incorporados progressivamente.

## Bases públicas de imagens

| Fase | Base | Uso principal |
|---|---|---|
| 1 | Montgomery County CXR Set | Segmentação pulmonar e avaliação com máscaras esquerda/direita |
| 2 | Shenzhen Hospital CXR Set | Teste de generalização em outra instituição |
| 3 | CheXpert | Classificação exploratória de achados e comparação com rótulos |
| 4 | MIMIC-CXR-JPG | Estudos em larga escala, metadados, rótulos e futura geração de texto |

Os links oficiais, requisitos de acesso e estrutura esperada estão documentados em [`docs/DATASETS.md`](docs/DATASETS.md).

## Estratégia de desenvolvimento

```text
Radiografia
    ↓
Anonimização
    ↓
Normalização
    ↓
CLAHE e filtragem
    ↓
Histograma e estatísticas
    ↓
Detecção de bordas
    ↓
Segmentação anatômica
    ↓
Dice e IoU
    ↓
Medições quantitativas
    ↓
Tabela e visualização
    ↓
Descrição técnica estruturada
```

## Versões planejadas

### v0.1 — Fundamentos de PDI

- leitura PNG/JPG/TIFF/DICOM;
- anonimização de metadados;
- mascaramento manual de regiões com texto;
- CLAHE;
- filtros Gaussiano, mediana e bilateral;
- Sobel e Canny;
- histograma e estatísticas;
- Dice e IoU;
- tabela de resultados;
- descrição técnica estruturada.

### v0.2 — Segmentação pulmonar validada

- integração inicial com Montgomery;
- leitura das máscaras esquerda e direita;
- composição da máscara pulmonar completa;
- segmentação clássica;
- cálculo de Dice e IoU;
- análise visual dos erros;
- teste posterior com Shenzhen.

### v0.3 — Silhueta cardíaca e medições anatômicas

- segmentação da silhueta cardíaca;
- cálculo exploratório do índice cardiotorácico;
- identificação aproximada dos ângulos costofrênicos;
- tabela de medidas e visualizações explicativas.

### v0.4 — Aprendizado profundo

- U-Net ou arquitetura equivalente;
- treinamento, validação e teste;
- comparação com métodos clássicos;
- análise de generalização entre bases;
- registro de experimentos.

### v0.5 — Dispositivos e descrição estruturada

- detecção de eletrodos, cateteres e tubos;
- classificação exploratória de dispositivos;
- identificação de regiões de maior opacidade;
- comparação longitudinal entre exames;
- geração de rascunho técnico estruturado;
- estudo de integração com XNAT/OHIF.

## Estrutura

```text
segmentacao-rx-torax/
├── README.md
├── LICENSE
├── requirements.txt
├── .gitignore
├── docs/
│   └── DATASETS.md
├── notebooks/
│   └── segmentacao_rx_torax.ipynb
├── src/
│   ├── anonymization.py
│   ├── io_utils.py
│   ├── preprocessing.py
│   ├── segmentation.py
│   ├── measurements.py
│   ├── metrics.py
│   ├── visualization.py
│   ├── report.py
│   └── devices.py
├── tests/
│   └── test_metrics.py
├── images/
│   └── exemplos/
├── data/
├── models/
└── results/
```

## Privacidade

O padrão do projeto é:

- remover nome, ID, prontuário, accession number, instituição e médico;
- remover ou substituir UIDs;
- preservar apenas sexo quando necessário;
- utilizar idade ou faixa etária em vez de data de nascimento completa;
- mascarar textos gravados nos pixels;
- revisar visualmente a imagem antes de qualquer publicação;
- nunca versionar imagens clínicas privadas no GitHub.

A simples substituição do nome por um código caracteriza pseudonimização e não garante anonimização completa.

## Executando no Colab

1. Clique no botão **Abrir no Colab** no início desta página.
2. Execute as células de cima para baixo.
3. Use inicialmente uma imagem pública da base Montgomery.
4. Não envie imagens privadas ou identificáveis.

## Executando localmente

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
pip install -r requirements.txt
```

Linux/macOS:

```bash
source .venv/bin/activate
pip install -r requirements.txt
```

## Dados e licenças

As imagens não serão incluídas diretamente neste repositório. Cada base possui sua própria forma de acesso, licença, termos de uso e citação obrigatória.

Consulte [`docs/DATASETS.md`](docs/DATASETS.md) antes de baixar ou utilizar qualquer conjunto de dados.

## Licença do código

O código deste repositório é disponibilizado sob licença MIT. Essa licença não se estende automaticamente às imagens, aos relatórios, aos rótulos ou aos pesos de modelos de terceiros.
