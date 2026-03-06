# 🎓 Grade Calc System

Um gerenciador e calculador de notas interativo via terminal (CLI) desenvolvido em Python. O sistema permite cadastrar matérias com fórmulas de avaliação personalizadas e calcula automaticamente a nota mínima necessária nas próximas avaliações para garantir a aprovação.

## ✨ Funcionalidades

* **Fórmulas Personalizadas**: Suporte para expressões matemáticas dinâmicas (ex: `(p1 + p2*2)/3`). O sistema analisa a fórmula, extrai as variáveis e valida a sintaxe automaticamente.
* **Grade Solver (Busca Binária)**: Você não precisa ficar "chutando" notas para ver se passa. O sistema usa um algoritmo de busca binária para calcular com precisão a nota mínima exata que você precisa tirar na variável alvo para ser aprovado.
* **Gerenciador de Saves**: Crie múltiplos arquivos `.json` para separar diferentes semestres, anos ou até mesmo grades de diferentes alunos.
* **Interface Rica (TUI)**: Menus interativos, formatação de cores e validação de input de usuário direto no terminal, construídos com a biblioteca `rich`.
* **Status Automático**: Acompanhe rapidamente se a matéria está `[APROVADO]`, `[PENDENTE]` ou `[REPROVADO]`.

## 📂 Arquitetura do Projeto

O projeto adota uma arquitetura modularizada, separando a lógica de negócios da interface visual:

* `main.py`: Ponto de entrada da aplicação.
* `models/`: Contém as estruturas de dados principais, como a *Data Class* `Subject`, que gerencia o estado e avaliação de cada matéria.
* `core/`: Lógica de negócios pura do sistema.
    * `formula.py`: Validação de expressões e extração de variáveis via Regex/AST.
    * `solver.py`: Algoritmo de busca binária para o cálculo da nota alvo.
    * `save_manager.py`: Serialização e persistência de dados em arquivos JSON.
    * `subject_manager.py`: Funções para manipulação e atualização de matérias no estado atual.
* `cli/`: Tudo relacionado à interação com o usuário no terminal.
    * `menu.py` e `actions.py`: Estrutura de menus dinâmicos e suas respectivas ações de controle.
    * `prompts.py`: Lógica de inputs, sanitização e loops de validação.
    * `views.py` e `formatting.py`: Telas de visualização e utilitários do `rich`.
* `utils/`: Tipagens (Type Hints) e constantes de configuração do sistema (notas mínimas, limites, diretórios).

## 🚀 Como Executar

### Pré-requisitos
* Python 3.10 ou superior.
* Biblioteca `rich`.

### Passo a Passo

1. Clone o repositório:
```bash
git clone [https://github.com/seu-usuario/grade-calc-system.git](https://github.com/seu-usuario/grade-calc-system.git)
cd grade-calc-system
```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
```bash
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate
```

3. Instale as dependências:
```
pip install rich
```

4. Inicie a aplicação:
```
python main.py
```

## ⚙️ Configurações
Se desejar alterar a média da faculdade ou os limites das notas, basta editar o arquivo utils/types_and_constants.py:
```
MIN_PASSING_GRADE = 70.0 # Nota para aprovação
MIN_GRADE = 0.0          # Nota mínima possível
MAX_GRADE = 100.0        # Nota máxima possível
```

