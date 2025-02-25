# 📚 **excel-toolkit - Manipulação Eficiente de Arquivos Excel**

📊 **excel-toolkit** é um pacote Python que facilita a **leitura, manipulação e exportação de arquivos Excel e CSV** usando `pandas` e `openpyxl`. Ideal para automação de processos com planilhas!

---

## ✨ **Principais Funcionalidades**

- 📥 **Leitura de arquivos Excel (`.xlsx`) e CSV (`.csv`).**
- 📤 **Exportação de DataFrames para Excel e CSV.**
- 📊 **Suporte a múltiplas planilhas.**
- 🔄 **Manipulação simplificada de dados com `pandas`.**
- ✅ **Integração com `pytest` para testes automatizados.**

---

## ⚡ **Instalação**

Instale o pacote via **PyPI**:

```bash
pip install excel-toolkit-for-py
```

> O pacote depende de `pandas` e `openpyxl`, que serão instalados automaticamente.

---

## 🚀 **Como Usar**

### 📥 **Leitura de Arquivos Excel e CSV**

```python
from excel_toolkit.reader import read_excel, read_csv

# Lendo um arquivo Excel (planilha 'Sheet1')
df_excel = read_excel("dados.xlsx", sheet_name="Sheet1")
print(df_excel.head())

# Lendo um arquivo CSV
df_csv = read_csv("dados.csv")
print(df_csv.head())
```

---

### 📤 **Exportação de DataFrames para Excel e CSV**

```python
from excel_toolkit.writer import write_excel, write_csv
import pandas as pd

# Criando um DataFrame de exemplo
df = pd.DataFrame({
    "Nome": ["Alice", "Bob", "Carlos"],
    "Idade": [25, 30, 22]
})

# Exportando para Excel
write_excel(df, "saida.xlsx", sheet_name="Usuarios")

# Exportando para CSV
write_csv(df, "saida.csv")
```

---

### 🔄 **Fluxo Completo: Leitura, Manipulação e Escrita**

```python
# Leitura -> Manipulação -> Escrita
from excel_toolkit.reader import read_excel
from excel_toolkit.writer import write_excel

# Ler planilha
df = read_excel("dados.xlsx", sheet_name="Sheet1")

# Filtrar usuários com mais de 25 anos
df_filtrado = df[df["Idade"] > 25]

# Salvar dados filtrados em um novo arquivo
write_excel(df_filtrado, "dados_filtrados.xlsx", sheet_name="Filtrados")
```

---

## 🧪 **Testes**

Execute os testes unitários com `pytest`:

```bash
pytest tests/
```

Para saída detalhada:

```bash
pytest -v
```

---

## 🏗 **Estrutura do Projeto**

```
excel_toolkit/
│
├── excel_toolkit/                # 📦 Código do pacote
│   ├── __init__.py
│   ├── reader.py            # 📥 Funções de leitura de arquivos
│   ├── writer.py            # 📤 Funções de exportação de arquivos
│
├── tests/                   # 🧪 Testes unitários
│   ├── test_reader.py
│   ├── test_writer.py
│
├── setup.py                 # ⚙️ Configuração para publicação no PyPI
├── pyproject.toml           # 📦 Configuração moderna (opcional)
├── README.md                # 📚 Documentação do projeto
├── LICENSE                  # 📜 Licença MIT
└── MANIFEST.in              # 📋 Arquivos extras incluídos
```

---

## 📝 **Licença**

Distribuído sob a **Licença MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---
## 👨‍💻 **Autor**

Desenvolvido por **[Roberto Lima](https://robertolima-developer.vercel.app/)** 🚀✨

---

## 💬 **Contato**

- 📧 **Email**: robertolima.izphera@gmail.com
- 💼 **LinkedIn**: [Roberto Lima](https://www.linkedin.com/in/roberto-lima-01/)  

---

## ⭐ **Gostou do projeto?**

Deixe uma ⭐ no repositório e compartilhe com a comunidade! 🚀✨  
```

---

## 🌟 **O que este README oferece?**
- 🎯 **Descrição clara** do projeto e seu propósito.  
- 🛠 **Instruções detalhadas de instalação** e **uso prático**.  
- 🧪 **Guia de testes** para garantir que o código funciona.  
- 🏗 **Estrutura do projeto** para facilitar a navegação.  
- 🔄 **Seção de contribuição** para quem deseja ajudar no desenvolvimento.  
- 📝 **Licença e informações do autor** para transparência.
